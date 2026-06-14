"""
CAMIX Daily Email Service
=========================
Sends personalised day-by-day coaching emails to enrolled participants
for 30 days after enrolment.

Dispatch is triggered by POST /api/camix/daily-dispatch (called daily
by a Render cron job at 07:00 UTC).

Content strategy
----------------
  Days  1–7   : Foundation / orientation
  Days  8–14  : Progression / building habits
  Days 15–21  : Challenge / intensity
  Days 22–30  : Consolidation / maintenance mindset

Each day has:
  - A topic  (same for all participants on that day / phase)
  - A tip    (track-specific)
  - A micro-challenge (short, actionable)

GPT-4o is used to personalise the email body when an API key is
present; otherwise the template fallback is used directly.
"""

from __future__ import annotations

import os
import json
from typing import Optional

from services.email_service import _send
from services.ai_service import generate_text

BASE_URL = os.getenv("BASE_URL", "https://nl.centrocami.it")

# ── 30-day content map ───────────────────────────────────────────────────────
# Each entry: (topic, tip_A, tip_B, challenge)
# tip_A = CAMI Restore (clinical / 50+)
# tip_B = CAMI Perform (athletic / 25-55)

_DAYS: list[dict] = [
    # ── Foundation (1-7) ────────────────────────────────────────────────────
    {"day": 1,  "phase": "Foundation",
     "topic":     "Welcome to your 30-day journey",
     "tip_A":     "Start with 5 minutes of gentle joint mobility every morning — it costs nothing and compounds fast.",
     "tip_B":     "Log your baseline lifts today. You'll want this reference in 30 days.",
     "challenge": "Take a 10-minute walk today. Notice your posture."},

    {"day": 2,  "phase": "Foundation",
     "topic":     "The science of habit loops",
     "tip_A":     "Pair your exercises with an existing habit (morning coffee, evening news) to make them stick.",
     "tip_B":     "Set a fixed training window. Consistency beats intensity at this stage.",
     "challenge": "Write down your #1 movement goal for this month."},

    {"day": 3,  "phase": "Foundation",
     "topic":     "Breathing — your most underused tool",
     "tip_A":     "Diaphragmatic breathing reduces cortisol and improves core stability. Try 4-7-8 breathing before bed.",
     "tip_B":     "Practise box breathing (4-4-4-4) to improve VO2 efficiency and recovery.",
     "challenge": "Do 5 minutes of intentional diaphragmatic breathing today."},

    {"day": 4,  "phase": "Foundation",
     "topic":     "Sleep: the hidden variable",
     "tip_A":     "7-9 hours of sleep reduces fall risk and inflammation markers by up to 30% in older adults.",
     "tip_B":     "Sleep is when growth hormone peaks. Prioritising it is a legal performance enhancer.",
     "challenge": "Set a consistent sleep time tonight — same time as tomorrow."},

    {"day": 5,  "phase": "Foundation",
     "topic":     "Protein: how much do you actually need?",
     "tip_A":     "Research supports 1.2–1.6g/kg/day for adults 50+ to maintain muscle mass.",
     "tip_B":     "Aim for 1.6–2.2g/kg/day and distribute it across 3–4 meals for optimal muscle protein synthesis.",
     "challenge": "Track your protein intake for just today. No judgement — just awareness."},

    {"day": 6,  "phase": "Foundation",
     "topic":     "Hydration and joint health",
     "tip_A":     "Synovial fluid is 80% water. Even mild dehydration increases joint stiffness and perceived pain.",
     "tip_B":     "Dehydration by 2% impairs strength output by ~6%. Drink before you feel thirsty.",
     "challenge": "Drink 500 ml of water before your first meal today."},

    {"day": 7,  "phase": "Foundation",
     "topic":     "Week 1 check-in — how are you doing?",
     "tip_A":     "If something hurts beyond DOMS, reduce intensity — not duration. Movement is the medicine.",
     "tip_B":     "DOMS from this week means you recruited fibres that weren't used. Good sign.",
     "challenge": "Rate your energy today 1-10. Keep this number in mind as a baseline."},

    # ── Progression (8-14) ──────────────────────────────────────────────────
    {"day": 8,  "phase": "Progression",
     "topic":     "Progressive overload — the principle that drives all gains",
     "tip_A":     "Add 1 repetition or 30 seconds to each exercise this week. Small increments prevent injury.",
     "tip_B":     "Apply the 2-for-2 rule: if you hit 2 extra reps on 2 consecutive sessions, increase load by ~5%.",
     "challenge": "Pick one exercise and add 1 rep today."},

    {"day": 9,  "phase": "Progression",
     "topic":     "Balance and proprioception",
     "tip_A":     "Unilateral balance training (single-leg stance) is one of the strongest predictors of longevity in adults over 50.",
     "tip_B":     "Proprioceptive work reduces ACL and ankle sprain risk by up to 50% in sport contexts.",
     "challenge": "Stand on one leg for 30 seconds each side. Eyes open first, then closed."},

    {"day": 10, "phase": "Progression",
     "topic":     "Mobility vs. flexibility — know the difference",
     "tip_A":     "Flexibility is passive range. Mobility is active control of that range. Train mobility, not just stretching.",
     "tip_B":     "Mobility work done before lifting improves force production. It's not just injury prevention.",
     "challenge": "Do 2 minutes of hip 90/90 stretching before any lower-body activity today."},

    {"day": 11, "phase": "Progression",
     "topic":     "Managing fatigue intelligently",
     "tip_A":     "Fatigue is information. If you're consistently tired after training, reduce volume (sets) before intensity.",
     "tip_B":     "Fatigue management separates good periodisation from junk volume. Earn your rest days.",
     "challenge": "Rate your fatigue today 1-10. If ≥8, take an active rest day (walk, stretch)."},

    {"day": 12, "phase": "Progression",
     "topic":     "The role of stress in recovery",
     "tip_A":     "Psychological stress and physical stress share recovery resources. A stressful day = reduced training capacity.",
     "tip_B":     "HRV (Heart Rate Variability) is the best individual marker of recovery readiness. Track it if you can.",
     "challenge": "Spend 5 minutes today doing something purely restorative — no screens, no tasks."},

    {"day": 13, "phase": "Progression",
     "topic":     "Consistency over intensity",
     "tip_A":     "5 gentle sessions per week outperform 2 intense sessions for pain reduction and functional improvement.",
     "tip_B":     "Training frequency matters more than session duration for neurological adaptations.",
     "challenge": "Plan next week's sessions right now. Put them in your calendar."},

    {"day": 14, "phase": "Progression",
     "topic":     "Week 2 complete — notice what changed",
     "tip_A":     "Compare your energy today to Day 7. Most people notice improved morning stiffness by now.",
     "tip_B":     "Review your training log. Which session felt best? Do more of that format.",
     "challenge": "Write one thing that improved physically this week. No matter how small."},

    # ── Challenge (15-21) ───────────────────────────────────────────────────
    {"day": 15, "phase": "Challenge",
     "topic":     "Entering the challenge phase — time to push",
     "tip_A":     "Increase walking pace or duration by 10% this week. Your cardiovascular system is ready.",
     "tip_B":     "Add a technique session this week: slow down the eccentric phase to 3-4 seconds per rep.",
     "challenge": "Do today's session at 5% more intensity than usual."},

    {"day": 16, "phase": "Challenge",
     "topic":     "Compound movements: more return per minute",
     "tip_A":     "Sit-to-stand, step-ups, and wall push-ups train multiple joints simultaneously — maximising functional return.",
     "tip_B":     "Squat, hinge, push, pull, carry, rotate — master these six patterns and you cover everything.",
     "challenge": "Identify which of the 6 fundamental patterns is your weakest. Focus on it this week."},

    {"day": 17, "phase": "Challenge",
     "topic":     "Pain vs. discomfort — drawing the line",
     "tip_A":     "Discomfort (muscle burn, mild fatigue) is productive. Pain (sharp, joint-specific, >5/10) is a stop signal.",
     "tip_B":     "Learn to train around discomfort, not through pain. Ego lifts cause most acute injuries.",
     "challenge": "For every exercise today: rate comfort 1-10. Stop at anything ≥6/10 sharp pain."},

    {"day": 18, "phase": "Challenge",
     "topic":     "Recovery modalities — what actually works",
     "tip_A":     "Evidence supports: sleep, cold/contrast showers, gentle movement. Ice baths and foam rolling: mild benefit at best.",
     "tip_B":     "Cold exposure (10-15°C, 10 min) blunts some muscle protein synthesis. Use it after cardio, not strength sessions.",
     "challenge": "Take a contrast shower today (alternating 30s cold / 60s hot × 3 cycles)."},

    {"day": 19, "phase": "Challenge",
     "topic":     "Social accountability",
     "tip_A":     "Partnered exercise increases adherence by up to 65%. Find an exercise buddy in Utrecht.",
     "tip_B":     "Training with someone of similar ability raises output by an average of 15% (Kohler motivation effect).",
     "challenge": "Tell one person today about your 30-day CAMI journey. Saying it out loud increases commitment."},

    {"day": 20, "phase": "Challenge",
     "topic":     "Nutrition timing around exercise",
     "tip_A":     "A light snack with protein + carbs 60-90 min before exercise improves session quality noticeably at 50+.",
     "tip_B":     "Pre-workout carbs sustain performance. Post-workout protein (20-40g) within 2h optimises muscle repair.",
     "challenge": "Plan your pre- and post-exercise nutrition for your next 3 sessions."},

    {"day": 21, "phase": "Challenge",
     "topic":     "Three weeks in — you've built a habit",
     "tip_A":     "Research shows 21 days is enough to encode a basic habit loop. You've done it.",
     "tip_B":     "Neurological adaptations plateau around week 3-4 — now structural (muscle) changes accelerate.",
     "challenge": "Compare today's baseline metric (energy, a lift, walk time) to Day 1. Document the gap."},

    # ── Consolidation (22-30) ───────────────────────────────────────────────
    {"day": 22, "phase": "Consolidation",
     "topic":     "Building the maintenance mindset",
     "tip_A":     "The goal shifts from 'starting' to 'never stopping'. What's the minimum effective dose you can sustain forever?",
     "tip_B":     "Maintenance requires ~1/3 of the volume that built the adaptation. You've earned some flexibility.",
     "challenge": "Define your personal 'minimum dose' for each week post-programme."},

    {"day": 23, "phase": "Consolidation",
     "topic":     "Inflammation and lifestyle",
     "tip_A":     "Chronic low-grade inflammation is modifiable: improve sleep, reduce ultra-processed foods, move daily.",
     "tip_B":     "Omega-3s (2-3g EPA+DHA/day) reduce DOMS and support cardiovascular health for high-load training.",
     "challenge": "Replace one ultra-processed food today with a whole-food alternative."},

    {"day": 24, "phase": "Consolidation",
     "topic":     "Strength training as longevity medicine",
     "tip_A":     "Grip strength is the single best physical predictor of all-cause mortality in older adults. Train it.",
     "tip_B":     "The strongest predictor of athletic longevity is injury prevention, not peak performance. Train smart.",
     "challenge": "Do a 30-second dead-hang or farmer's carry to train grip strength today."},

    {"day": 25, "phase": "Consolidation",
     "topic":     "Movement outside the gym",
     "tip_A":     "NEAT (Non-Exercise Activity Thermogenesis) accounts for 15-30% of daily caloric expenditure. Stairs, walking, gardening — it all counts.",
     "tip_B":     "Zone 2 cardio (conversational pace) for 150+ min/week is the most evidence-supported longevity intervention available.",
     "challenge": "Take the stairs or walk an extra 10 minutes somewhere today."},

    {"day": 26, "phase": "Consolidation",
     "topic":     "Community and purpose in movement",
     "tip_A":     "Group exercise classes have a 30% higher adherence rate than solo training. Find your community.",
     "tip_B":     "Having a performance goal (a race, a competition, a PR) extends athletic careers by years.",
     "challenge": "Set one concrete goal for the next 90 days post-programme."},

    {"day": 27, "phase": "Consolidation",
     "topic":     "Revisiting your assessment goals",
     "tip_A":     "Look back at your original assessment answers. How has your relationship with pain and mobility changed?",
     "tip_B":     "Compare your original performance goals with where you are today. Recalibrate targets upward.",
     "challenge": "Re-read your original assessment goals (check your Day 1 email). Rate progress on each 1-10."},

    {"day": 28, "phase": "Consolidation",
     "topic":     "The deload — strategic rest",
     "tip_A":     "One lighter week every 4-6 weeks is not laziness — it's programming. Your body rebuilds during recovery.",
     "tip_B":     "A true deload (50-60% volume, same intensity) supercompensates performance for the next training block.",
     "challenge": "Plan a lighter week after programme completion. Put it in your calendar now."},

    {"day": 29, "phase": "Consolidation",
     "topic":     "Teaching what you've learned",
     "tip_A":     "Explaining a concept to someone else is one of the best ways to consolidate it in memory.",
     "tip_B":     "Coaching others — even informally — forces precision in your own technique and programming.",
     "challenge": "Share one thing you've learned this month with a friend or family member."},

    {"day": 30, "phase": "Consolidation",
     "topic":     "Day 30 — you made it. What's next?",
     "tip_A":     "You've built the foundation. CAMI Monthly keeps the momentum going with progressive coaching.",
     "tip_B":     "Peak performance is a process, not a destination. CAMI Monthly keeps you on the structured path.",
     "challenge": "Book your next step: CAMI Monthly subscription or a second cohort. Don't let momentum die here."},
]

