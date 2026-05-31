# Auto-Deployment Workflow Analysis
**Date Created:** May 30, 2026
**Last Updated:** May 30, 2026 (asset path issue marked resolved)
**Purpose:** Research codebase structure for automated AWS deployment workflow
**Status:** ANALYSIS COMPLETE - Ready for workflow implementation (no blockers)

---

## Executive Summary

The Xenon_3 codebase is well-documented and prepared for AWS deployment. Current GitHub workflows follow professional patterns with integrity checks and testing. Asset structure is dual-deployment-ready (GitHub Pages + AWS S3). Main issues identified:

1. ~~**Asset path inconsistency**~~ ✅ RESOLVED (fixed April 2026, commit fd7d0d6)
2. **Missing deployment automation**: No AWS CI/CD workflow exists yet
3. **Large audio files**: 20MB in `assets/audio/` will impact S3 sync performance (mitigation: exclude from workflow)
4. **GitHub secrets**: Need AWS credentials and CloudFront distribution ID setup

**Note:** Asset path analysis below reflects historical state. All `/Xenon_3/` paths have been fixed.

---

## 1. CURRENT WORKFLOW PATTERNS

### Existing GitHub Actions Workflows

#### A. `/github/workflows/integrity-check.yml`
- **Trigger**: Push to main + pull requests
- **Purpose**: Verify game.html and game_mobile.html contain required functions
- **Coverage**: 96 function/pattern checks across both files
- **Pattern**: Grep-based function validation (bash scripts)

**Key checks:**
- Core game functions: `startFromCard()`, `playAgain()`, `playerTakeDamage()`
- Survey system: `showSurveyBanner()`, `submitSurvey()`, `dismissSurvey()`
- Leaderboard: `showFullLeaderboard()`, `closeLeaderboardModal()`
- AI Agent v1.0: `getTierMultiplier()`, `addScore()`, `increaseTier()`
- Analytics events: `game_complete`, `ai_difficulty_adjusted`, `scorecard_viewed`
- Banned patterns: `buildSurveyHTML`, `'phase'.*'standard'`

**Workflow pattern:** Simple bash checks, no external dependencies

#### B. `/github/workflows/test.yml`
- **Trigger**: All branches (push) + main/develop (pull requests)
- **Purpose**: Validate HTML, GA4 tracking, A/B testing implementation
- **Steps**:
  1. Checkout code
  2. HTML validation (npm html-validate)
  3. Google Analytics ID verification (`G-9ECFZ9JBE5`)
  4. A/B testing code presence (`ab_music_group`)

**Pattern**: Sequential validation steps, checks specific GA4 ID and feature flags

### Workflow Analysis

**Strengths:**
- Simple, maintainable bash scripts
- Clear function/pattern documentation
- No complex dependencies
- Fast execution (< 1 minute)

**Weaknesses:**
- No deployment automation
- No asset optimization checks
- No file size validation
- No S3 deployment capability

---

## 2. ASSET STRUCTURE & SYNC REQUIREMENTS

### Directory Structure

```
/Xenon_3/
├── Root-level HTML files (3 files)
│   ├── index.html                    [97 KB] Main menu
│   ├── game.html                     [~280 KB] Desktop version
│   └── game_mobile.html              [~280 KB] Mobile version
│
├── Root-level sprite images (16 files)
│   ├── player.webp                   [4 KB]
│   ├── enemy.webp - enemy4.webp      [2-70 KB each]
│   ├── Boss.webp                     [75 KB]
│   ├── *_Red.webp variants           [25-108 KB each]
│   └── *_purple.webp variants        [38-70 KB each]
│
├── assets/ (20 MB total)
│   └── audio/
│       ├── music/                    [59 MB - 6 tracks]
│       │   ├── NonexFullSong.mp3     [4.6 MB] Default
│       │   ├── SystemOverload.mp3    [12.8 MB]
│       │   ├── VastUniverse.mp3      [13.6 MB]
│       │   ├── VoidOfEchoes.mp3      [9.9 MB]
│       │   ├── Ximer_EE.mp3          [9.8 MB]
│       │   └── Rift.mp3              [varies]
│       │
│       └── sfx/                      [35 KB - 6 files]
│           ├── playerBullet.mp3
│           ├── playerHit.mp3
│           ├── playerDead.mp3
│           ├── enemyDead.mp3
│           ├── bossIntro.mp3
│           └── powerUp.mp3
│
├── docs/                             [NOT DEPLOYED]
│   ├── design/
│   ├── guides/
│   ├── memory/
│   └── summaries/
│
├── backups/                          [NOT DEPLOYED]
│   ├── 2026-04-13/
│   └── archived/
│
└── scripts/
    └── sync_paim.sh                  [Utility script]
```

