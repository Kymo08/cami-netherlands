# CAMI Netherlands
**Clinical Exercise & Athletic Performance Programs - Utrecht**

## Project Overview
Trilingual (IT/EN/NL) landing page and funnel for CAMI clinical exercise and performance training programs in Utrecht, Netherlands. Targets expat community (50+/60+/70+) with chronic pain/mobility issues (Track A) and athletes/active individuals seeking performance improvement (Track B).

## Architecture
- **Domain**: `nl.centrocami.it` (subdomain funnel, main brand `www.centrocami.it`)
- **Positioning**: Dual track (Clinical + Performance), not just elderly/pathology
- **Payment**: Stripe Checkout (premium UX, EU support)
- **Personalization**: CAMIX-powered daily email recommendations (ASRM + POSOLOGIE + SENTINEL)
- **Compliance**: GDPR Art.9 health data consent, medical disclaimers, PAR-Q+ red flags
- **Tech Stack**: Single-file HTML landing (mobile-first), multi-step assessment form, Stripe webhook automation, Python/CAMIX backend integration

## Project Structure
```
cami-netherlands/
├── docs/
│   ├── positioning/          # Track A (clinical) + Track B (performance) positioning
│   ├── compliance/           # GDPR, medical disclaimers, consent flows
│   ├── intake-schemas/       # Assessment schemas for clinical/performance/triage
│   ├── integrations/         # CAMIX/Stripe integration specs
│   └── funnel/               # Conversion funnel architecture
├── web/
│   ├── landing/              # Trilingual landing page (IT/EN/NL)
│   ├── assessment/           # Multi-step intake forms
│   └── booking/              # Calendar integration
├── data/
│   └── schemas/              # JSON schemas for intake/triage/routing
├── integrations/
│   ├── stripe/               # Payment flow + webhook handlers
│   ├── camix/                # ASRM/POSOLOGIE/SENTINEL routing
│   └── email/                # SMTP delivery setup
├── automation/
│   ├── email/                # Daily personalization templates Track A/B
│   └── scheduler/            # NL timezone scheduler
└── analytics/                # UTM tracking, conversion KPIs, dashboard

```

## MVP Timeline (7 days)
1. **Day 1**: Repo structure + positioning docs + competitor intel ✅
2. **Day 2**: Landing page trilingual (IT/EN/NL) + mobile-first design
3. **Day 3**: Assessment multi-step form + triage routing + safety gates
4. **Day 4**: Stripe integration Phase 1 (Payment Links) + webhook setup
5. **Day 5**: CAMIX integration (ASRM mapping + POSOLOGIE routing + SENTINEL gates)
6. **Day 6**: Email daily personalization (Track A/B templates + scheduler)
7. **Day 7**: End-to-end test + analytics + go-live ads ready

## Key Decisions
- **Separate repo**: Clean isolation from `gemini_project/`, future merge via subtree/submodule
- **Dual track positioning**: Clinical (Track A) + Performance (Track B) fills Utrecht market gap
- **Subdomain strategy**: `nl.centrocami.it` for ads tracking, links back to `www.centrocami.it` for trust
- **Stripe over Mollie**: Premium UX, better international support, easier integration
- **Daily email cadence**: CAMIX-generated content, micro-cycle weekly, NL timezone scheduler
- **Consent-first UX**: GDPR Art.9 health data explicit consent separate from marketing opt-in

## Target Market
- **Track A (Clinical)**: Utrecht expats 50+/60+/70+ (Terwijde, Leidsche Rijn), sedentary, chronic pain, mobility issues, seeking autonomy/prevention
- **Track B (Performance)**: Athletes, amateur/competitive, strength training, maximal training, power/speed, outdoor/indoor preparation

## Program Structure
**3-Day Monthly Event** (max 10 participants):
- **Day 1**: Assessment & Screening (posture, mobility, balance, breathing, functional tests)
- **Day 2**: Back & Legs (spine, hips, knees, strengthening, fall prevention)
- **Day 3**: Neck, Shoulders & Breathing (cervical, shoulders, scapula, diaphragm, endurance)

**Daily Email Personalization**:
- **Track A**: Mobility, posture, breathing, prevention, micro-routines (CAMIX-generated)
- **Track B**: Strength, maximal lifts, power, speed, recovery protocols (CAMIX-generated)

## Compliance
- GDPR Art.9 explicit consent for health data processing
- Medical disclaimer: "wellness not diagnosis, consult physician"
- PAR-Q+ red flags screening
- Emergency contact procedures
- Data minimization + progressive profiling
- Double opt-in email (recommended)

## Analytics & KPIs
- **Funnel metrics**: view → start_assessment → complete_assessment → start_checkout → paid
- **Email metrics**: open rate, click rate, adherence (7/30 days), retention
- **Paid acquisition**: CPL, ROAS, conversion rate by source (Meta/Google)
- **UTM tracking**: Complete campaign/source/medium/content tracking

## Integration Points
- **CAMIX ASRM**: Client profile → evolutionary memory → weekly progression
- **CAMIX POSOLOGIE**: Daily content generation Track A/B (Python generator)
- **CAMIX SENTINEL**: Safety gates for red flags, unsuitable recommendations filter
- **Stripe**: Checkout Session API + `checkout.session.completed` webhook
- **Email**: `@centrocami.it` domain (temporary SMTP, migrate later)

## Contact
Main brand: [www.centrocami.it](https://www.centrocami.it)  
Project lead: CAMIX development team
