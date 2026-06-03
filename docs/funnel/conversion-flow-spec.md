# Conversion Funnel Specification
**CAMI Netherlands - Landing to Onboarding Flow**

## Funnel Overview
**Goal**: Convert Utrecht expats (50+ clinical, 25-55 performance athletes) from awareness to paid enrollment with high-quality leads.

**Strategy**: Assessment-first (build trust + qualify leads) → Safety screening (filter red flags) → Payment (Stripe Checkout) → Onboarding (calendar + community).

**Success metrics**:
- Landing → Start Assessment: 10-15%
- Complete Assessment: 70-80% of starts
- Assessment → Payment: 30-40%
- Overall conversion (landing → payment): 2-4%

---

## Stage 1: Awareness (Paid Ads)

### Traffic Sources
**Meta Ads (Facebook/Instagram)**:
- **Track A targeting**: Utrecht region, age 50-70, interests (health, wellness, physiotherapy, chronic pain), languages IT/EN
- **Track B targeting**: Utrecht region, age 25-55, interests (strength training, CrossFit, running, cycling, sports performance), languages IT/EN
- **Creative**: Carousel ads (before/after testimonials), video (coach intro + program overview), static (value proposition + CTA)
- **Budget**: €500-1000/month test phase, scale based on CPL/CPA

**Google Ads (Search)**:
- **Track A keywords**: "chronic pain Utrecht", "movimento senza dolore", "clinical exercise", "fysiotherapie alternatief", "expat health Utrecht"
- **Track B keywords**: "strength training Utrecht", "allenamento forza", "athletic performance", "personal trainer Utrecht", "CrossFit alternatief"
- **Ad copy**: Problem-aware (pain point) → Solution (3-day program + daily coaching) → CTA (Apply for Assessment)
- **Budget**: €300-600/month test phase

**Organic (SEO/Content)**:
- Blog posts (IT/EN/NL): "How to manage chronic back pain without pills", "5 strength training mistakes killing your progress"
- Google My Business (if physical location)
- Social media organic (Instagram reels, client stories, coach tips)

### Landing Page URL Structure
**Track A**: `nl.centrocami.it/?track=clinical&utm_source=meta&utm_medium=cpc&utm_campaign=trackA-utrecht-50plus`  
**Track B**: `nl.centrocami.it/?track=performance&utm_source=google&utm_medium=cpc&utm_campaign=trackB-strength`

**UTM parameters**: Capture source/medium/campaign/content for conversion attribution.

---

## Stage 2: Landing Page (`nl.centrocami.it`)

### Page Structure
**Single-page trilingual** (IT/EN/NL tabs or URL parameter `?lang=it`)

**Sections**:
1. **Hero**: Value proposition + CTA "Apply for Assessment" / "Prenota Valutazione" / "Aanvragen voor Assessment"
2. **Problem**: Pain points (Track A: chronic pain, fear of falling; Track B: plateaus, injury risk)
3. **Solution**: 3-day program overview + daily personalized coaching (CAMIX-powered)
4. **How it works**: 4-step process (Apply → Assess → Pay → Train)
5. **Why CAMI**: Expertise (clinical + performance), trilingual, technology-enhanced, community
6. **Program details**: Day 1-3 breakdown (Track A: mobility/balance/breathing; Track B: strength/power/conditioning)
7. **Testimonials**: Client stories, before/after (pain reduction, strength gains)
8. **Scientific backing**: Evidence-based protocols, clinical expertise credentials
9. **Founder story**: Brief bio (authenticity, trust)
10. **Pricing**: Transparent €200-300, what's included
11. **FAQ**: Common objections (insurance, time commitment, medical clearance, results)
12. **CTA (multiple)**: "Apply Now" buttons throughout page

**Design**:
- Mobile-first responsive (70%+ mobile traffic expected)
- Apple/Stripe/Notion aesthetic (clean, spacious, premium)
- Color palette: Deep blue (trust), white (clarity), green accent (vitality)
- Animations: Subtle CSS (fade-in, scroll-triggered), SVG illustrations inline
- Load time: <2s (single-file HTML, no heavy images, lazy load below fold)