_DAY_MAP = {d["day"]: d for d in _DAYS}

# ── Subject lines ─────────────────────────────────────────────────────────────

_SUBJECTS = {
    "it": "CAMI Giorno {day} – {topic}",
    "en": "CAMI Day {day} – {topic}",
    "nl": "CAMI Dag {day} – {topic}",
}

# ── HTML email template ───────────────────────────────────────────────────────

_HTML_TPL = """\
<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CAMI Day {day}</title>
</head>
<body style="margin:0;padding:0;background:#F9FAFB;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#F9FAFB;padding:32px 16px;">
  <tr><td align="center">
    <table width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;background:#ffffff;border-radius:16px;overflow:hidden;box-shadow:0 2px 12px rgba(0,0,0,.06);">

      <!-- Header -->
      <tr>
        <td style="background:#1E3A8A;padding:28px 40px;text-align:center;">
          <p style="margin:0;color:#93C5FD;font-size:13px;letter-spacing:2px;text-transform:uppercase;">{phase_label} · {day_label}</p>
          <h1 style="margin:8px 0 0;color:#ffffff;font-size:22px;font-weight:700;line-height:1.3;">{topic}</h1>
        </td>
      </tr>

      <!-- Greeting -->
      <tr>
        <td style="padding:32px 40px 0;">
          <p style="margin:0;font-size:17px;color:#1F2937;">{greeting}</p>
        </td>
      </tr>

      <!-- Main body -->
      <tr>
        <td style="padding:24px 40px 0;">
          {body_html}
        </td>
      </tr>

      <!-- Today's tip -->
      <tr>
        <td style="padding:24px 40px 0;">
          <table width="100%" cellpadding="0" cellspacing="0" style="background:#EFF6FF;border-left:4px solid #1E3A8A;border-radius:0 8px 8px 0;">
            <tr>
              <td style="padding:16px 20px;">
                <p style="margin:0 0 6px;font-size:11px;font-weight:700;color:#1E3A8A;letter-spacing:1.5px;text-transform:uppercase;">{tip_label}</p>
                <p style="margin:0;font-size:15px;color:#1F2937;line-height:1.6;">{tip}</p>
              </td>
            </tr>
          </table>
        </td>
      </tr>

      <!-- Challenge -->
      <tr>
        <td style="padding:20px 40px 0;">
          <table width="100%" cellpadding="0" cellspacing="0" style="background:#ECFDF5;border-left:4px solid #10B981;border-radius:0 8px 8px 0;">
            <tr>
              <td style="padding:16px 20px;">
                <p style="margin:0 0 6px;font-size:11px;font-weight:700;color:#10B981;letter-spacing:1.5px;text-transform:uppercase;">{challenge_label}</p>
                <p style="margin:0;font-size:15px;color:#1F2937;line-height:1.6;font-weight:600;">{challenge}</p>
              </td>
            </tr>
          </table>
        </td>
      </tr>

      <!-- CTA -->
      <tr>
        <td style="padding:28px 40px;">
          <p style="margin:0 0 16px;font-size:14px;color:#6B7280;">{cta_text}</p>
          <a href="{assessment_url}" style="display:inline-block;background:#1E3A8A;color:#ffffff;text-decoration:none;padding:12px 28px;border-radius:8px;font-size:15px;font-weight:600;">{cta_btn}</a>
        </td>
      </tr>

      <!-- Footer -->
      <tr>
        <td style="padding:20px 40px;border-top:1px solid #E5E7EB;">
          <p style="margin:0;font-size:12px;color:#9CA3AF;line-height:1.6;">
            CAMI Netherlands · Utrecht<br>
            Dott. Gabriele Liuzzo — Chinesiologo Clinico, Direttore Tecnico<br>
            <a href="{base_url}" style="color:#1E3A8A;text-decoration:none;">nl.centrocami.it</a> ·
            <a href="mailto:info@centrocami.it" style="color:#1E3A8A;text-decoration:none;">info@centrocami.it</a>
          </p>
        </td>
      </tr>

    </table>
  </td></tr>
</table>
</body>
</html>
"""

