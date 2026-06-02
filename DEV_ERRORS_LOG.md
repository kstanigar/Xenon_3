# Development Environment Errors Log

**Purpose:** Permanent log of all errors discovered in dev environment that must be fixed before production deployment.

**Organization:** Reverse chronological order (newest errors first)

**Status Key:**
- 🔴 **CRITICAL** - Blocks production deployment
- 🟡 **WARNING** - Should fix before production
- 🟢 **RESOLVED** - Fixed and verified
- 📝 **DOCUMENTED** - Known issue, workaround exists

---

## Instructions

### When to Add an Entry:
- Any error found during dev environment testing
- Console errors that impact functionality
- User-reported issues on dev site
- Failed deployments or broken features

### Entry Format:
```
## [Date] - [Brief Title] - [Status Icon]

**Discovered:** [Date and time]
**Environment:** dev.nonx.standingtiger.com
**Severity:** [CRITICAL/WARNING/INFO]
**Status:** [OPEN/IN PROGRESS/RESOLVED]

**Error:**
[Error message or description]

**Impact:**
- [What's broken]
- [What doesn't work]

**Root Cause:**
[Why this happened]

**Solution:**
[How to fix it]

**Resolution:**
[What was done, when, by whom]
```

---

# Error Log Entries

## May 31, 2026 - Music File 403 Forbidden - 🟢 RESOLVED

**Discovered:** May 31, 2026, 9:00 PM (Phase 7 testing)
**Environment:** https://dev.nonx.standingtiger.com
**Browser:** Chrome
**Severity:** CRITICAL
**Status:** ✅ RESOLVED

### Error Messages:
```
GET https://dev.nonx.standingtiger.com/assets/audio/music/NonexFullSong.mp3 403 (Forbidden)
(appears 2 times)

game.html:8612 Uncaught (in promise) NotSupportedError: The element has no supported sources.
```

### Impact:
- ❌ Background music does not play
- ❌ Audio mute button has nothing to mute (appears non-functional)
- ✅ Sound effects work correctly
- ⚠️ Game is playable but silent (missing atmosphere)

### Root Cause:
GitHub Actions workflow `.github/workflows/deploy-aws.yml` line 66 explicitly excludes music files from deployment:
```yaml
--exclude "assets/audio/music/*"
```

**Why Music Was Excluded:**
- Music files are large (~5-10 MB per file)
- Exclusion speeds up deployment time
- Reduces S3 storage costs
- Likely added for optimization during initial workflow setup

**Problem:**
Game code expects music file at `/assets/audio/music/NonexFullSong.mp3` but file was never deployed to S3 bucket `nonx-dev-032614958698-us-east-2-an`.

### Solution:
**Option 1: Remove music exclusion (Recommended)**

**File:** `.github/workflows/deploy-aws.yml`
**Lines:** 60-70

**BEFORE (Current - Music Excluded):**
```yaml
      - name: Sync to S3 (${{ steps.target.outputs.environment }})
        run: |
          aws s3 sync . s3://${{ steps.target.outputs.bucket }} \
            --exclude ".git/*" \
            --exclude ".github/*" \
            --exclude "docs/*" \
            --exclude "backups/*" \
            --exclude "scripts/*" \
            --exclude "assets/audio/music/*" \    # ← LINE 66: REMOVE THIS LINE
            --exclude "*.md" \
            --exclude ".DS_Store" \
            --exclude ".claude/*" \
            --delete
```

**AFTER (Fixed - Music Included):**
```yaml
      - name: Sync to S3 (${{ steps.target.outputs.environment }})
        run: |
          aws s3 sync . s3://${{ steps.target.outputs.bucket }} \
            --exclude ".git/*" \
            --exclude ".github/*" \
            --exclude "docs/*" \
            --exclude "backups/*" \
            --exclude "scripts/*" \
            --exclude "*.md" \
            --exclude ".DS_Store" \
            --exclude ".claude/*" \
            --delete
```

**Change Summary:**
- **Remove line 66:** `--exclude "assets/audio/music/*" \`
- All other exclusions remain unchanged
- Music files will now deploy to S3

**Steps to Apply:**
1. Edit `.github/workflows/deploy-aws.yml`
2. Delete line 66 completely
3. Commit with message: `fix: deploy music files to enable background audio`
4. Create PR to dev branch
5. Merge PR
6. GitHub Actions will auto-deploy (~15-20 seconds)
7. Verify music file accessible at: `https://dev.nonx.standingtiger.com/assets/audio/music/NonexFullSong.mp3`

**Trade-offs:**
- Deployment time: +5-10 seconds per deploy
- S3 storage: +~5-10 MB
- Cost impact: ~$0.01/month (negligible)

**Option 2: Optimize then deploy**
1. Compress music file (320kbps → 192kbps MP3)
2. Remove exclusion from workflow
3. Deploy optimized file
4. 40% smaller file, minimal quality loss

### Files Involved:
- `.github/workflows/deploy-aws.yml` (line 66)
- `game.html` (line 8612, 8627)
- `assets/audio/music/NonexFullSong.mp3` (local only, not deployed)

### Resolution:
**Status:** ✅ RESOLVED
**Resolved By:** User + Claude Sonnet 4.5
**Resolved Date:** May 31, 2026, 10:30 PM

