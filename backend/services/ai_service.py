"""
CAMIX AI Analysis Service
Calls OpenAI GPT-4 to generate a personalised 2-3 paragraph assessment
recommendation in the user's language (IT / EN / NL).

Gracefully degrades: if OPENAI_API_KEY is not set, or the API call fails,
returns None so the rest of the pipeline continues unaffected.
"""
import os
import json

# Optional import – don't crash if openai is not installed
try:
    from openai import OpenAI
    _openai_available = True
except ImportError:
    _openai_available = False

_TRACK_LABEL = {
    'A':      {'it': 'CAMI Restore (Esercizio Clinico)', 'en': 'CAMI Restore (Clinical Exercise)', 'nl': 'CAMI Restore (Klinische Oefening)'},
    'B':      {'it': 'CAMI Perform (Performance Atletica)', 'en': 'CAMI Perform (Athletic Performance)', 'nl': 'CAMI Perform (Atletische Prestaties)'},
    'Hybrid': {'it': 'Programma Ibrido',                   'en': 'Hybrid Program',                        'nl': 'Hybride Programma'},
}

_SYSTEM_PROMPT = {
    'it': (
        "Sei CAMIX, l'assistente AI clinico di Centro CAMI Netherlands. "
        "Sei esperto in esercizio clinico, chinesiologia, riabilitazione funzionale e preparazione atletica. "
        "Il tuo stile è professionale, caldo e motivante. "
        "Quando analizzi una valutazione, fornisci 2-3 paragrafi brevi che spiegano: "
        "1) la comprensione della situazione specifica del cliente; "
        "2) perché il programma consigliato è la scelta giusta; "
        "3) i primi passi pratici e cosa aspettarsi. "
        "Usa 'tu' (informale). Non usare elenchi puntati. Non usare markdown. "
        "Lunghezza massima: 200 parole."
    ),
    'en': (
        "You are CAMIX, the clinical AI assistant for Centro CAMI Netherlands. "
        "You specialise in clinical exercise, kinesiology, functional rehabilitation and athletic preparation. "
        "Your tone is professional, warm, and motivating. "
        "When analysing an assessment, provide 2-3 short paragraphs covering: "
        "1) understanding of the client's specific situation; "
        "2) why the recommended program is the right choice; "
        "3) practical first steps and what to expect. "
        "Address the client as 'you'. No bullet points. No markdown. "
        "Maximum length: 200 words."
    ),
    'nl': (
        "Je bent CAMIX, de klinische AI-assistent van Centro CAMI Netherlands. "
        "Je bent gespecialiseerd in klinische oefening, kinesiologie, functionele revalidatie en atletische voorbereiding. "
        "Je toon is professioneel, warm en motiverend. "
        "Analyseer de beoordeling en geef 2-3 korte alinea's over: "
        "1) begrip van de specifieke situatie van de cliënt; "
        "2) waarom het aanbevolen programma de juiste keuze is; "
        "3) praktische eerste stappen en wat te verwachten. "
        "Spreek de cliënt aan met 'je/jij'. Geen opsommingstekens. Geen markdown. "
        "Maximale lengte: 200 woorden."
    ),
}


def analyze_assessment(
    profile: dict,
    goals: list,
    screening: dict,
    track: str,
    lang: str = 'en',
) -> str | None:
    """
    Generate a personalised AI analysis for a completed CAMI assessment.

    Parameters
    ----------
    profile   : dict  – name, age, language, referral_source, etc.
    goals     : list  – list of goal strings (e.g. ['reduce_chronic_pain', ...])
    screening : dict  – PAR-Q answers, pain severity, injury history, etc.
    track     : str   – 'A', 'B', or 'Hybrid'
    lang      : str   – 'it', 'en', or 'nl'

    Returns
    -------
    str | None  – The AI-generated paragraph text, or None on failure.
    """
    api_key = os.getenv('OPENAI_API_KEY', '').strip()
    if not api_key:
        print('[AI] OPENAI_API_KEY not set – skipping AI analysis')
        return None
    if not _openai_available:
        print('[AI] openai package not installed – skipping AI analysis')
        return None

    # Normalise lang
    lang = lang if lang in ('it', 'en', 'nl') else 'en'
    track_label = _TRACK_LABEL.get(track, _TRACK_LABEL['Hybrid'])[lang]

    # Build a concise user message with just the data GPT-4 needs
    user_msg = _build_user_message(profile, goals, screening, track_label, lang)

    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model='gpt-4o',
            messages=[
                {'role': 'system', 'content': _SYSTEM_PROMPT[lang]},
                {'role': 'user',   'content': user_msg},
            ],
            max_tokens=350,
            temperature=0.7,
        )
        text = response.choices[0].message.content.strip()
        print(f'[AI] Analysis generated ({len(text)} chars, lang={lang})')
        return text
    except Exception as e:
        print(f'[AI] OpenAI call failed: {e}')
        return None


