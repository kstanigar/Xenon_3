# Current Project Priorities

**Updated:** June 1, 2026
**Phase:** 6/7 Complete (86%), Phase 7 in progress

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

### 2. ⏳ Phase 7: AWS Deployment Testing & Verification (CRITICAL)

**Status:** In Progress (music fix complete, remaining items below)

**Remaining Tasks:**
- [ ] Test Firebase/leaderboard with ad blockers disabled
- [ ] Verify production CloudFront Default Root Object = `index.html`
- [ ] Update production S3 bucket security (Block Public Access + OAC)
- [ ] Enable versioning on production bucket
- [ ] Full game functionality testing on dev site
- [ ] Deploy to production (dev → main merge)

**Why Critical:** Must complete before working on new features

**Estimated Time:** 30-45 minutes

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

**Issues to Investigate:**
- [ ] Why data tags may not be hitting GA4
- [ ] NON-X analytics API setup and configuration
- [ ] Event tracking verification
- [ ] Real-time data flow testing
- [ ] Dashboard configuration

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
| Phase 7 Testing | ⏳ In Progress | CRITICAL | 30-45 min remaining |
| Security Audit | ⏳ Not Started | HIGH | Before production |
| Pink Infinite Level | ⏳ Planned | ABSOLUTE MUST | #1 feature |
| GA4 Analytics Fix | ⏳ Research Needed | MEDIUM | Investigate issues |
| Hero Ship Colors | ⏳ Designed | MEDIUM | After Pink level |
| Performance Optimization | ⏳ Eventually | LOW | Game runs well |
| Music Selector | ❌ Cancelled | N/A | Replaced by ship colors |

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

**Last Updated:** June 1, 2026
**Current Phase:** 6/7 Complete (86%)
**Critical Path:** Phase 7 → Security Audit → Pink Infinite Level