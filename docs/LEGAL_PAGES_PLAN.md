# Legal Pages Implementation Plan — NON-X

**Created:** June 15, 2026
**Company:** Standing Tiger Engineering & Development (Texas, USA)
**Haiku Agent Research:** Completed June 15, 2026

---

## Overview

Two legal HTML pages needed:
1. `/privacy.html` — Privacy Policy (linked from existing cookie consent banner)
2. `/terms.html` — Terms and Conditions

Both pages must comply with: **TDPSA** (Texas), **COPPA** (US federal), and **GDPR** (EU users).

---

## Haiku Agent Research Findings

### Key Legal Frameworks That Apply

| Law | Applies? | Why |
|---|---|---|
| **TDPSA** (Texas Data Privacy and Security Act) | ✅ YES | Company is Texas-based; collects TX resident data; NO revenue threshold exemption |
| **COPPA** | ✅ YES (decision needed) | NON-X may be directed at children under 13 (space shooter genre) |
| **GDPR** | ✅ YES (if EU users can access) | Applies regardless of US location if EU residents play |
| **CCPA** | ❌ No | Requires $25M+ revenue or 100k+ CA consumers — NON-X doesn't qualify |

**TDPSA effective date:** July 1, 2024 (full enforcement January 2025) — applies NOW

**COPPA 2026 update:** New stricter rules effective April 22, 2026 — parental consent methods, product design safeguards, data minimization for children

### Texas (TDPSA) — Key Differences

- **No revenue or data volume threshold** — applies to all businesses processing Texas resident data
- Requires affirmative opt-in for sensitive data
- Consumers have: access, delete, opt-out, correction rights
- TDPSA defers to COPPA for children's data

### reCAPTCHA v3 — 2026 Change (Critical)

As of April 2, 2026: **Standing Tiger is the data controller; Google is the processor** for reCAPTCHA v3.
This means privacy policy must explicitly disclose reCAPTCHA data collection and processing.

### COPPA Decision Required Before Implementation

Space shooter genre commonly attracts under-13 players. Decision tree:

- **If NON-X is directed at children / no age restriction:**
  - Add age gate at entry ("You must be 13+ to play")
  - Implement verifiable parental consent before collecting display name
  - Restrict GA4 behavioral tracking for under-13 users

- **If NON-X is 13+ only:**
  - State in T&C: "You must be 13 or older to play"
  - State in Privacy Policy: "We do not knowingly collect data from children under 13"
  - No parental consent mechanism required

**Recommended approach:** 13+ age restriction (no age gate needed — just disclosures)

---

## Data Collected by NON-X

| Data Type | Purpose | Third Party | Consent Required |
|---|---|---|---|
| Player display name | Leaderboard display | Firebase/Firestore | By playing (implied) |
| Score | Leaderboard ranking | Firebase/Firestore | By playing (implied) |
| IP address / device identifiers | Analytics | Google Analytics 4 | ✅ Cookie consent |
| reCAPTCHA risk signals | Bot detection / App Check | Google | Disclosed in policy |
| Firestore DB IDs + timestamps | Leaderboard operation | Google Cloud | By playing (implied) |
| Cookie preferences | Consent tracking | localStorage | Self-referential |
| Ko-fi click data | Donation tracking | Ko-fi | Ko-fi's own policy |

---

## Privacy Policy — Required Sections

1. **Data We Collect** — display name, score, analytics data, reCAPTCHA signals, cookies
2. **How We Use Your Data** — leaderboard, analytics, bot prevention, game improvement
3. **Third-Party Services** (each with link to their privacy policy):
   - Google Analytics 4 — behavioral tracking (with cookie consent)
   - Firebase / Firestore — leaderboard data storage (Google Cloud)
   - Firebase App Check + reCAPTCHA v3 — bot detection (Standing Tiger is controller)
   - Ko-fi — donation button (Ko-fi handles payments independently)
4. **Cookies and Tracking**
   - GA4 cookies: only enabled after user accepts consent banner
   - How to decline: use the consent banner
5. **Leaderboard Data is Public** — display name + score visible to all players
6. **Data Retention** — leaderboard data kept indefinitely until deletion request; GA4 default 14 months
7. **Your Rights (TDPSA + GDPR)**
   - Access your data
   - Request deletion
   - Opt-out of tracking (use cookie banner)
   - Correct inaccurate data
   - Response time: 30 days