def generate_text(prompt: str, max_tokens: int = 200, temperature: float = 0.7) -> str | None:
    """
    Generic GPT-4o text generation.
    Returns the completion string or None on failure / missing key.
    """
    api_key = os.getenv('OPENAI_API_KEY', '')
    if not api_key or not _openai_available:
        return None
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model='gpt-4o',
            messages=[{'role': 'user', 'content': prompt}],
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f'[AI] generate_text failed: {e}')
        return None


# ── Internal helpers ──────────────────────────────────────────────────────────

def _build_user_message(
    profile: dict,
    goals: list,
    screening: dict,
    track_label: str,
    lang: str,
) -> str:
    name = profile.get('name', '').split()[0] or 'Cliente'
    age  = profile.get('age', '?')

    goal_map = {
        'reduce_chronic_pain':      {'it': 'riduzione dolore cronico',       'en': 'chronic pain reduction',        'nl': 'chronische pijnvermindering'},
        'improve_mobility':         {'it': 'miglioramento mobilità',         'en': 'mobility improvement',          'nl': 'mobiliteitverbetering'},
        'improve_balance':          {'it': 'miglioramento equilibrio',       'en': 'balance improvement',           'nl': 'balanverbetering'},
        'maintain_independence':    {'it': 'mantenimento autonomia',         'en': 'maintain independence',         'nl': 'zelfstandigheid behouden'},
        'injury_recovery_return':   {'it': 'recupero da infortunio',        'en': 'injury recovery',               'nl': 'herstel van blessure'},
        'increase_strength':        {'it': 'aumento forza',                 'en': 'strength increase',             'nl': 'krachtstoename'},
        'improve_power':            {'it': 'miglioramento potenza',         'en': 'power development',             'nl': 'explosiviteitsverbetering'},
        'competition_prep':         {'it': 'preparazione gare',             'en': 'competition preparation',       'nl': 'wedstrijdvoorbereiding'},
        'general_fitness':          {'it': 'forma fisica generale',         'en': 'general fitness',               'nl': 'algemene fitheid'},
    }

    goals_text = ', '.join(
        goal_map.get(g, {}).get(lang, g) for g in goals
    ) or ('nessun obiettivo specificato' if lang == 'it' else
          'no goals specified' if lang == 'en' else
          'geen doelen opgegeven')

    pain_severity = screening.get('pain_severity', 0)
    pain_location = screening.get('pain_location', '')
    has_chronic   = screening.get('chronic_condition', False)
    par_q_count   = sum(1 for k, v in screening.items() if k.startswith('parq_') and v)
    training_yrs  = screening.get('training_years', '')
    training_freq = screening.get('training_frequency', '')

    if lang == 'it':
        msg = (
            f"Valutazione di {name}, {age} anni.\n"
            f"Obiettivi: {goals_text}.\n"
            f"Programma consigliato dall'algoritmo: {track_label}.\n"
        )
        if pain_severity:
            msg += f"Dolore attuale: {pain_severity}/10"
            if pain_location:
                msg += f" ({pain_location})"
            msg += ".\n"
        if has_chronic:
            msg += "Ha una condizione cronica o usa farmaci regolarmente.\n"
        if par_q_count:
            msg += f"Risposte positive al PAR-Q+: {par_q_count}.\n"
        if training_yrs:
            msg += f"Anni di allenamento: {training_yrs}.\n"
        if training_freq:
            msg += f"Frequenza di allenamento attuale: {training_freq}.\n"
        msg += "\nScrivi l'analisi personalizzata per questo cliente."
    elif lang == 'nl':
        msg = (
            f"Beoordeling van {name}, {age} jaar.\n"
            f"Doelen: {goals_text}.\n"
            f"Door algoritme aanbevolen programma: {track_label}.\n"
        )
        if pain_severity:
            msg += f"Huidige pijn: {pain_severity}/10"
            if pain_location:
                msg += f" ({pain_location})"
            msg += ".\n"
        if has_chronic:
            msg += "Heeft een chronische aandoening of gebruikt regelmatig medicatie.\n"
        if par_q_count:
            msg += f"Positieve PAR-Q+ antwoorden: {par_q_count}.\n"
        if training_yrs:
            msg += f"Jaren training: {training_yrs}.\n"
        if training_freq:
            msg += f"Huidige trainingsfrequentie: {training_freq}.\n"
        msg += "\nSchrijf de gepersonaliseerde analyse voor deze cliënt."
    else:  # en
        msg = (
            f"Assessment for {name}, age {age}.\n"
            f"Goals: {goals_text}.\n"
            f"Algorithm-recommended program: {track_label}.\n"
        )
        if pain_severity:
            msg += f"Current pain: {pain_severity}/10"
            if pain_location:
                msg += f" ({pain_location})"
            msg += ".\n"
        if has_chronic:
            msg += "Has a chronic condition or takes regular medication.\n"
        if par_q_count:
            msg += f"Positive PAR-Q+ answers: {par_q_count}.\n"
        if training_yrs:
            msg += f"Years of training: {training_yrs}.\n"
        if training_freq:
            msg += f"Current training frequency: {training_freq}.\n"
        msg += "\nWrite the personalised analysis for this client."

    return msg