### Total Size Breakdown
- **Root sprites**: ~850 KB (16 .webp files)
- **Audio assets**: ~59 MB (6 music tracks, 6 SFX)
- **HTML/config**: ~600 KB
- **Docs/backups/git**: ~134 MB (not deployed)
- **Total project**: 167 MB

---

### S3 Sync Requirements

#### Files TO SYNC (Production deployment)
```bash
# HTML files
index.html
game.html
game_mobile.html

# Sprite images (root directory)
*.webp (16 files)

# Audio assets (preserve directory structure)
assets/audio/music/*.mp3
assets/audio/sfx/*.mp3

# Configuration
.DS_Store (if necessary) - RECOMMEND EXCLUDING
```

#### Files TO EXCLUDE (do not sync)
```bash
.git/*                  # Git repository
.github/*               # Workflow definitions
docs/*                  # Documentation (keep in Git only)
backups/*               # Backup files
scripts/*               # Development scripts
*.md                    # README and documentation
*.htm                   # HTML exports
*.docx                  # Word documents
*.pdf                   # PDF files
.DS_Store              # macOS metadata
*.tmp, *.log, *.bak    # Temporary files
node_modules/*         # If npm used (currently not)
```

#### Recommended `--exclude` Patterns for `aws s3 sync`
```bash
--exclude ".git/*" \
--exclude ".github/*" \
--exclude "docs/*" \
--exclude "backups/*" \
--exclude "scripts/*" \
--exclude "*.md" \
--exclude "*.htm" \
--exclude "*.docx" \
--exclude "*.pdf" \
--exclude ".DS_Store" \
--exclude "*.tmp" \
--exclude "*.log"
```

---

## 3. ASSET LOADING PATHS ~~(Current Implementation)~~ HISTORICAL - RESOLVED ✅

**⚠️ NOTE: This section documents the ORIGINAL state (pre-April 2026). All `/Xenon_3/` paths have been fixed to relative paths in commit fd7d0d6. The analysis below is for historical reference only.**

### Desktop Version (game.html) - ORIGINAL STATE (FIXED)

**Pattern: ~~Absolute paths with `/Xenon_3/` prefix~~ → NOW RELATIVE PATHS**

#### Sprites
```javascript
// Line 915: Image assets use absolute paths (GitHub Pages compatibility)
playerImg.src = "/Xenon_3/player.webp";
enemyImg1.src = "/Xenon_3/enemy.webp";
enemyImg2.src = "/Xenon_3/enemy2.webp";
enemyImg3.src = "/Xenon_3/enemy3.webp";
enemyImg4.src = "/Xenon_3/enemy4.webp";
bossImg.src = "/Xenon_3/Boss.webp";

// Red phase variants
enemyImg1Red.src = "/Xenon_3/enemy1_Red.webp";
enemyImg2Red.src = "/Xenon_3/enemy2_Red.webp";
enemyImg3Red.src = "/Xenon_3/enemy3_Red.webp";
enemyImg4Red.src = "/Xenon_3/enemy4_Red.webp";
bossImgRed.src = "/Xenon_3/boss_Red.webp";

// Purple phase variants
enemyImg1Purple.src = "/Xenon_3/enemy1_purple.webp";
enemyImg2Purple.src = "/Xenon_3/enemy2_purple.webp";
enemyImg3Purple.src = "/Xenon_3/enemy3_purple.webp";
enemyImg4Purple.src = "/Xenon_3/enemy4_purple.webp";
bossImgPurple.src = "/Xenon_3/boss_purple.webp";
```

