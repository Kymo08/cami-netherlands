"""
Admin API routes — protected by HTTP Basic Auth.
Set ADMIN_PASSWORD in environment.

Endpoints:
  GET    /api/admin/stats
  GET    /api/admin/assessments           ?page=1&per_page=20&track=A&status=new&q=name
  GET    /api/admin/assessments/<id>
  PATCH  /api/admin/assessments/<id>      {status, notes, stripe_payment_link}
"""
import json
import os
import functools

from flask import Blueprint, request, jsonify, Response

from models.database import get_db

admin_bp = Blueprint('admin', __name__)

ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'cami-admin-2026')


# ── Auth ───────────────────────────────────────────────────────────────────────

def require_auth(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        auth = request.authorization
        if not auth or auth.password != ADMIN_PASSWORD or auth.username != 'admin':
            return Response(
                'Authentication required',
                401,
                {'WWW-Authenticate': 'Basic realm="CAMI Admin"'},
            )
        return fn(*args, **kwargs)
    return wrapper


def _row_to_dict(row) -> dict:
    d = dict(row)
    for json_field in ('goals', 'screening'):
        if isinstance(d.get(json_field), str):
            try:
                d[json_field] = json.loads(d[json_field])
            except Exception:
                pass
    return d


# ── Stats ──────────────────────────────────────────────────────────────────────

@admin_bp.route('/api/admin/stats')
@require_auth
def stats():
    db = get_db()
    try:
        total      = db.execute("SELECT COUNT(*) FROM assessments").fetchone()[0]
        by_track   = {r['track_recommended']: r['cnt'] for r in
                      db.execute("SELECT track_recommended, COUNT(*) cnt FROM assessments GROUP BY track_recommended")}
        by_status  = {r['status']: r['cnt'] for r in
                      db.execute("SELECT status, COUNT(*) cnt FROM assessments GROUP BY status")}
        by_payment = {r['payment_status']: r['cnt'] for r in
                      db.execute("SELECT payment_status, COUNT(*) cnt FROM assessments GROUP BY payment_status")}
        medical    = db.execute("SELECT COUNT(*) FROM assessments WHERE medical_clearance_required=1").fetchone()[0]
        declined   = db.execute("SELECT COUNT(*) FROM assessments WHERE sentinel_status='declined'").fetchone()[0]
        revenue    = (by_payment.get('paid', 0)) * 250
    finally:
        db.close()

    return jsonify({
        'total':          total,
        'by_track':       by_track,
        'by_status':      by_status,
        'by_payment':     by_payment,
        'medical_flags':  medical,
        'declined':       declined,
        'revenue_eur':    revenue,
    })


# ── List ───────────────────────────────────────────────────────────────────────

@admin_bp.route('/api/admin/assessments')
@require_auth
def list_assessments():
    page     = max(1, int(request.args.get('page', 1)))
    per_page = min(100, int(request.args.get('per_page', 20)))
    offset   = (page - 1) * per_page

    where, params = [], []

    if track := request.args.get('track'):
        where.append("track_recommended = ?")
        params.append(track)
    if status := request.args.get('status'):
        where.append("status = ?")
        params.append(status)
    if sentinel := request.args.get('sentinel'):
        where.append("sentinel_status = ?")
        params.append(sentinel)
    if q := request.args.get('q', '').strip():
        where.append("(name LIKE ? OR email LIKE ?)")
        params += [f'%{q}%', f'%{q}%']

    clause = ('WHERE ' + ' AND '.join(where)) if where else ''

    db = get_db()
    try:
        total = db.execute(f"SELECT COUNT(*) FROM assessments {clause}", params).fetchone()[0]
        rows  = db.execute(
            f"""SELECT id, created_at, name, email, age, track_recommended,
                       sentinel_status, medical_clearance_required,
                       clinical_score, performance_score,
                       status, payment_status, stripe_payment_link, language
                FROM assessments {clause}
                ORDER BY created_at DESC LIMIT ? OFFSET ?""",
            params + [per_page, offset],
        ).fetchall()
    finally:
        db.close()

    return jsonify({
        'total':    total,
        'page':     page,
        'per_page': per_page,
        'pages':    max(1, -(-total // per_page)),
        'items':    [_row_to_dict(r) for r in rows],
    })


# ── Detail ─────────────────────────────────────────────────────────────────────

@admin_bp.route('/api/admin/assessments/<assessment_id>')
@require_auth
def get_assessment(assessment_id):
    db = get_db()
    try:
        row = db.execute("SELECT * FROM assessments WHERE id = ?", (assessment_id,)).fetchone()
    finally:
        db.close()

    if not row:
        return jsonify({'status': 'error', 'message': 'Not found'}), 404

    return jsonify(_row_to_dict(row))


# ── Update ─────────────────────────────────────────────────────────────────────

ALLOWED_STATUSES = {'new', 'reviewing', 'approved', 'payment_sent', 'enrolled', 'declined', 'waitlist'}

@admin_bp.route('/api/admin/assessments/<assessment_id>', methods=['PATCH'])
@require_auth
def update_assessment(assessment_id):
    data = request.get_json(silent=True) or {}

    sets, params = [], []

    if 'status' in data:
        if data['status'] not in ALLOWED_STATUSES:
            return jsonify({'status': 'error', 'message': f'Invalid status. Allowed: {ALLOWED_STATUSES}'}), 422
        sets.append("status = ?")
        params.append(data['status'])

    if 'notes' in data:
        sets.append("notes = ?")
        params.append(str(data['notes'])[:2000])

    if 'stripe_payment_link' in data:
        sets.append("stripe_payment_link = ?")
        params.append(str(data['stripe_payment_link'])[:500])

    if 'payment_status' in data and data['payment_status'] in ('pending', 'paid', 'refunded'):
        sets.append("payment_status = ?")
        params.append(data['payment_status'])

    if not sets:
        return jsonify({'status': 'error', 'message': 'Nothing to update'}), 400

    params.append(assessment_id)
    db = get_db()
    try:
        db.execute(f"UPDATE assessments SET {', '.join(sets)} WHERE id = ?", params)
        db.commit()
        row = db.execute("SELECT * FROM assessments WHERE id = ?", (assessment_id,)).fetchone()
    finally:
        db.close()

    if not row:
        return jsonify({'status': 'error', 'message': 'Not found'}), 404

    return jsonify({'status': 'success', 'assessment': _row_to_dict(row)})
