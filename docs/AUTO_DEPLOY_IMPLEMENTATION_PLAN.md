# Auto-Deployment Implementation Plan

**Created:** May 30, 2026
**Effort:** 2.5-3.5 hours
**Risk:** Low (tested on feature branch first)

## Task Checklist

### Phase 1: AWS Credentials Setup (15 min)
- [ ] 1.1 Create IAM user `github-actions-deploy`
- [ ] 1.2 Attach inline policy (S3 + CloudFront permissions)
- [ ] 1.3 Generate access keys
- [ ] 1.4 Add GitHub secrets (3 required)

### Phase 2: Create Workflow File (30 min)
- [ ] 2.1 Create `.github/workflows/deploy-aws.yml`
- [ ] 2.2 Verify YAML syntax
- [ ] 2.3 Test on feature branch
- [ ] 2.4 Confirm S3 sync works

### Phase 3: Fix Asset Paths ✅ COMPLETE (April 2026)
- [x] 3.1 Update game.html lines 915-990 (24 paths) - DONE (commit fd7d0d6)
- [x] 3.2 Test local paths - VERIFIED
- [x] 3.3 Verify on staging - LIVE on AWS (no issues)

### Phase 4: Production Deploy (15 min)
- [ ] 4.1 Merge to main
- [ ] 4.2 Monitor workflow execution
- [ ] 4.3 Verify CloudFront invalidation
- [ ] 4.4 Test live site

### Phase 5: Post-Deploy (30 min)
- [ ] 5.1 Update Firebase allowed domains
- [ ] 5.2 Update GA4 data stream
- [ ] 5.3 Test all game features
- [ ] 5.4 Monitor for 24 hours

---

## ~~Critical Issue: Asset Path Fix Required~~ ✅ RESOLVED

### Problem → FIXED
**File:** `game.html`
**Lines:** 915-990 (24 references)
**Issue:** Absolute paths with `/Xenon_3/` prefix won't work on S3 root
**Status:** ✅ RESOLVED in commit fd7d0d6 (April 2026, AWS migration)

### ~~Current Code (BROKEN on AWS)~~ FIXED
```javascript
// BEFORE (lines 915-942) - BROKEN
playerImg.src = "/Xenon_3/player.webp";
enemyImgs.Standard.src = "/Xenon_3/Enemy_Standard.webp";
bossImgs.boss_Green.src = "/Xenon_3/boss_Green.webp";
```

### Current Code (Works on both GitHub Pages & AWS) ✅
```javascript
// AFTER (lines 915-962) - WORKING
playerImg.src = "player.webp";  // Relative path
enemyImg1.src = "enemy.webp";
bossImg.src = "Boss.webp";
// All 24 paths now use relative paths
```

### Implementation → COMPLETE
**Search:** `/Xenon_3/` → 0 matches found (verified May 30, 2026)
**Replace:** All instances removed in April 2026
**Files:** `game.html` (game_mobile.html already used relative paths)
**Lines affected:** 24 total (all fixed)
**Verification:** Live site at https://nonx.standingtiger.com loads all sprites correctly

---

## GitHub Actions Workflow

### File: `.github/workflows/deploy-aws.yml`

```yaml
name: Deploy to AWS S3

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-2

      - name: Sync files to S3 (excluding music for speed)
        run: |
          aws s3 sync . s3://nonx.standingtiger.com \
            --exclude ".git/*" \
            --exclude ".github/*" \
            --exclude "docs/*" \
            --exclude "backups/*" \
            --exclude "scripts/*" \
            --exclude "assets/audio/music/*" \
            --exclude "*.md" \
            --exclude ".DS_Store" \
            --delete

      - name: Invalidate CloudFront cache
        run: |
          aws cloudfront create-invalidation \
            --distribution-id ${{ secrets.CLOUDFRONT_DISTRIBUTION_ID }} \
            --paths "/*"

      - name: Deployment complete
        run: echo "✅ Deployed to https://nonx.standingtiger.com"
```

**Lines:** 37
**Trigger:** Push to main
**Duration:** 1-2 minutes (without music), 5+ minutes (with music)

---

## GitHub Secrets Configuration

Navigate to: **Settings > Secrets and variables > Actions > New repository secret**

