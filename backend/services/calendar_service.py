"""
Calendar service: generates Google Calendar URLs and .ics content.

Program structure: 3 sessions (default: 3 consecutive Saturdays at 10:00).
Configure via env:
  PROGRAM_START_DATE=2026-07-05   (first Saturday, YYYY-MM-DD)
  PROGRAM_SESSION_HOUR=10         (start hour, 24h, default 10)
  PROGRAM_SESSION_DURATION=4      (hours per session, default 4)
  PROGRAM_LOCATION=Utrecht, Netherlands
"""
import os
from datetime import datetime, timedelta, timezone
from urllib.parse import quote

LOCATION     = os.getenv('PROGRAM_LOCATION', 'Utrecht, Netherlands')
SESSION_HOUR = int(os.getenv('PROGRAM_SESSION_HOUR', 10))
DURATION_H   = int(os.getenv('PROGRAM_SESSION_DURATION', 4))
ORGANIZER    = 'info@centrocami.it'


def _next_saturday(weeks_ahead: int = 2) -> datetime:
    today = datetime.today()
    days_to_sat = (5 - today.weekday()) % 7 or 7
    return today + timedelta(days=days_to_sat + weeks_ahead * 7)


def get_program_days() -> list[datetime]:
    """Returns [day1, day2, day3] datetimes for the 3 program sessions."""
    raw = os.getenv('PROGRAM_START_DATE', '').strip()
    if raw:
        try:
            start = datetime.strptime(raw, '%Y-%m-%d')
        except ValueError:
            start = _next_saturday(2)
    else:
        start = _next_saturday(2)

    start = start.replace(hour=SESSION_HOUR, minute=0, second=0, microsecond=0)
    return [
        start,
        start + timedelta(weeks=1),
        start + timedelta(weeks=2),
    ]


# ── Track labels ───────────────────────────────────────────────────────────────
_TRACK_LABEL = {
    'A':      {'it': 'CAMI Restore – Esercizio Clinico',    'en': 'CAMI Restore – Clinical Exercise',     'nl': 'CAMI Restore – Klinische Oefening'},
    'B':      {'it': 'CAMI Perform – Performance Atletica', 'en': 'CAMI Perform – Athletic Performance',  'nl': 'CAMI Perform – Atletische Prestaties'},
    'Hybrid': {'it': 'CAMI Hybrid',                         'en': 'CAMI Hybrid',                          'nl': 'CAMI Hybrid'},
}

_DAY_DESC = {
    'it': ['Sessione 1 di 3 – Valutazione e introduzione al programma CAMI Netherlands.',
           'Sessione 2 di 3 – Esercizi personalizzati e feedback progressi.',
           'Sessione 3 di 3 – Sessione finale + avvio coaching quotidiano 30 giorni.'],
    'en': ['Session 1 of 3 – Assessment and introduction to the CAMI Netherlands program.',
           'Session 2 of 3 – Personalised exercises and progress feedback.',
           'Session 3 of 3 – Final session + start of 30-day daily coaching.'],
    'nl': ['Sessie 1 van 3 – Beoordeling en introductie tot het CAMI Netherlands programma.',
           'Sessie 2 van 3 – Gepersonaliseerde oefeningen en voortgangsbespreking.',
           'Sessie 3 van 3 – Eindsessie + start 30 dagen dagelijkse coaching.'],
}


def _fmt_gcal(dt: datetime) -> str:
    """Format datetime as Google Calendar timestamp (UTC-naive = local)."""
    return dt.strftime('%Y%m%dT%H%M%S')


def _fmt_ics(dt: datetime) -> str:
    """Format datetime as iCalendar local time string."""
    return dt.strftime('%Y%m%dT%H%M%S')


def google_calendar_links(track: str, lang: str = 'en') -> list[dict]:
    """
    Returns a list of 3 dicts, one per program day:
      { day: 1, url: 'https://calendar.google.com/...' }
    """
    days  = get_program_days()
    label = _TRACK_LABEL.get(track, _TRACK_LABEL['A']).get(lang, _TRACK_LABEL['A']['en'])
    descs = _DAY_DESC.get(lang, _DAY_DESC['en'])
    links = []

    for i, dt in enumerate(days):
        dt_end  = dt + timedelta(hours=DURATION_H)
        title   = f"CAMI NL – {label} – Dag {i+1}" if lang == 'nl' else f"CAMI NL – {label} – Day {i+1}"
        if lang == 'it':
            title = f"CAMI NL – {label} – Giorno {i+1}"

        params = (
            f"action=TEMPLATE"
            f"&text={quote(title)}"
            f"&dates={_fmt_gcal(dt)}/{_fmt_gcal(dt_end)}"
            f"&details={quote(descs[i])}"
            f"&location={quote(LOCATION)}"
            f"&sf=true&output=xml"
        )
        links.append({'day': i + 1, 'url': f"https://calendar.google.com/calendar/render?{params}"})

    return links


def generate_ics(track: str, lang: str = 'en', client_name: str = '',
                 client_email: str = '') -> str:
    """
    Returns the full .ics text containing 3 VEVENT entries (one per program day).
    """
    days  = get_program_days()
    label = _TRACK_LABEL.get(track, _TRACK_LABEL['A']).get(lang, _TRACK_LABEL['A']['en'])
    descs = _DAY_DESC.get(lang, _DAY_DESC['en'])
    now   = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')

    day_word = {'it': 'Giorno', 'nl': 'Dag'}.get(lang, 'Day')

    lines = [
        'BEGIN:VCALENDAR',
        'VERSION:2.0',
        'PRODID:-//CAMI Netherlands//EN',
        'CALSCALE:GREGORIAN',
        'METHOD:REQUEST',
        f'X-WR-CALNAME:CAMI Netherlands – {label}',
        'X-WR-TIMEZONE:Europe/Amsterdam',
    ]

    for i, dt in enumerate(days):
        dt_end = dt + timedelta(hours=DURATION_H)
        uid    = f"cami-nl-{track.lower()}-day{i+1}-{dt.strftime('%Y%m%d')}@centrocami.it"
        summary = f"CAMI NL – {day_word} {i+1}: {label}"

        lines += [
            'BEGIN:VEVENT',
            f'DTSTART;TZID=Europe/Amsterdam:{_fmt_ics(dt)}',
            f'DTEND;TZID=Europe/Amsterdam:{_fmt_ics(dt_end)}',
            f'DTSTAMP:{now}',
            f'UID:{uid}',
            f'SUMMARY:{summary}',
            f'DESCRIPTION:{descs[i].replace(",", "\\,")}',
            f'LOCATION:{LOCATION}',
            f'ORGANIZER;CN=CAMI Netherlands:mailto:{ORGANIZER}',
        ]
        if client_email:
            lines.append(
                f'ATTENDEE;CUTYPE=INDIVIDUAL;ROLE=REQ-PARTICIPANT;'
                f'CN={client_name}:mailto:{client_email}'
            )
        lines += [
            'STATUS:CONFIRMED',
            'SEQUENCE:0',
            'END:VEVENT',
        ]

    lines.append('END:VCALENDAR')
    return '\r\n'.join(lines) + '\r\n'
