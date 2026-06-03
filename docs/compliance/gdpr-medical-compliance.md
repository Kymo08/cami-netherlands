# Compliance Framework: GDPR & Medical Risk Management
**CAMI Netherlands - Legal, Privacy, and Safety Protocols**

## Executive Summary
CAMI Netherlands processes **health data** (GDPR Art. 9 special category) and delivers **clinical exercise/performance training** (liability risk). Compliance requires:
1. **GDPR Art. 9 explicit consent** for health data processing (separate from marketing)
2. **Medical disclaimers** to clarify scope (wellness, not diagnosis/treatment)
3. **Safety screening** (PAR-Q+, red flags, SENTINEL automation)
4. **Transparent data practices** (minimization, purpose limitation, retention, subject rights)
5. **Dutch consumer protection** (UCPD anti-dark-patterns, transparent pricing, clear terms)

**Approach**: Consent-first, progressive profiling, transparent claims, dignity-preserving language, safety-first screening.

---

## 1. GDPR Compliance (General Data Protection Regulation)

### 1.1 Legal Basis for Processing
**Personal data** (name, email, age, contact): **Legitimate interest** OR **Contract** (provide service)  
**Health data** (pain level, mobility, medical history, injury): **Explicit consent** (GDPR Art. 9(2)(a))

**Why explicit consent for health data**:
- Health information is "special category" data under GDPR Art. 9
- Requires higher protection than general personal data
- Must be freely given, specific, informed, and unambiguous
- User must opt-in with affirmative action (checkbox, signature)
- Separate from marketing consent (not bundled)

### 1.2 Data We Collect

#### Track A (Clinical Exercise)
**Required for service delivery**:
- Profile: Name, age, gender, email, phone
- Health data: Chronic pain (location, severity, duration), mobility limitations, balance issues, medical history (conditions, medications, surgeries), injury history
- Goals: Why they're seeking clinical exercise, what they want to achieve
- PAR-Q+ screening: Cardiovascular, respiratory, metabolic conditions; symptoms requiring medical clearance

**Optional (progressive profiling)**:
- Emergency contact (name, phone, relationship)
- GP contact (for medical clearance if needed)
- Insurance information (if they want reimbursement support)
- Lifestyle factors (activity level, sleep, stress, nutrition)

#### Track B (Performance)
**Required for service delivery**:
- Profile: Name, age, gender, email, phone
- Performance data: Sport/activity, training history (years, frequency), current strength baselines (1RM estimates or recent PRs), injury history
- Goals: Performance targets (strength gains, competition prep, sport-specific)
- PAR-Q+ screening: Same as Track A

**Optional (progressive profiling)**:
- Sport-specific metrics (race times, competition results, training volume)
- Recovery data (sleep quality, readiness scores, fatigue indicators)
- Equipment/facility access (for tailored recommendations)

### 1.3 Purpose Limitation
We collect and process data **only for these purposes**:
1. **Service delivery**: Personalize clinical exercise or performance program, generate daily email recommendations (CAMIX)
2. **Safety screening**: Identify red flags, contraindications, injury risks (SENTINEL)
3. **Progress tracking**: Monitor outcomes, adapt programming (ASRM)
4. **Communication**: Send program updates, daily emails, scheduling
5. **Marketing** (separate consent): Send promotional emails, program announcements

**We do NOT**:
- Sell or share health data with third parties (except required service providers: email service, payment processor)
- Use health data for marketing or profiling beyond service personalization
- Combine health data with external data sources (no data broker partnerships)

### 1.4 Data Retention
- **Active clients**: Data retained for duration of service + 1 year (EU limitation period for liability claims)
- **Inactive clients**: After 1 year of no enrollment, we send notice: "Would you like to continue or delete your data?"
- **Deleted data**: Securely erased within 30 days of deletion request or inactivity confirmation
- **Anonymized data**: Aggregated statistics (no personal identifiers) retained indefinitely for research and service improvement

### 1.5 User Rights (GDPR Chapter 3)
**Right to access**: Request copy of all data we hold (delivered within 30 days)  
**Right to rectification**: Correct inaccurate data at any time  
**Right to erasure**: Request deletion of all data (within 30 days)  
**Right to restrict processing**: Limit how we use data (e.g., only for legal claims)  
**Right to data portability**: Receive data in machine-readable format (JSON)  
**Right to object**: Object to processing (we must stop unless compelling legitimate grounds)  
**Right to withdraw consent**: Withdraw health data consent at any time (service may no longer be possible)