#### Sound Effects
```javascript
// Line 970-975: SFX using absolute paths
sfx: {
  playerBullet: new Audio("/Xenon_3/assets/audio/sfx/playerBullet.mp3"),
  playerHit: new Audio("/Xenon_3/assets/audio/sfx/playerHit.mp3"),
  playerDead: new Audio("/Xenon_3/assets/audio/sfx/playerDead.mp3"),
  enemyDead: new Audio("/Xenon_3/assets/audio/sfx/enemyDead.mp3"),
  bossIntro: new Audio("/Xenon_3/assets/audio/sfx/bossIntro.mp3"),
  powerUp: new Audio("/Xenon_3/assets/audio/sfx/powerUp.mp3")
}
```

#### Background Music
```javascript
// Line 980, 985: Music using absolute paths
var bgMusic = new Audio("/Xenon_3/assets/audio/music/NonexFullSong.mp3");
var creditsMusic = new Audio("/Xenon_3/assets/audio/music/NonexFullSong.mp3");
```

**Location in code**: Lines 904-990 in game.html

---

### Mobile Version (game_mobile.html)

**Pattern: Relative paths (no `/Xenon_3/` prefix)**

#### Sprites
```javascript
// Line 849: Image assets use relative paths (flexible deployment)
playerImg.src = "player.webp";
enemyImg1.src = "enemy.webp";
enemyImg2.src = "enemy2.webp";
enemyImg3.src = "enemy3.webp";
enemyImg4.src = "enemy4.webp";
bossImg.src = "Boss.webp";

// Red phase variants
enemyImg1Red.src = "enemy1_Red.webp";
enemyImg2Red.src = "enemy2_Red.webp";
enemyImg3Red.src = "enemy3_Red.webp";
enemyImg4Red.src = "enemy4_Red.webp";
bossImgRed.src = "boss_Red.webp";

// Purple phase variants
enemyImg1Purple.src = "enemy1_purple.webp";
enemyImg2Purple.src = "enemy2_purple.webp";
enemyImg3Purple.src = "enemy3_purple.webp";
enemyImg4Purple.src = "enemy4_purple.webp";
bossImgPurple.src = "boss_purple.webp";
```

#### Sound Effects
```javascript
// Line 902-907: SFX using relative paths
sfx: {
  playerBullet: new Audio("assets/audio/sfx/playerBullet.mp3"),
  playerHit: new Audio("assets/audio/sfx/playerHit.mp3"),
  playerDead: new Audio("assets/audio/sfx/playerDead.mp3"),
  enemyDead: new Audio("assets/audio/sfx/enemyDead.mp3"),
  bossIntro: new Audio("assets/audio/sfx/bossIntro.mp3"),
  powerUp: new Audio("assets/audio/sfx/powerUp.mp3")
}
```

#### Background Music
```javascript
// Line 911, 916: Music using relative paths
var bgMusic = new Audio("assets/audio/music/NonexFullSong.mp3");
var creditsMusic = new Audio("assets/audio/music/NonexFullSong.mp3");
```

**Location in code**: Lines 838-920 in game_mobile.html

---

### Path Strategy Analysis

**Desktop (absolute paths with `/Xenon_3/`):**
- Designed for GitHub Pages: `https://kstanigar.github.io/Xenon_3/`
- Assumes deployment in subdirectory
- Breaking change if moved to S3 bucket root

