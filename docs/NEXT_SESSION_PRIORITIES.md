# Next Session Priorities

**Created:** May 31, 2026
**Session Ended:** Phase 6 Complete (86% overall progress)
**Remaining Work:** Phase 7 - Testing & Verification (Final Phase)

---

## 🎯 Priority 1: Test Dev Environment (CRITICAL)

**Objective:** Verify dev site is fully functional before any production deployment

**URL to Test:** https://dev.nonx.standingtiger.com

### Testing Checklist

**1. Initial Load Test**
- [ ] Site loads without errors
- [ ] Open browser console (F12) - check for JavaScript errors
- [ ] Verify no 403 or 404 errors
- [ ] Check network tab for failed resources

**2. Landing Page Features**
- [ ] Starfield animation renders (160 particles)
- [ ] Animation runs at 60fps (smooth, no lag)
- [ ] Platform selection buttons appear (Computer/Mobile)
- [ ] Settings toggles visible (Music, Movement, Analytics)
- [ ] "Keep the Lights On" button visible and functional
- [ ] UI is responsive (resize window, check mobile view)

**3. Game Launcher**
- [ ] Click "Computer" → Should route to game.html
- [ ] Click "Mobile" → Should route to game_mobile.html
- [ ] Both routes load correctly
- [ ] Settings persist across routes

**4. Game Functionality (Desktop - game.html)**
- [ ] Game canvas renders
- [ ] Player ship appears and responds to controls
- [ ] Enemies spawn correctly
- [ ] Level progression works (test levels 1-3 minimum)
- [ ] Boss encounters functional
- [ ] Scoring system accurate
- [ ] Game over screen appears correctly

**5. Game Functionality (Mobile - game_mobile.html)**
- [ ] Game canvas renders
- [ ] Touch controls responsive
- [ ] Same functionality as desktop version
- [ ] Orientation handling works

**6. Firebase Integration**
- [ ] Leaderboard displays (top 10 scores)
- [ ] Score submission works after game over
- [ ] No Firebase errors in console

**7. Google Analytics**
- [ ] GA4 tracking code loads (check network tab for analytics.js)
- [ ] Events being sent (check network for /collect requests)
- [ ] No GA errors in console

### Expected Issues (and Fixes)

**Issue #1: Firebase Domain Not Authorized**
- **Symptom:** Firebase errors in console about unauthorized domain
- **Fix:** Add `dev.nonx.standingtiger.com` to Firebase allowed domains
  - Firebase Console → Project settings → Authorized domains → Add domain
  - Wait 5-10 minutes for propagation

**Issue #2: Google Analytics Not Configured**
- **Symptom:** No analytics events in network tab
- **Fix:** Add `dev.nonx.standingtiger.com` to GA4 data stream
  - Google Analytics → Admin → Data Streams → Edit stream → Add domain
  - Verify Measurement ID matches code (G-9ECFZ9JBE5)

**Issue #3: CORS or Mixed Content Warnings**
- **Symptom:** Console shows blocked resources
- **Fix:** Verify all resources load via HTTPS (dev uses CloudFront SSL)
  - Check for any hardcoded HTTP URLs in code
  - Update to relative URLs or HTTPS

---

## 🎯 Priority 2: Production Environment Security (CRITICAL - DO BEFORE PROD DEPLOYMENT)

**Objective:** Update production infrastructure to match dev security configuration

**⚠️ WARNING:** Production currently has INSECURE configuration (public bucket access). Must fix before deploying.

### Task 1: Verify Production CloudFront Configuration

**CloudFront Distribution:** ED9CRAIN93YRS (nonx.standingtiger.com)

**Critical Check:**
1. Navigate to CloudFront console → Distribution ED9CRAIN93YRS
2. Click "General" tab
3. **Verify Default root object = `index.html`**
   - If empty or missing → **MUST FIX** (same 403 error will occur)
   - If set correctly → ✅ Proceed to next check

4. Click "Origins" tab
5. **Verify Origin Access Control is configured**
   - Should show OAC for S3 bucket `nonx.standingtiger.com`
   - If not configured → Must set up OAC (same as dev)