**Trust signals**:
- Credentials (certifications, years experience)
- Social proof (testimonials, client count, satisfaction %)
- Transparent pricing (no hidden fees)
- Medical disclaimers (professional, not fearful)
- Contact info (email, phone, address if physical location)

**CTA variants**:
- Primary: "Apply for Initial Assessment" (Track A), "Apply for Performance Assessment" (Track B)
- Secondary: "Book Free 15-Min Call" (for hesitant leads)
- Urgency (honest): "Next program starts [date], 10 spots available"

### Conversion Optimization
- **A/B testing**: Hero headline, CTA button text/color, testimonial placement
- **Exit intent popup**: "Wait! Get our free guide: '5 Exercises to Reduce Chronic Pain at Home'" (email capture)
- **Chat widget**: Live chat or chatbot for immediate questions (office hours)
- **Video**: 60-90s founder intro (face, voice, authenticity) auto-play muted with captions

---

## Stage 3: Assessment Form (Multi-Step)

### Design Principles
- **Multi-step** (not single long form): Reduce cognitive load, show progress bar
- **Conversational tone**: "Let's get to know you" not "Patient intake"
- **Progressive profiling**: Required data first, optional data after value demonstration
- **Mobile-optimized**: Large buttons, simple inputs, minimal typing

### Step 1: Profile (Required)
**Purpose**: Basic contact info, language preference, triage hint.

**Fields**:
- Name (text input)
- Email (email input, validation)
- Age (number input, range 18-99, for triage Track A/B hint)
- Language preference (dropdown: Italiano, English, Nederlands)
- How did you hear about us? (dropdown: Meta ad, Google ad, Friend referral, Website, Other)

**CTA**: "Next" (progress: 1/6)

### Step 2: Goals (Required)
**Purpose**: Understand motivation, triage Track A vs. B.

**Question**: "What brings you to CAMI?" (select all that apply)
- [ ] Reduce chronic pain (back, neck, knees, joints)
- [ ] Improve mobility and balance
- [ ] Prevent falls and maintain independence
- [ ] Increase strength and build muscle
- [ ] Improve athletic performance (power, speed, endurance)
- [ ] Prepare for competition or sport season
- [ ] Recover from injury and return to training
- [ ] Other (text input)

**Triage logic** (background, not visible to user):
- If pain/mobility/balance selected → Track A likely
- If strength/performance/competition selected → Track B likely
- If both → Hybrid candidate, manual review

**CTA**: "Next" (progress: 2/6)

### Step 3a: Health Screening (Track A Path)
**Shown if**: Triage suggests Track A (pain/mobility/balance goals).

**PAR-Q+ Questions** (7 core, yes/no checkboxes):
1. Has your doctor ever said you have a heart condition?
2. Do you have chest pain when you do physical activity?
3. In the past month, have you had chest pain when not active?
4. Do you lose balance due to dizziness or lose consciousness?
5. Do you have a bone or joint problem that could worsen with activity?
6. Is your doctor prescribing medication for blood pressure or heart?
7. Do you know any other reason you should not do physical activity?

**If YES to any**: Show follow-up question (text area): "Please describe your condition and any medical guidance you've received."

**Track A Additional Questions**:
- Do you experience chronic pain? (Yes/No)
  - If Yes: Location (dropdown: back, neck, knees, hips, shoulders, other), Severity (slider 0-10), Duration (dropdown: <3 months, 3-12 months, 1-5 years, 5+ years)
- Have you fallen in the past year? (Yes/No, if yes: how many times?)
- Do you have difficulty with balance or walking? (Yes/No, text area if yes)
- Have you been diagnosed with osteoporosis, arthritis, or chronic musculoskeletal condition? (Yes/No, text area if yes)

**CTA**: "Next" (progress: 3/6)

### Step 3b: Performance Screening (Track B Path)
**Shown if**: Triage suggests Track B (strength/performance goals).

**PAR-Q+ Questions**: Same 7 core questions as Track A.