8. **Children's Privacy (COPPA)** — "This game is intended for users 13+. We do not knowingly collect data from children under 13. If you believe we have collected data from a child, contact us for deletion."
9. **Data Security** — reasonable security safeguards; Firebase security standards
10. **Contact Information** — Standing Tiger Engineering & Development, Texas
11. **Policy Updates** — how/when we notify users of changes
12. **Governing Law** — State of Texas

---

## Terms and Conditions — Required Sections

1. **Acceptance of Terms** — by playing you agree to these terms; right to modify with notice
2. **Age Requirement** — 13+ only; by playing you confirm you are 13 or older
3. **Intellectual Property** — all game code, assets, and art owned by Standing Tiger E&D
4. **User Conduct**
   - No cheating, hacking, or exploits
   - No offensive display names
   - No automated bots (other than reCAPTCHA-verified requests)
5. **Leaderboard Rules**
   - Display name + score are publicly visible
   - Standing Tiger may reset leaderboard for maintenance or to remove cheated scores
   - Standing Tiger may remove any entry without notice
6. **Donations via Ko-fi**
   - Ko-fi handles all payment processing (link to Ko-fi Terms)
   - Donations are voluntary; no in-game advantage guaranteed
   - Refund requests handled by Ko-fi, not Standing Tiger
7. **Third-Party Services** — Firebase, Google Analytics, reCAPTCHA, Ko-fi are independent; Standing Tiger not liable for their outages
8. **Disclaimer of Warranties** — game provided "as-is"; no guarantee of uninterrupted service
9. **Limitation of Liability** — Standing Tiger not liable for data loss, leaderboard resets, or game discontinuation
10. **Indemnification** — users agree to indemnify Standing Tiger for T&C violations
11. **Game Discontinuation** — Standing Tiger may shut down at any time; no compensation owed
12. **Dispute Resolution** — Governing law: State of Texas; informal resolution first
13. **Severability** — invalid provisions do not void the rest

---

## Cookie Consent — GA4 Disclosure Language (2026 Best Practice)

```
This site uses Google Analytics 4 to understand how users interact 
with the game. Analytics cookies track session duration, pages visited, 
and user interactions. You can accept or decline analytics tracking 
using the banner above. Declining will prevent GA4 tracking.
```

This language already matches what was implemented in Phase 3 (Finding 5).

---

## Implementation Plan

### Task List

- [ ] **Task 1** — Create `/privacy.html`
  - Styled to match NON-X dark theme (dark navy background, cyan/white text)
  - All 12 sections from Privacy Policy plan above
  - Link back to main game (`index.html`)
  - Standing Tiger footer credit

- [ ] **Task 2** — Create `/terms.html`
  - Same dark theme styling
  - All 13 sections from T&C plan above
  - Link back to main game
  - Standing Tiger footer credit

- [ ] **Task 3** — Update consent banner in `index.html`
  - Verify `/privacy.html` link points correctly (already coded as `/privacy.html`)
  - Add `/terms.html` link to consent banner or footer

- [ ] **Task 4** — Add footer links to `index.html`
  - Add "Privacy Policy | Terms of Use" links below Standing Tiger footer credit

- [ ] **Task 5** — Deploy via PR
  - Branch: `feat/legal-pages`
  - Base: dev

### Files to Create/Modify

| Action | File | Notes |
|---|---|---|
| CREATE | `/privacy.html` | New file |
| CREATE | `/terms.html` | New file |
| MODIFY | `/index.html` | Add T&C link to footer/banner |

### Styling Notes

- Background: `#0a0a1a` (matches NON-X dark theme)
- Text: `rgba(255,255,255,0.85)` for body; `#00ffff` for headings
- Font: same as index.html (system sans-serif stack)
- Max-width: 800px centered
- Mobile responsive
- Back link to NON-X at top

---

## Sources (Haiku Agent Research)

- TDPSA: feroot.com, cside.com, ketch.com, osano.com, practicallaw.thomsonreuters.com
- COPPA 2026: flexyconsent.com, gamesbeat.com, usercentrics.com, ftc.gov
- GA4 / Firebase Privacy: iubenda.com, freeprivacypolicy.com, termly.io
- reCAPTCHA 2026: capmonster.cloud, usercentrics.com, consentmo.com
- GDPR: raidboxes.io, cleverroad.com, kiteworks.com, european-commission.europa.eu

---

## Status

| Task | Status |
|---|---|
| Haiku agent research | ✅ Complete |
| Plan documented | ✅ Complete |
| `/privacy.html` created | ✅ Complete |
| `/terms.html` created | ✅ Complete |
| `index.html` updated | ✅ Complete |
| PR merged to dev | ⏳ Pending |

**Last Updated:** June 15, 2026
