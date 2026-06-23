# Current Project Priorities

**Updated:** June 15, 2026 (evening)
**Phase:** 7/7 Complete (100%) ✅

---

## ✅ Security Audit — COMPLETE (June 13–15, 2026)

**Status:** ✅ All 4 phases complete (18 findings resolved)
**Plan:** SECURITY_AUDIT_PLAN.md — full details

| Phase | Items | Status |
|---|---|---|
| Phase 1 — Critical | 3 tasks | ✅ Complete |
| Phase 2 — High Priority | 6 tasks | ✅ Complete |
| Phase 3 — Medium Priority | 7 tasks | ✅ Complete |
| Phase 4 — Low Priority / Polish | 7 tasks | ✅ Complete |

**Phase 4 final status (June 15, 2026):**
- ✅ 4A — sync_paim.sh: env vars + .gitignore (PR #141)
- ✅ 4B — SRI: N/A (no eligible scripts, mitigated by CSP)
- ✅ 4C — HTTPS: Redirect HTTP to HTTPS — prod + dev verified
- ✅ 4D — TLS: prod TLSv1.3_2025 / dev TLSv1.2_2021 — both ✅
- ✅ 4E — Access logging: N/A (Pro plan required, mitigated by CSP + App Check)
- ✅ 4F — CSP enforcement: complete, zero violations
- ✅ 4G — GA4 final_score: code + DebugView verified (⏳ dashboard ~June 16–17)

**🟡 In progress — App Check enforcement + Firestore hardening (see HANDOFF_SUMMARY.md for full plan):**
- ✅ Task 1: Firestore security rules tightened (June 23) — `request.app.token.valid == true` on create + update; bot writes now blocked at rules level
- ⏳ Task 2: App Check enforcement (Firebase Console → App Check → Cloud Firestore → Enforce) — PENDING; do not enforce until verified % reaches ~90% and outdated % drops to ~0%. Re-check ~July 6–7.
- ⏳ Task 3: Update leaderboard error message in game.html + game_mobile.html (code change — pending enforcement)

**⚠️ Two time-gated items remain:**
- **App Check enforcement** — NOT ready. Do NOT enforce until verified % reaches ~90%+ and outdated % drops to ~0%. Last check June 23: 33% verified / 61% invalid / 7% outdated (46 requests). June 22 check: 57% verified / 31% invalid / 12% outdated (503 requests). Outdated trending down (12% → 7%) — cache-control fix (PR #149) working. Enforcement is a full block including reads — real users on outdated clients would lose leaderboard access. Task 1 complete (June 23): Firestore rules now block bot writes at rules level via `request.app.token.valid == true`. Re-check metrics ~July 6–7. See HANDOFF_SUMMARY.md for full details.
- **GA4 dashboard chart** — check GA4 Explore for `final_score` data, then build Final Score × New Tier chart. See docs/GA4_FINAL_SCORE_IMPLEMENTATION.md.

---

## ✅ Legal Pages — Complete (June 15, 2026)

- `privacy.html` — 13 sections; TDPSA + COPPA + GDPR compliant; full analytics pipeline disclosed (GA4 → BigQuery → AWS Lambda → public dashboard); 13+ age disclosure; Texas governing law
- `terms.html` — 15 sections; analytics toggle documented; public dashboard consent disclosed; Ko-fi, AWS, Firebase, BigQuery third-party terms linked; Texas governing law
- `contact.html` — standalone contact form (name/email/reason/message); FormSubmit AJAX; in-place confirmation; matches NON-X dark theme
- `index.html` — Privacy, Terms, Contact links in consent banner and footer (centered, wraps correctly on mobile)
- ⚠️ Contact email placeholder — add Standing Tiger business email to privacy.html + terms.html once created
- Research: `docs/LEGAL_PAGES_PLAN.md`

---

## ✅ Standing Tiger Favicon (Item 6) — Complete (June 15, 2026)

- `favicon_st.png` (new asset) cropped to 768×768, resized to 32×32 + 180×180 via Python script (`scripts/make_favicon.py`)
- `favicon-32x32.png` + `apple-touch-icon.png` generated with dark background
- `<link rel="icon">` + `<link rel="apple-touch-icon">` added to all 3 HTML files (index.html, game.html, game_mobile.html)
- Open Graph + Twitter card meta tags added to `index.html` (OG image: `favicon_st.png`)
- Standing Tiger footer credit added below Play button on `index.html`

---

## ✅ FIXED: 120fps Game Loop (June 15, 2026)

**Status:** Fixed — PR #137 merged to dev
**Severity:** HIGH — broke core gameplay on 120Hz monitors
**Fix:** `performance.now()` timestamp-based 60fps cap in `draw()` — rAF fires at display rate, frames skipped until 16.67ms elapsed. Applied to game.html + game_mobile.html.

**Also fixed:** Spacebar blocked in survey/comments textarea — `if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;` added at top of keydown handler in game.html (line 7301) + game_mobile.html (line 7843). PR #139 merged to dev June 15, 2026.

---

## 🐯 Standing Tiger Branding (Favicon + Studio Identity)

**Asset:** `st_favicon.png` — 1024×1024 RGBA PNG, transparent background, circular badge
**Brand:** Standing Tiger Engineering & Development
**Philosophy:** Logo stays subconscious — game titles and features shine; ST brand builds recognition passively

**Implementation plan (subtlest → most visible):**
1. **Browser tab favicon** — resize to 32×32 + 180×180 (Apple touch); add `<link rel="icon">` to all 3 HTML files
2. **Open Graph meta tags** — `og:image` uses logo; shows when URL shared on Discord/social. Invisible to players
3. **HTML footer on index.html** — small `© Standing Tiger Engineering & Development` below play button
4. **Game scorecard corner watermark** — tiny ST logo watermark bottom-right of end-screen scorecard
5. **PWA app manifest** — logo as app icon if player installs to home screen

**Format note:** Source file (1024×1024) is perfect to keep. Need to generate:
- `favicon-32x32.png` — browser tab
- `apple-touch-icon.png` (180×180) — iOS home screen
- `favicon.ico` — legacy fallback (optional)

**Status:** Asset ready, implementation pending (not part of current security audit)

---

## Completed Priorities

### ✅ Adaptive AI Difficulty - COMPLETE
**Status:** Fully implemented and deployed on main branch
**Verified:** June 1, 2026 via Haiku agent audit
**Features Working:**
- Tier-based difficulty system (Tiers -3 to +3)
- Dynamic adjustments based on player deaths
- Cycle completion increases difficulty
- Speed ratchet prevents exploitation
- Score multipliers prevent low-tier dominance

---

### 2. ✅ Phase 7: AWS Deployment Testing & Verification - COMPLETE

**Status:** ✅ COMPLETE (June 3, 2026)

**Completed Tasks:**
- [x] Priority 1: Dev environment testing (June 2, 2026)
  - Firebase/leaderboard tested
  - GA4 tracking verified
  - Desktop & mobile game tested
- [x] Priority 2: Production security update (June 3, 2026)
  - CloudFront migrated to S3 bucket endpoint with OAC
  - Production S3 bucket secured (Block Public Access + OAC policy)
  - Versioning enabled
  - Tags added
  - Production site tested and verified working
- [ ] Priority 3: Firebase spam prevention (deferred to separate phase)

**Total Time:** ~50 minutes (actual)

---

### 3. 🔴 Security Audit (HIGH PRIORITY)

**Status:** Not Started

**Scope:**
- [ ] Review all user input sanitization
- [ ] Check Firebase database spam protection
- [ ] Test console-based Firebase abuse scenarios
- [ ] Verify no SQL injection vectors
- [ ] Check for XSS vulnerabilities
- [ ] Review CORS policies
- [ ] Audit Ko-fi button security
- [ ] Test leaderboard submission rate limiting

**Why Critical:** Zero vulnerabilities before production deployment

**Estimated Time:** 2-3 sessions

---

### 4. 🎯 Pink Infinite Level (ABSOLUTE MUST)

**Status:** Planned

**Requirements:**
- [ ] Infinite scrolling background
- [ ] Pink color theme variants
- [ ] Updated enemy spawn patterns for infinite mode
- [ ] SystemOverload.mp3 music (already in repo)
- [ ] Leaderboard integration for infinite mode
- [ ] UI entry point (main menu or level select)

**Music Asset:** ✅ SystemOverload.mp3 (3.2 MB) - ready for use

**Priority Ranking:** #1 feature after Phase 7 + Security Audit

**Estimated Time:** 3-4 sessions

---

## Secondary Priorities (After Above Complete)

### 5. 📊 GA4 Analytics Investigation

**Status:** Research Needed

**Objective:** Verify complete data flow from code → AWS → GA4 → NONX_analytics dashboard

**Analytics Data Flow Verification:**
- [ ] Audit all data tags in codebase (game.html, game_mobile.html, index.html)
- [ ] Document all tracking events and their parameters
- [ ] Track data tags through AWS CloudFront logs
- [ ] Verify tags hitting GA4 (check GA4 DebugView and Realtime reports)
- [ ] Confirm API calls reaching NONX_analytics dashboard
- [ ] Verify data consistency across entire pipeline
- [ ] Test event tracking for all game actions (start, level complete, game over, etc.)
- [ ] Validate custom dimensions and metrics

**Investigation Areas:**
- [ ] Why some data tags may not be hitting GA4
- [ ] NON-X analytics API setup and configuration
- [ ] Event tracking verification
- [ ] Real-time data flow testing
- [ ] Dashboard configuration and data display

**Deliverables:**
- [ ] Complete data tag inventory (all events tracked)
- [ ] Data flow diagram (code → AWS → GA4 → dashboard)
- [ ] Identified gaps or broken connections
- [ ] Fix recommendations

**Estimated Time:** 1-2 sessions

---

### 6. 🎨 Hero Ship Color Purchase (NEW FEATURE)

**Status:** Designed (docs/design/HERO_SHIP_COLOR_PURCHASE.md)

**Replaces:** Music Selector feature (marked irrelevant)

**Concept:**
- In-game purchase for hero ship colors
- Shield color matches ship color (purple hero = purple shield)
- Current: blue hero + blue shield
- Planned: 5-7 color options

**Requirements:**
- [ ] Design color palette
- [ ] Create hero ship .webp assets for each color
- [ ] Build color selection UI
- [ ] Integrate Ko-fi/payment system
- [ ] Test shield color rendering
- [ ] localStorage persistence

**Priority:** After Pink Infinite Level

**Estimated Time:** 2-3 sessions (including asset creation)

---

### 7. ⚡ Performance Optimization

**Status:** Needed Eventually

**Scope:**
- [ ] Reduce dev mode logging overhead
- [ ] Optimize canvas rendering
- [ ] Review bullet/enemy object pooling
- [ ] Profile frame rate on lower-end devices
- [ ] Minimize garbage collection pauses

**Branch:** `perf/dev-mode-logging` (may exist)

**Priority:** Low (game runs well currently)

**Estimated Time:** 1-2 sessions

---

## Archived / Irrelevant

### ❌ Music Selector Feature
**Status:** Cancelled/Irrelevant
**Reason:** Replaced by Hero Ship Color Purchase feature
**Previous Plan:** Let players choose background music from 6 tracks

---

## Feature Completion Status

| Feature | Status | Priority | Notes |
|---------|--------|----------|-------|
| Adaptive AI Difficulty | ✅ Complete | N/A | Deployed on main |
| Auto-Deploy (dev/main) | ✅ Complete | N/A | Phase 6 done |
| Phase 7 Testing | ✅ Complete | N/A | Completed June 3, 2026 |
| Production Security | ✅ Complete | N/A | CloudFront OAC migration done |
| Security Audit | ⏳ Not Started | HIGH | Before new features |
| Pink Infinite Level | ⏳ Planned | ABSOLUTE MUST | #1 feature |
| Firebase Spam Prevention | ⏳ Not Started | HIGH | Priority 3 from Phase 7 |
| GA4 Analytics Fix | ⏳ Research Needed | MEDIUM | Investigate issues |
| Hero Ship Colors | ⏳ Designed | MEDIUM | After Pink level |
| Performance Optimization | ⏳ Eventually | LOW | Game runs well |
| Music Selector | ❌ Cancelled | N/A | Replaced by ship colors |
| Favicon Creation | ⏳ Optional | LOW | Eliminate 403 error |

---

## Next Session Actions

**Immediate (if continuing tonight):**
1. Finish Phase 7 remaining tasks (30-45 min)
2. Deploy to production

**Next Session (if starting fresh):**
1. Security audit (2-3 sessions)
2. Pink Infinite Level implementation (3-4 sessions)
3. GA4 analytics investigation

---

**Last Updated:** June 3, 2026
**Current Phase:** 7/7 Complete (100%) ✅
**Critical Path:** Security Audit → Firebase Spam Prevention → Pink Infinite Level