**Track B Additional Questions**:
- What is your primary sport or activity? (dropdown: Running, Cycling, Strength training, CrossFit, Martial arts, Team sports, Other)
- How many years have you been training? (dropdown: <1, 1-3, 3-5, 5-10, 10+ years)
- Current training frequency? (dropdown: 1-2x, 3-4x, 5-6x, 7+ sessions per week)
- Have you had any injuries in the past 6 months? (Yes/No)
  - If Yes: Location, Status (healed, healing, still painful), Medical clearance received? (Yes/No)
- Do you have any current pain or movement limitations? (Yes/No, text area if yes)
- Estimated 1RM or recent PRs (optional, text area): "If you know your current strength levels (squat, deadlift, bench, etc.), share them here. This helps us tailor your program."

**CTA**: "Next" (progress: 3/6)

### Step 4: Safety Gate (Automated Background Check)
**Shown to user**: Loading spinner "Reviewing your information..."

**SENTINEL Processing** (backend):
- Check PAR-Q+ responses for red flags
- Check injury history and current pain levels
- Determine: **Pass** (proceed to consent) OR **Medical Clearance Required** (email notification) OR **Decline** (unsuitable, refund offered if already paid—but payment is later, so just message)

**Outcomes**:
- **Pass**: Proceed to Step 5 (consent)
- **Medical Clearance Required**: 
  - Message: "Based on your health screening, we require medical clearance from your physician before enrollment. We'll send you a clearance form via email. Once you obtain clearance, we'll review and confirm your enrollment."
  - CTA: "Submit Assessment" (partial submission, manual review triggered)
- **Decline** (rare, only if severe red flags):
  - Message: "Thank you for your interest. Based on your screening, we recommend consulting your physician before starting an exercise program. We're unable to enroll you at this time, but please reach out if your medical status changes."
  - CTA: "Contact Us" (link to support email)

**If Pass**: Proceed automatically to Step 5.

### Step 5: Consent (GDPR Health Data + Liability)
**Purpose**: Explicit consent for health data processing and assumption of risk.

**Health Data Consent** (Track A/B):
- Full text (as per compliance doc, scrollable box)
- [ ] **Checkbox**: "I consent to CAMI Netherlands processing my health information."

**Marketing Consent** (Optional):
- [ ] **Checkbox**: "I consent to receive marketing emails from CAMI Netherlands (optional)."

**Liability Waiver**:
- Full text (assumption of risk, as per compliance doc)
- [ ] **Checkbox**: "I acknowledge the risks and release CAMI from liability except in cases of gross negligence."

**CTA**: "Complete Assessment" (progress: 5/6)

**Backend**: Record consent timestamp, IP address, consent version for audit trail.

### Step 6: Assessment Summary & Next Steps
**Shown after**: Consent checkboxes confirmed, assessment submitted.

**Message**:
> **Thank you, [Name]!**  
> 
> Your assessment is complete. Here's what happens next:
> 
> 1. **Review**: Our team will review your assessment within 24 hours.
> 2. **Track Recommendation**: Based on your goals and screening, we recommend **[Track A: Clinical Exercise / Track B: Performance Training / Hybrid Program]**.
> 3. **Program Details**: You'll receive an email with:
>    - Your personalized program recommendation
>    - Next program dates (Day 1-3 schedule)
>    - Pricing and payment link (€200-300)
>    - What to expect and how to prepare
> 4. **Questions?**: Reply to the email or contact us at support@centrocami.it.
> 
> **Check your email ([user email]) within 24 hours.**

**CTA**: "Return to Homepage" or "Close"

**Backend**:
- Save assessment to database (profile + goals + screening + consent)
- Tag with Track A/B recommendation (auto-triage based on goals + screening)
- Trigger email: "Assessment received, review in progress" (immediate auto-reply)
- Notify admin: "New assessment submitted: [Name], Track [A/B], Medical clearance [Required/Not Required]" (Slack/email notification)

---

## Stage 4: Email Follow-Up (Assessment to Payment)

### Email 1: Assessment Received (Immediate Auto-Reply)
**Subject**: "Assessment Received - Next Steps | CAMI Netherlands"

