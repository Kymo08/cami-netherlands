# CAMI Netherlands Assessment Form

Multi-step assessment form for CAMI Netherlands clinical exercise and athletic performance programs. Collects profile, goals, health screening (PAR-Q+), performs safety checks (SENTINEL), obtains GDPR-compliant consent, and provides track recommendations.

## Overview

**Type**: Multi-step form (6 steps)  
**Languages**: Italian, English, Dutch (trilingual)  
**Design**: Mobile-first responsive, Apple/Stripe/Notion aesthetic  
**Compliance**: GDPR Art. 9 (health data), Dutch UCPD, medical disclaimers  
**File**: Single-file HTML (~1,800 lines) with embedded CSS and JavaScript

## Features

### Core Functionality
- **6-Step Flow**: Profile → Goals → Screening → Safety Gate → Consent → Summary
- **Dynamic Question Routing**: Shows Track A (clinical) or Track B (performance) questions based on goals selected in Step 2
- **PAR-Q+ Screening**: Standard 7-question pre-exercise screening with conditional follow-up
- **SENTINEL Safety Check**: Automated safety assessment with 3 outcomes (Pass / Medical Clearance Required / Declined)
- **GDPR Compliance**: Explicit consent for health data (Art. 9) with scrollable legal text, separate marketing consent, liability waiver
- **Track Recommendation**: Algorithm calculates Track A / Track B / Hybrid based on goals, age, and screening responses
- **Progress Indicator**: Visual progress bar showing step X of 6 with percentage
- **Language Switcher**: Persistent language selection (localStorage) across IT/EN/NL
- **Form Validation**: Client-side validation with error messages in all 3 languages
- **Visual Feedback**: Checkbox cards with selected state, error highlighting, smooth animations