6. Click "General" tab → "Settings"
7. **Verify SSL certificate**
   - Should be: `*.standingtiger.com` OR custom cert for `nonx.standingtiger.com`
   - Must be valid and issued

8. **Verify Alternate domain names (CNAMEs)**
   - Should include: `nonx.standingtiger.com`

### Task 2: Update Production S3 Bucket Security

**S3 Bucket:** `nonx.standingtiger.com`

**Current (INSECURE) Configuration:**
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Sid": "PublicReadGetObject",
    "Effect": "Allow",
    "Principal": "*",
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::nonx.standingtiger.com/*"
  }]
}
```

**Steps to Secure:**

**Step 1: Enable Block Public Access**
1. S3 Console → Bucket `nonx.standingtiger.com`
2. Click "Permissions" tab
3. Click "Edit" under "Block public access (bucket settings)"
4. **Enable ALL 4 checkboxes:**
   - ✅ Block all public access
   - ✅ Block public access to buckets and objects granted through new access control lists (ACLs)
   - ✅ Block public access to buckets and objects granted through any access control lists (ACLs)
   - ✅ Block public access to buckets and objects granted through new public bucket or access point policies
   - ✅ Block public access to buckets and objects granted through any public bucket or access point policies
5. Click "Save changes"
6. Type "confirm" when prompted

**Step 2: Update Bucket Policy to CloudFront OAC**
1. Click "Bucket policy" under Permissions
2. **Replace existing policy** with OAC policy:

```json
{
    "Version": "2008-10-17",
    "Id": "PolicyForCloudFrontPrivateContent",
    "Statement": [
        {
            "Sid": "AllowCloudFrontServicePrincipal",
            "Effect": "Allow",
            "Principal": {
                "Service": "cloudfront.amazonaws.com"
            },
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::nonx.standingtiger.com/*",
            "Condition": {
                "ArnLike": {
                    "AWS:SourceArn": "arn:aws:cloudfront::032614958698:distribution/ED9CRAIN93YRS"
                }
            }
        }
    ]
}
```

3. Click "Save changes"

**Step 3: Enable Versioning (Rollback Protection)**
1. Click "Properties" tab
2. Scroll to "Bucket Versioning"
3. Click "Edit"
4. Select "Enable"
5. Click "Save changes"

**Step 4: Add Tags (Organization)**
1. Click "Properties" tab
2. Scroll to "Tags"
3. Click "Edit"
4. Add tags:
   - Key: `Environment`, Value: `production`
   - Key: `Project`, Value: `nonx`
5. Click "Save changes"

**Step 5: Verify CloudFront Can Still Access Bucket**
1. Wait 2-5 minutes for policy propagation
2. Visit: https://nonx.standingtiger.com
3. **Expected Result:** Site should still load (CloudFront uses OAC)
4. **If 403 error:** Check OAC is configured in CloudFront Origins tab

---

## 📊 Production Security Comparison

| Setting | Dev (Secure) | Prod (Current - Insecure) | Prod (Target - Secure) |
|---------|--------------|---------------------------|------------------------|
| **Block Public Access** | ✅ All 4 enabled | ❌ All 4 disabled | ✅ All 4 enabled |
| **Bucket Policy** | ✅ CloudFront OAC only | ❌ Public read access | ✅ CloudFront OAC only |
| **Versioning** | ✅ Enabled | ❌ Disabled | ✅ Enabled |
| **Tags** | ✅ 2 tags | ❌ None | ✅ 2 tags |
| **Default Root Object** | ✅ index.html | ⚠️ VERIFY | ✅ index.html |

---

## ⚠️ CRITICAL WARNINGS

### Warning 1: Test on Dev Before Prod
- **NEVER merge dev → main without testing Phase 7 Priority 1**
- Production deployment is IMMEDIATE (13 seconds)
- No manual approval step
- No rollback mechanism (must revert commits)

### Warning 2: Verify Production CloudFront Default Root Object
- **If missing:** Same 403 error will occur on production
- **This is the #1 cause** of the dev site 403 error we fixed
- **Check this BEFORE any production deployment**

### Warning 3: Production Bucket Security
- **Current state:** Public read access (anyone can access directly)
- **Risk:** Bypasses CloudFront (no caching, no CDN, no HTTPS enforcement)
- **Fix:** Enable Block Public Access + OAC policy (like dev)
- **When to fix:** Before production deployment (Priority 2)

### Warning 4: GitHub Base Branch Selection
- **GitHub UI defaults to merging into `main`** (DANGEROUS!)
- **Always verify base branch** before creating PRs
- **Use terminal commands** for safety: `gh pr create --base dev`
- Review: docs/GIT_COMMIT_WORKFLOW.md (Rule #2)

---

## 📝 Documentation Updates After Completion

**When Phase 7 is complete, update:**

1. **DEPLOYMENT_PROGRESS.md**
   - Mark Phase 7 as COMPLETE
   - Update overall progress to 7/7 (100%)
   - Document any issues found during testing

2. **HANDOFF_SUMMARY_2026-05-31.md**
   - Mark Priority 1 items as complete
   - Mark Priority 2 items as complete
   - Update "Next Immediate Actions" section

3. **LIVE_SITE_STATUS.md** (if exists)
   - Update dev site status (tested and verified)
   - Update prod site status (ready for deployment)

4. **AWS_DEPLOYMENT_STATUS.md** (if exists)
   - Mark all infrastructure as operational
   - Document final configuration details

---

## 🚀 Production Deployment Process (After Phase 7)

**Only proceed when:**
- ✅ Dev site fully tested (Priority 1 complete)
- ✅ Production CloudFront verified (Default Root Object = index.html)
- ✅ Production bucket security updated (Priority 2 complete)
- ✅ Firebase configured for both domains
- ✅ Google Analytics configured for both domains

**Deployment Steps:**
1. Ensure dev branch is fully tested and working
2. Create PR: dev → main
3. **VERIFY base branch = main** (not dev!)
4. Merge PR
5. GitHub Actions automatically deploys to production (~13 seconds)
6. Wait for CloudFront invalidation (2-5 minutes)
7. Test production site: https://nonx.standingtiger.com
8. Verify same functionality as dev
9. Monitor for errors (check console, network tab)

**Terminal Command (Safer):**
```bash
# Ensure dev is up to date
git checkout dev
git pull origin dev

# Create PR to main
gh pr create --base main --head dev \
  --title "chore: deploy tested dev environment to production" \
  --body "## Summary
Deploying fully tested dev environment to production.

## Testing Completed
- ✅ Dev site tested and verified
- ✅ All game features functional
- ✅ Firebase integration working
- ✅ Google Analytics tracking confirmed
- ✅ Production CloudFront verified
- ✅ Production bucket security updated

## Deployment
This will trigger automatic deployment to:
- URL: https://nonx.standingtiger.com
- CloudFront: ED9CRAIN93YRS
- S3: nonx.standingtiger.com"

# Review PR
gh pr view

# Merge when ready
gh pr merge --squash
```

---

## 📚 Reference Documents

**Must Read Before Starting:**
1. HANDOFF_SUMMARY_2026-05-31.md (session context)
2. DEPLOYMENT_PROGRESS.md (phase tracking)
3. GIT_COMMIT_WORKFLOW.md (git safety rules)

**Reference During Work:**
1. DEV_PROD_DEPLOYMENT_PLAN.md (original plan)
2. GITHUB_BRANCH_PROTECTION_GUIDE.md (branch protection details)

---

## ✅ Success Criteria

**Phase 7 is complete when:**
- ✅ Dev site tested and all features working
- ✅ Firebase configured for dev domain
- ✅ Google Analytics configured for dev domain
- ✅ Production CloudFront Default Root Object verified
- ✅ Production bucket security updated to match dev
- ✅ All documentation updated
- ✅ Ready for production deployment

**Estimated Time:** 30-45 minutes total
- Priority 1 (Dev Testing): 15-20 minutes
- Priority 2 (Prod Security): 15-20 minutes
- Documentation Updates: 5 minutes

---

**Last Updated:** May 31, 2026
**Current Phase:** 6/7 Complete (86%)
**Next Action:** Test dev site at https://dev.nonx.standingtiger.com