# Triage Routing Logic
**CAMI Netherlands - Automated Track A / Track B / Hybrid Recommendation**

## Purpose
Automatically recommend the most appropriate program (Track A Clinical, Track B Performance, or Hybrid) based on assessment responses.

## Input Data
Assessment responses from intake form (goals, health screening, training history, pain/injury).

## Triage Algorithm

### Step 1: Analyze Goals
**Score each goal category:**
- **Clinical goals** (Track A indicators):
  - `reduce_chronic_pain` = +3 points
  - `improve_mobility` = +3 points
  - `improve_balance` = +3 points
  - `prevent_falls` = +3 points
  - `maintain_independence` = +2 points

- **Performance goals** (Track B indicators):
  - `increase_strength` = +3 points
  - `build_muscle` = +2 points
  - `improve_power` = +3 points
  - `improve_speed` = +3 points
  - `improve_endurance` = +2 points
  - `competition_prep` = +4 points

- **Hybrid indicators**:
  - `injury_recovery_return` = Hybrid candidate (recovery → performance transition)

**Calculate goal scores:**
- `clinical_score` = sum of Track A goal points
- `performance_score` = sum of Track B goal points

### Step 2: Analyze Age
**Age modifiers:**
- Age 18-45: `performance_score += 1` (younger, likely performance-focused)
- Age 46-55: No modifier (ambiguous, could be either)
- Age 56-65: `clinical_score += 1` (increased risk of chronic conditions)
- Age 66+: `clinical_score += 2` (higher priority for fall prevention, autonomy)

### Step 3: Analyze Health Screening
**PAR-Q+ red flags** (any YES response):
- Heart condition, chest pain, dizziness, bone/joint problem, blood pressure medication, other medical reason
- If ANY PAR-Q+ red flag: `medical_clearance_required = true`
- If 2+ PAR-Q+ red flags: `clinical_score += 2` (higher risk, clinical approach safer)

**Track A specific screening:**
- Chronic pain: `clinical_score += pain_severity` (0-10 scale, more pain → more clinical focus)
- Fall history (fallen in past year): `clinical_score += 3`
- Balance difficulty: `clinical_score += 3`
- Chronic conditions (osteoporosis, arthritis, etc.): `clinical_score += 2`
- Medications affecting balance: `clinical_score += 2`

**Track B specific screening:**
- Recent injury (past 6 months):
  - Status "healed" + medical clearance: No modifier (ready for performance)
  - Status "healing" or "still_painful": `hybrid_candidate = true` (needs clinical foundation before full performance)
  - No medical clearance: `medical_clearance_required = true`

- Current pain or movement limitations:
  - Has limitations: `hybrid_candidate = true` (clinical + performance blend)
  - No limitations: `performance_score += 1` (clear for full performance training)

### Step 4: Analyze Training History (Track B only)
**Training experience modifiers:**
- Years training:
  - <1 year: `performance_score += 0` (beginner, may need movement quality first)
  - 1-3 years: `performance_score += 1`
  - 3-5 years: `performance_score += 2`
  - 5-10 years: `performance_score += 3`
  - 10+ years: `performance_score += 4`

- Training frequency:
  - 1-2x/week: `clinical_score += 1` (low activity, may benefit from clinical foundation)
  - 3-4x/week: No modifier (moderate, could be either)
  - 5-6x/week: `performance_score += 2` (high volume, serious athlete)
  - 7+x/week: `performance_score += 3` (very high volume, dedicated athlete)

- Strength baselines (if provided any 1RM data):
  - `performance_score += 2` (shows performance focus, training maturity)

### Step 5: Triage Decision
**Calculate final recommendation:**

