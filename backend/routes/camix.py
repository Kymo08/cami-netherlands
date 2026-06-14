"""
CAMIX Daily Email Routes
========================
POST /api/camix/daily-dispatch
    Called by Render cron job daily at 07:00 UTC.
    Finds all enrolled participants who are due for their next daily email
    and sends it. Uses CAMIX_DISPATCH_SECRET env var for simple auth.

GET  /api/camix/preview/<assessment_id>/<int:day>
    Returns the HTML email for a given participant + day (no send).
    Protected by the same secret (passed as ?secret=... query param).

POST /api/camix/enroll/<assessment_id>
    Marks an assessment as CAMIX-enrolled (sets camix_enrolled_at = now,
    camix_current_day = 0). Called by stripe webhook after payment.
"""

from __future__ import annotations

import os
from datetime import datetime, timezone

from flask import Blueprint, jsonify, request, make_response

from models.database import get_db
from services.camix_service import send_daily_email, build_daily_email

camix_bp = Blueprint("camix", __name__)

_SECRET = os.getenv("CAMIX_DISPATCH_SECRET", "camix-dev-secret")


def _auth_ok(req) -> bool:
    """Check dispatch secret from header or query param."""
    return (
        req.headers.get("X-Camix-Secret") == _SECRET
        or req.args.get("secret") == _SECRET
    )


# ── Enroll ────────────────────────────────────────────────────────────────────

@camix_bp.route("/api/camix/enroll/<assessment_id>", methods=["POST"])
def enroll(assessment_id: str):
    """Mark assessment as CAMIX enrolled."""
    if not _auth_ok(request):
        return jsonify({"error": "unauthorized"}), 401

    now = datetime.now(timezone.utc).isoformat()
    conn = get_db()
    row = conn.execute(
        "SELECT id, camix_enrolled_at FROM assessments WHERE id = ?",
        (assessment_id,)
    ).fetchone()

    if not row:
        conn.close()
        return jsonify({"error": "assessment not found"}), 404

    if row["camix_enrolled_at"]:
        conn.close()
        return jsonify({"status": "already_enrolled", "enrolled_at": row["camix_enrolled_at"]})

    conn.execute(
        "UPDATE assessments SET camix_enrolled_at = ?, camix_current_day = 0 WHERE id = ?",
        (now, assessment_id)
    )
    conn.commit()
    conn.close()

    return jsonify({"status": "enrolled", "enrolled_at": now, "assessment_id": assessment_id})


# ── Daily dispatch ────────────────────────────────────────────────────────────

@camix_bp.route("/api/camix/daily-dispatch", methods=["POST"])
def daily_dispatch():
    """
    Send today's CAMIX email to all enrolled participants who are due.
    A participant is due if:
      - camix_enrolled_at is set
      - camix_current_day < 30
      - camix_last_sent_at is NULL or was > 20h ago (prevents duplicate sends)
    """
    if not _auth_ok(request):
        return jsonify({"error": "unauthorized"}), 401

    now = datetime.now(timezone.utc)
    sent = []
    skipped = []
    errors = []

    conn = get_db()
    rows = conn.execute("""
        SELECT id, name, email, language, track_recommended, goals, age,
               camix_current_day, camix_enrolled_at, camix_last_sent_at
        FROM assessments
        WHERE camix_enrolled_at IS NOT NULL
          AND (camix_current_day IS NULL OR camix_current_day < 30)
          AND consent_marketing = 1
    """).fetchall()

    for row in rows:
        assessment = dict(row)
        last_sent = row["camix_last_sent_at"]

        # Cooldown: skip if last email was <20h ago
        if last_sent:
            try:
                last_dt = datetime.fromisoformat(last_sent.replace("Z", "+00:00"))
                hours_since = (now - last_dt).total_seconds() / 3600
                if hours_since < 20:
                    skipped.append({"id": row["id"], "reason": f"cooldown ({hours_since:.1f}h since last)"})
                    continue
            except Exception:
                pass

        next_day = (row["camix_current_day"] or 0) + 1

        try:
            result = send_daily_email(assessment, next_day)
            conn.execute(
                "UPDATE assessments SET camix_current_day = ?, camix_last_sent_at = ? WHERE id = ?",
                (next_day, now.isoformat(), row["id"])
            )
            conn.commit()
            sent.append({"id": row["id"], "name": row["name"], "day": next_day,
                         "email": row["email"], "result": result})
        except Exception as exc:
            errors.append({"id": row["id"], "error": str(exc)})

    conn.close()

    return jsonify({
        "dispatched_at": now.isoformat(),
        "sent": len(sent),
        "skipped": len(skipped),
        "errors": len(errors),
        "detail": {"sent": sent, "skipped": skipped, "errors": errors},
    })


# ── Preview ───────────────────────────────────────────────────────────────────

@camix_bp.route("/api/camix/preview/<assessment_id>/<int:day>", methods=["GET"])
def preview(assessment_id: str, day: int):
    """Return the rendered HTML email (no send) for testing."""
    if not _auth_ok(request):
        return jsonify({"error": "unauthorized"}), 401

    conn = get_db()
    row = conn.execute(
        "SELECT id, name, email, language, track_recommended, goals, age FROM assessments WHERE id = ?",
        (assessment_id,)
    ).fetchone()
    conn.close()

    if not row:
        return jsonify({"error": "assessment not found"}), 404

    assessment = dict(row)
    subject, html = build_daily_email(assessment, day, use_ai=False)

    if not subject:
        return jsonify({"error": f"day {day} out of range (1-30)"}), 400

    resp = make_response(html)
    resp.headers["Content-Type"] = "text/html; charset=utf-8"
    resp.headers["X-CAMIX-Subject"] = subject
    return resp


# ── Status ────────────────────────────────────────────────────────────────────

@camix_bp.route("/api/camix/status", methods=["GET"])
def status():
    """Summary of CAMIX enrolled participants (no auth required — only counts)."""
    conn = get_db()
    total = conn.execute(
        "SELECT COUNT(*) FROM assessments WHERE camix_enrolled_at IS NOT NULL"
    ).fetchone()[0]
    completed = conn.execute(
        "SELECT COUNT(*) FROM assessments WHERE camix_current_day >= 30"
    ).fetchone()[0]
    active = conn.execute(
        "SELECT COUNT(*) FROM assessments WHERE camix_enrolled_at IS NOT NULL AND camix_current_day < 30"
    ).fetchone()[0]
    conn.close()

    return jsonify({
        "camix_enrolled_total": total,
        "camix_active": active,
        "camix_completed_30d": completed,
    })
