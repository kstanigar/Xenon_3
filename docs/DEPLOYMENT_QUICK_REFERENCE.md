# Deployment Workflow - Quick Reference
**Last Updated:** May 30, 2026
**Purpose:** Quick lookup for auto-deployment implementation

---

## Asset Paths Summary

### game.html (Desktop) - ABSOLUTE PATHS
```javascript
// Current (GitHub Pages)
playerImg.src = "/Xenon_3/player.webp";
sfx.playerBullet = new Audio("/Xenon_3/assets/audio/sfx/playerBullet.mp3");

// Required for AWS S3 bucket root
playerImg.src = "/player.webp";
sfx.playerBullet = new Audio("/assets/audio/sfx/playerBullet.mp3");
```

### game_mobile.html (Mobile) - RELATIVE PATHS ✓
```javascript
// Already AWS-compatible
playerImg.src = "player.webp";
sfx.playerBullet = new Audio("assets/audio/sfx/playerBullet.mp3");
```

---

## S3 Sync Command

### With Music Files (Slower)
```bash
aws s3 sync . s3://non-x.com \
  --exclude ".git/*" \
  --exclude ".github/*" \
  --exclude "docs/*" \
  --exclude "backups/*" \
  --exclude "scripts/*" \
  --exclude "*.md" \
  --exclude ".DS_Store" \
  --delete
```
**Time**: 5-10 minutes (first run), 2-5 minutes (subsequent)

### Without Music Files (Faster) - RECOMMENDED
```bash
aws s3 sync . s3://non-x.com \
  --exclude ".git/*" \
  --exclude ".github/*" \
  --exclude "docs/*" \
  --exclude "backups/*" \
  --exclude "scripts/*" \
  --exclude "assets/audio/music/*" \
  --exclude "*.md" \
  --exclude ".DS_Store" \
  --delete
```
**Time**: 1-2 minutes (all runs)

---

## CloudFront Cache Invalidation

```bash
aws cloudfront create-invalidation \
  --distribution-id E1234ABCD5678 \
  --paths "/*"
```

Replace `E1234ABCD5678` with actual distribution ID from AWS Console.

---

## GitHub Workflow Template

File: `.github/workflows/deploy-aws.yml`

```yaml
name: Deploy to AWS S3

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      - name: Sync to S3
        run: |
          aws s3 sync . s3://non-x.com \
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

      - name: Verify assets exist
        run: |
          echo "Verifying critical files exist..."
          test -f game.html || exit 1
          test -f game_mobile.html || exit 1
          test -f index.html || exit 1
          test -d assets/audio/sfx || exit 1
          echo "✓ All critical files present"
```

---

## GitHub Secrets Required

Add to: Repository → Settings → Secrets and variables → Actions

| Secret Name | Value | Example |
|------------|-------|---------|
| AWS_ACCESS_KEY_ID | IAM access key | AKIAIOSFODNN7EXAMPLE |
| AWS_SECRET_ACCESS_KEY | IAM secret key | wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY |
| CLOUDFRONT_DISTRIBUTION_ID | CloudFront dist ID | E1234ABCD5678 |

---

## Files to Update for AWS Deployment

### 1. game.html (Lines 915-990)
- [x] Sprites: Change `/Xenon_3/*.webp` to `/` (optional if standardizing)
- [x] SFX: Change `/Xenon_3/assets/` to `/assets/`
- [x] Music: Change `/Xenon_3/assets/` to `/assets/`

### 2. Audio Upload (One-time)
```bash
# Upload music files once to S3
aws s3 sync assets/audio/music/ s3://non-x.com/assets/audio/music/ \
  --exclude ".DS_Store"
```

### 3. DNS Records (One-time)
- Create Route 53 A record (root): Alias to CloudFront distribution
- Create Route 53 A record (www): Alias to CloudFront distribution

---

## Files NOT to Sync to S3

```
.git/                  # Repository history (not needed in production)
.github/               # Workflow definitions
docs/                  # Internal documentation
backups/               # Backup files
scripts/               # Development scripts
*.md                   # README, documentation
*.htm                  # HTML exports from web
*.docx, *.pdf          # Documents
.DS_Store              # macOS metadata
```