**How to exercise rights**: Email privacy@centrocami.it or contact form on website

### 1.6 Data Security
- **Encryption**: Data encrypted in transit (TLS) and at rest (AES-256)
- **Access control**: Role-based access, only authorized personnel (coaches, admin) can view health data
- **Audit logs**: All data access logged and monitored
- **Third-party processors**: GDPR-compliant processors only (Stripe, email service provider, hosting)
- **Breach notification**: Within 72 hours to supervisory authority and affected individuals (if high risk)

### 1.7 Data Controller and DPO
**Data Controller**: CAMI Netherlands (legal entity TBD: sole proprietorship, BV, or Italian entity)  
**Contact**: privacy@centrocami.it  
**Data Protection Officer (DPO)**: Not required (fewer than 250 employees, not large-scale special category processing), but designate privacy contact  
**Supervisory Authority**: Autoriteit Persoonsgegevens (Netherlands) - [autoriteitpersoonsgegevens.nl](https://autoriteitpersoonsgegevens.nl)

---

## 2. Consent Flows (UX Implementation)

### 2.1 Health Data Consent (GDPR Art. 9)
**When**: During intake assessment (after profile, before health questions)

**Consent text example** (clear, specific, plain language):
> **Consent to Process Health Information**  
> 
> To personalize your clinical exercise program, we need to collect health information such as:
> - Pain level and location
> - Mobility and balance limitations
> - Medical history (conditions, medications, injuries)
> - Physical assessment results
> 
> This information will be used **only** to:
> - Design your personalized exercise program
> - Identify safety considerations (contraindications, red flags)
> - Generate daily recommendations tailored to your needs
> - Track your progress and adapt the program
> 
> Your health data will be:
> - Stored securely (encrypted)
> - Accessed only by authorized CAMI coaches and admin
> - Not shared with third parties (except service providers: email, payment)
> - Retained for 1 year after your last enrollment, then deleted
> 
> You have the right to:
> - Access, correct, or delete your data at any time
> - Withdraw this consent (though we may not be able to provide the service)
> - File a complaint with the Dutch Data Protection Authority
> 
> [ ] **I consent to CAMI Netherlands processing my health information for the purposes described above.**

**Implementation**:
- Separate checkbox (not pre-checked)
- User must scroll through full text before checkbox is enabled (proof of informed consent)
- If user declines: "We cannot provide personalized clinical exercise without this information. Please consult a physician or general fitness program instead."
- Record consent: timestamp, IP address, consent version (for audit trail)

### 2.2 Marketing Consent (Separate)
**When**: After health data consent, before final submission

**Consent text example**:
> **Marketing Communications (Optional)**  
> 
> We'd love to keep you updated on:
> - New program offerings and events
> - Health and performance tips from our team
> - Special promotions and discounts
> 
> [ ] **I consent to receive marketing emails from CAMI Netherlands.**
> 
> You can unsubscribe at any time by clicking the link in any email.

**Implementation**:
- Separate checkbox (not bundled with health data consent)
- Optional (user can complete assessment without marketing consent)
- Unsubscribe link in every marketing email (legally required in NL/EU)

### 2.3 Progressive Profiling
**Principle**: Collect minimum data upfront, request additional data after demonstrating value.

**Upfront (required)**:
- Name, email, age
- Health data consent
- Core health/performance questions for assessment

**After value demonstration** (post-assessment, pre-payment):
- Emergency contact (framed as safety: "In case of medical emergency during in-person sessions")
- GP contact (only if PAR-Q+ indicates medical clearance needed)
- Optional lifestyle questions (activity level, sleep, nutrition) for enhanced personalization

**After first program** (if re-enrolling):
- Progress feedback (pain changes, strength gains, satisfaction)
- Refined goals for next cycle

**Benefit**: Lower friction upfront, users more willing to share data after experiencing value.

---

## 3. Medical Disclaimers

### 3.1 General Disclaimer (Website Footer)
> **Medical Disclaimer**  
> CAMI Netherlands provides wellness and exercise coaching services. We do not diagnose, treat, or cure any medical conditions. Our programs are not a substitute for medical advice, diagnosis, or treatment. Always consult your physician before starting any exercise program, especially if you have a medical condition, injury, or take medications. If you experience severe pain, dizziness, chest pain, or unusual symptoms during exercise, stop immediately and seek medical attention.

### 3.2 Track A Disclaimer (Clinical Exercise)
> **Clinical Exercise Disclaimer**  
> Our clinical exercise program is designed to improve movement quality, reduce chronic pain, and enhance functional autonomy. However, individual results vary. We cannot guarantee specific outcomes. This program is not physiotherapy, rehabilitation, or medical treatment. If you have a diagnosed medical condition or acute injury, consult your physician before enrollment. We may require medical clearance for certain conditions (identified in PAR-Q+ screening).

### 3.3 Track B Disclaimer (Performance Training)
> **Performance Training Disclaimer**  
> Our performance program involves high-intensity strength, power, and conditioning training. There is inherent risk of injury with any athletic training. You assume full responsibility for your participation. We screen for injury history and movement limitations, but cannot eliminate all risk. Consult your physician before enrollment if you have any medical conditions or recent injuries. Stop training immediately if you experience severe pain or unusual symptoms, and seek medical attention if needed.

### 3.4 Emergency Situations (In-Person Programs)
> **Emergency Protocol**  
> In the unlikely event of a medical emergency during our in-person programs:
> 1. We will stop activity immediately
> 2. Assess the situation (first aid trained staff on-site)
> 3. Call 112 (emergency services) if needed
> 4. Contact your emergency contact
> 5. Provide first aid until emergency services arrive
> 
> Please ensure your emergency contact information is up-to-date. If you have specific medical conditions (asthma, diabetes, allergies), inform us before the program and bring necessary medications (inhaler, glucose, EpiPen).

**Implementation**: Display during intake (after PAR-Q+), require acknowledgment checkbox before payment.

---

## 4. Safety Screening (PAR-Q+ and SENTINEL)

### 4.1 PAR-Q+ Screening
**Purpose**: Identify individuals who require medical clearance before exercise participation.

**PAR-Q+ Standard Questions** (7 core):
1. Has your doctor ever said you have a heart condition and recommended only medically supervised activity?
2. Do you have chest pain when you do physical activity?
3. In the past month, have you had chest pain when you were not doing physical activity?
4. Do you lose your balance because of dizziness, or do you ever lose consciousness?
5. Do you have a bone or joint problem that could be made worse by a change in your physical activity?
6. Is your doctor currently prescribing medication for your blood pressure or heart condition?
7. Do you know of any other reason why you should not do physical activity?

**If YES to any**: Follow-up questions to assess severity → Determine if medical clearance required.

**Track A Additional Questions** (Clinical Exercise):
- Do you experience chronic pain? (location, severity 0-10, duration)
- Have you fallen in the past year? (how many times, circumstances)
- Do you have difficulty with balance or walking?
- Have you been diagnosed with osteoporosis, arthritis, or chronic musculoskeletal condition?
- Do you take medications that affect balance or coordination? (e.g., sedatives, blood pressure meds)

**Track B Additional Questions** (Performance):
- Have you had any injuries in the past 6 months? (location, severity, treatment, current status)
- Do you have any current pain or movement limitations? (location, severity, impact on training)
- Have you had surgery in the past year? (type, recovery status, medical clearance received?)
- Do you have a history of overtraining or burnout? (symptoms, management strategies)

**Medical Clearance Required if**:
- YES to PAR-Q+ core questions without satisfactory follow-up
- Recent surgery or major injury (within 6 months) without MD clearance
- Uncontrolled chronic condition (diabetes, hypertension, asthma)
- Severe osteoporosis with fracture history (Track A)
- Cardiovascular condition without exercise clearance (Track B)

**Clearance Process**:
1. Email client: "Based on your screening, we require medical clearance from your physician before enrollment."
2. Provide physician clearance form (template: "Patient [name] has been cleared for [clinical exercise / strength training]")
3. Client obtains clearance, uploads form
4. We review and approve enrollment (or decline if concerns remain)

### 4.2 SENTINEL Safety Gates (Automated)
**Purpose**: Filter daily email recommendations to exclude unsuitable exercises based on individual profile.

**SENTINEL Rules**:
- **Chronic pain filters**: If lumbar pain > 5/10, exclude exercises with heavy spinal loading (deadlift, squat, overhead press)
- **Mobility restrictions**: If limited ankle dorsiflexion, modify squat depth recommendations or suggest alternatives
- **Balance risk**: If fall history, exclude single-leg exercises without support cues
- **Injury history**: If recent knee surgery, avoid plyometrics or high-impact movements until cleared
- **Cardiovascular risk**: If hypertension, limit high-intensity intervals, include RPE monitoring cues
- **Age-related**: If 70+, default to lower impact, emphasize safety and balance, include rest day reminders

**Implementation**: CAMIX SENTINEL module checks profile data before generating daily email → Filters exercise database → Only suitable exercises recommended.

---

## 5. Dutch Consumer Protection (UCPD - Unfair Commercial Practices Directive)

### 5.1 Transparent Pricing
**Requirement**: Clear, upfront pricing without hidden fees.

**Implementation**:
- Display price on landing page: "€200-300 per 3-day program (includes 30 days daily coaching)"
- Specify what's included (assessment, sessions, emails, support chat)
- Specify what's NOT included (travel, accommodation, supplements, equipment)
- No hidden fees or surprise charges at checkout

### 5.2 Anti-Dark-Patterns
**Prohibited practices** (considered unfair under Dutch UCPD):
- **False urgency**: "Only 2 spots left!" (unless true and verifiable)
- **Misleading claims**: "Guaranteed pain-free in 7 days" (individual results vary)
- **Hidden opt-ins**: Pre-checked marketing consent boxes (must be opt-in)
- **Confusing unsubscribe**: Hard-to-find or multi-step unsubscribe (must be 1-click)
- **Fake reviews**: Fabricated testimonials or paid reviews without disclosure
- **Bait-and-switch**: Advertise low price, then upsell required add-ons

**Our approach**:
- Honest urgency: "10 participants max per event" (real constraint)
- Realistic claims: "Most clients report reduced pain after 30 days" (individual results vary, based on client feedback)
- Opt-in consent: Unchecked boxes, clear labels, separate health vs. marketing
- Easy unsubscribe: 1-click link in every email footer
- Authentic reviews: Real client testimonials with permission, no fabrication
- Transparent value: Clear inclusions, no required upsells (optional add-ons disclosed upfront)

### 5.3 Cancellation and Refund Policy
**Dutch distance selling** (online purchases) require **14-day cooling-off period** for consumers.

**Exception**: Services that begin during cooling-off period (with consumer consent) are NOT refundable.

**Our policy**:
- **Before 3-day program**: 14-day cooling-off period, full refund if requested
- **After 3-day program starts**: No refund (service has begun, consumer agreed to start)
- **Cancellation notice**: Must cancel at least 7 days before program start for full refund (after 14-day cooling-off)
- **Reschedule**: If client cannot attend, can reschedule to next available program (within 6 months)

**Disclosure**: Display refund policy clearly before payment, checkbox acknowledgment at checkout.

---

## 6. Insurance and Liability

### 6.1 Professional Liability Insurance
**Requirement**: Coverage for claims arising from injury during programs.

**Coverage needed**:
- Professional liability (exercise instruction, personalized programming)
- General liability (injury during in-person sessions)
- Coverage amount: €1-2 million (standard in NL for health/fitness services)
- Territory: Netherlands (in-person) + EU (online coaching emails)

**Provider**: Check Dutch professional liability insurers (Centraal Beheer, Allianz, AON) for fitness/health coaching coverage.

### 6.2 Liability Waivers
**Waiver at enrollment** (checkbox acknowledgment before payment):
> **Assumption of Risk and Release of Liability**  
> 
> I understand that participation in clinical exercise and performance training involves inherent risks, including but not limited to: muscle soreness, strains, sprains, falls, and in rare cases, more serious injury.
> 
> I acknowledge that:
> - I have disclosed all relevant medical conditions and injury history
> - I have obtained medical clearance if required
> - I am responsible for following instructions and using proper form
> - I will stop activity immediately if I experience pain or unusual symptoms
> - I will notify CAMI staff of any concerns or changes in my condition
> 
> I assume full responsibility for my participation and release CAMI Netherlands, its instructors, and staff from liability for any injury or loss arising from my participation, except in cases of gross negligence or intentional misconduct.
> 
> [ ] **I acknowledge and agree to the above.**

**Legal note**: Waivers do NOT eliminate liability for gross negligence, but demonstrate informed consent and assumption of risk (reduces claims). Always maintain proper safety protocols and professional liability insurance.

---

## 7. Email Compliance (Marketing & Transactional)

### 7.1 CAN-SPAM and GDPR Email Rules
**Transactional emails** (program updates, daily personalized recommendations): Consent implied by service enrollment, no opt-out required.

**Marketing emails** (promotions, new programs): Require explicit opt-in consent, must include:
- Clear "From" name and email (no deceptive headers)
- Accurate subject line (no misleading)
- Unsubscribe link (1-click, processed within 10 days)
- Physical address (business location)

**Implementation**:
- Separate marketing list from service list (don't email marketing to non-consented users)
- Honor unsubscribe immediately (automated)
- Double opt-in recommended (send confirmation email, user clicks to confirm) to reduce spam complaints

### 7.2 Daily Email Personalization (CAMIX)
**Classification**: Transactional/service emails (not marketing).

**Rationale**: Daily recommendations are core service delivery, expected by client as part of paid program.

**Content rules**:
- Primary purpose: Deliver personalized exercise/health recommendations
- No promotional content (new program sales, third-party ads)
- Minimal branding (logo, brand colors OK, but not promotional messaging)
- CTA: "Log your practice" or "Rate today's session" (service-related, not marketing)

**Unsubscribe**: Not required for transactional emails, BUT best practice to include opt-out with explanation:
> "These daily recommendations are part of your CAMI program. If you wish to stop receiving them, please contact support@centrocami.it. Note: opting out may impact your program experience."

---

## 8. Compliance Checklist (Pre-Launch)

### Legal Documents
- [ ] Privacy Policy (GDPR-compliant, covers health data Art. 9)
- [ ] Terms of Service (scope, liability, refunds, cancellation)
- [ ] Cookie Policy (if website uses cookies beyond essential)
- [ ] Consent forms (health data, marketing, liability waiver)

### Technical Implementation
- [ ] Consent checkboxes (separate, not pre-checked, audit trail)
- [ ] Encryption (TLS in transit, AES-256 at rest)
- [ ] Data access controls (role-based, audit logs)
- [ ] Data subject rights workflow (access, deletion, portability requests)
- [ ] Unsubscribe automation (1-click, processed immediately)

### Safety Protocols
- [ ] PAR-Q+ screening implemented (intake form)
- [ ] Medical clearance workflow (email, form, approval)
- [ ] SENTINEL safety gates (CAMIX integration)
- [ ] Emergency protocols (first aid, 112, emergency contact)
- [ ] Professional liability insurance (certificate obtained)

### Transparency
- [ ] Pricing displayed clearly (landing page, before payment)
- [ ] Disclaimers visible (medical, performance, emergency)
- [ ] Refund policy disclosed (before checkout, acknowledgment checkbox)
- [ ] Marketing consent separate and optional (not bundled)
- [ ] No dark patterns (honest urgency, realistic claims, no hidden fees)

---

## 9. Monitoring and Auditing

### Quarterly Reviews
- Review consent rates (health data, marketing)
- Review data subject rights requests (access, deletion)
- Review safety incidents (injuries, medical clearances required)
- Review email compliance (unsubscribe rates, spam complaints)

### Annual Audits
- Privacy policy and terms review (update if services change)
- Data retention audit (delete inactive client data per policy)
- Security audit (penetration testing, access logs review)
- Insurance renewal (professional liability)

### Incident Response
- **Data breach**: Notify supervisory authority within 72 hours, notify affected individuals if high risk
- **Injury during program**: Document incident, provide first aid, notify insurer if claim expected
- **Compliance complaint**: Respond within 30 days, escalate to legal counsel if needed

---

**Document status**: v1.0 - Compliance framework ready for implementation  
**Last updated**: 2026-06-03  
**Owner**: CAMI Netherlands team  
**Legal review**: Recommended before launch (consult Dutch privacy/health law attorney)
