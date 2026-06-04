# CAMI Netherlands – Operational Plan W1→W12
**Go-to-market**: Utrecht, organic, 0 ad budget. Max 10 persone/classe in presenza.
**Target cohort 1 start**: 2026-07-05 (update `PROGRAM_START_DATE` in Render env)

---

## PHASE 1 – Foundation (W1–W2)
**Goal: live infrastructure + first 3 assessment completions**

### W1
| Task | Owner | Done when |
|------|-------|-----------|
| Deploy su Render.com (connect GitHub → auto-deploy) | Gabriele | `/api/health` returns 200 at `api.nl.centrocami.it` |
| Impostare tutti gli env vars nel Render dashboard | Gabriele | Checklist `.env.example` completata |
| Creare Stripe Payment Links (4 link) | Gabriele | URL pronti per tutti e 4 i prodotti |
| Inserire i 4 Stripe Payment Link URLs nelle CTA | Dev | Bottoni "Acquista" puntano a Stripe reali |
| Creare Google Business Profile Utrecht | Gabriele | Profilo live, categoria "Fitness instructor" |
| Setup email Resend.com (dominio verificato) | Gabriele | Email di test ricevuta da `info@centrocami.it` |

**Stripe Payment Links da creare:**
- CAMI Restore in presenza – 199 EUR (una tantum)
- CAMI Perform in presenza – 199 EUR (una tantum)
- CAMI Move – 9,90 EUR/mese (abbonamento ricorrente)
- CAMI Guide – 24,90 EUR/mese (abbonamento ricorrente, featured)
- CAMI Coach – 49,90 EUR/mese (abbonamento ricorrente)

**KPI W1**: sito live + 1 payment link funzionante + Google Business attivo

### W2
| Task | Owner | Done when |
|------|-------|-----------|
| Pubblicare 3 post su Google Business (IT/EN/NL) | Gabriele | Visibili nel profilo |
| Condividere landing page in 2 gruppi expat Utrecht (Facebook/Meetup) | Gabriele | Link condiviso in: Utrecht Expats, Italiani a Utrecht |
| Contattare 5 fisioterapisti/medici olandesi (referral outreach) | Gabriele | 5 email/DM inviati (template in `docs/sales-copy.md`) |
| Completare assessment di prova (auto-test) | Dev | Email di assessment ricevuta correttamente |
| Verificare webhook Stripe (test mode) | Dev | `stripe listen --forward-to` → email enrollment ricevuta |

**KPI W2**: 3+ assessment completati, 1+ contatto referral risposto

---

## PHASE 2 – First Traction (W3–W5)
**Goal: 5 iscrizioni classe + abbonamento mensile attivo**

### W3
| Task | Owner | Done when |
|------|-------|-----------|
| Follow-up cold outreach fisioterapisti (secondo contatto) | Gabriele | 2+ risposte positive / incontro programmato |
| Primo post LinkedIn (Gabriele personal brand) | Gabriele | Post publicato, min 20 reazioni |
| Condividere eBook Restore nel gruppo Utrecht Expats + Italiani a Utrecht | Gabriele | 10+ download/visualizzazioni tracciate via analytics |
| Aggiungere Google Analytics / Plausible al sito | Dev | Tracking eventi: assessment_start, assessment_complete, ebook_view |
| Creare QR code landing page (per materiale fisico Utrecht) | Gabriele | QR generato e testato |

**KPI W3**: 10+ visite/giorno, 2+ assessment completati in settimana

### W4
| Task | Owner | Done when |
|------|-------|-----------|
| Prima sessione info (online 30 min, Zoom) aperta agli interessati | Gabriele | Min 3 partecipanti |
| Offerta lancio "Early bird": 10% off prima classe (codice CAMI10) | Gabriele | Stripe coupon attivo, comunicato via email lista |
| Raccogliere 2 testimonianze da contatti personali (training pre-lancio) | Gabriele | 2 quote con foto aggiunte al sito |
| Aggiungere sezione testimonial reale (sostituisce placeholder) | Dev | Landing page aggiornata |

