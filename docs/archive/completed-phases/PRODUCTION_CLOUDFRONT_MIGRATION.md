# Production CloudFront Migration Plan

**Date Created:** June 3, 2026
**Status:** Ready to Execute
**Estimated Time:** 40 minutes (includes 15 min propagation wait)
**Risk Level:** LOW (Dev environment validates approach, 5-min rollback available)

---

## Overview

**Objective:** Migrate production CloudFront from S3 website endpoint to S3 bucket endpoint with Origin Access Control (OAC).

**Current State:**
- Origin: `nonx.standingtiger.com.s3-website.us-east-2.amazonaws.com` (S3 website endpoint)
- Protocol: HTTP only
- Security: Bucket must be public (insecure)
- OAC: Not supported

**Target State:**
- Origin: `nonx.standingtiger.com.s3.us-east-2.amazonaws.com` (S3 bucket endpoint)
- Protocol: HTTPS
- Security: Bucket private with OAC (secure)
- OAC: Enabled

**Why This Migration?**
1. **Security:** Private bucket (Block Public Access enabled)
2. **HTTPS:** Encrypted origin-to-CloudFront communication
3. **Best Practice:** Matches dev environment and AWS 2026 standards
4. **Consistency:** Dev and prod configurations identical

---

## Pre-Migration Checklist

**Before starting, verify:**