**Mobile (relative paths):**
- Deployment-agnostic
- Works at: `https://github.io/Xenon_3/` AND `https://non-x.com/`
- More portable for AWS migration

**AWS S3 Bucket Structure Options:**

**Option A: Bucket root deployment (RECOMMENDED)**
```
Bucket: non-x.com
- index.html
- game.html
- game_mobile.html
- player.webp
- *.webp (all sprites)
- assets/
  └── audio/
      ├── music/*.mp3
      └── sfx/*.mp3
```

**Option B: Subdirectory deployment**
```
Bucket: non-x.com
└── xenon_3/
    - (same structure as Option A)
```

**Path Changes Required:**

For Option A (bucket root):
- `game.html`: Change `/Xenon_3/...` to `/...` (remove `/Xenon_3/`)
- `game_mobile.html`: No changes needed (already relative)

For Option B (subdirectory):
- `game.html`: Change `/Xenon_3/` to `/xenon_3/` or leave as-is depending on subdomain setup
- `game_mobile.html`: May need `xenon_3/` prefix

---

## 4. EXISTING AWS CLI COMMANDS & DEPLOYMENT SCRIPTS

### AWS Deployment Plan Document
**File**: `/docs/AWS_DEPLOYMENT_PLAN.md` (579 lines)
**Status**: Planning phase - provides reference implementation

### Manual Deployment Command (from doc)
```bash
# Current recommended manual sync command
aws s3 sync . s3://non-x.com \
  --exclude ".git/*" \
  --exclude "node_modules/*" \
  --exclude "backups/*" \
  --exclude "docs/*" \
  --exclude "scripts/*" \
  --exclude ".github/*" \
  --exclude "*.md" \
  --exclude ".DS_Store" \
  --delete
```

### CloudFront Invalidation Command
```bash
# Invalidate cache after upload (forces immediate content update)
aws cloudfront create-invalidation \
  --distribution-id E1234ABCD5678 \
  --paths "/*"
```

### GitHub Actions Deployment Workflow Template (from doc)

**File**: Not yet created - but template provided in `/docs/AWS_DEPLOYMENT_PLAN.md` (lines 287-328)

**Referenced workflow**:
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
      - name: Checkout code
        uses: actions/checkout@v3

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
            --exclude "node_modules/*" \
            --exclude "backups/*" \
            --exclude "docs/*" \
            --exclude "scripts/*" \
            --exclude ".github/*" \
            --exclude "*.md" \
            --exclude ".DS_Store" \
            --delete

      - name: Invalidate CloudFront cache
        run: |
          aws cloudfront create-invalidation \
            --distribution-id ${{ secrets.CLOUDFRONT_DISTRIBUTION_ID }} \
            --paths "/*"
```

**Status**: Template exists, needs implementation

---

## 5. S3 BUCKET NAME & STRUCTURE

### Planned Configuration
**Domain**: `non-x.com` (or alternate: `nonx.io`, `planonx.com`)
**S3 Bucket Name**: `non-x.com` (exact match to domain)
**AWS Region**: `us-east-1` (required for CloudFront integration)
**Bucket Versioning**: ENABLED (for rollback capability)
**Static Website Hosting**: ENABLED
  - Index document: `index.html`
  - Error document: `index.html` (SPA-style routing)

### Bucket Policy (from doc, lines 90-106)
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::non-x.com/*"
    }
  ]
}
```

### Content Delivery
- **CloudFront Distribution**: Required for global CDN
- **CDN Domain**: `d1234abcd.cloudfront.net` (auto-generated)
- **SSL Certificate**: AWS Certificate Manager (free, auto-renewing)
- **DNS**: Route 53 (Alias records to CloudFront)

### Estimated Bandwidth & Cost
- **Monthly cost**: $1-3/month (CloudFront + S3)
- **Annual cost**: $30-50/year (plus $12-15 domain registration)

---

## 6. REQUIRED GITHUB SECRETS