**Content**:
> Hi [Name],
> 
> Thank you for completing your assessment! We've received your information and our team is reviewing it now.
> 
> **What happens next**:
> - Within 24 hours, you'll receive a personalized email with:
>   - Your recommended program (Track A, Track B, or Hybrid)
>   - Next available program dates
>   - Pricing and payment instructions
> 
> **In the meantime**: Check out our [blog/social media] for tips on [pain management / strength training] while you wait.
> 
> Questions? Reply to this email anytime.
> 
> Best,  
> [Coach Name]  
> CAMI Netherlands

### Email 2: Program Recommendation + Payment Link (Within 24 Hours)
**Subject**: "Your CAMI Program Recommendation + Next Steps"

**Content** (Track A example):
> Hi [Name],
> 
> Great news! Based on your assessment, we recommend our **Track A: Clinical Exercise & Healthy Aging Program**.
> 
> **Why Track A is right for you**:
> - You mentioned [chronic pain in lower back / mobility concerns / balance issues]
> - Our 3-day program focuses on [reducing pain / improving mobility / fall prevention]
> - You'll receive 30 days of daily personalized coaching tailored to your needs
> 
> **Next Program Dates**:
> - Day 1 (Assessment & Screening): [Date, Time, Location]
> - Day 2 (Back & Legs): [Date, Time, Location]
> - Day 3 (Neck, Shoulders & Breathing): [Date, Time, Location]
> 
> **Pricing**: €[250] (includes 3-day program + 30 days daily email coaching)
> 
> **👉 Ready to join? [Book Your Spot - Stripe Payment Link]**
> 
> **What's included**:
> - Full postural, mobility, and balance assessment
> - 3 in-person group sessions (max 10 participants)
> - Personalized exercise program
> - 30 days of daily email recommendations (CAMIX-powered)
> - Private WhatsApp support group
> - Progress tracking and adaptation
> 
> **What to bring**: Comfortable athletic clothing, water bottle, any mobility aids you use (cane, walker).
> 
> **Note**: [If medical clearance required: "We noticed you indicated [condition]. Please obtain medical clearance from your physician using this form [link] before your first session."]
> 
> Questions? Reply to this email or call/WhatsApp [phone number].
> 
> Looking forward to helping you move pain-free!
> 
> [Coach Name]  
> CAMI Netherlands

**CTA**: Stripe Payment Link (generated per client, includes their name and Track A/B metadata).

**Track B version**: Adjust language (performance goals, strength/power focus, what to bring: athletic shoes, gym clothes, recent training log if available).

### Email 3: Payment Reminder (If No Payment After 3 Days)
**Subject**: "Spots Filling Up - Secure Your Place in [Program Name]"

**Content**:
> Hi [Name],
> 
> Just checking in! We sent you your program recommendation a few days ago.
> 
> Our next **[Track A / Track B] program starts [Date]**, and we only have **[X spots remaining]** (max 10 participants per cohort).
> 
> **Haven't booked yet?** Here's your payment link: [Stripe link]
> 
> **Questions or concerns?** I'm here to help. Reply to this email or call [phone].
> 
> Best,  
> [Coach Name]

**Honest urgency**: Only state "X spots remaining" if true (track spots in CRM/database).

### Email 4: Payment Reminder Final (If No Payment After 7 Days)
**Subject**: "Last Call - [Program Name] Starts [Date]"

**Content**:
> Hi [Name],
> 
> This is a final reminder that our **[Track A / Track B] program starts [Date]**, and we're now fully booked except for **[1-2 spots if true, or skip this sentence if full]**.
> 
> If you're still interested, please book by [deadline, e.g., 48 hours before program start]: [Stripe link]
> 
> If this timing doesn't work for you, no problem! Our next program is [next month date]. Reply "next month" and I'll add you to the waitlist.
> 
> Thanks for considering CAMI. Hope to see you soon!
> 
> [Coach Name]

**After 7 days no payment**: Tag lead as "cold", add to nurture sequence (monthly newsletter, tips, future program announcements).

---

## Stage 5: Payment (Stripe Checkout)

### Phase 1: Payment Links (MVP Launch)
**Implementation**: Manually generated Stripe Payment Links per client.

