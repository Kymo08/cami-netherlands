# CAMI Netherlands Landing Page
**Trilingual (IT/EN/NL) Landing Page - Utrecht**

## Overview
Single-file HTML landing page for CAMI Netherlands clinical exercise and performance programs. Fully responsive, mobile-first design with trilingual support (Italian, English, Dutch).

## Features
- ✅ **Trilingual**: IT/EN/NL language switcher with localStorage persistence
- ✅ **Mobile-first responsive**: Tailwind CSS, works on all devices
- ✅ **Premium design**: Apple/Stripe/Notion aesthetic (deep blue, white, green accent)
- ✅ **Animations**: Fade-in on scroll (IntersectionObserver), smooth transitions
- ✅ **SEO ready**: Meta tags, Open Graph, semantic HTML
- ✅ **Performance**: <2s load time (single-file, Tailwind CDN for MVP)
- ✅ **Accessibility**: Semantic HTML, good contrast ratios, keyboard navigation

## Sections
1. **Hero**: Value proposition + CTA "Book Free Assessment" / Language switcher
2. **Stats**: Social proof (85% pain reduction, 10+ years experience, max 10 participants)
3. **Problem**: Pain points (Track A: chronic pain, Track B: performance plateaus)
4. **Solution**: Track A (Clinical Exercise) + Track B (Athletic Performance) cards
5. **How It Works**: 4-step process (Assessment → Enrollment → 3 Days → 30 Days coaching)
6. **Why CAMI**: 6 benefits (Trilingual, Adaptive Coaching, Clinical Expertise, Small Group, Safety, Results)
7. **Testimonials**: 3 client stories (Track A, Track B, Trilingual)
8. **Pricing**: €250 transparent pricing, full breakdown (refund policy, what's included)
9. **FAQ**: 6 common questions with accordion (exercise experience, insurance, location, rescheduling, personalization, time commitment)
10. **CTA Final**: "Ready to Start?" → "Start Free Assessment" button
11. **Footer**: Links, contact, privacy/terms

## Design System

### Colors
- **Primary**: `#1E3A8A` (Deep blue - trust, professionalism)
- **Primary Light**: `#3B82F6` (Lighter blue - hover states)
- **Accent**: `#10B981` (Green - vitality, growth)
- **Text**: `#1F2937` (Dark gray - body text)
- **Text Light**: `#6B7280` (Medium gray - secondary text)
- **Background**: `#FFFFFF` (White - main background)
- **Background Alt**: `#F9FAFB` (Light gray - section alternating background)

### Typography
- **Font**: System font stack (-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif)
- **Hero H1**: 5xl (3rem) md:6xl (3.75rem), font-bold
- **Section H2**: 4xl (2.25rem), font-bold
- **Card H3**: 2xl (1.5rem), font-semibold
- **Body**: base (1rem), regular
- **Lead**: xl (1.25rem), regular

### Spacing
- **Section padding**: py-20 (5rem vertical)
- **Container max-width**: 5xl (64rem) for content, 7xl (80rem) for full-width
- **Card gap**: gap-8 (2rem)
- **Button padding**: px-8 py-4 (2rem horizontal, 1rem vertical)

## Testing

### Local Testing
1. Open `index.html` in browser (double-click or `file://` protocol)
2. Test language switcher (IT/EN/NL buttons in navigation)
3. Test all CTAs (should link to `/assessment` or anchor links `#how-it-works`)
4. Test mobile responsive (browser DevTools → Responsive mode)
5. Test FAQ accordion (click questions to expand/collapse)
6. Test smooth scroll (click anchor links, should scroll smoothly)
7. Test animations (scroll down, elements should fade in)

### Browser Testing
- ✅ Chrome/Edge (Chromium)
- ✅ Firefox
- ✅ Safari (Mac/iOS)
- ⚠️ IE11 (not supported, Tailwind CDN requires modern browsers)

### Mobile Testing
- Test on real devices (iOS Safari, Android Chrome)
- Use browser DevTools responsive mode (iPhone 12, Samsung Galaxy S21)
- Check touch targets (buttons, links should be min 44×44px)

### Performance Testing
- Google PageSpeed Insights: https://pagespeed.web.dev/
- Target scores:
  - Performance: 90+
  - Accessibility: 95+
  - Best Practices: 90+
  - SEO: 95+

### Accessibility Testing
- Screen reader test (NVDA, VoiceOver)
- Keyboard navigation (Tab, Enter, Esc)
- Color contrast (WebAIM Contrast Checker)
- ARIA labels (ensure buttons/links have descriptive text)

## Deployment

### Option 1: Static Hosting (Vercel, Netlify, GitHub Pages)
**Recommended for MVP**

#### Vercel (easiest)
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy from cami-netherlands/web/landing/
cd /data/data/com.termux/files/home/cami-netherlands/web/landing
vercel

# Follow prompts:
# - Project name: cami-netherlands-landing
# - Deploy: yes
# - Domain: nl.centrocami.it (add custom domain later)
```

#### Netlify
1. Drag and drop `web/landing/` folder to netlify.com/drop
2. Or connect GitHub repo → Auto-deploy on push
3. Custom domain: Settings → Domain management → Add custom domain `nl.centrocami.it`

#### GitHub Pages
1. Create repo `cami-netherlands-landing`
2. Push `index.html` to `main` branch
3. Settings → Pages → Source: `main` branch, `/` root
4. Custom domain: Add `CNAME` file with `nl.centrocami.it`

### Option 2: Traditional Web Hosting (cPanel, Hostinger, etc.)
1. Upload `index.html` to server via FTP/SFTP
2. Place in subdomain folder (e.g., `public_html/nl/` for `nl.centrocami.it`)
3. Configure DNS (A record or CNAME pointing to hosting IP)
4. Enable HTTPS (Let's Encrypt via cPanel or hosting provider)

### Option 3: CDN (Cloudflare Pages)
```bash
# Install Wrangler CLI
npm install -g wrangler

# Deploy
cd /data/data/com.termux/files/home/cami-netherlands/web/landing
wrangler pages publish . --project-name=cami-nl-landing

# Custom domain: Cloudflare Dashboard → Pages → Custom domains
```

## Production Optimizations

### Before Launch (Priority)
1. **Replace Tailwind CDN with inline CSS**: Extract critical CSS, inline in `<style>`, remove CDN script
2. **Add real images**: Replace placeholder text with real photos (hero, testimonials, coach)
3. **Optimize images**: Convert to WebP, lazy load below-the-fold images
4. **Update meta tags**: Real OG image URL, final domain `nl.centrocami.it`
5. **Update contact info**: Real phone number, email, address (footer)
6. **Google Analytics**: Add GA4 tracking code (if desired)
7. **Update CTA links**: `/assessment` should point to real assessment form URL

### After Launch (Performance)
1. **Inline critical CSS**: Remove Tailwind CDN, inline only used CSS classes (~50KB compressed)
2. **Image optimization**: WebP format, responsive images `<picture>`, lazy loading `loading="lazy"`
3. **Font optimization**: Add `font-display: swap` if using custom fonts
4. **Minify HTML**: Remove whitespace, comments (optional, minimal gains)
5. **CDN delivery**: Serve static assets via Cloudflare or similar CDN
6. **HTTP/2 or HTTP/3**: Enable on server for faster multiplexing

## Customization

### Change Colors
Update CSS custom properties in `<style>`:
```css
:root {
    --color-primary: #1E3A8A; /* Change to your brand color */
    --color-accent: #10B981; /* Change to your accent color */
}
```

### Change Content
All content is in HTML with `data-lang-content` attributes:
- `data-lang-content="it"` → Italian
- `data-lang-content="en"` → English
- `data-lang-content="nl"` → Dutch

Edit text directly in HTML. Language switcher will show/hide based on active language.

### Add/Remove Sections
Sections are independent `<section>` blocks. To remove:
1. Delete entire `<section>...</section>` block
2. Update navigation anchor links if needed

To add:
1. Copy existing section structure
2. Add `data-lang-content` for multilingual text
3. Use `.fade-in` class for scroll animation

### Change CTA Links
Update all CTA buttons:
```html
<!-- Current (placeholder) -->
<a href="/assessment" class="btn-primary">...</a>

<!-- After assessment form is ready -->
<a href="https://nl.centrocami.it/assessment" class="btn-primary">...</a>
```

## Translations

### Adding a New Language (e.g., German)
1. Add button to language switcher:
```html
<button onclick="switchLanguage('de')" data-lang-btn="de">DE</button>
```

2. Add German content for each section:
```html
<div data-lang-content="de" class="text-center fade-in">
    <h2>Bewege Dich Ohne Schmerzen</h2>
    <!-- ... German content ... -->
</div>
```

3. Update all sections with German translations (copy IT/EN/NL structure).

### Translation Guidelines
- **Keep it concise**: Landing pages work best with clear, short copy
- **Maintain tone**: Professional, empowering, not patronizing
- **Localize, don't translate literally**: Adapt idioms, cultural references
- **Test with native speakers**: Ensure clarity and naturalness

## SEO

### Meta Tags (Update in `<head>`)
```html
<title>CAMI Netherlands - Clinical Exercise & Performance Training | Utrecht</title>
<meta name="description" content="Clinical exercise and athletic performance programs in Utrecht. Trilingual support (IT/EN/NL). Personalized coaching for pain relief, mobility, strength, and performance.">
```

### Open Graph (Update URLs)
```html
<meta property="og:image" content="https://nl.centrocami.it/og-image.jpg">
<meta property="og:url" content="https://nl.centrocami.it">
```

### Sitemap (Optional)
For multi-page site, create `sitemap.xml`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://nl.centrocami.it/</loc>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://nl.centrocami.it/assessment</loc>
    <priority>0.8</priority>
  </url>
</urlset>
```

## Analytics

### Google Analytics 4 (Recommended)
Add tracking code before `</head>`:
```html
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

### Events to Track
- **Page view**: Automatic (GA4)
- **Language switch**: `gtag('event', 'language_switch', { language: 'it' });`
- **CTA clicks**: `gtag('event', 'cta_click', { button_text: 'Book Assessment', location: 'hero' });`
- **Scroll depth**: Use GA4 enhanced measurement or custom triggers

## Support

### Issues
- Check browser console for JavaScript errors
- Test language switcher (localStorage must be enabled)
- Verify all links point to correct URLs
- Test on multiple devices and browsers

### Contact
- Project lead: CAMI Netherlands team
- Technical issues: Create issue in project repo or contact dev team

---

**Status**: ✅ Ready for MVP testing  
**Last updated**: 2026-06-03  
**Version**: 1.0