### Design System
- **Colors**: Deep blue primary (#1E3A8A), green accent (#10B981), white background
- **Typography**: System font stack, responsive sizing (base to 3xl)
- **Animations**: Fade-in step transitions, smooth scrolling, hover effects
- **Responsive**: Mobile-first (320px+), tablet (768px+), desktop (1024px+)

## Step-by-Step Breakdown

### Step 1: Profile (17%)
**Purpose**: Collect basic contact information  
**Fields**:
- Name* (text, required)
- Email* (email validation, required)
- Age* (number, 18-99, required)
- Phone (text, optional)
- Referral source* (select: Meta/Google/Friend/Website/Other, required)

**Validation**: Name non-empty, valid email regex, age 18-99, referral selected  
**Data saved**: `formData.profile` = {name, email, age, phone, referral, language}

---

### Step 2: Goals (33%)
**Purpose**: Identify client goals to route to Track A (clinical) or Track B (performance)  
**Options**: 8 checkbox goals with emoji icons + descriptions

**Track A Goals** (Clinical Exercise):
- 🩹 Reduce chronic pain (back, neck, knees, joints)
- 🤸 Improve mobility (flexibility, joint ROM)
- ⚖️ Improve balance (stability, fall prevention)
- 🚶 Maintain independence (daily activities without assistance)

**Track B Goals** (Athletic Performance):
- 💪 Increase strength (1RM, build muscle)
- ⚡ Improve power (explosiveness, speed)
- 🏆 Competition preparation (races, sport events)
- 🩺 Injury recovery (return to training after injury) *[Hybrid indicator]*

**Validation**: At least 1 goal selected  
**Data saved**: `formData.goals` = array of selected goal values  
**Side effect**: Triggers `updateTrackQuestions()` to show/hide Track A or Track B additional questions in Step 3

---

### Step 3: Health & Performance Screening (50%)
**Purpose**: Safety screening (PAR-Q+) + Track-specific questions

#### PAR-Q+ Core Questions (always shown)
7 yes/no radio questions in blue box:
1. Heart condition diagnosed by doctor?
2. Chest pain during physical activity?
3. Chest pain at rest in past month?
4. Dizziness or loss of consciousness?
5. Bone/joint problem that worsens with activity?
6. Blood pressure or heart medication?
7. Any other reason not to do physical activity?

**Conditional Follow-up**: If any question = YES, yellow box appears with textarea asking for details + medical guidance received.

#### Track A Additional Questions (shown if any clinical goal selected in Step 2)
- **Chronic pain**: Yes/No radio
  - If Yes → show pain details:
    - **Pain location**: Checkboxes (Back/Neck/Knees/Hips/Shoulders/Other)
    - **Pain severity**: Slider 0-10 with live value display
    - **Pain duration**: Dropdown (Less than 3 months / 3-12 months / 1-5 years / 5+ years)
- **Fall history**: Fallen in past year? Yes/No radio
- **Balance difficulty**: Difficulty with balance or walking? Yes/No radio

#### Track B Additional Questions (shown if any performance goal selected in Step 2)
- **Primary sport/activity**: Dropdown (Running/Cycling/Strength training/CrossFit/Martial arts/Team sports/Other)
- **Training years**: Dropdown (Less than 1 year / 1-3 years / 3-5 years / 5-10 years / 10+ years)
- **Training frequency**: Dropdown (1-2x / 3-4x / 5-6x / 7+x per week)
- **Recent injury**: Any injuries in past 6 months? Yes/No radio

**Validation**: 
- All 7 PAR-Q+ questions answered (alert if missing)
- If Track A shown: has_chronic_pain answered, if yes then pain location (≥1), severity, duration required + fall/balance questions answered
- If Track B shown: primary sport, training years, training frequency, recent injury all answered

**Data saved**: `formData.screening` = {parq: {...}, has_chronic_pain, pain_location[], pain_severity, pain_duration, has_fallen, balance_difficulty, primary_sport, training_years, training_frequency, recent_injury}

---

### Step 4: Safety Gate (SENTINEL) (67%)
**Purpose**: Automated safety review with loading simulation + outcome display

#### Loading State (2 seconds)
- Spinning loader animation
- Text: "Analyzing..." (IT: "Analisi in corso...", NL: "Analyseren...")

#### Outcome 1: Pass ✅ (Green box)
- **Criteria**: No PAR-Q+ YES answers, pain severity <8
- **Message**: "All Clear! You can safely proceed with the program. Click Next to continue."
- **Action**: Allow next step
- **Data saved**: `formData.sentinel_status = 'pass'`

#### Outcome 2: Medical Clearance Required ⚠️ (Yellow box)
- **Criteria**: 1-2 PAR-Q+ YES answers, OR pain severity ≥8
- **Message**: "Based on your responses, we need clearance from your doctor before starting. This is for your safety. We'll send you a form to complete with your doctor within 24 hours. You can still complete the assessment."
- **Action**: Allow next step (client can continue, admin will follow up)
- **Data saved**: `formData.sentinel_status = 'medical_clearance_required'`

#### Outcome 3: Declined ❌ (Red box)
- **Criteria**: ≥3 PAR-Q+ YES answers
- **Message**: "Unfortunately, based on your responses, this program is not suitable for you at this time. We recommend consulting with a doctor or physiotherapist before starting an exercise program."
- **Contact**: info@centrocami.it
- **Action**: Allow next step (form completion for record)
- **Data saved**: `formData.sentinel_status = 'declined'`

**Algorithm**: `calculateSentinelStatus()` function
```javascript
yesCount = count PAR-Q+ YES answers
painSeverity = pain slider value (if Track A + has_chronic_pain)

if painSeverity >= 8: return 'clearance'
if yesCount === 0: return 'pass'
if yesCount >= 3: return 'decline'
else: return 'clearance'
```

---

### Step 5: Consent & Privacy (83%)
**Purpose**: GDPR-compliant explicit consent for health data processing

#### Health Data Consent (GDPR Art. 9) - REQUIRED
- **Blue box** with scrollable legal text (IT/EN/NL)
- **Content**: 
  - Explicit consent to process health data (pain, mobility, balance, medical conditions, history)
  - Purposes: (1) Safety assessment, (2) Exercise personalization, (3) Progress monitoring, (4) Service communications
  - Retention: 1 year, encrypted
  - Withdrawal: privacy@centrocami.it anytime
- **Checkbox**: "I consent to the processing of my health data *" (required)
- **Error message**: "This consent is required to continue"

#### Marketing Consent - OPTIONAL
- **Gray box** (not required)
- **Content**: Receive emails with tips, new programs, special offers; unsubscribe anytime
- **Checkbox**: "I would like to receive emails..." (optional, unchecked by default)

#### Liability Waiver - REQUIRED
- **Gray box** with scrollable legal text (IT/EN/NL)
- **Content**:
  - Acknowledge: (1) Exercise involves risks, (2) Wellness program not medical advice, (3) Stop if pain/dizziness/symptoms, (4) Responsible for own safety, (5) Provided accurate health info
  - Release CAMI from liability except gross negligence
- **Checkbox**: "I have read and accept the liability waiver *" (required)
- **Error message**: "This consent is required to continue"

**Validation**: Health consent + liability waiver both checked (required), marketing optional

**Data saved**: `formData.consent` = {health_data: true, marketing: true/false, liability: true, timestamp: ISO8601, ip: 'CLIENT_IP'}

---

### Step 6: Summary (100%)
**Purpose**: Thank you + track recommendation + next steps

#### Thank You Message
- 🎉 emoji
- **Title**: "Assessment Complete!" (IT: "Valutazione Completata!", NL: "Beoordeling Voltooid!")
- **Text**: "Thank you for completing the assessment. We have everything we need to personalize your program."

#### Track Recommendation (Blue gradient box)
Algorithm `calculateTrackRecommendation()`:
```javascript
clinicalScore = count clinical goals * 3 + age modifiers
performanceScore = count performance goals * 3 + age modifiers
injury_recovery_return goal → +1 both (hybrid indicator)

Age modifiers:
- age >= 66: clinicalScore +2
- age >= 56: clinicalScore +1
- age <= 45: performanceScore +1

Decision:
if abs(clinicalScore - performanceScore) <= 2: return 'Hybrid'
if clinicalScore > performanceScore: return 'A'
else: return 'B'
```

**Display**:
- **Track A**: 🧘 Clinical Exercise & Healthy Aging - "Perfect program to reduce chronic pain, improve mobility and balance with safe, personalized exercises."
- **Track B**: 🏋️ Performance & Athletic Preparation - "Ideal program to increase strength, power, and sport-specific preparation with periodized training."
- **Hybrid**: 🔄 Hybrid Program - "A personalized program combining clinical and performance elements for your unique goals."

#### Next Steps (ordered list)
1. "You'll receive a confirmation email within 5 minutes"
2. "We'll send you the program recommendation and payment link within 24 hours"
3. "Check your inbox (and spam) for updates"

#### CTA Button
- **Link**: `<a href="/">` (return to landing page)
- **Text**: "← Back to Home" (IT: "← Torna alla Home", NL: "← Terug naar Home")

**Data saved**: `formData.track_recommended` = 'A' / 'B' / 'Hybrid'

---

## Technical Implementation

### JavaScript State Management
```javascript
let currentStep = 1;
const totalSteps = 6;
const formData = {
  profile: {name, email, age, phone, referral, language},
  goals: ['goal1', 'goal2', ...],
  screening: {parq: {...}, ...},
  sentinel_status: 'pass' | 'medical_clearance_required' | 'declined',
  consent: {health_data, marketing, liability, timestamp, ip},
  track_recommended: 'A' | 'B' | 'Hybrid'
};
```

### Key Functions

#### Language Management
- `switchLanguage(lang)`: Updates DOM with IT/EN/NL content, saves to localStorage
- All content uses `data-lang-content="lang"` attributes with `.active` class for visibility

#### Navigation
- `showStep(step)`: Show/hide step content, update progress bar, scroll to top
- `updateProgress()`: Calculate percentage (currentStep / totalSteps * 100)
- `updateStepDisplay()`: Update step counter in all 3 languages
- Previous button hidden on Step 1, Next button hidden on Step 6

#### Validation
- `validateStep(step)`: Step-specific validation logic
- `showError(fieldId)` / `hideError(fieldId)`: Toggle error messages + field highlighting
- Step 1: Name, email (regex), age (18-99), referral
- Step 2: At least 1 goal selected
- Step 3: All PAR-Q+ answered, Track A/B questions if shown
- Step 5: Health consent + liability waiver checked

#### Dynamic Question Routing
- `updateTrackQuestions()`: Called after Step 2 validation
  - If any clinical goal selected → show Track A questions (display: block)
  - If any performance goal selected → show Track B questions (display: block)
  - If both → show both
  - If neither → hide both (shouldn't happen due to validation)

#### PAR-Q+ Logic
- `updateParqFollowup()`: Event listener on all 7 PAR-Q+ radio buttons
  - If any = YES → show yellow followup textarea
  - If all = NO → hide followup

#### Pain Severity Slider
- Event listener on `#pain_severity` range input
- Updates `#pain-value` span text in real-time as slider moves

#### SENTINEL Check
- `performSentinelCheck()`: Called when entering Step 4
  - Show loading spinner for 2 seconds (setTimeout)
  - Call `calculateSentinelStatus()` to determine outcome
  - Hide loading, show Pass / Clearance / Decline box
- `calculateSentinelStatus()`: Logic based on PAR-Q+ YES count + pain severity

#### Track Recommendation
- `displayTrackRecommendation()`: Called when entering Step 6
  - Call `calculateTrackRecommendation()` to determine Track A/B/Hybrid
  - Generate HTML with emoji icon + title + description in user's language
  - Inject into `#track-recommendation-content`
- `calculateTrackRecommendation()`: Scoring algorithm based on goals + age

### CSS Features
- `:root` CSS variables for colors (--color-primary, --color-accent, etc.)
- `.step-content.active` controls visibility + fadeIn animation
- `.checkbox-card.selected` blue border + background when checked
- `.error` class red border on fields, `.error-message.show` displays error text
- Responsive breakpoints via Tailwind classes (md:, lg:, etc.)

### Browser Events
- `DOMContentLoaded`: Initialize language, update step display, add slider/PAR-Q+ listeners
- `beforeunload`: Log formData to console (for debugging, would submit to backend in production)
- Click handlers: Next button (validate + advance), Previous button (go back)
- Change handlers: Checkbox card selection, PAR-Q+ followup, pain details toggle

---

## Form Data Structure

Example completed assessment:
```json
{
  "profile": {
    "name": "Maria Rossi",
    "email": "maria@esempio.com",
    "age": 62,
    "phone": "+31 6 1234 5678",
    "referral": "meta_ad",
    "language": "it"
  },
  "goals": ["reduce_chronic_pain", "improve_mobility", "improve_balance"],
  "screening": {
    "parq": {
      "parq_heart": "no",
      "parq_chest_active": "no",
      "parq_chest_rest": "no",
      "parq_dizziness": "no",
      "parq_bone_joint": "yes",
      "parq_medication": "no",
      "parq_other": "no",
      "followup": "Ho artrite al ginocchio controllata con fisioterapia"
    },
    "has_chronic_pain": true,
    "pain_location": ["back", "neck", "knees"],
    "pain_severity": 6,
    "pain_duration": "1_5_years",
    "has_fallen": false,
    "balance_difficulty": true
  },
  "sentinel_status": "medical_clearance_required",
  "consent": {
    "health_data": true,
    "marketing": true,
    "liability": true,
    "timestamp": "2026-06-03T14:32:15.678Z",
    "ip": "CLIENT_IP"
  },
  "track_recommended": "A"
}
```

---

## Testing Checklist

### Functional Testing
- [ ] **Language switcher**: Toggle IT/EN/NL, verify all text updates, check localStorage persistence
- [ ] **Step 1 validation**: Try empty name/invalid email/age out of range, verify error messages
- [ ] **Step 2 goals**: Select 0 goals (should error), select Track A only, Track B only, both, check visual feedback
- [ ] **Step 3 PAR-Q+**: Answer all NO (followup hidden), answer 1+ YES (followup shows)
- [ ] **Step 3 Track A**: Select Track A goals → verify Track A questions appear, test pain details toggle
- [ ] **Step 3 Track B**: Select Track B goals → verify Track B questions appear
- [ ] **Step 3 validation**: Leave PAR-Q+ unanswered (should alert), leave Track questions unanswered (should alert)
- [ ] **Step 4 SENTINEL**: 
  - No PAR-Q+ YES + pain <8 → Pass ✅
  - 1-2 PAR-Q+ YES → Clearance ⚠️
  - 3+ PAR-Q+ YES → Decline ❌
  - Pain severity ≥8 → Clearance ⚠️
- [ ] **Step 5 consent**: Uncheck required consents (should error), check optional marketing
- [ ] **Step 6 track recommendation**: 
  - Mostly clinical goals + age 60+ → Track A
  - Mostly performance goals + age <40 → Track B
  - Mixed goals or injury recovery → Hybrid
- [ ] **Navigation**: Previous button (hidden Step 1), Next button (hidden Step 6), progress bar updates

### Browser Testing
- [ ] **Chrome/Edge**: Latest version, all features working
- [ ] **Firefox**: Latest version, all features working
- [ ] **Safari**: Latest version (macOS/iOS), all features working
- [ ] **Mobile Safari (iOS)**: iPhone 12+, touch targets ≥44px, no horizontal scroll
- [ ] **Chrome Mobile (Android)**: Galaxy/Pixel, touch targets, no horizontal scroll

### Responsive Testing
- [ ] **Mobile (320px-767px)**: Single column, stacked layout, readable text
- [ ] **Tablet (768px-1023px)**: 2-column pain location grid, comfortable spacing
- [ ] **Desktop (1024px+)**: Max-width container (1024px), generous whitespace

### Accessibility
- [ ] **Keyboard navigation**: Tab through form, Enter to submit, Space to check boxes
- [ ] **Screen reader**: Semantic HTML (<label>, <fieldset>), ARIA labels on custom elements
- [ ] **Color contrast**: Text passes WCAG AA (4.5:1 minimum), error red passes AA
- [ ] **Focus indicators**: Visible blue outline on focused elements

### Performance
- [ ] **Page load**: <2 seconds on 3G
- [ ] **Bundle size**: Single-file HTML ~180KB (acceptable for MVP with Tailwind CDN)
- [ ] **Animations**: Smooth 60fps on mid-range devices

---

## Deployment

### Option 1: Vercel (Recommended for MVP)
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd /path/to/cami-netherlands/web/assessment
vercel

# Custom domain (after first deploy)
vercel domains add nl.centrocami.it
```

### Option 2: Netlify
1. Drag-drop `web/assessment/` folder to [Netlify Drop](https://app.netlify.com/drop)
2. Or connect GitHub repo for auto-deploy on push
3. Custom domain: Site settings → Domain management → Add custom domain → `nl.centrocami.it`

### Option 3: Traditional Hosting (cPanel/Hostinger)
1. Create subdomain `nl.centrocami.it` in cPanel
2. FTP upload `index.html` to subdomain folder
3. Enable HTTPS via Let's Encrypt in cPanel

### DNS Setup
**Subdomain**: `nl.centrocami.it`
- **A record**: Point to server IP (Vercel/Netlify provides)
- **CNAME**: Or CNAME to `cname.vercel-dns.com` / `YOUR-SITE.netlify.app`

---

## Production Optimizations

### Before Launch
1. **Replace Tailwind CDN**: Inline critical CSS (<50KB) for faster first paint
2. **Add real images**: Hero image, testimonial photos, coach photo
3. **Update contact info**: Real phone number, email address, WhatsApp link
4. **Update meta tags**: Real Open Graph image, final domain URL
5. **Google Analytics**: Add GA4 tracking code before `</head>`
6. **Backend integration**: Connect form submission to `/api/assessment/submit` endpoint
7. **Email automation**: Trigger "Assessment received" auto-reply on submit

### After Launch
1. **Monitor analytics**: Conversion rates per step, drop-off points
2. **A/B test**: Hero copy, CTA button text, step order
3. **Collect feedback**: User testing, survey on Step 6
4. **Iterate**: Add/remove questions based on data quality needs

---

## Backend Integration

### POST Endpoint: `/api/assessment/submit`
**Request Body**: `formData` object (JSON)
**Response**: 
```json
{
  "status": "success",
  "assessment_id": "uuid-here",
  "track_recommended": "A",
  "medical_clearance_required": true,
  "message": "Assessment received. Check your email within 5 minutes."
}
```

**Backend Actions**:
1. Validate JSON against schema (`data/schemas/intake-track-a.json` or `intake-track-b.json`)
2. Run triage algorithm (`data/schemas/triage-routing-logic.md`) to confirm track recommendation
3. Save to database (SQLite/PostgreSQL/MongoDB)
4. Trigger emails:
   - Client: "Assessment received" auto-reply (immediate)
   - Admin: Slack/email notification "New assessment: [Name], Track [A/B], Medical clearance [Yes/No]"
5. If medical clearance required: Attach clearance form PDF
6. Schedule: "Program recommendation + Payment Link" email (within 24h, manual send for MVP)

---

## Troubleshooting

### Issue: Language switcher not working
- **Check**: Browser localStorage enabled (some privacy modes block)
- **Fix**: Add fallback to cookie or URL param `?lang=it`

### Issue: Step doesn't advance after clicking Next
- **Check**: Browser console for validation errors
- **Debug**: `console.log(formData)` after each step to see saved data
- **Fix**: Ensure all required fields filled, check validation logic

### Issue: Track A/B questions not showing
- **Check**: Step 2 goals selected, `formData.goals` array populated
- **Debug**: `console.log(formData.goals)` after Step 2 validation
- **Fix**: Verify `updateTrackQuestions()` called in Step 2 validation success

### Issue: SENTINEL always shows loading
- **Check**: JavaScript errors in console (typo in function names)
- **Fix**: Ensure `setTimeout` callback executes, check `calculateSentinelStatus()` returns valid string

### Issue: Form data lost on refresh
- **Expected behavior**: Client-side only, no persistence
- **Fix**: For production, add autosave to localStorage every step, or warn on `beforeunload`

---

## Contact

**Project Lead**: CAMI Netherlands  
**Technical Support**: OpenCode development team  
**Email**: info@centrocami.it  
**Repository**: `/data/data/com.termux/files/home/cami-netherlands/`

---

## Status

**Version**: 1.0 (MVP)  
**Date**: 2026-06-03  
**Status**: ✅ Complete and ready for testing  
**Next Steps**: End-to-end testing, backend integration, deployment
