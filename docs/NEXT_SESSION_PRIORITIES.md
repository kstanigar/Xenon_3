# Next Session Priorities

**Updated:** June 3, 2026
**Phase 7:** ✅ COMPLETE (100%)
**Next Focus:** Security Audit & Feature Development

## File Maintenance
When items complete: Mark `[x]` and add date. When file exceeds 150 lines of completed items, archive to `COMPLETED_PRIORITIES_ARCHIVE.md`.

---

## 🎉 Phase 7 Complete!

**All deployment and infrastructure work finished:**
- ✅ Dev environment tested (June 2, 2026)
- ✅ Production CloudFront migrated to OAC (June 3, 2026)
- ✅ Production S3 bucket secured (June 3, 2026)
- ✅ Both environments verified working

---

## 🎯 Priority 1: Security Audit (HIGH - 2-3 sessions)

**Objective:** Ensure zero vulnerabilities before new feature development

### Audit Checklist

**1. Input Sanitization**
- [ ] Review all user input fields
- [ ] Verify leaderboard name input sanitization
- [ ] Check for XSS vulnerabilities in displayed content
- [ ] Test special characters in all input fields

**2. Firebase Security**
- [ ] Review Firestore security rules
- [ ] Test unauthorized access attempts
- [ ] Verify read/write permissions
- [ ] Check for data exposure risks

**3. Console-Based Abuse**
- [ ] Test console-based Firebase manipulation
- [ ] Verify API endpoint protection
- [ ] Check for client-side validation bypasses
- [ ] Test leaderboard spam scenarios

**4. Additional Checks**
- [ ] Verify no SQL injection vectors (Firebase uses NoSQL, but check)
- [ ] Review CORS policies
- [ ] Audit Ko-fi button security
- [ ] Check for mixed content issues
- [ ] Verify HTTPS enforcement

**Documentation:** Create SECURITY_AUDIT_RESULTS.md with findings

---

## 🎯 Priority 2: Firebase Spam Prevention (HIGH - 1-2 sessions)

**Objective:** Implement device-based rate limiting for leaderboard

### Implementation Checklist

**1. Research Phase**
- [ ] Research browser fingerprinting options
- [ ] Evaluate localStorage device tracking
- [ ] Review Firestore security rules for rate limiting
- [ ] Investigate Cloud Functions for server-side rate limiting

**2. Implementation Phase**
- [ ] Implement device ID tracking
- [ ] Update Firestore security rules to enforce 1 entry per device
- [ ] Add client-side validation
- [ ] Create admin bypass mechanism (for testing)

**3. Testing Phase**
- [ ] Test spam scenarios (multiple submissions from same device)
- [ ] Verify legitimate users not blocked
- [ ] Test across different browsers
- [ ] Test incognito/private browsing behavior

**Documentation:** Update FIRESTORE_SECURITY_RULES.md

---

## 🎯 Priority 3: Pink Infinite Level (ABSOLUTE MUST - 3-4 sessions)

**Objective:** Implement the #1 requested feature

### Planning Checklist

**1. Design Phase**
- [ ] Review existing design doc: HERO_SHIP_COLOR_PURCHASE.md (if exists)
- [ ] Define infinite scrolling background mechanics
- [ ] Plan pink color theme variants
- [ ] Design enemy spawn patterns for infinite mode
- [ ] Plan difficulty scaling algorithm

**2. Implementation Phase**
- [ ] Implement infinite scrolling background
- [ ] Create pink theme assets
- [ ] Update enemy spawn system for infinite mode
- [ ] Integrate SystemOverload.mp3 music (already in repo, 3.2 MB)
- [ ] Add leaderboard category for infinite mode

**3. UI Integration**
- [ ] Add infinite mode entry point (main menu or level select)
- [ ] Create infinite mode UI elements
- [ ] Add mode indicator during gameplay
- [ ] Update game over screen for infinite mode

**4. Testing Phase**
- [ ] Test infinite scrolling performance
- [ ] Verify difficulty scaling
- [ ] Test leaderboard integration
- [ ] Verify music plays correctly
- [ ] Test on desktop and mobile

**Documentation:** Create PINK_INFINITE_LEVEL_IMPLEMENTATION.md

---

## 🔧 Optional / Low Priority

### Favicon Creation
**Priority:** LOW
**Time:** 15 minutes
**Status:** Optional

- [ ] Create favicon.ico (16x16, 32x32, 48x48)
- [ ] Add to root directory
- [ ] Test on dev environment
- [ ] Deploy to production
- [ ] Verify 403 error eliminated

### GA4 Analytics Investigation
**Priority:** MEDIUM
**Time:** 1-2 sessions
**Status:** Research needed

**Objective:** Verify complete analytics data flow from code to dashboard

**Phase 1: Code Audit (30 min)**
- [ ] Audit all data tags in game.html
- [ ] Audit all data tags in game_mobile.html
- [ ] Audit all data tags in index.html
- [ ] Document all tracking events and parameters
- [ ] Create complete event inventory (spreadsheet or .md file)

**Phase 2: AWS CloudFront Verification (20 min)**
- [ ] Access CloudFront logs for production (nonx.standingtiger.com)
- [ ] Track sample data tags through CloudFront request logs
- [ ] Verify tags are passing through CDN correctly
- [ ] Check for any tag stripping or modification

**Phase 3: GA4 Verification (30 min)**
- [ ] Open GA4 DebugView (real-time event monitoring)
- [ ] Trigger test events from production site
- [ ] Verify events appearing in GA4 DebugView
- [ ] Check GA4 Realtime report for event counts
- [ ] Verify custom dimensions and metrics
- [ ] Check for any missing or malformed events

**Phase 4: NONX_analytics Dashboard API (30 min)**
- [ ] Review NONX_analytics API documentation
- [ ] Verify API endpoint configuration
- [ ] Test API calls manually (Postman or curl)
- [ ] Confirm data reaching dashboard database
- [ ] Check for API errors or timeouts
- [ ] Verify data consistency (GA4 vs dashboard)

**Phase 5: End-to-End Testing (20 min)**
- [ ] Play full game session on production
- [ ] Track specific event through entire pipeline:
  - Event fires in code → CloudFront → GA4 → Dashboard
- [ ] Document any breaks in the data flow
- [ ] Create data flow diagram

**Deliverables:**
- [ ] Complete data tag inventory document
- [ ] Data flow diagram (code → AWS → GA4 → dashboard)
- [ ] Identified gaps or issues
- [ ] Fix recommendations with priority ranking

**Known Issues:**
- Some data tags may not be hitting GA4 (reported)
- Dashboard may not show real-time data (to be verified)

**Documentation:** Create docs/analytics/GA4_DATA_FLOW_AUDIT.md

### Hero Ship Color Purchase
**Priority:** MEDIUM (after Pink Infinite Level)
**Time:** 2-3 sessions
**Status:** Designed

- Deferred until after Pink Infinite Level completion
- Design doc: docs/design/HERO_SHIP_COLOR_PURCHASE.md

---

## 📋 Current Project State

**Infrastructure:** ✅ 100% Complete
- Dev environment: https://dev.nonx.standingtiger.com (secured)
- Prod environment: https://nonx.standingtiger.com (secured)
- Auto-deploy: Working (dev & main branches)

**Active Branch:** dev

**Git Status:** Clean

**Next Milestone:** Complete security audit before feature development

---

**Last Updated:** June 3, 2026
**Phase 7 Completion Date:** June 3, 2026
**Next Review:** After security audit completion