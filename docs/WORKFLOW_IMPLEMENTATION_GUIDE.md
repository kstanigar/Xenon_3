# GitHub Actions Deployment Workflow - Implementation Guide
**Date Created:** May 30, 2026
**Status:** Ready for implementation
**Estimated Time:** 2-3 hours total

---

## Overview

This guide provides step-by-step instructions to implement automated deployment from GitHub to AWS S3 + CloudFront.

**Prerequisites:**
- AWS account with S3 bucket created and CloudFront distribution enabled
- GitHub repository with write access
- AWS CLI installed locally (for testing)

---

## Phase 1: GitHub Secrets Setup (15 minutes)

### Step 1.1: Get AWS Credentials

1. Log into AWS Console
2. Navigate to: IAM → Users → Create user
3. User name: `github-actions-deploy`
4. Click "Next"
5. Attach policy (select one):
   - Option A: `AmazonS3FullAccess` + `CloudFrontFullAccess` (permissive)
   - Option B: Use custom policy (recommended for security):

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "S3Access",
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:DeleteObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::non-x.com",
        "arn:aws:s3:::non-x.com/*"
      ]
    },
    {
      "Sid": "CloudFrontInvalidation",
      "Effect": "Allow",
      "Action": "cloudfront:CreateInvalidation",
      "Resource": "*"
    }
  ]
}
```

6. Click "Next" → "Create user"
7. Click the new user name
8. Go to "Security credentials" tab
9. Click "Create access key"
10. Select "Application running outside AWS"
11. Click "Next"
12. Click "Create access key"
13. **IMPORTANT**: Save the access key ID and secret key somewhere safe (won't show again)

### Step 1.2: Get CloudFront Distribution ID

1. AWS Console → CloudFront → Distributions
2. Find your distribution for `non-x.com`
3. Copy the "Distribution ID" (e.g., `E1234ABCD5678`)

### Step 1.3: Add Secrets to GitHub

1. Open your GitHub repository
2. Go to: Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Add three secrets:

**Secret 1:**
- Name: `AWS_ACCESS_KEY_ID`
- Value: `AKIA...` (from Step 1.1, step 13)
- Click "Add secret"

**Secret 2:**
- Name: `AWS_SECRET_ACCESS_KEY`
- Value: `wJal...` (from Step 1.1, step 13)
- Click "Add secret"

**Secret 3:**
- Name: `CLOUDFRONT_DISTRIBUTION_ID`
- Value: `E1234ABCD5678` (from Step 1.2)
- Click "Add secret"

**Verification**: Secrets should appear in the list (values hidden with dots)

---

## Phase 2: Create Workflow File (30 minutes)

### Step 2.1: Understand Current Structure

Existing workflows are in: `/.github/workflows/`
- `integrity-check.yml` - Function validation
- `test.yml` - HTML validation

You will add: `deploy-aws.yml` - S3 + CloudFront deployment

### Step 2.2: Create the Workflow File

Create new file: `.github/workflows/deploy-aws.yml`

```yaml
name: Deploy to AWS S3

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    name: Deploy game to AWS S3 + CloudFront

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      - name: List files to sync
        run: |
          echo "Files to be synced:"
          find . -maxdepth 1 -type f \( -name "*.html" -o -name "*.webp" \) | sort
          echo ""
          echo "Audio files to be synced:"
          find assets/audio/sfx -type f 2>/dev/null | sort

      - name: Sync to S3
        run: |
          echo "Starting S3 sync..."
          aws s3 sync . s3://non-x.com \
            --exclude ".git/*" \
            --exclude ".github/*" \
            --exclude "docs/*" \
            --exclude "backups/*" \
            --exclude "scripts/*" \
            --exclude "assets/audio/music/*" \
            --exclude "*.md" \
            --exclude "*.htm" \
            --exclude "*.docx" \
            --exclude "*.pdf" \
            --exclude ".DS_Store" \
            --exclude "*.tmp" \
            --exclude "*.log" \
            --delete \
            --cache-control "max-age=31536000" \
            --metadata-directive REPLACE \
            --acl public-read
          echo "S3 sync complete"

      - name: Verify assets in S3
        run: |
          echo "Verifying critical files in S3..."
          aws s3 ls s3://non-x.com/index.html || exit 1
          aws s3 ls s3://non-x.com/game.html || exit 1
          aws s3 ls s3://non-x.com/game_mobile.html || exit 1
          aws s3 ls s3://non-x.com/assets/audio/sfx/ || exit 1
          echo "✓ All critical files verified in S3"

      - name: Invalidate CloudFront cache
        run: |
          echo "Invalidating CloudFront cache..."
          aws cloudfront create-invalidation \
            --distribution-id ${{ secrets.CLOUDFRONT_DISTRIBUTION_ID }} \
            --paths "/*" \
            --query 'Invalidation.Id' \
            --output text
          echo "CloudFront invalidation requested"

      - name: Deployment summary
        run: |
          echo "=========================================="
          echo "✓ Deployment Complete!"
          echo "=========================================="
          echo "Website: https://non-x.com"
          echo "S3 Bucket: s3://non-x.com"
          echo "CloudFront: Check AWS Console for distribution status"
          echo "Note: CloudFront cache clears in ~5 minutes"
          echo "=========================================="