# ── Localisation strings ──────────────────────────────────────────────────────

_L10N = {
    "it": {
        "greeting":        "Ciao {name},",
        "tip_label":       "Il Consiglio di Oggi",
        "challenge_label": "La Sfida del Giorno",
        "phase_label":     {"Foundation": "Fondamento", "Progression": "Progressione",
                            "Challenge": "Intensificazione", "Consolidation": "Consolidamento"},
        "day_label":       "Giorno {day} di 30",
        "cta_text":        "Hai domande? Rispondi a questa email o accedi alla tua area personale.",
        "cta_btn":         "Area Personale →",
    },
    "en": {
        "greeting":        "Hi {name},",
        "tip_label":       "Today's Tip",
        "challenge_label": "Today's Challenge",
        "phase_label":     {"Foundation": "Foundation", "Progression": "Progression",
                            "Challenge": "Challenge", "Consolidation": "Consolidation"},
        "day_label":       "Day {day} of 30",
        "cta_text":        "Got questions? Reply to this email or visit your personal area.",
        "cta_btn":         "Personal Area →",
    },
    "nl": {
        "greeting":        "Hoi {name},",
        "tip_label":       "Tip van de Dag",
        "challenge_label": "Uitdaging van de Dag",
        "phase_label":     {"Foundation": "Fundament", "Progression": "Progressie",
                            "Challenge": "Uitdaging", "Consolidation": "Consolidatie"},
        "day_label":       "Dag {day} van 30",
        "cta_text":        "Vragen? Beantwoord deze e-mail of ga naar jouw persoonlijke gebied.",
        "cta_btn":         "Persoonlijk Gebied →",
    },
}


