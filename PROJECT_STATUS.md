# CAMI Netherlands - Project Status
**Last Updated**: 2026-06-03 (Day 2 complete)

## ✅ Completed

### Day 1 - Foundation (2026-06-03 morning)

### 1. Project Structure
- [x] Separate repo created: `/data/data/com.termux/files/home/cami-netherlands/`
- [x] Clean folder hierarchy: `docs/`, `web/`, `data/`, `integrations/`, `automation/`, `analytics/`
- [x] Independent from `gemini_project/` (no path dependencies, future merge possible)

### 2. Strategic Documentation
- [x] **README.md**: Project overview, architecture, MVP timeline, integration points
- [x] **Track A Positioning** (`docs/positioning/track-a-clinical.md`): Clinical Exercise & Healthy Aging program spec (target audience, problem/solution, messaging, pricing, funnel, compliance, metrics)
- [x] **Track B Positioning** (`docs/positioning/track-b-performance.md`): Performance & Athletic Preparation program spec (athletes, strength/power focus, differentiation, hybrid potential)
- [x] **Competitor Intel** (`docs/positioning/competitor-intel-utrecht.md`): Utrecht market analysis (15+ competitors analyzed, 5 market gaps identified, positioning matrix, defensibility strategy)

### 3. Compliance Framework
- [x] **GDPR & Medical Compliance** (`docs/compliance/gdpr-medical-compliance.md`): GDPR Art. 9 health data consent, medical disclaimers, PAR-Q+ screening, Dutch UCPD anti-dark-patterns, refund policy, insurance requirements, email compliance

### 4. Conversion Funnel
- [x] **Funnel Spec** (`docs/funnel/conversion-flow-spec.md`): 10-stage flow (awareness → landing → assessment → payment → onboarding → daily emails → retention), email sequences, Stripe integration (Phase 1 Payment Links, Phase 2 webhooks), analytics KPIs

### 5. Data Schemas
- [x] **Track A Schema** (`data/schemas/intake-track-a.json`): JSON schema for clinical exercise intake (profile, goals, health screening PAR-Q+, chronic pain, fall history, balance, conditions, consent GDPR/liability, metadata)
- [x] **Track B Schema** (`data/schemas/intake-track-b.json`): JSON schema for performance training intake (profile, goals, sport/activity, training history, strength baselines, injury history, limitations, consent, metadata)
- [x] **Triage Logic** (`data/schemas/triage-routing-logic.md`): Automated Track A/B/Hybrid recommendation algorithm (goal scoring, age modifiers, health screening analysis, medical clearance rules, example scenarios, testing plan)

### Day 2 - Landing Page (2026-06-03 afternoon)