**KPI W4**: 2+ iscrizioni classe pagate (€199/cad)

### W5
| Task | Owner | Done when |
|------|-------|-----------|
| Confermare data e luogo classe Cohort 1 (min 4 iscrizioni = go) | Gabriele | Email di conferma inviata agli iscritti |
| Attivare email CAMIX post-assessment per tutti i lead in lista | Dev | Daily email automatica funzionante |
| Secondo post LinkedIn (case study anonimizzato) | Gabriele | Post pubblicato |
| Proposta partnership con 1 studio fisioterapia Utrecht | Gabriele | Meeting programmato |

**KPI W5**: 4+ iscrizioni classe, 1+ abbonamento mensile attivo

---

## PHASE 3 – First Cohort (W6–W8)
**Goal: Cohort 1 completata + recensioni + upsell**

### W6
| Task | Owner | Done when |
|------|-------|-----------|
| Raggiungere 10 iscrizioni oppure avviare con min 4 | Gabriele | Decision point: go/no-go entro W6 |
| Inviare email pre-programma (logistics + preparazione) | Gabriele | Ricevuta da tutti gli iscritti |
| Preparare schede personalizzate CAMIX per ogni partecipante | Gabriele | 1 scheda/persona pronta prima del Day 1 |
| Attivare OPENAI_API_KEY su Render (se non ancora fatto) | Dev | AI analysis attiva nelle email |

**KPI W6**: 4–10 partecipanti confermati, 0 cancellazioni last-minute

### W7 – Cohort 1 in esecuzione
| Task | Owner | Done when |
|------|-------|-----------|
| Day 1 classe in presenza | Gabriele | Completato |
| Day 2 classe in presenza | Gabriele | Completato |
| Day 3 classe in presenza | Gabriele | Completato |
| Raccogliere feedback scritto dopo Day 3 (form Google/Typeform) | Gabriele | Min 80% partecipanti compilano |
| Offrire accesso gratuito 30gg Guide plan a tutti i partecipanti | Dev/Gabriele | Codice inviato via email enrollment |

**KPI W7**: NPS ≥ 8/10, 0 richieste di rimborso

### W8 – Post-cohort & upsell
| Task | Owner | Done when |
|------|-------|-----------|
| Email upsell CAMI Monthly (template `docs/sales-copy.md`) | Gabriele | Inviata a tutti i partecipanti D+2 |
| Raccogliere 3+ recensioni Google Business | Gabriele | Recensioni pubblicate e visibili |
| Aggiornare landing page con testimonianze reali della Cohort 1 | Dev | Live sul sito |
| Aprire iscrizioni Cohort 2 (date: +6 settimane) | Gabriele | Pagina /assessment con nuove date |
| Report Cohort 1: conversione assessment→iscrizione, NPS, revenue | Gabriele | Doc in `docs/cohort-1-report.md` |

**KPI W8**: 2+ upsell mensili attivi, 3+ recensioni ≥ 4★

---

## PHASE 4 – Scale & Referral (W9–W12)
**Goal: pipeline costante, 2 classi/mese, abbonamenti ricorrenti**

### W9
| Task | Owner | Done when |
|------|-------|-----------|
| Attivare referral informale: ogni partecipante Cohort 1 porta 1 amico (sconto €20) | Gabriele | Comunicato via email, codice CAMIREFERRAL attivo su Stripe |
| Meeting con studio fisioterapia partner | Gabriele | Accordo referral definito (commissione o baratto) |
| Aumentare frequenza posting LinkedIn (2x/settimana) | Gabriele | Calendario editoriale 4 settimane scritto |
| Review analytics sito: pagine più visitate, drop-off assessment | Dev | Report condiviso, 2+ A/B test pianificati |

**KPI W9**: 8+ assessment/settimana, 5+ abbonamenti mensili attivi

