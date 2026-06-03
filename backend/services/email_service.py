"""
Email service using Resend.com
Reads RESEND_API_KEY from .env
"""
import os
import re
from pathlib import Path

import resend

from services.calendar_service import google_calendar_links, get_program_days


TEMPLATE_DIR = Path(__file__).parent.parent / 'emails' / 'templates'

TRACK_LABELS = {
    'A':      {'it': 'Esercizio Clinico & Invecchiamento Sano',
               'en': 'Clinical Exercise & Healthy Aging',
               'nl': 'Klinische Oefening & Gezond Ouder Worden'},
    'B':      {'it': 'Performance & Preparazione Atletica',
               'en': 'Performance & Athletic Preparation',
               'nl': 'Prestatie & Atletische Voorbereiding'},
    'Hybrid': {'it': 'Programma Ibrido',
               'en': 'Hybrid Program',
               'nl': 'Hybride Programma'},
}

SUBJECTS = {
    'it': 'Valutazione ricevuta – CAMI Netherlands',
    'en': 'Assessment received – CAMI Netherlands',
    'nl': 'Beoordeling ontvangen – CAMI Netherlands',
}

ENROLLMENT_SUBJECTS = {
    'it': '🎉 Sei iscritto! – CAMI Netherlands',
    'en': '🎉 You\'re enrolled! – CAMI Netherlands',
    'nl': '🎉 Je bent ingeschreven! – CAMI Netherlands',
}

BASE_URL = os.getenv('BASE_URL', 'https://nl.centrocami.it')


def _load_template(name: str) -> str:
    path = TEMPLATE_DIR / name
    return path.read_text(encoding='utf-8')


def _render(template: str, ctx: dict) -> str:
    """Minimal {{var}} and {{#if flag}}...{{/if}} renderer."""
    # Simple if blocks
    def replace_if(m):
        flag_name = m.group(1)
        block     = m.group(2)
        return block if ctx.get(flag_name) else ''

    out = re.sub(r'\{\{#if (\w+)\}\}(.*?)\{\{/if\}\}', replace_if, template, flags=re.DOTALL)

    # Variable substitution
    for key, val in ctx.items():
        out = out.replace('{{' + key + '}}', str(val) if val is not None else '')

    return out


def _send(to: str, subject: str, html: str) -> dict:
    api_key = os.getenv('RESEND_API_KEY', '')
    if not api_key:
        # Dev mode: just log, don't fail
        print(f"[EMAIL-DEV] Would send to={to} subject={subject}")
        print(html[:400])
        return {'id': 'dev-mode', 'status': 'logged'}

    resend.api_key = api_key
    resp = resend.Emails.send({
        'from':    'CAMI Netherlands <info@centrocami.it>',
        'to':      [to],
        'subject': subject,
        'html':    html,
    })
    return {'id': resp.get('id'), 'status': 'sent'}


# ── PUBLIC API ─────────────────────────────────────────────────────────────────

def send_assessment_confirmation(assessment: dict) -> dict:
    """Send trilingual confirmation email to the client."""
    lang  = assessment.get('language', 'en')
    if lang not in ('it', 'en', 'nl'):
        lang = 'en'

    track  = assessment.get('track_recommended', 'A')
    labels = TRACK_LABELS.get(track, TRACK_LABELS['A'])

    ctx = {
        'name':          assessment['name'],
        'track':         track,
        'track_label':   labels.get(lang, labels['en']),
        'assessment_id': assessment['id'],
        'medical_clearance': assessment.get('medical_clearance_required', False),
    }

    tpl_name = f'assessment_confirmation_{lang}.html'
    html     = _render(_load_template(tpl_name), ctx)
    subject  = SUBJECTS.get(lang, SUBJECTS['en'])

    return _send(assessment['email'], subject, html)