#### 6. Landing Page Trilingual
- [x] **Single-file HTML** (`web/landing/index.html`): 500+ lines, complete trilingual (IT/EN/NL) landing page
- [x] **Language switcher**: Persistent (localStorage), smooth transition between IT/EN/NL
- [x] **Mobile-first responsive**: Tailwind CSS, works on all screen sizes (320px - 1920px+)
- [x] **Design system**: Apple/Stripe/Notion aesthetic implemented (deep blue #1E3A8A, white, green accent #10B981)
- [x] **11 sections**: Hero + CTA, Social proof stats, Problem (Track A/B), Solution (Track A/B cards), How It Works (4 steps), Why CAMI (6 benefits), Testimonials (3 stories), Pricing (€250 transparent), FAQ (6 questions accordion), CTA Final, Footer
- [x] **Animations**: Fade-in on scroll (IntersectionObserver), smooth transitions, hover effects
- [x] **SEO ready**: Meta tags, Open Graph, semantic HTML, accessibility labels
- [x] **Performance optimized**: Single-file, Tailwind CDN (MVP), <2s load time target
- [x] **README** (`web/landing/README.md`): Deployment instructions (Vercel/Netlify/GitHub Pages), testing checklist, customization guide, production optimizations

**Key Features**:
- Language switcher with localStorage persistence (IT/EN/NL)
- Track A (Clinical Exercise) and Track B (Athletic Performance) program cards with CTA
- FAQ accordion (expandable questions)
- Transparent pricing €250 with full breakdown
- Mobile-first responsive (tested 320px - 1920px)
- Smooth scroll anchor links
- All CTAs link to `/assessment` (ready for assessment form integration)

---

## 🚧 Next Steps (Day 3-4 - Assessment & Payment)

### Priority 1: Assessment Form (Day 3)
- [ ] Multi-step form (6 steps: Profile → Goals → Screening → Safety Gate → Consent → Summary)
- [ ] Conversational tone, mobile-optimized
- [ ] Track A/B path routing based on goals
- [ ] PAR-Q+ screening (7 core + Track-specific questions)
- [ ] SENTINEL safety gate (automated background check for red flags)
- [ ] GDPR consent checkboxes (health data Art. 9 + marketing + liability)
- [ ] Assessment summary page (track recommendation, next steps email within 24h)

**Files**: 
- `web/assessment/index.html` (multi-step form UI)
- `web/assessment/form-validation.js` (client-side validation)
- Backend API endpoint needed (see Priority 2)

### Priority 2: Assessment Form (Day 3)
- [ ] Multi-step form (6 steps: Profile → Goals → Screening → Safety Gate → Consent → Summary)
- [ ] Conversational tone, mobile-optimized
- [ ] Track A/B path routing based on goals
- [ ] PAR-Q+ screening (7 core + Track-specific questions)
- [ ] SENTINEL safety gate (automated background check for red flags)
- [ ] GDPR consent checkboxes (health data Art. 9 + marketing + liability)
- [ ] Assessment summary page (track recommendation, next steps email within 24h)

**Files**: 
- `web/assessment/form.html` (or React/Vue component if dynamic)
- `web/assessment/submit-handler.js` (API call to backend)

### Priority 2: Backend API (Day 3-4)
- [ ] Endpoint: `POST /api/assessment/submit` (receive assessment JSON, validate against schema)
- [ ] Triage engine (calculate scores, determine Track A/B/hybrid/medical_clearance)
- [ ] Database save (client record with assessment data, track_recommended, status "assessment_complete")
- [ ] Email trigger: "Assessment received" (auto-reply)
- [ ] Admin notification: Slack/email "New assessment: [Name], Track [A/B], Medical clearance [Yes/No]"

**Tech stack decision needed**:
- Option 1: Python Flask/FastAPI + SQLite/PostgreSQL (integrates easily with CAMIX)
- Option 2: Node.js Express + MongoDB (if frontend is JS-heavy)
- Option 3: Serverless (AWS Lambda, Vercel, Cloudflare Workers) + Firebase/Supabase DB

### Priority 3: Stripe Payment (Day 4)
**Phase 1 (MVP, manual):**
- [ ] Stripe account setup (business account, KYC verification)
- [ ] Create products: "CAMI Track A - Utrecht [Date]" (€250), "CAMI Track B - Utrecht [Date]" (€250)
- [ ] Generate Payment Links manually per client (after assessment review)
- [ ] Email template: "Program Recommendation + Payment Link"
- [ ] Success page: `web/thank-you.html` (confirmation, next steps, email check)
- [ ] Admin receives Stripe notification → manually sends onboarding email

**Phase 2 (automation, if time allows):**
- [ ] Stripe Checkout Session API (programmatic link generation)
- [ ] Webhook endpoint: `POST /webhooks/stripe` (handle `checkout.session.completed`)
- [ ] Auto-update client status: `assessment_complete` → `paid`
- [ ] Auto-send onboarding email with calendar invite, WhatsApp group link

---

## 🔮 Future Priorities (Day 5-7 - CAMIX Integration & Launch)

### Day 5: CAMIX Integration
- [ ] ASRM mapping: Client profile → memory initialization (pain/mobility/balance for Track A, strength/training for Track B)
- [ ] POSOLOGIE routing: Daily content generation logic (Track A: mobility/posture/breathing/prevention; Track B: strength/power/recovery/sport-specific)
- [ ] SENTINEL gates: Red flag filters (pain > 7 → exclude heavy loading, injury history → exclude contraindicated exercises, age 70+ → low-impact default)
- [ ] Test content generation: Generate 7 days of sample emails for Track A and Track B

**Files**:
- `integrations/camix/asrm-client-profile.py` (create ASRM profile from assessment data)
- `integrations/camix/posologie-track-a.py` (Track A content generator)
- `integrations/camix/posologie-track-b.py` (Track B content generator)
- `integrations/camix/sentinel-safety-rules.json` (safety gate configuration)

### Day 6: Email Automation
- [ ] Email service setup (SendGrid / Mailchimp / SMTP via Hostinger `@centrocami.it`)
- [ ] Template design (responsive HTML, plain-text fallback, unsubscribe link)
- [ ] Onboarding email (calendar .ics, WhatsApp invite, what to bring, pre-program prep)
- [ ] Daily email scheduler (7:00 AM NL timezone, CET/CEST aware)
- [ ] Daily email template (personalized via CAMIX, CTA "Log Today's Practice")
- [ ] Re-enrollment email (Day 25, special offer returning clients)
- [ ] Post-program survey (Day 31, feedback + testimonial request)

**Files**:
- `automation/email/templates/` (onboarding.html, daily-track-a.html, daily-track-b.html, re-enrollment.html, survey.html)
- `automation/scheduler/daily-email-cron.py` (scheduler logic, timezone-aware)

### Day 7: Testing & Launch
- [ ] End-to-end test: Landing → Assessment (Track A, Track B, Hybrid) → Triage → Email → Payment → Onboarding → Daily Email Day 1
- [ ] Google Analytics 4 setup (UTM tracking, goal conversions: view, start_assessment, complete_assessment, start_checkout, paid)
- [ ] CRM/database (Airtable / Notion / custom): Track clients, funnel stages, program dates, payment status
- [ ] Analytics dashboard (Google Data Studio / Metabase): Conversion rates, email metrics, retention
- [ ] Soft launch: Invite Centro CAMI Italy clients (email existing list), friends/family test
- [ ] Collect feedback: Survey (UX issues, messaging clarity, pricing perception)
- [ ] Iterate: Fix bugs, adjust copy, optimize conversion
- [ ] Paid ads launch: Meta/Google campaigns (€500-1000 budget), UTM tracking, monitor CPL/CPA

---

## 📊 Key Metrics to Track (Post-Launch)

### Acquisition Metrics
- **Landing page views** (by source: Meta, Google, Organic, Referral)
- **Cost per click (CPC)**: Ad spend / Clicks
- **Cost per lead (CPL)**: Ad spend / Assessment starts (target: €15-30)
- **Cost per acquisition (CPA)**: Ad spend / Payments (target: €100-180)

### Conversion Funnel
- **Landing → Start Assessment**: Target 10-15%
- **Start → Complete Assessment**: Target 70-80%
- **Complete → Payment**: Target 30-40%
- **Overall (Landing → Payment)**: Target 2-4%

### Engagement
- **Email open rates**: Onboarding (target 60-70%), Daily (target 40-55%), Re-enrollment (target 45-55%)
- **Email click rates**: Target 15-25% (CTA: log practice, payment link)
- **WhatsApp group activity**: Messages per day, participation rate
- **Daily practice adherence**: Target 50-70% of clients log practice daily

### Retention
- **30-day completion**: Target 80-90% (receive all 30 daily emails without unsubscribe)
- **Re-enrollment rate**: Target 40-60% (pay for next month's program)
- **90-day retention**: Target 40-50% (still active after 3 months)

### Outcomes (Self-Reported)
- **Track A - Pain reduction**: Target 60-70% report reduced pain after 30 days
- **Track A - Mobility improvement**: Target 70-80% report better ROM or balance
- **Track B - Strength gains**: Target 70-80% report 5-10% increase in 1RM
- **Track B - Performance improvement**: Target 70-80% report measurable gains (jump, sprint, endurance)
- **NPS (Net Promoter Score)**: Target 50+ (% promoters 9-10 minus % detractors 0-6)

---

## 🧩 Integration Points (CAMIX Sovereign)

### ASRM (Adaptive Semantic Reservoir Memory)
**Path**: `/data/data/com.termux/files/home/gemini_project/DEPARTMENTS/BRAIN/asrm/`  
**Purpose**: Store client profiles, track weekly progression, adapt recommendations based on feedback.

**Integration**:
- After enrollment (payment confirmed), create ASRM profile:
  - `client_id`, `track` (A/B/hybrid)
  - Track A: `pain_locations`, `pain_severity`, `mobility_score`, `balance_risk`, `fall_history`
  - Track B: `training_years`, `frequency`, `strength_baselines`, `injury_history`, `sport_demands`
- Daily email generation: Query ASRM for current state → POSOLOGIE generates content → ASRM updates based on feedback (practice logged, pain rating)
- Weekly adaptation: ASRM analyzes 7-day adherence + feedback → adjusts next week's intensity/volume/focus

### POSOLOGIE (Daily Content Generator)
**Path**: `/data/data/com.termux/files/home/gemini_project/DEPARTMENTS/POSOLOGIE/`  
**Purpose**: Generate personalized daily recommendations (exercises, cues, tips).

**Integration**:
- Input: ASRM profile (client state, track, day in program 1-30)
- Output: Daily email content (exercises, reps/sets/time, why it helps, CTA)
- Track A templates: Mobility drills, posture resets, breathing exercises, prevention tips, micro-routines
- Track B templates: Strength cues, power drills, recovery protocols, sport-specific skills

### SENTINEL (Safety Gates)
**Path**: `/data/data/com.termux/files/home/gemini_project/DEPARTMENTS/SENTINEL/`  
**Purpose**: Filter recommendations based on safety rules (red flags, contraindications).

**Integration**:
- Before sending daily email: SENTINEL checks ASRM profile
  - If `pain_severity > 7` in lower back → exclude deadlift, heavy squat, overhead press
  - If `injury_history` includes shoulder → exclude overhead movements until healed
  - If `age > 70` and `balance_risk = high` → exclude single-leg exercises without support cues
  - If `fall_history = true` → emphasize safety, include balance cues, default to supported exercises
- Output: Filtered exercise database (safe recommendations only)

### Open Design (Landing Page Generation)
**Path**: `/data/data/com.termux/files/home/gemini_project/DEPARTMENTS/FACTORY/open_design_bridge.py`  
**Purpose**: Generate premium UI components and landing page HTML.

**Integration**:
- Use Open Design skills: `web-prototype`, `saas-landing`
- Input: Content (sections, copy), design system (CAMI blue/white/green, Apple/Stripe aesthetic)
- Output: Single-file HTML with inline CSS, SVG animations, responsive mobile-first

---

## 🤝 Team & Responsibilities (If Scaling)

### Roles Needed (Post-MVP)
1. **Product/Strategy** (You): Define positioning, pricing, features, roadmap
2. **Marketing/Growth**: Paid ads (Meta/Google), SEO, content creation, A/B testing, conversion optimization
3. **Coach/Delivery**: Lead in-person 3-day programs, answer client questions (WhatsApp/email), review assessments, approve medical clearances
4. **Tech/Automation**: Maintain backend API, CAMIX integration, email automation, database, analytics dashboard
5. **Operations**: Scheduling, calendar management, payment tracking, refunds, customer support

**MVP (solo or 2-person team)**:
- You: Product + Tech + Coach (wear all hats)
- Outsource: Paid ads to freelancer or agency (after MVP validation)

---

## 💡 Risks & Mitigations

### Risk 1: Low conversion (landing → assessment < 5%)
**Mitigation**:
- A/B test landing page (hero headline, CTA copy, testimonials, pricing display)
- Offer lead magnet (free guide: "5 Exercises to Reduce Chronic Pain" for email capture)
- Retargeting ads (Meta Pixel, Google Ads remarketing) for visitors who didn't complete assessment

### Risk 2: Medical clearance bottleneck (clients can't get MD clearance quickly)
**Mitigation**:
- Partner with local GPs or telemedicine service for fast clearance
- Offer "light version" program for clients without clearance (low-intensity, no contraindications)
- Clearly communicate clearance requirement upfront (avoid surprise after payment)

### Risk 3: Email fatigue (high unsubscribe rate, low open rate)
**Mitigation**:
- Personalize content (CAMIX ensures relevance, not generic advice)
- Vary send times (test 7 AM vs. 9 AM vs. 6 PM)
- Vary content types (exercise demos, quick tips, success stories, Q&A)
- Allow frequency preference (daily vs. 3x/week for those who prefer less)

### Risk 4: Low retention (clients don't re-enroll after first month)
**Mitigation**:
- Demonstrate value early (immediate pain reduction, strength gains, community support)
- Mid-program check-in (Day 15: "How's it going? Any questions?")
- Celebrate progress (Day 20: "You've completed 20 days! Here's what you've achieved...")
- Returning client discount (€25 off next program)
- Long-term packages (3-month commitment, discounted)

### Risk 5: Operational overwhelm (too many clients, can't scale in-person programs)
**Mitigation**:
- Cap enrollment (max 10 per cohort, 2-3 cohorts per month = 20-30 clients max)
- Hire assistant coach for in-person programs (after 3 cohorts, revenue covers cost)
- Hybrid model (in-person Day 1 assessment, Days 2-3 online group Zoom sessions if needed)
- Raise prices (€300-400) to limit demand and increase revenue per client

---

## 📝 Notes & Decisions Log

### 2026-06-03 Morning (Day 1)
- **Decision**: Separate repo `cami-netherlands/` (not mixed with `gemini_project/`) for clean organization, future merge possible via subtree/submodule
- **Decision**: Subdomain `nl.centrocami.it` for ads funnel (not main site `www.centrocami.it`) for conversion tracking and separation of brand vs. funnel
- **Decision**: Stripe Checkout over Mollie/PayPal for premium UX, EU support, reliability
- **Decision**: Daily email cadence (not weekly or 3x/week) to maximize engagement and adherence, micro-cycle weekly progression
- **Decision**: Dual track positioning (Clinical Track A + Performance Track B) to avoid "only elderly" perception and capture broader Utrecht market
- **Completed**: Day 1 foundation (structure, positioning, compliance, funnel, schemas, triage logic - 10 strategic docs, 8500+ lines)

### 2026-06-03 Afternoon (Day 2)
- **Decision**: Tailwind CSS CDN for MVP speed (production: inline critical CSS for performance)
- **Decision**: Language switcher with localStorage persistence (better UX than URL params for returning visitors)
- **Decision**: FAQ accordion (expandable, not all-visible) to reduce page length, improve mobile UX
- **Decision**: Single-file HTML (not multi-page) for MVP simplicity, easy deployment (Vercel/Netlify drag-drop)
- **Completed**: Landing page trilingual complete (500+ lines HTML, 11 sections, mobile-first responsive, SEO ready, animations, README deployment guide)

---

**Status**: Day 2 complete ✅  
**Next**: Day 3 - Assessment form multi-step (6 steps, Track A/B routing, PAR-Q+, consent, triage backend)  
**Owner**: CAMI Netherlands team
