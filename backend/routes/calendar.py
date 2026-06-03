"""
Calendar routes.

GET /api/calendar/<assessment_id>.ics  → download .ics file
GET /api/calendar/<assessment_id>/links → JSON with Google Cal URLs
GET /api/calendar/preview.ics          → quick test (no auth)
"""
from flask import Blueprint, Response, jsonify, request
from models.database import get_db
from services.calendar_service import generate_ics, google_calendar_links, get_program_days

calendar_bp = Blueprint('calendar', __name__)


@calendar_bp.route('/api/calendar/<assessment_id>.ics')
def download_ics(assessment_id):
    db = get_db()
    try:
        row = db.execute(
            "SELECT name, email, track_recommended, language FROM assessments WHERE id=?",
            (assessment_id,)
        ).fetchone()
    finally:
        db.close()

    if not row:
        return jsonify({'error': 'Not found'}), 404

    lang  = row['language'] or 'en'
    track = row['track_recommended'] or 'A'
    ics   = generate_ics(track, lang, row['name'], row['email'])

    return Response(
        ics,
        mimetype='text/calendar',
        headers={
            'Content-Disposition': f'attachment; filename="cami-netherlands-{track.lower()}.ics"',
            'Cache-Control': 'no-cache',
        }
    )


@calendar_bp.route('/api/calendar/<assessment_id>/links')
def get_links(assessment_id):
    db = get_db()
    try:
        row = db.execute(
            "SELECT track_recommended, language FROM assessments WHERE id=?",
            (assessment_id,)
        ).fetchone()
    finally:
        db.close()

    if not row:
        return jsonify({'error': 'Not found'}), 404

    lang  = row['language'] or 'en'
    track = row['track_recommended'] or 'A'
    days  = get_program_days()

    return jsonify({
        'track':           track,
        'google_calendar': google_calendar_links(track, lang),
        'ics_url':         f'/api/calendar/{assessment_id}.ics',
        'program_days':    [d.strftime('%A %d %B %Y, %H:%M') for d in days],
    })


@calendar_bp.route('/api/calendar/preview.ics')
def preview_ics():
    """Dev/test: returns a sample .ics without DB lookup."""
    track = request.args.get('track', 'A')
    lang  = request.args.get('lang', 'en')
    ics   = generate_ics(track, lang, 'Test User', 'test@example.com')
    return Response(ics, mimetype='text/calendar',
                    headers={'Content-Disposition': 'inline; filename="preview.ics"'})