**Actions Taken:**
1. User optimized music files (removed 4 unused songs: VoidOfEchoes, Rift, VastUniverse, Ximer_EE)
2. Kept 2 essential music files:
   - NonexFullSong.mp3 (4.4 MB) - Current game music
   - SystemOverload.mp3 (3.2 MB) - Pink infinite level (future)
3. Removed line 66 from `.github/workflows/deploy-aws.yml`
4. Total music: 7.6 MB (64% reduction from original 20.9 MB)

**Verification:**
- ✅ PR #116 merged to dev branch (June 1, 2026, 5:46 PM)
- ✅ Deployment successful (Deploy to AWS S3 + CloudFront #3, 17 seconds)
- ✅ Music files deployed to S3 (NonexFullSong.mp3, SystemOverload.mp3)
- ✅ Tested at https://dev.nonx.standingtiger.com
- ✅ Background music plays correctly
- ✅ Mute button functions properly
- ✅ No console errors
- ✅ Sound effects still work

**Final Status:** Issue completely resolved and verified working in production

---

## May 31, 2026 - Firebase Connection Blocked by Client - 🟡 WARNING

**Discovered:** May 31, 2026, 9:00 PM (Phase 7 testing)
**Environment:** https://dev.nonx.standingtiger.com
**Browser:** Chrome (with extensions)
**Severity:** WARNING (user environment issue, not deployment bug)
**Status:** DOCUMENTED

### Error Message:
```
POST https://firestore.googleapis.com/google.firestore.v1.Firestore/Listen/channel...
net::ERR_BLOCKED_BY_CLIENT

Location: webchannel_connection.ts:287
```

### Impact:
- ⚠️ Leaderboard may not load
- ⚠️ Score submission may fail
- ⚠️ Real-time Firebase features unavailable

### Root Cause:
**Not a deployment bug** - Browser extension blocking Firebase requests.

**Likely Blockers:**
- Ad blocker (uBlock Origin, AdBlock Plus, Ghostery, Privacy Badger)
- Browser tracking protection (Brave, Firefox Enhanced Tracking Protection)
- Corporate firewall/proxy
- VPN with ad/tracker blocking

**Why Firebase Gets Blocked:**
- Uses Google domains (`firestore.googleapis.com`)
- Classified as tracking/analytics by some blockers
- Looks like Google Analytics to extensions

### Solution:
**For Testing (Phase 7):**
1. Disable ad blocker/extensions temporarily
2. Test in private/incognito mode (disables extensions)
3. Test in different browser
4. Whitelist `firestore.googleapis.com` in ad blocker

**For Production:**
1. Add documentation about ad blockers affecting functionality
2. Add Firebase error detection in code
3. Show user-friendly message if Firebase is blocked
4. Consider fallback UI for offline/blocked Firebase

**No code changes required** - This is environment-specific, not a bug.

### Files Involved:
- Firebase SDK (external)
- `game.html` (Firebase initialization, leaderboard code)

### Resolution:
**Status:** DOCUMENTED
**Action Required:** Test with ad blockers disabled for Phase 7
**Long-term:** Add Firebase error handling and user messaging
**Production Impact:** Document ad blocker compatibility in user guide

---

## May 31, 2026 - CloudFront 403 Access Denied (Default Root Object Missing) - 🟢 RESOLVED

**Discovered:** May 31, 2026, 6:30 PM (Phase 6 testing)
**Environment:** https://dev.nonx.standingtiger.com
**Severity:** CRITICAL (blocked site access)
**Status:** RESOLVED

### Error:
```
HTTP 403 Forbidden
<Error>
  <Code>AccessDenied</Code>
  <Message>Access Denied</Message>
</Error>
```

### Impact:
- ❌ Site returned 403 when accessing root URL
- ❌ Users could not access dev site at all
- ✅ S3 bucket and files existed
- ✅ CloudFront distribution was deployed

### Root Cause:
CloudFront distribution `E1Q496KLUYVM0Z` was missing **Default Root Object** setting.

**What Happened:**
1. During Phase 3 (CloudFront creation), Default Root Object field was left empty
2. When users visited `dev.nonx.standingtiger.com/`, CloudFront didn't know to serve `index.html`
3. CloudFront attempted to access S3 bucket root directly
4. S3 bucket has Block Public Access enabled (secure)
5. Result: 403 Access Denied

### Solution Applied:
1. CloudFront Console → Distribution E1Q496KLUYVM0Z
2. Edit distribution settings
3. Set **Default root object** = `index.html`
4. Save changes
5. Wait 2-5 minutes for propagation

### Files Involved:
- CloudFront Distribution: E1Q496KLUYVM0Z
- S3 Bucket: nonx-dev-032614958698-us-east-2-an (policy was already correct)

### Resolution:
**Status:** ✅ RESOLVED
**Resolved By:** Claude Sonnet 4.5 + User
**Resolved Date:** May 31, 2026, 6:45 PM
**Verification:** Site loads successfully at https://dev.nonx.standingtiger.com
**Prevention:** Added to Phase 7 checklist - verify production CloudFront has Default Root Object set

**Documentation References:**
- DEPLOYMENT_PROGRESS.md (lines 836-899)
- HANDOFF_SUMMARY_2026-05-31.md (lines 60-108)

---

# Archive (Resolved Issues)

**Note:** Resolved issues remain in this log for historical reference and learning. Never delete entries.

---

**Last Updated:** May 31, 2026
**Maintained By:** Development team
**Review Frequency:** After every dev environment test