```

### Step 2.3: Save and Commit the Workflow

1. Save the file as `.github/workflows/deploy-aws.yml`
2. Commit to your repository:
   ```bash
   git add .github/workflows/deploy-aws.yml
   git commit -m "ci: add AWS S3 deployment workflow"
   git push origin main
   ```

---

## Phase 3: Test Deployment on Feature Branch (30 minutes)

### Step 3.1: Create Test Branch

```bash
git checkout -b test/deployment-workflow
git push origin test/deployment-workflow
```

### Step 3.2: Make a Small Change

Edit `game.html` or `game_mobile.html` (just a comment change):

```javascript
// Add this comment to game.html (near line 1)
// AWS deployment test - May 30, 2026
```

### Step 3.3: Commit and Push

```bash
git add game.html
git commit -m "test: deployment workflow trigger"
git push origin test/deployment-workflow
```

### Step 3.4: Verify Workflow Runs (But Doesn't Deploy)

1. Go to GitHub → Actions
2. You should see workflow running but NOT deploying (only main branch triggers deploy)
3. Wait for workflow to complete
4. If all steps pass (except deploy), you're good
5. If workflow fails, check logs for error details

### Step 3.5: Clean Up Test Branch

```bash
git checkout main
git branch -D test/deployment-workflow
git push origin --delete test/deployment-workflow
```

---

## Phase 4: Update Asset Paths for AWS (Optional but Recommended)

### Step 4.1: Understand Current Paths

**game.html** uses absolute paths with `/Xenon_3/`:
```javascript
playerImg.src = "/Xenon_3/player.webp";
sfx.playerBullet = new Audio("/Xenon_3/assets/audio/sfx/playerBullet.mp3");
```

**game_mobile.html** already uses relative paths:
```javascript
playerImg.src = "player.webp";
sfx.playerBullet = new Audio("assets/audio/sfx/playerBullet.mp3");
```

### Step 4.2: Update game.html

Option A: Change to relative paths (RECOMMENDED)
- Simpler standardization
- Works on GitHub Pages and AWS
- Fewer path differences

Option B: Change to absolute paths without `/Xenon_3/`
- Works with S3 bucket root deployment
- Different from mobile version

**Recommended Approach**: Use relative paths like mobile version

**Files to change in game.html:**

1. Lines 915-930: Sprite image paths
2. Lines 934-962: Red/Purple variant paths
3. Lines 970-975: SFX paths
4. Lines 980, 985: Music paths

**From:**
```javascript
playerImg.src = "/Xenon_3/player.webp";
```

**To:**
```javascript
playerImg.src = "player.webp";
```

**From:**
```javascript
sfx.playerBullet = new Audio("/Xenon_3/assets/audio/sfx/playerBullet.mp3");
```

**To:**
```javascript
sfx.playerBullet = new Audio("assets/audio/sfx/playerBullet.mp3");
```

### Step 4.3: Test Changes Locally

1. Open game.html in browser (or via local web server)
2. Verify sprites load
3. Start a game, verify sounds play
4. Test mobile version too

### Step 4.4: Commit Changes

```bash
git checkout -b feature/standardize-asset-paths
# Make the path changes...
git add game.html
git commit -m "refactor: standardize asset paths for AWS deployment

