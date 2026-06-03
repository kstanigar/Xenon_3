# Current Project Priorities

**Updated:** June 3, 2026
**Phase:** 7/7 Complete (100%) ✅

---

## Immediate Priorities (Complete These First)

### 1. ✅ Adaptive AI Difficulty - COMPLETE
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