# ── GPT-4o body personalisation ───────────────────────────────────────────────

def _ai_body(name: str, day_data: dict, track: str, lang: str, profile: Optional[dict] = None) -> Optional[str]:
    """
    Generate a 2-3 sentence personalised intro paragraph using GPT-4o.
    Returns None on error / missing key (fallback to static body).
    """
    try:
        tip = day_data["tip_A"] if track in ("A", "Hybrid") else day_data["tip_B"]
        profile_note = ""
        if profile:
            age = profile.get("age")
            goals = profile.get("goals", [])
            if age:
                profile_note += f" The participant is {age} years old."
            if goals:
                profile_note += f" Their goals include: {', '.join(goals[:3])}."

        prompt = (
            f"You are CAMIX, the AI coaching assistant for CAMI Netherlands (clinical exercise & athletic performance).\n"
            f"Write a warm, motivating 2-3 sentence personalised introduction for a Day {day_data['day']} coaching email.\n"
            f"Participant name: {name}. Track: {'CAMI Restore (clinical/50+)' if track in ('A','Hybrid') else 'CAMI Perform (athletic)'}."
            f"{profile_note}\n"
            f"Today's topic: {day_data['topic']}.\n"
            f"Write in {'Italian' if lang == 'it' else 'Dutch' if lang == 'nl' else 'English'}.\n"
            f"Keep it under 80 words. No subject line, no greeting — just the body paragraph."
        )
        text = generate_text(prompt, max_tokens=120, temperature=0.7)
        if text and len(text) > 20:
            return f"<p style='margin:0;font-size:15px;color:#374151;line-height:1.7;'>{text}</p>"
    except Exception as exc:  # noqa: BLE001
        print(f"[CAMIX] GPT-4o body failed: {exc}")
    return None