| Secret Name | Value Source | Example |
|-------------|--------------|---------|
| `AWS_ACCESS_KEY_ID` | IAM user access key | AKIAIOSFODNN7EXAMPLE |
| `AWS_SECRET_ACCESS_KEY` | IAM user secret key | wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY |
| `CLOUDFRONT_DISTRIBUTION_ID` | CloudFront console | E1234ABCD5678 |

---

## IAM Policy (Minimal Permissions)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:DeleteObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::nonx.standingtiger.com",
        "arn:aws:s3:::nonx.standingtiger.com/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": "cloudfront:CreateInvalidation",
      "Resource": "*"
    }
  ]
}
```

---

## Potential Issues & Solutions

### ~~Issue 1: Asset Path Mismatch~~ ✅ RESOLVED
**Error:** 404 on all sprites when deployed to S3
**Cause:** Absolute paths `/Xenon_3/player.webp` don't exist on S3 root
**Status:** FIXED in commit fd7d0d6 (April 2026)
**Solution Applied:** All paths changed to relative `player.webp`
**Verification:** Live site loads all sprites correctly (no 404 errors)

### Issue 2: Music Files Slow Deployment
**Error:** Workflow takes 5+ minutes
**Cause:** 59 MB of music files sync every deployment
**Solution:** Exclude `assets/audio/music/*` from sync (upload once manually)
**Detection:** Workflow duration > 3 minutes
**Fix time:** Add exclude line (already in workflow above)

### Issue 3: CloudFront Cache Not Cleared
**Error:** Old version still shows after deployment
**Cause:** CloudFront serves cached content
**Solution:** Invalidation step in workflow (already included)
**Detection:** Changes don't appear live
**Fix time:** N/A (prevented by workflow design)

### Issue 4: GitHub Secrets Missing
**Error:** `Error: Credentials could not be loaded`
**Cause:** Secrets not configured in repo settings
**Solution:** Add all 3 secrets before first deploy
**Detection:** Workflow fails at "Configure AWS credentials" step
**Fix time:** 5 minutes

### Issue 5: Wrong S3 Bucket Region
**Error:** `PermanentRedirect` or `NoSuchBucket`
**Cause:** Workflow uses wrong region (currently set to us-east-2)
**Solution:** Verify S3 bucket region in AWS console, update workflow
**Detection:** S3 sync fails with redirect error
**Fix time:** 2 minutes (change region in workflow line 15)

---

## Testing Protocol

### Feature Branch Test
```bash
# 1. Create test branch
git checkout -b feature/test-auto-deploy

# 2. Make small change (e.g., update version number in index.html comment)
# Edit index.html line 1: <!-- v1.0.1 test deploy -->

# 3. Commit and push
git add .
git commit -m "test: verify auto-deployment workflow"
git push -u origin feature/test-auto-deploy

# 4. Check GitHub Actions tab - workflow should NOT run (only main branch)

# 5. Merge to main via PR
# 6. Monitor workflow execution
# 7. Verify site updated (check version comment in source)
```

### Verification Checklist
After first auto-deploy:
- [ ] Workflow completed successfully (green checkmark)
- [ ] S3 sync uploaded files (check count in logs)
- [ ] CloudFront invalidation created (check invalidation ID in logs)
- [ ] Site loads at https://nonx.standingtiger.com
- [ ] All sprites load (no 404s in console)
- [ ] Game launches (test desktop + mobile)
- [ ] Leaderboard works
- [ ] Analytics tracks events

---

## Code Changes Required

### File 1: `game.html`

**Change 1: Line 915**
```javascript
// BEFORE
playerImg.src = "/Xenon_3/player.webp";

// AFTER
playerImg.src = "player.webp";
```

**Change 2-24: Lines 919-942**
Replace all 23 sprite paths:
```javascript
// BEFORE (Lines 919-942)
enemyImgs.Standard.src = "/Xenon_3/Enemy_Standard.webp";
enemyImgs.Red.src = "/Xenon_3/Enemy_Red.webp";
enemyImgs.Purple.src = "/Xenon_3/Enemy_Purple.webp";
bossImgs.boss_Green.src = "/Xenon_3/boss_Green.webp";
bossImgs.boss_Red.src = "/Xenon_3/boss_Red.webp";
bossImgs.boss_Purple.src = "/Xenon_3/boss_Purple.webp";
barrierImgs.barrier_Standard.src = "/Xenon_3/Barrier_Standard.webp";
barrierImgs.barrier_Red.src = "/Xenon_3/Barrier_Red.webp";
barrierImgs.barrier_Purple.src = "/Xenon_3/Barrier_Purple.webp";
powerupImgs.health.src = "/Xenon_3/Powerup_Health.webp";
powerupImgs.shield.src = "/Xenon_3/Powerup_Shield.webp";
powerupImgs.doubleLaser.src = "/Xenon_3/Powerup_DoubleLaser.webp";
powerupImgs.tripleLaser.src = "/Xenon_3/Powerup_TripleLaser.webp";
powerupImgs.quadLaser.src = "/Xenon_3/Powerup_QuadLaser.webp";
// ... 9 more lines

// AFTER (Lines 919-942)
enemyImgs.Standard.src = "Enemy_Standard.webp";
enemyImgs.Red.src = "Enemy_Red.webp";
enemyImgs.Purple.src = "Enemy_Purple.webp";
bossImgs.boss_Green.src = "boss_Green.webp";
bossImgs.boss_Red.src = "boss_Red.webp";
bossImgs.boss_Purple.src = "boss_Purple.webp";
barrierImgs.barrier_Standard.src = "Barrier_Standard.webp";
barrierImgs.barrier_Red.src = "Barrier_Red.webp";
barrierImgs.barrier_Purple.src = "Barrier_Purple.webp";
powerupImgs.health.src = "Powerup_Health.webp";
powerupImgs.shield.src = "Powerup_Shield.webp";
powerupImgs.doubleLaser.src = "Powerup_DoubleLaser.webp";
powerupImgs.tripleLaser.src = "Powerup_TripleLaser.webp";
powerupImgs.quadLaser.src = "Powerup_QuadLaser.webp";
// ... 9 more lines (all /Xenon_3/ removed)
```

**Automated Fix:**
```bash
# Use sed to replace all occurrences
sed -i '' 's|/Xenon_3/||g' game.html

# Verify changes
grep -n "\.src = " game.html | head -30
```

### File 2: `.github/workflows/deploy-aws.yml`

**Action:** Create new file (37 lines, shown above in workflow section)

---

## Execution Timeline

| Phase | Task | Duration | Blocker |
|-------|------|----------|---------|
| 1 | Create IAM user + keys | 10 min | AWS console access |
| 1 | Add GitHub secrets | 5 min | Repo admin access |
| 2 | Create workflow file | 15 min | - |
| 2 | Test on feature branch | 15 min | GitHub Actions enabled |
| ~~3~~ | ~~Fix asset paths (game.html)~~ | ~~20 min~~ | ✅ COMPLETE |
| ~~3~~ | ~~Test paths locally~~ | ~~10 min~~ | ✅ COMPLETE |
| 4 | Merge to main | 5 min | PR approval |
| 4 | Monitor deployment | 10 min | Workflow execution |
| 5 | Update Firebase/GA4 | 15 min | Firebase/GA4 console |
| 5 | Full site testing | 15 min | - |
| **TOTAL** | | **1h 30min** | (30 min faster - Phase 3 complete) |

**Buffer time:** +15-30 min for troubleshooting

---

## Success Criteria

**Auto-deployment is successful when:**
1. ✅ Workflow runs on every push to main
2. ✅ Files sync to S3 in 1-2 minutes
3. ✅ CloudFront cache invalidates automatically
4. ✅ Live site updates within 3 minutes of push
5. ✅ All game features work (sprites, audio, leaderboard)
6. ✅ No 404 errors in browser console
7. ✅ Analytics tracking continues working

---

## Rollback Plan

If auto-deployment breaks production:

**Immediate (< 5 minutes):**
```bash
# Disable workflow
mv .github/workflows/deploy-aws.yml .github/workflows/deploy-aws.yml.disabled

# Manual fix + deploy
# Fix issue locally
aws s3 sync . s3://nonx.standingtiger.com --exclude ... --delete
aws cloudfront create-invalidation --distribution-id E1234... --paths "/*"
```

**Long-term (< 1 hour):**
1. Revert problematic commit
2. Fix issue on feature branch
3. Test thoroughly
4. Re-enable workflow
5. Merge fix to main

---

## Documentation Updates Post-Implementation

Files to update after successful deploy:
- [ ] AWS_DEPLOYMENT_STATUS.md (mark auto-deploy active)
- [ ] README.md (note auto-deployment enabled)
- [ ] This file (mark tasks complete)

---

**Status:** Ready for implementation
**Approval:** Required before Phase 1
**Dependencies:** AWS credentials, GitHub repo admin access