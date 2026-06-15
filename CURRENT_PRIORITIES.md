# Current Project Priorities

**Updated:** June 15, 2026
**Phase:** 7/7 Complete (100%) ✅

---

## 🔴 CURRENT PRIORITY: Security Audit (Started June 13, 2026)

**Status:** In Progress
**Plan:** SECURITY_AUDIT_PLAN.md — 18 findings, 4 phases
**Critical Path:** Phase 1 (Firestore rules) → Phase 2 (API key, XSS, CSP, headers) → Phase 3 (consent, email, localStorage) → Phase 4 (polish)

| Phase | Items | Status |
|---|---|---|
| Phase 1 — Critical | 3 tasks | ✅ Complete |
| Phase 2 — High Priority | 6 tasks | ✅ Complete |
| Phase 3 — Medium Priority | 7 tasks | ✅ Complete |
| Phase 4 — Low Priority / Polish | 6 tasks | ⏳ In Progress (4F complete, remaining: SRI, HTTPS, TLS, sync_paim.sh) |

**Completed (June 13–14, 2026):**
- ✅ Finding 1 — Firestore security rules
- ✅ Finding 2 — Firebase API key restricted
- ✅ Finding 3 — XSS innerHTML fixed in game.html + game_mobile.html (PR #123)
- ✅ Finding 3 — XSS innerHTML fixed in index.html (PR merged June 14)
- ✅ Finding 6 — CloudFront security headers
- ✅ Finding 8 — Dev/god URL params gated to non-production (merged June 14)
- ✅ Finding 16 — Firebase App Check SDK integrated (PR #124)
- ✅ Finding 18 — Shift+D/Shift+A keyboard shortcuts gated to non-production (merged June 14)
- ✅ Finding 5 — GA4 Consent Mode v2 — consent banner + default deny on all 3 pages (PR #130, June 14)
- ✅ Finding 7 — FormSubmit email hash — replaced plaintext email with hash endpoint in game.html + game_mobile.html (PR #131, June 14)
- ✅ Finding 9 — Score from memory confirmed — in-memory `score` variable used at Firebase submission, localStorage only used as re-submission guard (no code change needed, June 14)
- ✅ Finding 10 — Production-safe logger — `logger` object added to all 3 files, 14 console.error/warn calls replaced (PR merged June 14)
- ✅ Finding 14 — HTML-encode savedHandle — `escapeAttr()` added to game.html + game_mobile.html, all 4 attribute injections wrapped (PR merged June 14)
- ✅ Finding 13 — Ko-fi onclick refactor — `buildKofiButton()` returns DOM element, event listeners attached via addEventListener, rel=noopener noreferrer added (PR #134, June 14)
- ✅ Finding 4 — CSP header — CloudFront Function `add-csp-header` deployed in enforcement mode (June 15). reCAPTCHA domains added, zero violations verified on prod, switched to `content-security-policy` enforcement.

**⚠️ App Check enforcement pending:** Do NOT enforce until verified % ≥ 85%. Last check 6:25 PM June 14: 61% verified / 21% outdated / 18% invalid (89+31+26 = 146 total). Previously 67% at 2:17 PM — slight drop, possibly more invalid requests appearing. Re-check June 15 ~5 AM. See DEV_ERRORS_LOG.md for full research.

**Phase 4 next priorities:**

**1. ✅ Task 4F — Fix reCAPTCHA CSP violations + switch to enforcement — Complete (June 15, 2026)**

**2. GA4 final_score custom dimension**
- Add `final_score` as event param on `player_won` event in game.html + game_mobile.html
- Register as GA4 custom dimension in GA4 console
- Unblocks NON-X Analytics dashboard: replace placeholder chart with `customEvent:final_score` × `customEvent:new_tier` scatter/bar
- No BigQuery needed — standard Lambda query once dim is registered. Cost: $0
- Estimate: 1–2 hours once game change ships

**3. App Check enforcement**
- Re-check June 15 ~5 AM. Enforce ONLY when verified % ≥ 85% (last check 6:25 PM June 14: 61%)

**4. Phase 4 polish** — SRI hashes, HTTPS verification, TLS policy, sync_paim.sh paths

**Reference:** See SECURITY_AUDIT_PLAN.md for full task list with step-by-step instructions per finding.

---

## 🟡 NEW BUG: 120fps Game Loop (Discovered June 15, 2026)

**Status:** Open — must fix before launch
**Severity:** HIGH — breaks core gameplay on 120Hz monitors
**Files:** game.html (game_mobile.html likely same issue)

**Problem:** Game loop uses uncapped `requestAnimationFrame` with zero delta-time compensation. On 120Hz monitors the game runs at 120fps — all frame-dependent mechanics run 2× faster than intended.

**Impact at 120fps vs 60fps:**
- Player, bullet, enemy speeds: 2× faster
- Enemy spawn rate: 2× more frequent
- Invincibility duration: halved (1s instead of 2s)
- Shield flash visual: imperceptible (~25ms)

**Key lines (game.html):**
- Game loop: 7712–7739 (uncapped `requestAnimationFrame`)
- Invincibility timer: 6962, 7018 (hardcoded 120 frames)
- Player speed: CONFIG ~line 788–801
- Enemy speed: 4141, 4155, 4167, 8033

**Fix options:**
1. **FPS cap (simple):** Replace `requestAnimationFrame(draw)` with `setTimeout(() => requestAnimationFrame(draw), 1000/60)` — forces 60fps cap
2. **Delta-time (proper):** Multiply all px/frame values by `deltaTime / (1000/60)` — frame-rate independent

**Recommendation:** FPS cap is low-risk, 1-line fix. Delta-time requires touching every movement calculation. Fix FPS cap first, delta-time as follow-up if needed.

**Also found:** Spacebar blocked in survey/comments textarea — global keydown handler (line ~7574) missing `if (e.target.tagName === 'TEXTAREA') return;` guard. Affects `surveyComments` (line 6101), `bugDescription` + `bugSteps` (lines 6363, 6367). Both game.html + game_mobile.html need the fix.

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