### Essential Secrets for Auto-Deployment

1. **AWS_ACCESS_KEY_ID**
   - Type: AWS IAM Access Key
   - Source: AWS Console → IAM → Users → Create user `github-actions-deploy`
   - Scope: Limited to S3 + CloudFront permissions only
   - Security: Use least-privilege IAM policy

2. **AWS_SECRET_ACCESS_KEY**
   - Type: AWS IAM Secret Access Key
   - Paired with `AWS_ACCESS_KEY_ID`
   - Security: Store only in GitHub Secrets, never in code/docs
   - Rotation: Regenerate if compromised

3. **CLOUDFRONT_DISTRIBUTION_ID**
   - Type: CloudFront distribution identifier
   - Format: Example - `E1234ABCD5678` (13 characters)
   - Source: AWS Console → CloudFront → Distributions
   - Purpose: Cache invalidation after S3 sync

### Recommended IAM Policy
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
        "arn:aws:s3:::non-x.com",
        "arn:aws:s3:::non-x.com/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "cloudfront:CreateInvalidation"
      ],
      "Resource": "*"
    }
  ]
}
```

### How to Create Secrets in GitHub
1. Navigate to: Repository → Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add each secret:
   - Name: `AWS_ACCESS_KEY_ID`, Value: `AKIA...`
   - Name: `AWS_SECRET_ACCESS_KEY`, Value: `wJal...`
   - Name: `CLOUDFRONT_DISTRIBUTION_ID`, Value: `E1234ABCD...`
4. Secrets are encrypted and only visible in workflow runs

---

## 7. ISSUES & RECOMMENDATIONS

### Critical Issues

#### 1. Asset Path Inconsistency (MEDIUM PRIORITY)
**Issue**: Desktop uses `/Xenon_3/` absolute paths, mobile uses relative paths
- Desktop breaks on AWS S3 bucket root deployment
- Requires path updates during migration
- Different deployments use different code paths (harder to maintain)

**Impact**:
- S3 sync upload works fine
- Game won't load assets after DNS cutover to AWS

**Solution Options**:

**Option A: Standardize to relative paths (RECOMMENDED)**
- Update `game.html` to use relative paths like `game_mobile.html`
- Fewer path changes needed
- More portable for future deployments
- Change count: ~16 sprite paths + 2 music paths + 6 SFX paths = ~24 changes

**Option B: Standardize to absolute paths**
- Update both to `/` root paths (works with S3 bucket root + CDN)
- Requires updating path loading logic
- Change count: Same ~24 changes

**Option C: Path abstraction layer**
- Create JavaScript config object with BASE_PATH variable
- Single point of change for environment-specific paths
- More complex but future-proof

**File locations to update**:
- `/game.html` lines 915-990 (sprites, SFX, music)

---

#### 2. Large Audio Files in S3 Sync (MEDIUM PRIORITY)
**Issue**: 59 MB of music files will cause slow S3 sync
- `aws s3 sync` includes all music tracks on each deployment
- Each music file 9-13 MB individually
- Multiple tracks increase upload time significantly
- Ideal for CloudFront caching but heavy for sync operations

**Impact**:
- First deployment: ~5-10 minutes (one-time)
- Subsequent deployments: ~2-5 minutes (if any music files change)
- Blocks deployment pipeline unnecessarily

**Solutions**:

**Option A: Exclude music from sync, manually upload once (PRAGMATIC)**
```bash
# Auto-deploy game code + SFX only
aws s3 sync . s3://non-x.com \
  --exclude "assets/audio/music/*" \
  ...

