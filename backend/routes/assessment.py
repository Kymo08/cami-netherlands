"""
Assessment route: POST /api/assessment/submit
"""
import json
import uuid
from datetime import datetime, timezone

from flask import Blueprint, request, jsonify

from models.database import get_db
from services.triage import triage, sentinel_check
from services.email_service import send_assessment_confirmation, send_admin_notification
from services.ai_service import analyze_assessment

assessment_bp = Blueprint('assessment', __name__)

ADMIN_EMAIL = 'info@centrocami.it'


def _normalize(data: dict) -> dict:
    """Normalize frontend payload to canonical form before validation."""
    profile = data.get('profile', {})

    # Accept first_name + last_name OR name
    if not profile.get('name') and (profile.get('first_name') or profile.get('last_name')):
        profile['name'] = f"{profile.get('first_name', '')} {profile.get('last_name', '')}".strip()

    # Language: top-level preferred_language → profile.language
    if not profile.get('language'):
        profile['language'] = data.get('preferred_language', 'en')

    data['profile'] = profile
    return data


def _validate_payload(data: dict) -> list[str]:
    errors = []
    profile = data.get('profile', {})
    if not profile.get('name', '').strip():
        errors.append('profile.name (or first_name/last_name) is required')
    if not profile.get('email', '').strip():
        errors.append('profile.email is required')
    if not isinstance(profile.get('age'), (int, float)):
        errors.append('profile.age must be a number')
    if not data.get('goals'):
        errors.append('goals must be a non-empty array')
    if not data.get('consent', {}).get('health_data'):
        errors.append('consent.health_data is required')
    if not data.get('consent', {}).get('liability'):
        errors.append('consent.liability is required')
    return errors


@assessment_bp.route('/api/assessment/submit', methods=['POST'])
def submit_assessment():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'status': 'error', 'message': 'Invalid JSON'}), 400

    data = _normalize(data)

    # Validate
    errors = _validate_payload(data)
    if errors:
        return jsonify({'status': 'error', 'errors': errors}), 422

    profile   = data['profile']
    goals     = data.get('goals', [])
    screening = data.get('screening', {})
    consent   = data.get('consent', {})

    age = int(profile.get('age', 30))

    # Run algorithms
    triage_result  = triage(goals, age, screening)
    sentinel_status = sentinel_check(goals, screening)

    # AI personalised analysis (non-blocking: None if key missing or call fails)
    lang = profile.get('language', 'en')
    ai_analysis = analyze_assessment(
        profile=profile,
        goals=goals,
        screening=screening,
        track=triage_result['track_recommended'],
        lang=lang,
    )

    assessment_id  = str(uuid.uuid4())
    now            = datetime.now(timezone.utc).isoformat()

    # Persist to DB
    db = get_db()
    try:
        db.execute("""
            INSERT INTO assessments
              (id, created_at, name, email, age, phone, referral_source, language,
               goals, screening,
               track_recommended, sentinel_status, clinical_score, performance_score,
               medical_clearance_required,
               consent_health, consent_marketing, consent_liability, consent_timestamp,
               utm_source, utm_medium, utm_campaign,
               ai_analysis)
            VALUES
              (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            assessment_id, now,
            profile['name'].strip(),
            profile['email'].strip().lower(),
            age,
            profile.get('phone', ''),
            profile.get('referral', ''),
            profile.get('language', 'en'),
            json.dumps(goals),
            json.dumps(screening),
            triage_result['track_recommended'],
            sentinel_status,
            triage_result['clinical_score'],
            triage_result['performance_score'],
            1 if triage_result['medical_clearance_required'] else 0,
            1 if consent.get('health_data') else 0,
            1 if consent.get('marketing')    else 0,
            1 if consent.get('liability')    else 0,
            consent.get('timestamp', now),
            data.get('utm_source', ''),
            data.get('utm_medium', ''),
            data.get('utm_campaign', ''),
            ai_analysis,
        ))
        db.commit()
    finally:
        db.close()

    # Build assessment dict for emails
    assessment_record = {
        'id':                      assessment_id,
        'created_at':              now,
        'name':                    profile['name'].strip(),
        'email':                   profile['email'].strip().lower(),
        'age':                     age,
        'phone':                   profile.get('phone', ''),
        'referral_source':         profile.get('referral', ''),
        'language':                profile.get('language', 'en'),
        'goals':                   goals,
        'screening':               screening,
        'track_recommended':       triage_result['track_recommended'],
        'sentinel_status':         sentinel_status,
        'clinical_score':          triage_result['clinical_score'],
        'performance_score':       triage_result['performance_score'],
        'medical_clearance_required': triage_result['medical_clearance_required'],
        'ai_analysis':             ai_analysis,
    }

    # Send emails (non-blocking: log errors but don't fail the request)
    try:
        send_assessment_confirmation(assessment_record)
    except Exception as e:
        print(f'[EMAIL] Client confirmation failed: {e}')

    try:
        send_admin_notification(assessment_record, ADMIN_EMAIL)
    except Exception as e:
        print(f'[EMAIL] Admin notification failed: {e}')

    return jsonify({
        'status':                    'success',
        'assessment_id':             assessment_id,
        'track_recommended':         triage_result['track_recommended'],
        'clinical_score':            triage_result['clinical_score'],
        'performance_score':         triage_result['performance_score'],
        'sentinel_status':           sentinel_status,
        'medical_clearance_required': triage_result['medical_clearance_required'],
        'ai_analysis':               ai_analysis,
        'message':                   'Assessment received. Check your email within 5 minutes.',
    }), 201