**Workflow**:
1. Admin receives assessment notification
2. Reviews assessment, determines Track A/B, selects program date
3. Generates Stripe Payment Link (product: "CAMI Track A - [Date]", price: €250, success URL: `nl.centrocami.it/thank-you`, cancel URL: `nl.centrocami.it/payment-cancelled`)
4. Sends Email 2 (Program Recommendation) with payment link
5. Client clicks link → Stripe Checkout → Pays → Redirected to thank-you page
6. Admin receives Stripe email notification → Manually sends onboarding email

**Pros**: Fast to implement, no code required.  
**Cons**: Manual workflow, doesn't scale.

### Phase 2: Checkout Sessions + Webhooks (Automation After MVP)
**Implementation**: Programmatic Stripe Checkout Session API + webhook automation.

**Workflow**:
1. Assessment submitted → Backend creates Checkout Session (Stripe API) with metadata (client ID, Track A/B, program date)
2. Email 2 includes dynamic payment link (Checkout Session URL)
3. Client pays → Stripe webhook `checkout.session.completed` → Backend triggered
4. Backend updates client status: `assessment_complete` → `paid`
5. Backend triggers onboarding email automatically (template populated with client name, program date, Track A/B details)

**Webhook handler** (pseudocode):
```python
@app.post("/webhooks/stripe")
def stripe_webhook(request):
    event = stripe.Webhook.construct_event(request.body, signature, secret)
    
    if event.type == "checkout.session.completed":
        session = event.data.object
        client_id = session.metadata.client_id
        track = session.metadata.track  # "A" or "B"
        
        # Update database
        client = db.get_client(client_id)
        client.status = "paid"
        client.payment_date = now()
        db.save(client)
        
        # Send onboarding email
        send_onboarding_email(client, track)
        
        # Add to WhatsApp group (manual or API if available)
        notify_admin_new_enrollment(client)
    
    return {"status": "success"}
```

**Pros**: Fully automated, scales.  
**Cons**: Requires backend code, webhook endpoint setup, testing.

### Payment Page UX (Stripe Hosted Checkout)
**Stripe Checkout** handles:
- Payment form (card details, billing address)
- Security (PCI compliance, 3D Secure)
- Error handling (declined cards, insufficient funds)
- Mobile-optimized UI

**Customization** (Stripe settings):
- Logo: CAMI logo
- Brand color: Deep blue
- Success URL: `nl.centrocami.it/thank-you?session_id={CHECKOUT_SESSION_ID}`
- Cancel URL: `nl.centrocami.it/payment-cancelled`

**Metadata** (passed to Stripe for webhook):
- `client_id`: Database ID
- `client_email`: Email
- `track`: "A" or "B"
- `program_date`: Date of Day 1
- `language`: "it", "en", or "nl"

---

## Stage 6: Onboarding (Post-Payment)

### Thank-You Page (`nl.centrocami.it/thank-you`)
**Shown immediately after payment success.**

**Content**:
> **🎉 Welcome to CAMI, [Name]!**
> 
> Your payment is confirmed. You're all set for **[Track A / Track B] - [Program Date]**.
> 
> **Check your email** ([user email]) for:
> - Calendar invite (add to your calendar)
> - Pre-program instructions (what to bring, how to prepare)
> - WhatsApp group invite (connect with your cohort)
> 
> **Next steps**:
> 1. Add the program dates to your calendar (email includes .ics file)
> 2. Join the WhatsApp group (link in email)
> 3. Complete pre-program preparation (light activity, hydration, rest)
> 
> **Questions?** Contact us at support@centrocami.it or WhatsApp [phone number].
> 
> See you on [Date]!

**CTA**: "Return to Homepage" or "Download Receipt" (link to Stripe receipt).

### Onboarding Email (Automated, Sent After Payment)
**Subject**: "You're In! Next Steps for Your CAMI Program"