- [ ] Read full migration plan (this document)
- [ ] Research report reviewed (agent a0d15fb confirmed safety)
- [ ] AWS Console access ready
- [ ] AWS Account ID noted: `032614958698`
- [ ] CloudFront Distribution ID: `ED9CRAIN93YRS`
- [ ] S3 Bucket Name: `nonx.standingtiger.com`
- [ ] Dev environment working (reference: https://dev.nonx.standingtiger.com)
- [ ] Current production working (baseline: https://nonx.standingtiger.com)

**Resources:**
- CloudFront Console: https://console.aws.amazon.com/cloudfront/
- S3 Console: https://console.aws.amazon.com/s3/
- AWS Account: 032614958698
- Region: us-east-1 (CloudFront is global, S3 bucket is us-east-2)

---

## Phase 1: CloudFront Origin Migration (15 minutes)

### Task 1.1: Create Origin Access Control (OAC)

**Time:** 3 minutes

1. **Navigate to CloudFront OAC Settings**
   ```
   AWS Console → CloudFront → Origin access → Origin access control
   ```

2. **Click "Create control setting"**

3. **Configure OAC:**
   ```
   Name: nonx-prod-oac
   Description: Origin Access Control for NON-X production
   Origin type: S3
   Signing behavior: Sign requests (recommended)
   ```

4. **Click "Create"**

5. **Verify OAC Created:**
   - [ ] OAC appears in list with name "nonx-prod-oac"
   - [ ] Status shows "Ready"

---

### Task 1.2: Edit CloudFront Origin Domain

**Time:** 5 minutes

1. **Navigate to Production Distribution**
   ```
   AWS Console → CloudFront → Distributions
   Click: ED9CRAIN93YRS
   ```

2. **Go to Origins Tab**
   ```
   Click: "Origins" tab
   ```

3. **Select Current Origin**
   ```
   Click: The origin row (nonx.standingtiger.com.s3-website...)
   Click: "Edit" button
   ```

4. **Change Origin Domain**
   ```
   Current: nonx.standingtiger.com.s3-website.us-east-2.amazonaws.com
   Change to: nonx.standingtiger.com.s3.us-east-2.amazonaws.com

   ⚠️ IMPORTANT: Use s3.us-east-2 (NOT s3-website.us-east-2)
   ```

5. **Scroll down to find "Origin access" section**
   ```
   (This section appears after changing to bucket endpoint)
   ```

6. **Configure Origin Access**
   ```
   Origin access: Select "Origin access control settings (recommended)"
   Origin access control: Select "nonx-prod-oac"
   ```

7. **Change Protocol**
   ```
   Protocol: Change from "HTTP only" to "HTTPS only"
   ```

8. **Review Settings Before Saving:**
   - [ ] Origin domain: `nonx.standingtiger.com.s3.us-east-2.amazonaws.com`
   - [ ] Origin access: Origin access control settings
   - [ ] OAC: nonx-prod-oac
   - [ ] Protocol: HTTPS only

9. **Click "Save changes"**

---

### Task 1.3: Copy Bucket Policy Statement

**Time:** 1 minute

**After clicking "Save changes", CloudFront will display a yellow banner:**

```
⚠️ Policy update required
The S3 bucket policy needs to be updated. Copy the policy below:
```

1. **Click "Copy policy"** (button in the yellow banner)

2. **Save policy to clipboard** (you'll need it in Phase 2)

**Policy format (for reference):**
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Sid": "AllowCloudFrontServicePrincipal",
    "Effect": "Allow",
    "Principal": {
      "Service": "cloudfront.amazonaws.com"
    },
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::nonx.standingtiger.com/*",
    "Condition": {
      "StringEquals": {
        "AWS:SourceArn": "arn:aws:cloudfront::032614958698:distribution/ED9CRAIN93YRS"
      }
    }
  }]
}
```

3. **Verify CloudFront Status:**
   - [ ] Navigate to: CloudFront → Distributions → ED9CRAIN93YRS
   - [ ] Status should show: "Deploying" (with timestamp)
   - [ ] Last modified: Should show current time

---

### Task 1.4: Wait for CloudFront Propagation

**Time:** 5-15 minutes (average 10 minutes)

**During this time, CloudFront is deploying changes to all edge locations globally.**

1. **Monitor Deployment Status:**
   ```
   AWS Console → CloudFront → Distributions → ED9CRAIN93YRS
   ```

2. **Status Timeline (Last Modified Column):**
   ```
   0-1 min:  "Deploying" - Initial update
   1-10 min: "Deploying" - Propagating to edge locations
   10+ min:  Timestamp (e.g., "June 3, 2026 at 7:00:44 AM UTC") - ✅ Ready for next phase
   ```

3. **Do NOT proceed to Phase 2 until "Last modified" shows a timestamp (not "Deploying")**

4. **While waiting, you can:**
   - Review Phase 2 steps
   - Keep this window open
   - Take a break

5. **Checkpoint:**
   - [ ] "Last modified" shows timestamp (e.g., "June 3, 2026 at 7:00:44 AM UTC"), NOT "Deploying"
   - [ ] "Status" column shows "Enabled"
   - [ ] No error messages

**Note:** AWS CloudFront does NOT use "Deployed" as a status. The "Last modified" field changes from "Deploying" to a timestamp when propagation is complete.

---

## Phase 2: S3 Bucket Security Update (10 minutes)

**⚠️ CRITICAL: Only start Phase 2 after CloudFront shows "Deployed"**

---

### Task 2.1: Enable Block Public Access

**Time:** 2 minutes

1. **Navigate to S3 Bucket**
   ```
   AWS Console → S3 → Buckets
   Click: nonx.standingtiger.com
   ```

2. **Go to Permissions Tab**
   ```
   Click: "Permissions" tab
   ```

3. **Edit Block Public Access Settings**
   ```
   Scroll to: "Block public access (bucket settings)"
   Click: "Edit" button
   ```

4. **Enable All 4 Settings:**
   ```
   ✅ Block all public access (check the master toggle)

   This enables all 4 sub-settings:
   ✅ Block public access to buckets and objects granted through new ACLs
   ✅ Block public access to buckets and objects granted through any ACLs
   ✅ Block public access to buckets and objects granted through new public bucket or access point policies
   ✅ Block public access to buckets and objects granted through any public bucket or access point policies
   ```

5. **Save Changes**
   ```
   Click: "Save changes"

   Confirmation prompt appears:
   Type: confirm
   Click: "Confirm"
   ```

6. **Verify:**
   - [ ] Block public access (bucket settings): **On** (should show as enabled)
   - [ ] All 4 sub-settings show as enabled

---

### Task 2.2: Update S3 Bucket Policy

**Time:** 3 minutes

1. **Navigate to Bucket Policy**
   ```
   Still in Permissions tab
   Scroll to: "Bucket policy"
   Click: "Edit"
   ```

2. **Current Policy Check:**
   ```
   Current policy may be empty or show public read policy

   If present, it looks like:
   {
     "Statement": [{
       "Effect": "Allow",
       "Principal": "*",
       "Action": "s3:GetObject",
       "Resource": "arn:aws:s3:::nonx.standingtiger.com/*"
     }]
   }
   ```

3. **Delete Current Policy**
   ```
   Select all text in the policy editor
   Delete it completely
   ```

4. **Paste New OAC Policy**
   ```
   Paste the policy copied from CloudFront (Task 1.3)

   OR manually enter:
   ```

   ```json
   {
     "Version": "2012-10-17",
     "Statement": [{
       "Sid": "AllowCloudFrontServicePrincipal",
       "Effect": "Allow",
       "Principal": {
         "Service": "cloudfront.amazonaws.com"
       },
       "Action": "s3:GetObject",
       "Resource": "arn:aws:s3:::nonx.standingtiger.com/*",
       "Condition": {
         "StringEquals": {
           "AWS:SourceArn": "arn:aws:cloudfront::032614958698:distribution/ED9CRAIN93YRS"
         }
       }
     }]
   }
   ```

5. **Verify Policy Format:**
   - [ ] Valid JSON (no syntax errors)
   - [ ] Principal: `"Service": "cloudfront.amazonaws.com"`
   - [ ] Resource: `arn:aws:s3:::nonx.standingtiger.com/*`
   - [ ] AWS:SourceArn includes distribution ID: `ED9CRAIN93YRS`

6. **Save Policy**
   ```
   Click: "Save changes"
   ```

7. **Confirm Success:**
   - [ ] Bucket policy section shows "✓" (checkmark)
   - [ ] No error messages about invalid policy

---

### Task 2.3: Enable Versioning

**Time:** 2 minutes

1. **Navigate to Properties Tab**
   ```
   Click: "Properties" tab (at top of bucket page)
   ```

2. **Find Bucket Versioning**
   ```
   Scroll to: "Bucket Versioning" section
   ```

3. **Edit Versioning**
   ```
   Click: "Edit" button
   ```

4. **Enable Versioning**
   ```
   Select: "Enable"
   Click: "Save changes"
   ```

5. **Verify:**
   - [ ] Bucket Versioning: **Enabled**

**Why versioning?** Allows rollback if files are accidentally overwritten or deleted.

---

### Task 2.4: Add Tags

**Time:** 2 minutes

1. **Still in Properties Tab**
   ```
   Scroll to: "Tags" section
   ```

2. **Edit Tags**
   ```
   Click: "Edit" button
   ```

3. **Add Tag #1:**
   ```
   Click: "Add tag"
   Key: Environment
   Value: production
   ```

4. **Add Tag #2:**
   ```
   Click: "Add tag"
   Key: Project
   Value: nonx
   ```

5. **Save Tags**
   ```
   Click: "Save changes"
   ```

6. **Verify:**
   - [ ] Tags section shows: 2 tags
   - [ ] Environment: production
   - [ ] Project: nonx

---

### Task 2.5: Verify Bucket Configuration Summary

**Checkpoint - All S3 settings should now be:**

```
✅ Block public access: On (all 4 enabled)
✅ Bucket policy: OAC-based (CloudFront service principal only)
✅ Versioning: Enabled
✅ Tags: 2 tags (Environment, Project)
```

**Time to wait:** 2-5 minutes for policy propagation

---

## Phase 3: Verification & Testing (10 minutes)

### Task 3.1: Basic Connectivity Test

**Time:** 2 minutes

1. **Wait 2 Minutes for Propagation**
   ```
   S3 bucket policy takes 2-5 minutes to propagate
   CloudFront may need to refresh its cache
   ```

2. **Test Production URL**
   ```
   Open browser: https://nonx.standingtiger.com
   ```

3. **Expected Results:**
   - ✅ Page loads (index.html appears)
   - ✅ No 403 Access Denied error
   - ✅ No certificate errors
   - ✅ HTTPS lock icon in browser

4. **If 403 Error Appears:**
   ```
   Wait additional 3 minutes (policy still propagating)
   Refresh browser (Ctrl+Shift+R or Cmd+Shift+R)

   If still 403 after 5 minutes total:
   - See Troubleshooting section below
   ```

---

### Task 3.2: Browser Console Check

**Time:** 2 minutes

1. **Open Developer Tools**
   ```
   Browser: Press F12 (Windows) or Cmd+Option+I (Mac)
   ```

2. **Check Console Tab**
   ```
   Look for errors (red text)
   ```

3. **Expected: No Errors**
   ```
   ✅ No 403 errors
   ✅ No 404 errors
   ✅ No CORS errors
   ✅ No mixed content warnings
   ```

4. **Check Network Tab**
   ```
   Click: "Network" tab
   Refresh page: Ctrl+R or Cmd+R
   ```

5. **Verify Resource Loading:**
   ```
   ✅ index.html: 200 OK
   ✅ game.html: 200 OK (if navigated)
   ✅ Assets (sprites, audio): 200 OK
   ✅ Firebase requests: 200 OK
   ```

---

### Task 3.3: Game Functionality Test

**Time:** 3 minutes

1. **Test Desktop Game**
   ```
   Navigate to: https://nonx.standingtiger.com/game.html
   ```

2. **Verify Game Loads:**
   - [ ] Game canvas renders
   - [ ] Player ship appears
   - [ ] Background music plays (if unmuted)
   - [ ] Sprites load correctly

3. **Test Game Controls:**
   - [ ] Arrow keys move ship
   - [ ] Spacebar fires weapons
   - [ ] Enemies spawn

4. **Test Leaderboard:**
   - [ ] Leaderboard button appears
   - [ ] Clicking shows top scores
   - [ ] Firebase data loads

5. **Test Mobile Game**
   ```
   Navigate to: https://nonx.standingtiger.com/game_mobile.html

   OR test on mobile device
   ```

6. **Verify Mobile Loads:**
   - [ ] Mobile layout renders
   - [ ] Touch controls work (if on mobile)
   - [ ] Game plays correctly

---

### Task 3.4: Analytics & Integrations Test

**Time:** 2 minutes

1. **Check Google Analytics**
   ```
   Browser console → Network tab
   Filter: analytics
   ```

2. **Verify GA4 Tracking:**
   - [ ] Requests to `google-analytics.com` or `analytics.google.com`
   - [ ] /collect requests sent
   - [ ] No GA errors in console

3. **Check Firebase Connectivity**
   ```
   Browser console → Network tab
   Filter: firestore
   ```

4. **Verify Firebase Works:**
   - [ ] Requests to `firestore.googleapis.com`
   - [ ] Leaderboard data loads
   - [ ] No Firebase errors (except if ad blocker enabled)

---

### Task 3.5: Compare with Dev Environment

**Time:** 1 minute

1. **Open Dev Site**
   ```
   New tab: https://dev.nonx.standingtiger.com
   ```

2. **Compare Behavior:**
   - [ ] Production loads like dev
   - [ ] Same game functionality
   - [ ] Same performance
   - [ ] Same layout/appearance

3. **If Differences Found:**
   ```
   Document differences
   Check if expected (different data, etc.)
   ```

---

## Success Criteria

**Migration is successful when ALL of these are true:**

### CloudFront
- [ ] Distribution status: "Deployed"
- [ ] Origin domain: `nonx.standingtiger.com.s3.us-east-2.amazonaws.com`
- [ ] Origin access: OAC (nonx-prod-oac)
- [ ] Protocol: HTTPS only

### S3 Bucket
- [ ] Block public access: All 4 enabled
- [ ] Bucket policy: OAC-based (CloudFront service principal)
- [ ] Versioning: Enabled
- [ ] Tags: 2 tags configured

### Production Site
- [ ] https://nonx.standingtiger.com loads without errors
- [ ] Game functionality works (desktop & mobile)
- [ ] Leaderboard loads (Firebase connectivity)
- [ ] Analytics tracking works
- [ ] No console errors
- [ ] Performance same or better

### Security
- [ ] Direct S3 access blocked (try accessing bucket directly → should get 403)
- [ ] CloudFront access works (via CDN → should get 200)

---

## Troubleshooting

### Issue 1: 403 Access Denied After Migration

**Symptoms:**
```
Browser shows: 403 Forbidden
Console shows: AccessDenied error
```

**Causes & Solutions:**

**Cause 1: Bucket policy not yet propagated**
```
Wait: 5 minutes total
Refresh: Hard refresh (Ctrl+Shift+R)
Check: S3 bucket policy is correct
```

**Cause 2: Bucket policy incorrect**
```
Verify:
- Principal: "Service": "cloudfront.amazonaws.com"
- AWS:SourceArn includes correct distribution ID
- Resource includes bucket name and /*
```

**Cause 3: OAC not attached**
```
Check:
CloudFront → ED9CRAIN93YRS → Origins → Origin access
Should show: "Origin access control settings"
Should list: nonx-prod-oac
```

**Fix:**
```
1. Go to CloudFront → ED9CRAIN93YRS → Origins
2. Edit origin
3. Verify OAC is selected
4. Save and wait 5 minutes
```

---

### Issue 2: Site Loads But Assets Return 404

**Symptoms:**
```
HTML loads but sprites/audio don't load
Console shows: 404 Not Found for asset files
```

**Cause:** Files missing in S3 bucket

**Fix:**
```
1. Check S3 bucket contains all files:
   - index.html
   - game.html
   - game_mobile.html
   - assets/ directory (sprites, audio)

2. If missing, deploy from dev:
   git push origin main (triggers workflow)
```

---

### Issue 3: Slow Performance or Stale Content

**Symptoms:**
```
Site loads but shows old content
Changes not appearing
```

**Cause:** CloudFront cache not invalidated

**Fix:**
```
AWS Console → CloudFront → ED9CRAIN93YRS → Invalidations
Click: "Create invalidation"
Object paths: /*
Click: "Create invalidation"

Wait: 1-3 minutes for invalidation to complete
```

---

### Issue 4: Mixed Content Warnings

**Symptoms:**
```
Console: "Mixed Content: The page at 'https://...'
was loaded over HTTPS, but requested an insecure
resource 'http://...'"
```

**Cause:** Some assets loaded via HTTP

**Fix:**
```
1. Check origin protocol: Should be HTTPS only
2. Check for hardcoded HTTP URLs in HTML/JS
3. Update to relative URLs or HTTPS
```

---

## Rollback Plan (If Needed)

**If migration fails and production is down, execute rollback:**

### Rollback Time: 5 minutes

**Step 1: Revert CloudFront Origin (2 min)**

1. Go to CloudFront → ED9CRAIN93YRS → Origins → Edit
2. Change origin domain back to:
   ```
   nonx.standingtiger.com.s3-website.us-east-2.amazonaws.com
   ```
3. Origin access: Change to "No" (public origin)
4. Protocol: Change to "HTTP only"
5. Save changes

**Step 2: Disable Block Public Access (1 min)**

1. Go to S3 → nonx.standingtiger.com → Permissions
2. Block public access → Edit
3. Uncheck all 4 boxes
4. Save changes → Confirm

**Step 3: Remove Bucket Policy (1 min)**

1. S3 → nonx.standingtiger.com → Permissions → Bucket policy
2. Delete the entire policy (leave blank)
3. Save changes

**Step 4: Wait for Propagation (1 min)**

1. CloudFront shows "Deploying"
2. Wait until shows "Deployed"
3. Test: https://nonx.standingtiger.com

**Total rollback time:** ~5 minutes

---

## Post-Migration Documentation

### Update These Files After Successful Migration:

1. **HANDOFF_SUMMARY.md**
   - Mark Priority 2 complete
   - Add migration completion date
   - Note production now matches dev security

2. **NEXT_SESSION_PRIORITIES.md**
   - Mark Priority 2 tasks complete
   - Update Phase 7 progress (Priority 2 complete)

3. **DEV_ERRORS_LOG.md** (if applicable)
   - Document any issues encountered
   - Add resolutions

4. **Tasks**
   - Mark Task #8 complete
   - Mark Task #9 complete
   - Mark Task #10 complete

---

## Migration Completion Checklist

**Before marking migration complete:**

- [ ] All Phase 1 tasks complete
- [ ] All Phase 2 tasks complete
- [ ] All Phase 3 tests passing
- [ ] Success criteria met
- [ ] No errors in console
- [ ] Game fully functional
- [ ] Documentation updated
- [ ] Tasks marked complete

**Time to mark complete:** When all above checkboxes are ✅

---

## Quick Reference

**AWS Resources:**
- Account ID: `032614958698`
- Region: `us-east-2` (S3 bucket)
- CloudFront Distribution: `ED9CRAIN93YRS`
- S3 Bucket: `nonx.standingtiger.com`
- OAC Name: `nonx-prod-oac`

**URLs:**
- Production: https://nonx.standingtiger.com
- Dev (reference): https://dev.nonx.standingtiger.com
- CloudFront Console: https://console.aws.amazon.com/cloudfront/
- S3 Console: https://console.aws.amazon.com/s3/

**Timeline:**
- Phase 1: 15 minutes (includes 10 min wait)
- Phase 2: 10 minutes
- Phase 3: 10 minutes
- Total: 35-40 minutes

---

**Last Updated:** June 3, 2026
**Research Agent:** a0d15fb
**Status:** Ready to execute