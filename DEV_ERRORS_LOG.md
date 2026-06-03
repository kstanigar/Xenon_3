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

## June 3, 2026 - AI Agent Added Non-Error Content to Error Log - 🟢 RESOLVED

**Discovered:** June 3, 2026, 3:30 AM (Post-Phase 7 documentation updates)
**Environment:** Documentation / File organization
**Severity:** WARNING
**Status:** ✅ RESOLVED

### Error Description:
AI agent incorrectly added GA4 analytics verification task to DEV_ERRORS_LOG.md. This file is specifically for discovered errors and bugs, not for planned verification tasks or to-do items.

### Incorrect Action Taken:
```
Added entry: "GA4 Analytics Data Flow Unverified - 🟡 INVESTIGATION NEEDED"
To file: DEV_ERRORS_LOG.md
Problem: This is a planned task, not a discovered error
```

### Impact:
- ❌ Confused purpose of DEV_ERRORS_LOG.md
- ❌ Mixed "tasks to do" with "bugs to fix"
- ❌ Set bad precedent for future documentation
- ✅ User caught error immediately

### Root Cause:
**AI Agent Did Not Understand File Purpose**

The agent treated DEV_ERRORS_LOG.md as a general issues/tasks log rather than a specific error tracking log. The agent did not verify the file's purpose before adding content.

**DEV_ERRORS_LOG.md Purpose:**
- Discovered errors during testing
- Console errors that break functionality
- Bugs found in dev/prod environments
- Issues that need fixing

**NOT for:**
- Planned verification tasks
- Proactive audits
- To-do lists
- Investigation tasks (unless triggered by a discovered error)