- Changed game.html to use relative paths (like game_mobile.html)
- Removes /Xenon_3/ prefix for S3 bucket root compatibility
- Works on GitHub Pages and AWS CloudFront
- All sprite and audio paths updated"
git push origin feature/standardize-asset-paths
```

5. Create pull request and merge after testing

---

## Phase 5: Deploy to Production (15 minutes)

### Step 5.1: Verify Everything is Ready

Before deploying:
- [ ] AWS S3 bucket created and versioning enabled
- [ ] CloudFront distribution created and enabled
- [ ] SSL certificate issued (ACM)
- [ ] Route 53 DNS records created (optional, for custom domain)
- [ ] GitHub Secrets configured (3 secrets)
- [ ] Deployment workflow file created
- [ ] Asset paths updated (if doing Phase 4)
- [ ] Local testing successful

### Step 5.2: Make a Real Change (or just Merge)

If you just want to deploy current code:
```bash
git log --oneline -1  # Check last commit
# Should see your latest changes
```

Or make a meaningful change:
```bash
git checkout -b release/v1.0-aws-deployment
# Make any final tweaks
git add .
git commit -m "release: ready for AWS production deployment"
git push origin release/v1.0-aws-deployment
```

### Step 5.3: Create Pull Request

1. Go to GitHub
2. Create Pull Request from your branch → main
3. Add description: "Initial AWS production deployment"
4. Get approved if needed (or self-approve)
5. Merge to main

### Step 5.4: Watch Deployment

1. Go to GitHub → Actions
2. Watch workflow execute:
   - Step 1: Checkout code
   - Step 2: Configure AWS credentials
   - Step 3: List files to sync
   - Step 4: Sync to S3 (this will take 1-5 minutes)
   - Step 5: Verify assets in S3
   - Step 6: Invalidate CloudFront cache
   - Step 7: Deployment summary

3. All steps should show green checkmarks ✓

### Step 5.5: Test Production Deployment

After workflow completes:

1. **Check S3 files:**
   ```bash
   aws s3 ls s3://non-x.com/ --recursive | head -20
   ```

2. **Test CloudFront URL:**
   - Open: `https://d1234abcd.cloudfront.net` (replace with your distribution domain)
   - Should load index.html menu
   - Click "Play Game"
   - Verify sprites load
   - Start a game, verify sounds play

3. **Test custom domain (if DNS configured):**
   - Open: `https://non-x.com`
   - Same tests as above

4. **Check SSL certificate:**
   - Click lock icon in browser address bar
   - Should show valid certificate
   - No warnings or errors

5. **Verify analytics:**
   - Open browser DevTools → Network tab
   - Start a game
   - Look for `google-analytics.com` requests
   - Should see GA4 events firing

---

## Phase 6: Monitor and Troubleshoot (Ongoing)

### Regular Monitoring

**GitHub Actions:**
- Monitor workflow runs after each push to main
- Check for failures in Actions tab
- All steps should complete in < 5 minutes

**AWS CloudFront:**
- Monitor cache hit rate (should be > 80%)
- Monitor 4xx/5xx errors (should be < 1%)
- Check data transfer costs (should be < $3/month)

### Common Issues and Solutions

#### Issue: Workflow fails with "Access Denied"
**Cause**: AWS credentials incorrect or expired
**Solution**:
1. Verify secrets in GitHub (Settings → Secrets)
2. Regenerate AWS access keys if needed
3. Update GitHub secrets with new keys

#### Issue: Game loads but no sprites visible
**Cause**: Asset paths incorrect
**Solution**:
1. Check asset paths in game.html (should be relative)
2. Verify files exist in S3: `aws s3 ls s3://non-x.com/player.webp`
3. Check CloudFront → Origins → check S3 origin is correct
4. Invalidate cache: `aws cloudfront create-invalidation --distribution-id E1234ABCD5678 --paths "/*"`

#### Issue: Audio not playing
**Cause**: Audio files not uploaded or CORS issue
**Solution**:
1. Verify audio files in S3: `aws s3 ls s3://non-x.com/assets/audio/sfx/`
2. Check MIME types are correct (should be audio/mpeg)
3. Check CloudFront CORS policy allows audio requests