def send_admin_notification(assessment: dict, admin_email: str) -> dict:
    """Send summary notification to the admin."""
    track   = assessment.get('track_recommended', '?')
    sentinel = assessment.get('sentinel_status', '')

    track_css_map   = {'A': 'track-a', 'B': 'track-b', 'Hybrid': 'hybrid'}
    sentinel_css_map = {
        'pass':                     'pass',
        'medical_clearance_required': 'clearance',
        'declined':                 'declined',
    }

    # Build goals HTML badges
    goals_raw = assessment.get('goals', [])
    if isinstance(goals_raw, str):
        import json
        try:
            goals_raw = json.loads(goals_raw)
        except Exception:
            goals_raw = []
    goals_html = ' '.join(f'<span>{g.replace("_", " ")}</span>' for g in goals_raw)

    # Screening summary
    sc = assessment.get('screening', {})
    if isinstance(sc, str):
        import json
        try:
            sc = json.loads(sc)
        except Exception:
            sc = {}

    highlights = []
    if sc.get('has_chronic_pain'):
        highlights.append(f"Dolore cronico: {sc.get('pain_location', [])} – severità {sc.get('pain_severity')}/10")
    if sc.get('has_fallen'):
        highlights.append('Cadute nell\'ultimo anno: SÌ')
    if sc.get('recent_injury'):
        highlights.append('Infortuni recenti (6 mesi): SÌ')
    parq = sc.get('parq', {})
    yes_flags = [k for k, v in parq.items() if v == 'yes']
    if yes_flags:
        highlights.append(f"PAR-Q+ YES flags: {', '.join(yes_flags)}")

    ctx = {
        'name':             assessment['name'],
        'email':            assessment['email'],
        'age':              assessment.get('age', '?'),
        'phone':            assessment.get('phone') or 'n/d',
        'language':         assessment.get('language', 'en').upper(),
        'referral_source':  assessment.get('referral_source', 'n/d'),
        'assessment_id':    assessment['id'],
        'created_at':       assessment.get('created_at', ''),
        'track_recommended': track,
        'track_css':        track_css_map.get(track, 'track-a'),
        'sentinel_status':  sentinel.replace('_', ' ').title(),
        'sentinel_css':     sentinel_css_map.get(sentinel, 'pass'),
        'clinical_score':   assessment.get('clinical_score', 0),
        'performance_score': assessment.get('performance_score', 0),
        'medical_clearance': '⚠️ SÌ' if assessment.get('medical_clearance_required') else '✅ NO',
        'goals_html':       goals_html,
        'screening_summary': '<br>'.join(highlights) if highlights else None,
    }

    html = _render(_load_template('admin_notification.html'), ctx)

    return _send(
        to      = admin_email,
        subject = f"🔔 Nuovo Assessment: {assessment['name']} – Track {track}",
        html    = html,
    )


def send_enrollment_confirmation(assessment: dict) -> dict:
    """
    Send a post-payment enrollment confirmation email to the client.
    Includes Google Calendar links and .ics download URL for all 3 program days.
    """
    lang = assessment.get('language', 'en')
    if lang not in ('it', 'en', 'nl'):
        lang = 'en'

    track  = assessment.get('track_recommended', 'A')
    labels = TRACK_LABELS.get(track, TRACK_LABELS['A'])

    # Calendar data
    days       = get_program_days()
    gcal_links = google_calendar_links(track, lang)
    day_fmt    = '%A %d %B %Y, %H:%M'

    assessment_id = assessment['id']
    ics_url       = f"{BASE_URL}/api/calendar/{assessment_id}.ics"

    ctx = {
        'name':        assessment['name'],
        'track':       track,
        'track_label': labels.get(lang, labels['en']),
        'assessment_id': assessment_id,
        # Day dates (human-readable)
        'day1_label':  days[0].strftime(day_fmt) if len(days) > 0 else '',
        'day2_label':  days[1].strftime(day_fmt) if len(days) > 1 else '',
        'day3_label':  days[2].strftime(day_fmt) if len(days) > 2 else '',
        # Google Calendar URLs
        'gcal_day1':   gcal_links[0]['url'] if len(gcal_links) > 0 else '#',
        'gcal_day2':   gcal_links[1]['url'] if len(gcal_links) > 1 else '#',
        'gcal_day3':   gcal_links[2]['url'] if len(gcal_links) > 2 else '#',
        # .ics download
        'ics_url':     ics_url,
    }

    tpl_name = f'enrollment_confirmation_{lang}.html'
    html     = _render(_load_template(tpl_name), ctx)
    subject  = ENROLLMENT_SUBJECTS.get(lang, ENROLLMENT_SUBJECTS['en'])

    return _send(assessment['email'], subject, html)