```python
def triage_recommendation(clinical_score, performance_score, hybrid_candidate, medical_clearance_required):
    # If medical clearance required, always manual review
    if medical_clearance_required:
        return {
            "track": "manual_review",
            "reason": "Medical clearance required based on PAR-Q+ or recent injury",
            "action": "email_medical_clearance_form"
        }
    
    # If hybrid candidate flag set (injury recovery or mixed clinical+performance indicators)
    if hybrid_candidate:
        return {
            "track": "hybrid",
            "reason": "Mixed indicators suggest blended clinical + performance approach",
            "action": "manual_review_recommend_hybrid"
        }
    
    # If clinical score significantly higher than performance score
    if clinical_score >= performance_score + 3:
        return {
            "track": "A",
            "reason": f"Clinical goals and screening prioritize Track A (score: {clinical_score} vs {performance_score})",
            "action": "recommend_track_a"
        }
    
    # If performance score significantly higher than clinical score
    if performance_score >= clinical_score + 3:
        return {
            "track": "B",
            "reason": f"Performance goals and training history prioritize Track B (score: {performance_score} vs {clinical_score})",
            "action": "recommend_track_b"
        }
    
    # If scores are close (within 2 points)
    if abs(clinical_score - performance_score) <= 2:
        # Edge cases: decide based on age or training experience
        if age >= 60:
            return {
                "track": "A",
                "reason": "Close scores, age 60+ prioritizes clinical safety and autonomy",
                "action": "recommend_track_a"
            }
        elif training_years >= "5_10" and training_frequency in ["5_6x", "7plus_x"]:
            return {
                "track": "B",
                "reason": "Close scores, high training volume prioritizes performance goals",
                "action": "recommend_track_b"
            }
        else:
            return {
                "track": "hybrid",
                "reason": "Close scores suggest hybrid approach (clinical foundation + performance goals)",
                "action": "manual_review_recommend_hybrid"
            }
    
    # Fallback (shouldn't reach here, but safety)
    return {
        "track": "manual_review",
        "reason": "Ambiguous scoring, manual review recommended",
        "action": "notify_admin"
    }
```

## Triage Outcomes

### Track A Recommendation
**When:**
- High chronic pain (severity 6-10)
- Fall history or balance difficulty
- Age 60+ with mobility concerns
- Clinical goals dominant (pain, balance, independence)

**Email message:**
> Based on your assessment, we recommend our **Track A: Clinical Exercise & Healthy Aging Program**.
> 
> Why Track A is right for you:
> - You mentioned [chronic pain / mobility concerns / balance issues]
> - Our program focuses on [reducing pain / improving mobility / fall prevention]
> - You'll build autonomy and confidence in daily activities
> 
> [Continue with program details, pricing, payment link]

### Track B Recommendation
**When:**
- Strength, power, competition goals dominant
- Training experience 3+ years, frequency 4+x/week
- No chronic pain or movement limitations
- Age <55 with performance focus

**Email message:**
> Based on your assessment, we recommend our **Track B: Performance & Athletic Preparation Program**.
> 
> Why Track B is right for you:
> - You mentioned [strength goals / competition prep / athletic performance]
> - Our program focuses on [maximal strength / power development / sport-specific conditioning]
> - You'll break through plateaus and optimize performance
> 
> [Continue with program details, pricing, payment link]

### Hybrid Recommendation
**When:**
- Mixed goals (clinical + performance)
- Injury recovery + return to performance
- Older athlete (50-60) with performance goals but clinical considerations
- Scores within 2 points (ambiguous)

**Email message:**
> Based on your assessment, we recommend a **Hybrid Program** combining elements of Track A (Clinical Exercise) and Track B (Performance Training).
> 
> Why Hybrid is right for you:
> - You mentioned both [clinical concerns: pain/mobility] and [performance goals: strength/competition]
> - Our hybrid approach builds a solid clinical foundation (movement quality, injury prevention) while progressing toward performance goals
> - You'll benefit from individualized programming tailored to your unique profile
> 
> **Next step**: Our team will review your assessment and create a custom hybrid program. You'll receive a follow-up email within 24 hours with your personalized plan and pricing.

**Action:** Notify admin for manual hybrid program design.

### Medical Clearance Required
**When:**
- Multiple PAR-Q+ red flags
- Recent injury without medical clearance
- Severe chronic conditions (uncontrolled diabetes, severe osteoporosis, cardiovascular disease)

**Email message:**
> Thank you for completing your assessment. Based on your health screening, we require **medical clearance from your physician** before enrollment.
> 
> **Why medical clearance?**
> - You indicated [heart condition / recent injury / chronic condition]
> - For your safety, we need confirmation from your doctor that exercise is appropriate
> 
> **Next steps**:
> 1. Download our medical clearance form: [link]
> 2. Bring the form to your next doctor's appointment
> 3. Upload the completed form: [link to upload]
> 4. Once we receive clearance, we'll confirm your enrollment
> 
> **Questions?** Reply to this email or call [phone number].

**Action:** Send medical clearance form, pause enrollment until clearance received.

## Example Scenarios

### Scenario 1: 65-year-old with chronic back pain
**Profile:**
- Age: 65
- Goals: reduce_chronic_pain, improve_mobility, maintain_independence
- Chronic pain: back, severity 7/10, duration 5+ years
- Fall history: none
- PAR-Q+: blood pressure medication (yes), others no

