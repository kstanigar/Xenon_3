# Dev Environment Testing Issues

**Testing Date:** May 31, 2026
**Environment:** https://dev.nonx.standingtiger.com
**Browser:** Chrome (assumed)
**Tester:** User

---

## Issue Summary

**Critical Issues Found:**
1. ❌ Music file returns 403 Forbidden (music not playing)
2. ❌ Audio mute button doesn't work
3. ⚠️ Firebase/Firestore connection blocked by client

**Working Features:**
- ✅ Site loads
- ✅ Sound effects trigger correctly
- ✅ Game renders and plays

---

## Error 1: Music File 403 Forbidden (CRITICAL)

**Error Message:**
```
GET https://dev.nonx.standingtiger.com/assets/audio/music/NonexFullSong.mp3 403 (Forbidden)
```

**Appears:** 2 times in console

**Impact:**
- No background music plays
- Audio mute button has nothing to mute (music-related)
- Game is silent except for sound effects

**Status:** CRITICAL - Music file not deployed to S3

---

## Error 2: NotSupportedError - No Audio Sources

**Error Message:**
```
game.html:8612 Uncaught (in promise) NotSupportedError: The element has no supported sources.
```

**Location:** game.html line 8612

**Impact:**
- HTML5 audio element cannot play (no valid source)
- Direct consequence of Error 1 (music file 403)

**Status:** CRITICAL - Caused by music file missing

---

## Error 3: Firebase/Firestore Connection Blocked

**Error Message:**
```
POST https://firestore.googleapis.com/google.firestore.v1.Firestore/Listen/channel...
net::ERR_BLOCKED_BY_CLIENT
```

**Location:** webchannel_connection.ts:287

**Error Stack:** Very long Firebase/Firestore connection error chain

**Impact:**
- Leaderboard may not load or update
- Score submission may fail
- Firebase real-time features blocked

**Status:** WARNING - Likely browser extension (ad blocker) blocking Firebase