# Manual one-time upload of music
aws s3 sync assets/audio/music s3://non-x.com/assets/audio/music/
```

**Option B: Separate S3 bucket for audio**
- Create `non-x-audio.s3.amazonaws.com` bucket
- Upload music once, serve via CloudFront domain
- Update `game.html` + `game_mobile.html` paths to point to different bucket
- More complex but allows independent audio updates

**Option C: Use CloudFront edge caching + conditional sync**
- Keep sync as-is
- Configure CloudFront to cache audio files with 30-day TTL
- Accept longer first deployment, fast subsequent deploys
- No code changes needed

**Recommendation**: Option A - exclude music, keeps deployment fast

---

#### 3. Missing Pre-Deployment Validation (LOW PRIORITY)
**Issue**: No automated checks for asset loading issues
- Assets might fail to load after S3 deployment
- No health check after deployment
- No verification that game works post-deployment

**Solution**: Add validation step to workflow
```yaml
- name: Verify assets exist
  run: |
    # Check critical files exist
    test -f game.html || exit 1
    test -f game_mobile.html || exit 1
    test -f index.html || exit 1
    test -d assets/audio/sfx || exit 1
    test -f assets/audio/music/NonexFullSong.mp3 || exit 1
    # Check all sprite files
    for sprite in player.webp enemy*.webp Boss.webp boss*.webp; do
      test -f "$sprite" || exit 1
    done