#### Issue: CloudFront shows old content
**Cause**: Cache not invalidated
**Solution**:
1. Force browser refresh: Cmd+Shift+R or Ctrl+Shift+F5
2. Wait 5 minutes for CloudFront cache to clear
3. Check invalidation status: `aws cloudfront list-invalidations --distribution-id E1234ABCD5678`

---

## Phase 7: Post-Deployment Tasks

### One-Time Setup

1. **Update README**
   ```markdown
   - Change demo link from GitHub Pages to custom domain
   - Add deployment info section
   ```

2. **Update external references**
   - Portfolio website
   - Social media links
   - Any other sites linking to game

3. **Update Firebase/Analytics**
   - Add custom domain to allowed referrers
   - Update GA4 property if needed

4. **Disable GitHub Pages** (optional)
   - Remove GitHub Pages from repository settings
   - Alternatively, set up redirect to custom domain

### Ongoing Maintenance

1. **After each code push to main:**
   - GitHub Actions will auto-deploy
   - No manual steps needed
   - Workflow completes in 2-5 minutes

2. **Monitoring checklist (weekly):**
   - [ ] Check GitHub Actions logs for errors
   - [ ] Verify game loads on custom domain
   - [ ] Check CloudFront cache hit rate
   - [ ] Review AWS cost (should be < $3/month)

---

## Rollback Plan (If Needed)

If something breaks after deployment:

### Quick Rollback (< 5 minutes)

1. **Identify the bad commit:**
   ```bash
   git log --oneline -5  # See recent commits
   ```

2. **Revert the commit:**
   ```bash
   git revert <commit-hash>  # Creates new commit that undoes changes
   git push origin main
   ```

3. **Monitor deployment:**
   - GitHub Actions auto-deploys
   - Watch workflow in Actions tab
   - Deployed in < 5 minutes

### Full Rollback (If Critical Issue)

1. **Use S3 versioning to restore previous version:**
   ```bash
   # List versions
   aws s3api list-object-versions --bucket non-x.com

   # Restore specific version
   aws s3api copy-object \
     --bucket non-x.com \
     --copy-source non-x.com/index.html?versionId=xyz123 \
     --key index.html
   ```

2. **Invalidate CloudFront cache:**
   ```bash
   aws cloudfront create-invalidation --distribution-id E1234ABCD5678 --paths "/*"
   ```

---

## Verification Checklist

After completing all phases:

- [ ] GitHub Secrets added (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, CLOUDFRONT_DISTRIBUTION_ID)
- [ ] Workflow file created (`.github/workflows/deploy-aws.yml`)
- [ ] Workflow tested on feature branch (didn't deploy)
- [ ] Asset paths updated for AWS (optional but recommended)
- [ ] Code merged to main
- [ ] Deployment workflow executed successfully
- [ ] Game loads via CloudFront URL
- [ ] Sprites and audio load correctly
- [ ] Analytics tracking working
- [ ] Mobile version works
- [ ] SSL certificate valid (no warnings)
- [ ] Custom domain resolves (if applicable)

---

## References

- AWS Deployment Plan: `/docs/AWS_DEPLOYMENT_PLAN.md`
- Auto-Deployment Analysis: `/docs/AUTO_DEPLOYMENT_ANALYSIS.md`
- Quick Reference: `/docs/DEPLOYMENT_QUICK_REFERENCE.md`
- GitHub Actions Docs: https://docs.github.com/en/actions
- AWS CLI Reference: https://aws.amazon.com/cli/

---

## Support

If you encounter issues:

1. **Check GitHub Actions logs:**
   - Repository → Actions → Click workflow → View logs
   - Look for specific error messages

2. **Check AWS CloudFront logs:**
   - AWS Console → CloudFront → Logs
   - Download and review error patterns

3. **Test AWS CLI locally:**
   ```bash
   aws s3 ls s3://non-x.com/
   aws cloudfront list-distributions
   ```

4. **Verify S3 bucket policy and CloudFront origin:**
   - AWS Console → S3 → Bucket → Permissions
   - AWS Console → CloudFront → Distributions → Origins

---

**Total Implementation Time:** 2-3 hours
**Difficulty Level:** Intermediate (requires AWS + GitHub knowledge)
**Risk Level:** Low (reversible, rollback available)

Ready to deploy? Start with Phase 1!