**Scoring:**
- `clinical_score` = 3 (pain) + 3 (mobility) + 2 (independence) + 2 (age 66+ modifier) + 7 (pain severity) = 17
- `performance_score` = 0
- `medical_clearance_required` = false (blood pressure medication alone doesn't require clearance unless uncontrolled)

**Outcome:** **Track A** (clinical_score >> performance_score)

### Scenario 2: 32-year-old competitive CrossFit athlete
**Profile:**
- Age: 32
- Goals: increase_strength, improve_power, competition_prep
- Training history: 5+ years, 6x/week
- Strength baselines: Squat 140kg, Deadlift 180kg, Bench 100kg
- No pain, no injuries, no PAR-Q+ red flags

**Scoring:**
- `clinical_score` = 0
- `performance_score` = 3 (strength) + 3 (power) + 4 (competition) + 1 (age 18-45) + 3 (training years 5-10) + 2 (frequency 5-6x) + 2 (baselines provided) = 18

**Outcome:** **Track B** (performance_score >> clinical_score)

### Scenario 3: 55-year-old recovering from knee injury, wants to return to running
**Profile:**
- Age: 55
- Goals: injury_recovery_return, improve_endurance, increase_strength
- Injury history: knee meniscus surgery 4 months ago, status "healing", medical clearance received
- Current limitations: limited knee ROM, pain during deep squats
- Training history: 10+ years running, currently 2x/week (reduced due to injury)
- PAR-Q+: bone/joint problem (yes, post-surgery)

**Scoring:**
- `clinical_score` = 2 (PAR-Q+ red flag modifier) = 2
- `performance_score` = 2 (endurance) + 3 (strength) + 4 (training years 10+) = 9
- `hybrid_candidate` = true (injury recovery flag + current limitations)

**Outcome:** **Hybrid** (injury recovery + performance goals, clinical foundation needed before full performance)

### Scenario 4: 70-year-old with multiple PAR-Q+ red flags
**Profile:**
- Age: 70
- Goals: maintain_independence, improve_balance
- PAR-Q+: heart condition (yes), blood pressure medication (yes), bone/joint problem (yes - osteoporosis)
- Chronic conditions: osteoporosis, arthritis
- No recent medical clearance for exercise

**Scoring:**
- `medical_clearance_required` = true (2+ PAR-Q+ red flags)

**Outcome:** **Medical Clearance Required** (manual review, send clearance form, pause enrollment until cleared)

## Implementation Notes

### Frontend (Assessment Form)
- Collect all required data per schema (Track A or Track B)
- On submission, send JSON to backend API endpoint `/api/assessment/submit`

### Backend (Triage Engine)
- Receive assessment JSON
- Run triage algorithm (calculate scores, apply modifiers, determine recommendation)
- Save assessment to database with `track_recommended` field ("A", "B", "hybrid", "manual_review")
- Trigger appropriate email (Track A/B recommendation, Hybrid manual review notice, or Medical clearance request)

### Admin Dashboard
- View all assessments with triage recommendation
- Filter by track (A, B, hybrid, manual_review)
- Manually override triage recommendation if needed (e.g., coach reviews and disagrees with algorithm)
- Approve enrollments after medical clearance received

### CAMIX ASRM Integration
- Once client enrolls, create ASRM profile with assessment data
- Track: "A", "B", or "hybrid"
- Clinical data: pain locations, severity, mobility scores, balance risk
- Performance data: training history, strength baselines, sport demands
- ASRM adapts weekly progressions based on track and individual profile

## Testing Plan

### Unit Tests (Triage Algorithm)
1. Test pure Track A scenario (high clinical score, low performance score) → expects "A"
2. Test pure Track B scenario (low clinical score, high performance score) → expects "B"
3. Test hybrid scenario (mixed goals, close scores) → expects "hybrid"
4. Test medical clearance scenario (multiple PAR-Q+ red flags) → expects "manual_review"
5. Test edge cases (age 60 with close scores → expects "A")

### Integration Tests (End-to-End)
1. Submit Track A assessment → verify triage recommendation → verify email sent with Track A details
2. Submit Track B assessment → verify triage recommendation → verify email sent with Track B details
3. Submit hybrid assessment → verify "hybrid" recommendation → verify admin notification sent
4. Submit medical clearance required assessment → verify "manual_review" → verify clearance form email sent

---

**Document status**: v1.0 - Triage logic ready for implementation  
**Last updated**: 2026-06-03  
**Owner**: CAMI Netherlands team