### Correct Action:
**GA4 analytics verification belongs in:**
- ✅ CURRENT_PRIORITIES.md (Priority #5: planned task)
- ✅ NEXT_SESSION_PRIORITIES.md (detailed implementation plan)
- ❌ NOT in DEV_ERRORS_LOG.md

### Resolution:
**Date:** June 3, 2026, 3:30 AM
**Action:** Removed GA4 analytics verification entry from DEV_ERRORS_LOG.md
**Verified By:** User caught error and requested correction

### Lesson Learned:
**ALWAYS verify the purpose of a documentation file before adding content.**

Before adding to any .md file:
1. Read the file header/purpose statement
2. Check existing entries to understand the pattern
3. Verify the new content matches the file's purpose
4. If unsure, ask the user first

**File Purpose Quick Reference:**
- **DEV_ERRORS_LOG.md** - Discovered errors/bugs only
- **CURRENT_PRIORITIES.md** - Feature roadmap and task priorities
- **NEXT_SESSION_PRIORITIES.md** - Detailed implementation plans
- **HANDOFF_SUMMARY.md** - Session summaries and current state

### Prevention:
- ✅ AI agent must understand file purpose before editing
- ✅ User enforces strict documentation standards
- ✅ Each file has clear purpose statement in header

---

## June 3, 2026 - S3 Bucket Tags Incorrect Button Name Documentation - 🟢 RESOLVED

**Discovered:** June 3, 2026, 2:30 AM (Phase 2 CloudFront Migration - Task 2.4)
**Environment:** Documentation / AWS Console guidance
**Severity:** WARNING
**Status:** ✅ RESOLVED

### Error Description:
AI agent provided incorrect button name for adding tags to S3 bucket in AWS Console. Instructed user to look for "Edit" button, but AWS Console actually shows "Add new Tag" button.

### Incorrect Information Provided:
```
Task 2.4: Add Tags

1. Scroll down to "Tags" section
2. Click "Edit" button (in Tags section)  ← WRONG
3. Add Tag #1...
```

### Impact:
- ❌ User confusion when following instructions
- ❌ User cannot find "Edit" button in Tags section
- ❌ User must stop and request verification
- ⚠️ Slows migration progress

### Root Cause:
**AI Agent Assumed Button Name Without Verifying AWS Console UI**

Similar to CloudFront status terminology error, the AI agent provided instructions based on assumptions rather than verified AWS documentation. The agent assumed S3 bucket tags would use an "Edit" button (common pattern in other AWS sections), but did not verify the actual button name in the current AWS Console.

**Actual AWS S3 Console Behavior:**
- **Tags section location:** Properties tab ✅ (this was correct)
- **Button name:** "Add new Tag" (singular) - NOT "Edit"
- **Action:** Opens "Add Tags" page where multiple tags can be added
- **Alternative:** Some console versions may show "Edit" but current version uses "Add new Tag"

### Solution Applied:
**Corrected Instructions:**
```
Task 2.4: Add Tags

1. Scroll down to "Tags" section
2. Look for "Add new Tag" button (or "Edit" in older console versions)
3. Click the button - This opens "Add Tags" page
4. Add Tag #1: Key = Environment, Value = production
5. Add Tag #2: Key = Project, Value = nonx
6. Click "Save changes"
```

### Verification:
- ✅ Haiku agent research confirmed correct button name (Agent ID: a78151b)
- ✅ AWS official documentation verified: "Choose Add new Tag" is the correct button
- ✅ User requested verification before proceeding
- ✅ Documentation corrected with exact button names

### Lesson Learned:
**ALWAYS verify AWS Console UI button names and field labels before documenting them.**

Pattern identified: This is the **second time** in this session that AWS Console UI terminology was documented incorrectly without verification:
1. CloudFront "Deployed" status (doesn't exist)
2. S3 Tags "Edit" button (should be "Add new Tag")

### Prevention:
- ✅ When documenting AWS Console steps, research MUST verify:
  - Exact button names
  - Exact field labels
  - Exact status values
  - Exact menu locations
- ✅ User enforces strict verification: "No guessing allowed"
- ✅ Use Haiku agents to verify AWS Console UI before providing instructions

### Sources:
- [Adding a tag to a bucket - Amazon Simple Storage Service](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucket-tag-add.html)
- Official AWS documentation verified by Haiku agent a78151b

---

## June 3, 2026 - CloudFront Documentation Incorrect Status Terminology - 🟢 RESOLVED

**Discovered:** June 3, 2026, 2:00 AM (Phase 1 CloudFront Migration)
**Environment:** Documentation / AWS Console guidance
**Severity:** WARNING
**Status:** ✅ RESOLVED

### Error Description:
Documentation file `docs/PRODUCTION_CLOUDFRONT_MIGRATION.md` contained incorrect AWS CloudFront status terminology, instructing users to wait for "Deployed" status which does not exist in AWS Console.

### Incorrect Information (Lines 193-208):
```
Status Timeline:
10+ min: "Deployed" - ✅ Ready for next phase

Do NOT proceed to Phase 2 until status shows "Deployed"
Checkpoint: CloudFront status shows: "Deployed" (not "Deploying")
```

### Impact:
- ❌ User confusion during CloudFront migration
- ❌ Potential for user to think migration failed (looking for non-existent status)
- ❌ AI agent hallucinated incorrect information by repeating documentation error
- ⚠️ Could block migration progress if user strictly follows docs

### Root Cause:
**Documentation Written Without Verifying AWS Console UI**

When PRODUCTION_CLOUDFRONT_MIGRATION.md was created (June 3, 2026), the status terminology was assumed based on common patterns rather than verified against actual AWS CloudFront Console.

**Actual AWS CloudFront Behavior:**
- **"Last modified" column:** Shows "Deploying" during propagation, then changes to **timestamp** (e.g., "June 3, 2026 at 7:00:44 AM UTC") when complete
- **"Status" column:** Shows "Enabled" or "Disabled" (distribution state, not deployment state)
- **No "Deployed" status exists** in AWS CloudFront Console

### Solution Applied:
**File:** `docs/PRODUCTION_CLOUDFRONT_MIGRATION.md` (Lines 193-210)

**CORRECTED to:**
```
2. Status Timeline (Last Modified Column):
   0-1 min:  "Deploying" - Initial update
   1-10 min: "Deploying" - Propagating to edge locations
   10+ min:  Timestamp (e.g., "June 3, 2026 at 7:00:44 AM UTC") - ✅ Ready for next phase

3. Do NOT proceed to Phase 2 until "Last modified" shows a timestamp (not "Deploying")

5. Checkpoint:
   - "Last modified" shows timestamp (e.g., "June 3, 2026 at 7:00:44 AM UTC"), NOT "Deploying"
   - "Status" column shows "Enabled"
   - No error messages

Note: AWS CloudFront does NOT use "Deployed" as a status.
```

### Verification:
- ✅ Haiku agent research confirmed correct AWS CloudFront terminology (Agent ID: a8ca0c6)
- ✅ User verified actual AWS Console shows timestamp, not "Deployed"
- ✅ Documentation updated with correct terminology
- ✅ Added clarifying note about AWS CloudFront status behavior

### Resolution:
**Date:** June 3, 2026, 2:05 AM
**Action:** Documentation corrected in PRODUCTION_CLOUDFRONT_MIGRATION.md
**Verified By:** User caught error, demanded verification before proceeding

### Lesson Learned:
**ALWAYS verify AWS Console UI terminology before documenting it.**

When writing migration guides:
1. Open actual AWS Console
2. Verify exact field names and status values
3. Take screenshots if needed
4. Never assume status terminology based on common patterns
5. Use research agents to verify if unsure

### Prevention:
- ✅ Added to project rules: No assumptions, verify all documentation
- ✅ User enforces strict verification requirement: "I will not tolerate wrong information"
- ✅ AI agents must research and verify before providing guidance

---

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

**Last Updated:** June 3, 2026
**Maintained By:** Development team
**Review Frequency:** After every dev environment test