**Content** (Track A example):
> Hi [Name],
> 
> **Welcome to CAMI Netherlands!** 🎉
> 
> Your enrollment in **Track A: Clinical Exercise & Healthy Aging** is confirmed. Here's everything you need to know:
> 
> **📅 Program Schedule**:
> - **Day 1** (Assessment & Screening): [Date, Time, Location]
> - **Day 2** (Back & Legs): [Date, Time, Location]
> - **Day 3** (Neck, Shoulders & Breathing): [Date, Time, Location]
> 
> **Add to calendar**: [.ics attachment or Google Calendar link]
> 
> **📍 Location**: [Full address, parking info, public transport directions]
> 
> **🎒 What to Bring**:
> - Comfortable athletic clothing (stretchy pants, breathable shirt)
> - Athletic shoes (supportive, non-slip)
> - Water bottle (refill station available)
> - Any mobility aids you use (cane, walker, braces)
> - [If medical clearance required: Medical clearance form from your physician]
> 
> **💬 Join Your Cohort (WhatsApp Group)**:
> We've created a private WhatsApp group for your cohort to connect, ask questions, and support each other.  
> **Join here**: [WhatsApp group invite link]
> 
> **📧 Daily Coaching Starts After Day 3**:
> After the 3-day program, you'll receive daily personalized recommendations via email (powered by CAMIX). These emails will include:
> - Mobility drills tailored to your assessment results
> - Posture tips for daily activities
> - Breathing exercises for pain management
> - Progress check-ins
> 
> **❓ Questions?**:
> Reply to this email or WhatsApp [coach phone number]. I'm here to help!
> 
> **See you on [Date]!** Can't wait to help you move pain-free.
> 
> Best,  
> [Coach Name]  
> CAMI Netherlands
> 
> ---
> **Receipt**: [Link to Stripe receipt]  
> **Refund Policy**: Full refund available until [14 days from payment, per Dutch distance selling rules]. After the program starts, no refunds.

**Track B version**: Adjust language (performance goals, bring training log, gym shoes, etc.).

---

## Stage 7: Pre-Program Communication

### Reminder Email (7 Days Before Day 1)
**Subject**: "Your CAMI Program Starts in 1 Week - Final Prep"

**Content**:
> Hi [Name],
> 
> Excited to see you in **1 week** for [Track A / Track B]!
> 
> **Quick reminders**:
> - Day 1 starts [Date, Time] at [Location]
> - Bring: Athletic clothing, shoes, water bottle [, medical clearance if required]
> - Arrive 10 minutes early for check-in
> 
> **Pre-program tips**:
> - Stay hydrated this week (2-3 liters water daily)
> - Get good sleep (7-8 hours) the night before
> - Eat a light meal 2 hours before Day 1 (not on empty stomach, but not too full)
> - [Track A: Avoid intense activity the day before | Track B: Take a rest day or light active recovery the day before]
> 
> **Have questions?** WhatsApp [phone] or reply to this email.
> 
> See you soon!  
> [Coach Name]

### Reminder SMS/WhatsApp (1 Day Before Day 1)
**Message**:
> Hi [Name], this is [Coach] from CAMI. Your program starts tomorrow at [Time]! Address: [Location]. Bring athletic clothing, shoes, water. See you at [Time-10min] for check-in. Questions? Reply here.

---

## Stage 8: In-Person Program (Day 1-3)

**Day 1**: Assessment & screening (90-120 min)  
**Day 2**: Track A (back/legs) or Track B (strength/power) (90 min)  
**Day 3**: Track A (neck/shoulders/breathing) or Track B (conditioning/sport-specific) (90 min)

**Post-Day 3**:
- Group photo (with permission, for testimonials)
- Feedback survey (quick 5 questions via Google Form or Typeform): satisfaction, pain/performance changes, likelihood to recommend
- Announcement: "Daily emails start tomorrow! Check your inbox every morning."

---

## Stage 9: Daily Email Personalization (Day 4-33, 30 Days)

### Email Delivery
**Timing**: Every morning 7:00 AM NL timezone (Utrecht = CET/CEST).

**From**: [Coach Name] <coaching@centrocami.it>  
**Subject**: Daily variety (not same every day, reduces email fatigue):
- "Day 4: Your Mobility Drill for Today"
- "Quick Check-In: How's Your Back Feeling?"
- "Power Tip: Boost Your Squat Strength"
- "Recovery Focus: Breathe Better, Feel Better"

**Content**: Generated by CAMIX POSOLOGIE based on:
- Track A: Mobility, posture, breathing, prevention, micro-routines (5-15 min practices)
- Track B: Strength cues, power drills, recovery, sport-specific skills