### W10
| Task | Owner | Done when |
|------|-------|-----------|
| Cohort 2 go/no-go decision (min 4 iscrizioni) | Gabriele | Decision confermata |
| Creare video testimonial 60 sec (smartphone, Gabriele + 1 cliente) | Gabriele | Video su LinkedIn + embedding landing page |
| Automatizzare report settimanale admin (clienti attivi, revenue, NPS) | Dev | Dashboard admin mostra KPI settimanali |
| Valutare espansione: 2a location Utrecht o online stream | Gabriele | Nota strategica scritta |

**KPI W10**: 10 iscrizioni Cohort 2 + 8+ abbonamenti attivi

### W11
| Task | Owner | Done when |
|------|-------|-----------|
| Cohort 2 in esecuzione | Gabriele | Day 1–3 completati |
| Aggiungere terzo eBook (in lingua NL, targeting olandesi) | Dev | `/ebooks/nl-bewegen-na-50` live |
| Setup Google Ads test budget €5/gg (solo se organico funziona) | Gabriele | Prima campagna attiva (decision gate: >€500 MRR abbonamenti) |

**KPI W11**: MRR abbonamenti ≥ €250

### W12 – Review trimestrale
| Task | Owner | Done when |
|------|-------|-----------|
| Retrospettiva W1–W12: revenue, clienti, NPS, conversion rates | Gabriele + Dev | Report in `docs/q2-2026-review.md` |
| Aggiornare prezzi se mercato lo regge (eventuale +€20 in presenza) | Gabriele | Decision documentata |
| Pianificare W13–W24 (Cohort 3–4, scaling, Stripe webhooks automation) | Gabriele + Dev | Piano scritto |

**KPI W12**: ≥ 2 classi completate, MRR ≥ €500, NPS medio ≥ 8/10

---

## KPI Dashboard – Numeri Target

| Metrica | W4 | W8 | W12 |
|---------|----|----|-----|
| Assessment completati (totale) | 10 | 35 | 80 |
| Iscrizioni classe pagate | 2 | 12 | 25 |
| Abbonamenti mensili attivi | 0 | 4 | 12 |
| Revenue totale (EUR) | 400 | 2.800 | 7.200 |
| Recensioni Google ≥ 4★ | 0 | 3 | 8 |
| NPS medio | – | ≥ 8 | ≥ 8.5 |

*Revenue calcolata: classe €199 × n + mix abbonamenti*

---

## Decision Gates

| Gate | Condizione GO | Condizione NO-GO |
|------|--------------|-----------------|
| **Cohort 1 start** (W6) | ≥ 4 iscrizioni pagate | < 4 → posticipare di 2 settimane |
| **Cohort 2 start** (W10) | ≥ 4 iscrizioni + ≥ 1 referral partner | < 4 → solo Monthly fino a trazione |
| **Stripe Webhooks automation** | > 20 transazioni/mese | < 20 → rimani su Payment Links manuali |
| **Google Ads** | MRR abbonamenti > €500 | < €500 → solo organico |
| **Seconda location / online** | Waitlist > 10 persone | Nessuna waitlist → concentrati sull'esistente |

---

## Restart Flask (dev / Termux)
```bash
fuser -k 5000/tcp && cd ~/cami-netherlands/backend && nohup python app.py > ~/cami_flask.log 2>&1 &
```

## Deploy checklist Render
1. Push su `main` → auto-deploy attivo
2. Env vars da settare manualmente nel dashboard Render:
   - `RESEND_API_KEY` (Resend.com → API Keys)
   - `ADMIN_PASSWORD` (scegli password forte)
   - `STRIPE_SECRET_KEY` (Stripe → Developers → API Keys → Secret)
   - `STRIPE_WEBHOOK_SECRET` (Stripe → Developers → Webhooks → Signing secret)
   - `OPENAI_API_KEY` (OpenAI → API Keys)
   - `PROGRAM_START_DATE` (data prima classe, es. `2026-07-05`)
3. Verificare `/api/health` → `{"status":"ok"}`
4. Inviare assessment di test → ricevere email
5. Fare pagamento test (Stripe test mode) → ricevere email enrollment