```

---

#### 4. .DS_Store Files in Git (LOW PRIORITY)
**Issue**: macOS `.DS_Store` files are tracked in `.gitignore` but still synced
- Will be uploaded to S3
- Not needed in production
- Clutters bucket with metadata

**Solution**: Already in `.gitignore` - add to exclude pattern
```bash
--exclude ".DS_Store" \  # Already in recommended pattern
```

---

### Non-Critical Recommendations

#### Optimization: Sprite Consolidation (FUTURE)
**Current**: 16 separate `.webp` files (~850 KB total)
**Alternative**: Single sprite sheet with CSS/Canvas positioning
**Benefit**: Reduce HTTP requests, smaller total size
**Timeline**: Post-AWS migration (music selector priority first)

#### Optimization: Audio Compression (FUTURE)
**Current**: 6 music tracks in MP3 format (59 MB)
**Alternative**: Use lower bitrate MP3 (128 kbps) or WAV format
**Potential savings**: 30-40% size reduction
**Trade-off**: Audio quality vs. bandwidth
**Timeline**: After music selector feature implementation

#### Enhancement: Deployment Status Badge
**Current**: No visible deployment status
**Enhancement**: Add GitHub Actions badge to README
**Benefit**: Visibility of deployment health
```markdown
![Deploy to AWS](https://github.com/kstanigar/Xenon_3/workflows/Deploy%20to%20AWS%20S3/badge.svg)
```

---

## 8. WORKFLOW MIGRATION CHECKLIST

### Pre-Implementation Steps
- [ ] Obtain AWS account access
- [ ] Create IAM user `github-actions-deploy` with limited permissions
- [ ] Generate access keys and secret key
- [ ] Configure Route 53 domain and hosted zone
- [ ] Create S3 bucket `non-x.com` in `us-east-1`
- [ ] Enable bucket versioning and static website hosting
- [ ] Request ACM SSL certificate for domain
- [ ] Create CloudFront distribution
- [ ] Test manual S3 sync: `aws s3 sync . s3://non-x.com --exclude ...`
- [ ] Verify game loads via CloudFront distribution domain
- [ ] Create Route 53 alias records to CloudFront

### GitHub Secrets Setup
- [ ] Add `AWS_ACCESS_KEY_ID` to repository secrets
- [ ] Add `AWS_SECRET_ACCESS_KEY` to repository secrets
- [ ] Add `CLOUDFRONT_DISTRIBUTION_ID` to repository secrets
- [ ] Verify secrets are not logged in workflow runs

### Workflow Implementation
- [ ] Create `.github/workflows/deploy-aws.yml`
- [ ] Test workflow on non-main branch first
- [ ] Verify S3 sync output
- [ ] Verify CloudFront invalidation
- [ ] Test game loads after deployment
- [ ] Merge workflow to main branch

### Post-Deployment
- [ ] Monitor deployment logs for errors
- [ ] Verify DNS propagation to custom domain
- [ ] Test game functionality with custom domain
- [ ] Update README with new domain
- [ ] Update external links (portfolio, GitHub, social media)
- [ ] Disable/redirect GitHub Pages

---

## 9. REFERENCE FILES

### Documentation
- `/docs/AWS_DEPLOYMENT_PLAN.md` - Comprehensive 5-phase migration plan (579 lines)
- `/docs/FILE_STRUCTURE.md` - Current file organization (276 lines)
- `/README.md` - Project overview

### GitHub Workflows
- `/.github/workflows/integrity-check.yml` - Function validation (225 lines)
- `/.github/workflows/test.yml` - HTML & GA4 validation (56 lines)

### Configuration
- `/.gitignore` - Git exclusion rules
- `/.claude/settings.local.json` - Claude Code permissions

### Deployment Scripts
- `/scripts/sync_paim.sh` - Bidirectional PAIM memory sync (project utility)

---

## 10. SUMMARY RECOMMENDATIONS

### Phase 1: Path Standardization (BEFORE AWS migration)
1. Update `game.html` to use relative paths (like `game_mobile.html`)
2. Reduces complexity during AWS cutover
3. Estimated effort: 30 minutes
4. No breaking changes (relative paths work on GitHub Pages too)

### Phase 2: Workflow Implementation (AFTER Phase 1)
1. Create `.github/workflows/deploy-aws.yml` using template from AWS_DEPLOYMENT_PLAN.md
2. Configure GitHub secrets (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, CLOUDFRONT_DISTRIBUTION_ID)
3. Test deployment to non-main branch first
4. Estimated effort: 1-2 hours

### Phase 3: Optimize Sync Patterns (OPTIONAL)
1. Exclude `assets/audio/music/*` from sync
2. Manually upload music files once
3. Reduces sync time by ~80%
4. Estimated effort: 15 minutes

### Phase 4: Add Validation (OPTIONAL)
1. Add pre-deployment asset validation step
2. Add post-deployment health checks
3. Estimated effort: 30 minutes

---

## 11. KEY DECISION POINTS FOR WORKFLOW DESIGN

### Decision 1: Path Strategy
**DECISION**: Standardize to relative paths before AWS migration
- All files use relative asset references
- Works on GitHub Pages + AWS S3 + localhost
- Reduces migration friction
- **Action**: Update game.html lines 915-990

### Decision 2: Audio Sync Strategy
**DECISION**: Exclude music from automated sync
- Music files are large and stable
- Upload once manually to S3
- Reduces build time from 5+ min to 1-2 min
- **Action**: Add `--exclude "assets/audio/music/*"` to sync command

### Decision 3: Validation Coverage
**DECISION**: Add asset existence checks to deployment workflow
- Verify all critical files synced successfully
- Catch deployment issues immediately
- Low overhead (<5 sec)
- **Action**: Add validation step after S3 sync

### Decision 4: Deployment Trigger
**DECISION**: Deploy only on push to main branch
- Prevents accidental deployments from feature branches
- Allows safe testing on branches before merge
- Matches current GitHub Actions pattern
- **Action**: Set `on: push: branches: [main]`

---

## Conclusion

The Xenon_3 codebase is well-structured and documented for AWS deployment. Existing GitHub Actions workflows follow professional patterns. Primary work items for auto-deployment:

1. **Standardize asset paths** (30 min) - relative paths for portability
2. **Create deploy-aws.yml workflow** (1-2 hours) - based on existing template
3. **Configure GitHub secrets** (15 min) - AWS credentials
4. **Optimize sync patterns** (15 min) - exclude large audio files
5. **Test deployment pipeline** (30 min) - verify game loads post-deploy

**Total estimated effort**: 3-4 hours active work

The infrastructure is ready; implementation is straightforward following the AWS_DEPLOYMENT_PLAN.md template.
