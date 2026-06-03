"""
SENTINEL Safety Gate
Mirrors the frontend logic but authoritative server-side.
Returns: 'pass' | 'medical_clearance_required' | 'declined'
"""


CLINICAL_GOALS    = {'reduce_chronic_pain', 'improve_mobility', 'improve_balance', 'maintain_independence'}
PERFORMANCE_GOALS = {'increase_strength', 'improve_power', 'competition_prep'}
HYBRID_GOAL       = 'injury_recovery_return'


# ── SENTINEL ──────────────────────────────────────────────────────────────────

def sentinel_check(goals: list, screening: dict) -> str:
    parq = screening.get('parq', {})
    parq_keys = ['parq_heart', 'parq_chest_active', 'parq_chest_rest',
                 'parq_dizziness', 'parq_bone_joint', 'parq_medication', 'parq_other']

    yes_count = sum(1 for k in parq_keys if parq.get(k) == 'yes')

    # Acute pain check (Track A)
    if screening.get('has_chronic_pain') and isinstance(screening.get('pain_severity'), int):
        if screening['pain_severity'] >= 8:
            return 'medical_clearance_required'

    # Recent injury without clearance (Track B)
    if screening.get('recent_injury') and not screening.get('injury_clearance'):
        return 'medical_clearance_required'

    if yes_count == 0:
        return 'pass'
    elif yes_count >= 3:
        return 'declined'
    else:
        return 'medical_clearance_required'


# ── TRIAGE ────────────────────────────────────────────────────────────────────

def triage(goals: list, age: int, screening: dict) -> dict:
    """
    Returns {
        track_recommended: 'A' | 'B' | 'Hybrid',
        clinical_score: int,
        performance_score: int,
        medical_clearance_required: bool
    }
    """
    clinical_score    = 0
    performance_score = 0
    hybrid_candidate  = False

    # Goal scoring
    goal_weights = {
        'reduce_chronic_pain':   ('clinical', 3),
        'improve_mobility':      ('clinical', 3),
        'improve_balance':       ('clinical', 3),
        'maintain_independence': ('clinical', 2),
        'increase_strength':     ('performance', 3),
        'improve_power':         ('performance', 3),
        'competition_prep':      ('performance', 4),
        'injury_recovery_return':('hybrid', 1),
    }

    for goal in goals:
        if goal in goal_weights:
            track, weight = goal_weights[goal]
            if track == 'clinical':
                clinical_score += weight
            elif track == 'performance':
                performance_score += weight
            elif track == 'hybrid':
                clinical_score    += weight
                performance_score += weight
                hybrid_candidate   = True

    # Age modifiers
    if age >= 66:
        clinical_score += 2
    elif age >= 56:
        clinical_score += 1
    elif age <= 45:
        performance_score += 1

    # Track A screening modifiers
    if screening.get('has_chronic_pain'):
        severity = screening.get('pain_severity', 0)
        clinical_score += min(severity // 2, 5)   # cap at +5

    if screening.get('has_fallen'):
        clinical_score += 3

    if screening.get('balance_difficulty'):
        clinical_score += 3

    # Track B screening modifiers
    years_map = {
        'less_1': 0, '1_3': 1, '3_5': 2, '5_10': 3, '10plus': 4
    }
    freq_map = {
        '1_2x': 0, '3_4x': 1, '5_6x': 2, '7plus_x': 3
    }

    training_years = screening.get('training_years', '')
    training_freq  = screening.get('training_frequency', '')

    performance_score += years_map.get(training_years, 0)
    performance_score += freq_map.get(training_freq, 0)

    # PAR-Q modifiers
    parq = screening.get('parq', {})
    parq_keys = ['parq_heart', 'parq_chest_active', 'parq_chest_rest',
                 'parq_dizziness', 'parq_bone_joint', 'parq_medication', 'parq_other']
    yes_count = sum(1 for k in parq_keys if parq.get(k) == 'yes')
    if yes_count >= 2:
        clinical_score += 2

    # Injury recovery hybrid
    if screening.get('recent_injury'):
        hybrid_candidate = True

    # Medical clearance
    medical_clearance_required = (
        yes_count >= 2 or
        (screening.get('recent_injury') and not screening.get('injury_clearance'))
    )

    # Decision
    diff = clinical_score - performance_score

    if hybrid_candidate and abs(diff) <= 3:
        track = 'Hybrid'
    elif diff >= 3:
        track = 'A'
    elif diff <= -3:
        track = 'B'
    else:
        # Edge: age breaks tie
        if age >= 60:
            track = 'A'
        elif age <= 45 and performance_score > 0:
            track = 'B'
        else:
            track = 'Hybrid'

    return {
        'track_recommended':        track,
        'clinical_score':           clinical_score,
        'performance_score':        performance_score,
        'medical_clearance_required': medical_clearance_required,
    }