**Note:** This is CLIENT-SIDE blocking (user's browser), not a server/deployment issue

---

## Root Cause Analysis

### Issue 1 & 2: Music File Missing (403 Forbidden)

**Root Cause:** GitHub Actions workflow excludes music files from deployment

**File:** `.github/workflows/deploy-aws.yml`

**Line 66:**
```yaml
--exclude "assets/audio/music/*"
```

**Why This Was Done:**
- Music files are typically large (~5-10 MB)
- Exclusion was likely added to:
  - Speed up deployments
  - Reduce S3 storage costs
  - Avoid unnecessary file transfers

**Problem:**
The game code expects music file to exist at:
```
/assets/audio/music/NonexFullSong.mp3
```

But the deployment workflow specifically excludes this directory, so the file never gets deployed to S3.

**Result:**
- CloudFront serves 403 Forbidden (file doesn't exist in S3 bucket)
- Audio element has no valid source
- Music doesn't play
- Mute button has nothing to control

---

### Issue 3: Firebase Blocked by Client

**Root Cause:** Browser extension or ad blocker blocking Firebase requests

**Likely Culprits:**
- Ad blocker (uBlock Origin, AdBlock Plus, etc.)
- Privacy extension (Privacy Badger, Ghostery, etc.)
- Tracking blocker (Brave browser, Firefox tracking protection, etc.)
- Corporate firewall/proxy

**Why Firebase Gets Blocked:**
- Firebase uses Google domains (firestore.googleapis.com)
- Some ad blockers treat Google services as tracking/analytics
- Looks like analytics/tracking to browser extensions

**Not a Deployment Issue:**
- This is CLIENT-SIDE blocking (ERR_BLOCKED_BY_CLIENT)
- Server/AWS deployment is working correctly
- Would need to test with ad blockers disabled

---

## Solutions

### Solution 1: Deploy Music Files to S3 (CRITICAL FIX)

**Option A: Remove music exclusion from workflow (Simple)**

Edit `.github/workflows/deploy-aws.yml` line 66:
```yaml
# BEFORE:
--exclude "assets/audio/music/*"

# AFTER:
# (remove this line entirely)
```

**Pros:**
- Simple fix (delete one line)
- Music will deploy automatically
- No code changes needed

**Cons:**
- Increases deployment time (~5-10 seconds for large music file)
- Increases S3 storage usage
- Increases CloudFront data transfer costs

---

**Option B: Remove music exclusion but optimize file size (Recommended)**

1. Remove exclusion from workflow
2. Compress music file to reduce size
3. Consider using lower bitrate MP3 (192kbps instead of 320kbps)

**File Size Comparison:**
- 320kbps MP3: ~10 MB for 4-minute song
- 192kbps MP3: ~6 MB for 4-minute song (40% smaller, minimal quality loss)
- 128kbps MP3: ~4 MB for 4-minute song (60% smaller, noticeable quality loss)

---

**Option C: Host music on CDN or separate service (Advanced)**

1. Upload music to separate CDN or audio hosting service
2. Update game code to load music from external URL
3. Keep workflow exclusion

**Pros:**
- Deployment stays fast
- S3 storage stays minimal
- Can use dedicated audio CDN (better streaming)

**Cons:**
- More complex setup
- Requires code changes
- External dependency

---

### Solution 2: Audio Mute Button (Dependent on Solution 1)

**No separate fix needed** - Once music files are deployed, the mute button should work automatically.

**Verification After Fix:**
1. Music file loads successfully
2. Music plays on game start
3. Mute button toggles music on/off
4. Sound effects still work when music is muted

---

### Solution 3: Firebase Blocked by Client (Documentation Only)

**This is NOT a bug** - It's user/environment-specific.

**Solutions for Users:**
1. Disable ad blocker for dev.nonx.standingtiger.com
2. Whitelist Firebase domains in ad blocker
3. Test in private/incognito mode (disables extensions)
4. Test in different browser

**For Production Deployment:**
- Add notice in docs about disabling ad blockers for full functionality
- Consider fallback UI if Firebase fails to load
- Add error handling for blocked Firebase requests

**No code changes needed for Phase 7 testing** - Just test with ad blockers disabled.

---

## Recommended Actions

### Immediate (Phase 7 Testing):

**Priority 1: Fix Music Deployment (CRITICAL)**
1. Edit `.github/workflows/deploy-aws.yml`
2. Remove line 66: `--exclude "assets/audio/music/*"`
3. Commit and push to dev branch
4. Wait for deployment (~15-20 seconds with music file)
5. Re-test dev site

**Priority 2: Test with Ad Blockers Disabled**
1. Disable browser ad blocker extensions
2. Test Firebase/Firestore features (leaderboard)
3. Verify score submission works
4. Document ad blocker compatibility issue

**Priority 3: Verify Music Works**
1. After redeployment, visit dev site
2. Verify music loads (check console for 403)
3. Verify music plays automatically
4. Test mute button functionality
5. Test sound effects still work

---

### Long-term Optimization:

**After Phase 7 Complete:**
1. Consider compressing music file (192kbps MP3)
2. Add loading indicator for music file (UX improvement)
3. Add error handling for failed music loads
4. Add fallback message if Firebase is blocked
5. Consider lazy-loading music (load after game starts)

---

## Testing Checklist Update

**Add to Phase 7 Priority 1 Testing:**
- [ ] ❌ Music file loads successfully (currently 403)
- [ ] ❌ Background music plays (currently silent)
- [ ] ❌ Mute button works (currently nothing to mute)
- [ ] ✅ Sound effects work (confirmed working)
- [ ] ⚠️ Test Firebase with ad blocker disabled

---

## File References

**Workflow File:** `.github/workflows/deploy-aws.yml`
- Line 66: Music exclusion

**Game Files:**
- `game.html` line 8612: Audio element error
- `game.html` line 8627: Music file load attempts

**Music File Location (Local):**
- `assets/audio/music/NonexFullSong.mp3`

**Expected URL (After Fix):**
- `https://dev.nonx.standingtiger.com/assets/audio/music/NonexFullSong.mp3`

---

**Status:** Documented - Awaiting user approval to proceed with fixes
**Next Step:** Remove music exclusion from workflow and redeploy