def _static_body(day_data: dict, track: str, lang: str) -> str:
    """Static fallback body paragraph."""
    topic = day_data["topic"]
    phase = day_data["phase"]
    texts = {
        "it": f"<p style='margin:0;font-size:15px;color:#374151;line-height:1.7;'>Siamo nella fase <strong>{phase}</strong> del tuo percorso. L'argomento di oggi è: <em>{topic}</em>. Leggi il consiglio qui sotto e completa la sfida del giorno — anche 5 minuti contano.</p>",
        "en": f"<p style='margin:0;font-size:15px;color:#374151;line-height:1.7;'>We're in the <strong>{phase}</strong> phase of your journey. Today's focus: <em>{topic}</em>. Read the tip below and complete today's challenge — even 5 minutes counts.</p>",
        "nl": f"<p style='margin:0;font-size:15px;color:#374151;line-height:1.7;'>We zitten in de <strong>{phase}</strong>-fase van jouw traject. Het onderwerp van vandaag: <em>{topic}</em>. Lees de tip hieronder en voltooi de dagelijkse uitdaging — ook 5 minuten telt.</p>",
    }
    return texts.get(lang, texts["en"])


# ── Public API ────────────────────────────────────────────────────────────────

def build_daily_email(
    assessment: dict,
    day: int,
    use_ai: bool = True,
) -> tuple[str, str]:
    """
    Build (subject, html) for a given participant and day number (1-30).
    Returns ('', '') if day is out of range.
    """
    if day < 1 or day > 30:
        return "", ""

    day_data = _DAY_MAP[day]
    lang = assessment.get("language", "en")
    if lang not in ("it", "en", "nl"):
        lang = "en"

    track = assessment.get("track_recommended", "A")
    name = assessment.get("name", "there").split()[0]  # first name only
    l10n = _L10N[lang]

    tip = day_data["tip_A"] if track in ("A", "Hybrid") else day_data["tip_B"]

    # Body paragraph
    body_html = None
    if use_ai:
        profile = {
            "age": assessment.get("age"),
            "goals": json.loads(assessment.get("goals", "[]")) if isinstance(assessment.get("goals"), str) else assessment.get("goals", []),
        }
        body_html = _ai_body(name, day_data, track, lang, profile)
    if not body_html:
        body_html = _static_body(day_data, track, lang)

    phase_label = l10n["phase_label"].get(day_data["phase"], day_data["phase"])
    day_label = l10n["day_label"].format(day=day)
    assessment_url = f"{BASE_URL}/assessment/{assessment.get('id', '')}"

    html = _HTML_TPL.format(
        lang=lang,
        day=day,
        phase_label=phase_label,
        day_label=day_label,
        topic=day_data["topic"],
        greeting=l10n["greeting"].format(name=name),
        body_html=body_html,
        tip_label=l10n["tip_label"],
        tip=tip,
        challenge_label=l10n["challenge_label"],
        challenge=day_data["challenge"],
        cta_text=l10n["cta_text"],
        cta_btn=l10n["cta_btn"],
        assessment_url=assessment_url,
        base_url=BASE_URL,
    )

    subject = _SUBJECTS.get(lang, _SUBJECTS["en"]).format(day=day, topic=day_data["topic"])
    return subject, html


def send_daily_email(assessment: dict, day: int) -> dict:
    """Send the day's email and return the Resend result dict."""
    subject, html = build_daily_email(assessment, day)
    if not subject:
        return {"status": "skipped", "reason": f"day {day} out of range"}

    result = _send(to=assessment["email"], subject=subject, html=html)
    return result