---

## Asset Inventory

### HTML Files (600 KB total)
- index.html (97 KB) - Main menu
- game.html (~280 KB) - Desktop version
- game_mobile.html (~280 KB) - Mobile version

### Sprite Images (850 KB total) - IN SYNC
- player.webp (4 KB)
- enemy*.webp (2-70 KB each, 12 files)
- boss*.webp (25-108 KB each, 3 files)

### Sound Effects (35 KB) - IN SYNC
- playerBullet.mp3
- playerHit.mp3
- playerDead.mp3
- enemyDead.mp3
- bossIntro.mp3
- powerUp.mp3

### Background Music (59 MB) - MANUAL UPLOAD
- NonexFullSong.mp3 (4.6 MB) - Default
- SystemOverload.mp3 (12.8 MB)
- VastUniverse.mp3 (13.6 MB)
- VoidOfEchoes.mp3 (9.9 MB)
- Ximer_EE.mp3 (9.8 MB)
- Rift.mp3 (varies)

---

## Workflow Setup Steps

1. **Create file**: `.github/workflows/deploy-aws.yml`
2. **Add secrets**: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, CLOUDFRONT_DISTRIBUTION_ID
3. **Test on branch**: Create feature branch, push, verify workflow runs (won't deploy)
4. **Update paths** (if needed): game.html lines 915-990
5. **Merge to main**: Auto-deployment triggers
6. **Monitor**: Check GitHub Actions logs for success/failure

---

## Deployment Timing

- **First deployment**: 3-5 minutes (includes all assets)
- **Subsequent deployments**: 1-2 minutes (with music excluded)
- **CloudFront cache clear**: < 5 minutes (automatic)
- **DNS propagation**: 5-60 minutes (one-time after domain setup)

---

## Troubleshooting

### Game won't load after deployment
- Check asset paths in game.html (should use `/` not `/Xenon_3/`)
- Verify S3 bucket policy allows public read access
- Check CloudFront distribution is enabled and pointing to S3
- Invalidate CloudFront cache: `aws cloudfront create-invalidation --distribution-id E1234ABCD5678 --paths "/*"`

### Audio not playing
- Verify audio files exist in S3: `aws s3 ls s3://non-x.com/assets/audio/sfx/`
- Check browser console for CORS errors
- Verify audio MIME types are correct (application/x-mpeg)

### Deployment workflow fails
- Check GitHub Actions logs for specific error
- Verify AWS credentials are correct in Secrets
- Verify distribution ID is correct
- Test AWS CLI locally: `aws s3 ls` (should work if credentials correct)

### CloudFront shows old content
- Invalidation cache hasn't propagated yet (wait 5 minutes)
- Hard refresh browser: `Cmd+Shift+R` or `Ctrl+Shift+F5`
- Check CloudFront distribution status (should be "Enabled")

---

## Cost Estimate

- **Route 53 Hosted Zone**: $0.50/month
- **S3 Storage** (~100 MB): $0.10/month
- **S3 Requests**: $0.01/month
- **CloudFront Data Transfer**: $0.50-2.00/month
- **CloudFront Requests**: $0.10/month
- **ACM SSL Certificate**: FREE (auto-renewing)
- **Total Monthly**: $1-3/month
- **Total Annual**: $30-50/year (+ $12-15 domain)

---

## Security Best Practices

1. **Never commit AWS credentials** - Use GitHub Secrets only
2. **IAM principle of least privilege** - Only S3 + CloudFront permissions
3. **Use separate IAM user** - Create `github-actions-deploy` user for CI/CD
4. **Rotate keys periodically** - Regenerate if compromised
5. **Enable S3 versioning** - Allows rollback if needed
6. **Monitor CloudFront logs** - Detect any unusual traffic patterns

---

## References

- Full analysis: `/docs/AUTO_DEPLOYMENT_ANALYSIS.md`
- AWS migration plan: `/docs/AWS_DEPLOYMENT_PLAN.md`
- File structure: `/docs/FILE_STRUCTURE.md`
- GitHub Workflows: `/.github/workflows/*.yml`