**Personalization variables**:
- Client name
- Track (A or B)
- Assessment results (pain location, mobility score, strength baselines, injury history)
- Day in program (Day 4-33, progression over time)
- Previous responses (if client logs practice or rates pain, CAMIX adapts next recommendation)

**CTA**: "Log Today's Practice" (link to simple form: Did you complete today's recommendation? Yes/No. How do you feel? 1-5 scale. Any pain or concerns? Text.)

**Example Track A Email (Day 10)**:
> **Subject**: Day 10: Desk Posture Reset (3-Minute Practice)
> 
> Good morning, [Name]!
> 
> You mentioned lower back pain during your assessment. Here's a quick 3-minute routine to reset your posture if you sit at a desk:
> 
> **Desk Posture Reset (3 min)**:
> 1. **Cat-Cow Stretch** (seated): 10 reps, slow and controlled. Focus on moving your lower back (the area you feel pain).
> 2. **Shoulder Rolls**: 10 forward, 10 backward. Release tension in your upper back.
> 3. **Deep Belly Breathing**: 5 breaths, inhale 4 counts (belly expands), exhale 6 counts (belly draws in).
> 
> **Why this helps**: Sitting compresses your lumbar spine. This routine decompresses, restores mobility, and activates your core.
> 
> **📝 Log your practice**: [Link to form] (30 seconds, helps me tailor tomorrow's recommendation)
> 
> Keep moving,  
> [Coach Name]

**Example Track B Email (Day 15)**:
> **Subject**: Day 15: Squat Depth Check (Mobility + Strength)
> 
> Hey [Name],
> 
> You're halfway through your 30-day program! Let's talk squat depth.
> 
> **Why depth matters**: Greater range of motion = more muscle activation (glutes, quads, hamstrings) and better performance.
> 
> **Today's drill** (10 min):
> 1. **Goblet Squat** (bodyweight or light KB): 3 sets × 8 reps, focus on hitting parallel or below (hip crease below knee). Rest 90s.
> 2. **Ankle Mobility Drill**: 2 sets × 10 reps per leg (elevated heel dorsiflexion stretch). This will help you squat deeper.
> 3. **Breathing Squat**: 1 set × 5 reps, pause at bottom for 5 seconds, deep belly breath. Feel the stretch.
> 
> **Next training session**: Apply this depth to your working sets. Film yourself if possible (side angle) to check form.
> 
> **📊 Log your progress**: [Link] - Did you hit depth? Any limitations?
> 
> Keep pushing,  
> [Coach Name]

### Email Metrics (Track for Optimization)
- Open rate (target 40-50% Track A, 45-55% Track B)
- Click rate on CTA (target 15-25%)
- Response rate on log form (target 30-40% of opens)
- Unsubscribe rate (target <1%)

**Optimization**:
- A/B test subject lines (curiosity vs. benefit vs. personalization)
- Test send time (7 AM vs. 9 AM)
- Test content length (short 2-min read vs. detailed 5-min)
- Test CTA (log practice vs. rate pain vs. ask question)

---

## Stage 10: Retention (Re-Enrollment)

### Re-Enrollment Prompt (Day 25 of 30-Day Program)
**Subject**: "5 Days Left - Continue Your Progress with [Next Program]?"

**Content**:
> Hi [Name],
> 
> You've got **5 days left** in your 30-day coaching program. Awesome work so far!
> 
> **Quick question**: Want to keep the momentum going?
> 
> Our next **[Track A / Track B] program** starts [Date]. It's a new 3-day in-person cycle + 30 more days of personalized coaching.
> 
> **Why continue?**:
> - Build on your progress (CAMIX adapts to your improvements)
> - Go deeper into [pain-free movement / strength gains]
> - Stay accountable (community + daily coaching)
> 
> **Special offer for returning clients**: €[225] (€25 off, normally €250) because you're already part of the CAMI community.
> 
> **👉 Re-enroll now**: [Stripe Payment Link - discounted]
> 
> **Not ready yet?** No problem. Reply and let me know when the next good timing is for you (we run programs monthly).
> 
> Thanks for being part of CAMI!
> 
> [Coach Name]

**Re-enrollment target**: 40-50% (Track A), 50-60% (Track B, higher because performance athletes more goal-driven).

### Post-Program Survey (Day 31, After 30-Day Completion)
**Subject**: "You Did It! Quick Feedback (2 Min Survey)"

**Content**:
> Hi [Name],
> 
> **Congrats!** You completed the full 30-day CAMI program. 🎉
> 
> **Quick favor**: Can you share your experience? It's a 2-minute survey that helps us improve.
> 
> **Take the survey**: [Google Form / Typeform link]
> 
> Questions:
> 1. Overall satisfaction (1-5 scale)
> 2. [Track A: Pain reduction | Track B: Performance improvement] (1-5 scale)
> 3. Likelihood to recommend to a friend (NPS: 0-10)
> 4. What did you like most?
> 5. What could we improve?
> 6. Testimonial (optional): "Can we share your story? Write a few sentences about your experience."
> 
> **Thank you for trusting CAMI.** Whether you re-enroll or not, you're always part of our community. Stay in touch!
> 
> Best,  
> [Coach Name]

**Incentive** (optional, test): "Complete the survey and get a free [resource, e.g., '10 At-Home Mobility Routines PDF']."

---

## Funnel Analytics Dashboard

### Key Metrics to Track
**Acquisition**:
- Landing page views (by source: Meta, Google, Organic, Referral)
- Cost per click (CPC)
- Cost per lead (CPL): Ad spend / Assessment starts
- Cost per acquisition (CPA): Ad spend / Payments

**Conversion**:
- Landing → Start Assessment: % (target 10-15%)
- Start → Complete Assessment: % (target 70-80%)
- Complete → Payment: % (target 30-40%)
- Overall Landing → Payment: % (target 2-4%)

**Engagement**:
- Email open rates (onboarding, daily coaching, re-enrollment)
- Email click rates (CTA: log practice, payment link)
- WhatsApp group activity (messages per day, participation rate)

**Retention**:
- 30-day completion rate (% who receive all 30 emails without unsubscribe)
- Re-enrollment rate (% who pay for next program)
- 90-day retention (% still active after 3 months)

**Outcomes** (self-reported):
- [Track A] Pain reduction (% who report lower pain after 30 days)
- [Track B] Performance improvement (% who report strength/power gains)
- NPS (Net Promoter Score): % promoters (9-10) - % detractors (0-6)

### Tools
- **Google Analytics 4**: Landing page views, UTM attribution, goal conversions (assessment start, complete, payment)
- **Stripe Dashboard**: Payment conversion, revenue, refunds
- **Email service provider** (Mailchimp, SendGrid, etc.): Email metrics (open, click, unsubscribe)
- **CRM/Database** (Airtable, Notion, custom): Client records, funnel stage, Track A/B, program dates, payment status
- **Dashboard** (Google Data Studio, Metabase, custom): Combine all sources into single view

---

## Next Steps: Implementation Priorities

### Week 1 (MVP Essentials)
1. ✅ Funnel spec complete
2. Create landing page (single-file HTML, trilingual, mobile-first)
3. Create assessment form (multi-step, Track A/B paths, PAR-Q+, consent)
4. Set up Stripe account (Payment Links Phase 1)
5. Write email templates (assessment received, program recommendation, onboarding, daily Track A/B examples)

### Week 2 (Testing)
6. End-to-end test (landing → assessment → email → payment → onboarding)
7. Set up Google Analytics 4 (UTM tracking, goal conversions)
8. Create CRM/database (track clients, funnel stage, program dates)

### Week 3 (Automation)
9. Integrate CAMIX POSOLOGIE (daily email content generation Track A/B)
10. Implement SENTINEL safety gates (filter recommendations based on profile)
11. Stripe webhook automation (Phase 2, optional if time allows)

### Week 4 (Launch)
12. Soft launch (invite existing Centro CAMI clients, friends, small test audience)
13. Collect feedback, iterate on messaging/UX
14. Paid ads launch (Meta/Google, start with €500-1000 budget)

---

**Document status**: v1.0 - Funnel specification complete  
**Last updated**: 2026-06-03  
**Owner**: CAMI Netherlands team
