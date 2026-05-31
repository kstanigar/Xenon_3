# Dev/Prod AWS Environment + Auto-Deployment Implementation Plan

**Created:** May 30, 2026
**Research:** 5 haiku agents (S3, CloudFront, Route 53, GitHub Actions, IAM)
**Effort:** 3-4 hours total
**Risk:** Low (tested on dev first, then prod)
**Cost:** ~$2-3/month total (dev + prod environments)

---

## Executive Summary

This plan implements a professional dual-environment deployment architecture:

**Production Environment:**
- Domain: `nonx.standingtiger.com`
- S3 Bucket: `nonx-prod-{account-id}-us-east-2-an`
- CloudFront: Existing distribution (reuse current)
- Branch: `main`

**Development Environment:**
- Domain: `dev.nonx.standingtiger.com`
- S3 Bucket: `nonx-dev-{account-id}-us-east-2-an`
- CloudFront: New distribution
- Branch: `dev`

**Workflow:**
```
feature/pink-infinite → dev branch → auto-deploy to dev.nonx.standingtiger.com
                                   → test and verify
                                   → merge to main → auto-deploy to nonx.standingtiger.com
```

**Key Benefits:**
- Test features safely before production
- Separate testing environment for pink infinite level
- Professional CI/CD workflow
- No manual S3 syncs ever again

---

## Table of Contents

1. [Prerequisites & Preparation](#prerequisites--preparation)
2. [Phase 1: Create Dev Branch](#phase-1-create-dev-branch-5-min)
3. [Phase 2: AWS S3 Dev Bucket Setup](#phase-2-aws-s3-dev-bucket-setup-15-min)
4. [Phase 3: CloudFront Dev Distribution](#phase-3-cloudfront-dev-distribution-30-min)
5. [Phase 4: Route 53 Subdomain](#phase-4-route-53-subdomain-10-min)
6. [Phase 5: IAM Setup for GitHub Actions](#phase-5-iam-setup-for-github-actions-20-min)
7. [Phase 6: GitHub Actions Workflow](#phase-6-github-actions-workflow-30-min)
8. [Phase 7: Testing & Verification](#phase-7-testing--verification-20-min)
9. [Cost Analysis](#cost-analysis)
10. [Potential Issues & Solutions](#potential-issues--solutions)
11. [Rollback Plan](#rollback-plan)

---

## Prerequisites & Preparation

**Before Starting:**
- [ ] AWS Console access with admin permissions
- [ ] GitHub repo admin access (to add secrets)
- [ ] Current AWS Account ID (find in console top-right)
- [ ] Current CloudFront Distribution ID for prod (find in CloudFront console)
- [ ] Route 53 hosted zone for standingtiger.com

**Information to Gather:**
1. AWS Account ID: `____________` (12 digits)
2. Current region: `us-east-2` (verify in S3 console)
3. Prod CloudFront Distribution ID: `____________` (starts with E)
4. Route 53 Hosted Zone ID: `____________` (starts with Z)

---

## Phase 1: Create Dev Branch (5 min)

### Step 1.1: Create and Push Dev Branch

**Terminal Commands:**
```bash
# Ensure main is up to date
git checkout main
git pull origin main

# Create dev branch from main
git checkout -b dev

# Push to remote
git push -u origin dev
```

**Expected Output:**
```
Branch 'dev' set up to track remote branch 'dev' from 'origin'.
```

### Step 1.2: Set Branch Protection Rules (Optional but Recommended)

**GitHub Console Path:**
1. Go to: `https://github.com/kstanigar/Xenon_3/settings/branches`
2. Click "Add branch protection rule"
3. Branch name pattern: `main`
4. Enable:
   - ✅ Require a pull request before merging
   - ✅ Require status checks to pass before merging
5. Save changes

**Screenshot Verification Points:**
- Branch protection rules page shows `main` protected
- Dev branch visible in branch dropdown

---

## Phase 2: AWS S3 Dev Bucket Setup (15 min)

### Step 2.1: Create Dev S3 Bucket

**AWS Console Path:**
1. Navigate to: `https://console.aws.amazon.com/s3/`
2. Click "Create bucket"

**Configuration:**
- **Bucket name:** `nonx-dev-{your-account-id}-us-east-2-an`
  (Replace `{your-account-id}` with your AWS account ID)
- **AWS Region:** `US East (Ohio) us-east-2`
- **Object Ownership:** ACLs disabled (recommended)
- **Block Public Access:** ✅ Enable all 4 settings (we'll use CloudFront OAC)
- **Bucket Versioning:** Enable (recommended for rollback capability)
- **Default encryption:** SSE-S3 (enabled by default, no cost)
- **Tags:** Add tags:
  - Key: `Environment`, Value: `development`
  - Key: `Project`, Value: `nonx`

**Click "Create bucket"**

### Step 2.2: Enable Static Website Hosting

**AWS Console Path:**
1. Select your new bucket
2. Click "Properties" tab
3. Scroll to "Static website hosting"
4. Click "Edit"

**Configuration:**
- **Static website hosting:** Enable
- **Hosting type:** Host a static website
- **Index document:** `index.html`
- **Error document:** `404.html` (optional)

**Click "Save changes"**

**Note the Bucket website endpoint:** `http://nonx-dev-{account-id}-us-east-2-an.s3-website.us-east-2.amazonaws.com`

### Step 2.3: Configure Bucket Policy for CloudFront OAC

**WAIT - Do this AFTER creating CloudFront distribution (Phase 3)**

**Screenshot Verification Points:**
- Bucket exists with correct name format
- Region shows "us-east-2"
- Block public access shows "On" for all settings
- Static website hosting shows "Enabled"

---

## Phase 3: CloudFront Dev Distribution (30 min)

### Step 3.1: Create CloudFront Distribution

**AWS Console Path:**
1. Navigate to: `https://console.aws.amazon.com/cloudfront/`
2. Click "Create distribution"

### Step 3.2: Origin Configuration

**Origin Domain:**
- Select from dropdown: `nonx-dev-{account-id}-us-east-2-an.s3.us-east-2.amazonaws.com`
- **IMPORTANT:** Use S3 REST endpoint (not website endpoint)

**Origin Access:**
- **Origin access control settings (recommended):** Selected
- Click "Create control setting"
  - **Name:** `nonx-dev-oac`
  - **Description:** `OAC for dev environment`
  - **Signing behavior:** Sign requests (recommended)
  - Click "Create"
- Select the newly created OAC from dropdown

**Origin Shield:** Disabled (not needed for small sites)

### Step 3.3: Default Cache Behavior

**Path Pattern:** Default (*)
**Viewer Protocol Policy:** Redirect HTTP to HTTPS
**Allowed HTTP Methods:** GET, HEAD
**Cache Policy:** Managed-CachingOptimized
**Origin Request Policy:** None
**Response Headers Policy:** None (or add security headers if desired)

### Step 3.4: Function Associations

Leave all empty (no Lambda@Edge needed)

### Step 3.5: Distribution Settings

**Price Class:** Use all edge locations (or select based on your user base)

**Alternate Domain Names (CNAMEs):**
- Add: `dev.nonx.standingtiger.com`

**Custom SSL Certificate:**
- **CRITICAL:** Certificate MUST be in us-east-1 region
- If you don't have a wildcard certificate for `*.nonx.standingtiger.com`:
  1. Open new tab: `https://console.aws.amazon.com/acm/home?region=us-east-1`
  2. Click "Request certificate"
  3. Domain names: `*.standingtiger.com` or `dev.nonx.standingtiger.com`
  4. Validation method: DNS validation (recommended)
  5. Add CNAME records to Route 53 (ACM provides the values)
  6. Wait for status "Issued" (2-5 minutes)
  7. Return to CloudFront tab and select the certificate

**Default Root Object:** `index.html`

**Logging:** Optional (enable if you want access logs)

**IPv6:** Enabled (recommended)

**Click "Create distribution"**

### Step 3.6: Copy S3 Bucket Policy

**IMPORTANT:** CloudFront will display a policy statement to add to your S3 bucket.

**Screenshot should show:**
```
"We've created your distribution, but you still need to edit your S3 bucket policy."
[Copy policy] button
```

**Click "Copy policy"**

### Step 3.7: Apply S3 Bucket Policy

1. Navigate back to S3 console
2. Select `nonx-dev-{account-id}-us-east-2-an` bucket
3. Click "Permissions" tab
4. Scroll to "Bucket policy"
5. Click "Edit"
6. Paste the policy copied from CloudFront
7. Click "Save changes"

**Expected Policy Format:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowCloudFrontServicePrincipalReadOnly",
      "Effect": "Allow",
      "Principal": {
        "Service": "cloudfront.amazonaws.com"
      },
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::nonx-dev-{account-id}-us-east-2-an/*",
      "Condition": {
        "StringEquals": {
          "AWS:SourceArn": "arn:aws:cloudfront::{account-id}:distribution/{DISTRIBUTION-ID}"
        }
      }
    }
  ]
}
```

### Step 3.8: Note Distribution Information

**Record these values:**
- Dev Distribution ID: `____________` (starts with E, e.g., E1A2B3C4D5E6F7)
- Dev Distribution Domain: `____________` (e.g., d111111abcdef8.cloudfront.net)

**Distribution Status:** "Deploying" (will take 5-10 minutes to complete)

**Screenshot Verification Points:**
- Distribution status shows "Deploying" or date/time
- Origin shows your S3 bucket with OAC enabled
- Alternate domain names shows `dev.nonx.standingtiger.com`
- SSL certificate shows ACM certificate

---

## Phase 4: Route 53 Subdomain (10 min)

### Step 4.1: Create A Record for Dev Subdomain

**AWS Console Path:**
1. Navigate to: `https://console.aws.amazon.com/route53/`
2. Click "Hosted zones" in left sidebar
3. Click on `standingtiger.com` hosted zone

### Step 4.2: Create Record

**Click "Create record"**

**Record Configuration:**
- **Record name:** `dev.nonx` (will become dev.nonx.standingtiger.com)
- **Record type:** A - IPv4 address
- **Alias:** Toggle ON
- **Route traffic to:**
  - Select: "Alias to CloudFront distribution"
  - Choose distribution: Select your dev distribution domain (d111111abcdef8.cloudfront.net)
- **Routing policy:** Simple routing
- **Evaluate target health:** No

**Click "Create records"**

### Step 4.3: Create AAAA Record for IPv6 (Optional but Recommended)

**Click "Create record"** again

**Record Configuration:**
- **Record name:** `dev.nonx`
- **Record type:** AAAA - IPv6 address
- **Alias:** Toggle ON
- **Route traffic to:** Alias to CloudFront distribution (same as above)
- Click "Create records"

### Step 4.4: Wait for DNS Propagation

**Propagation time:** 60 seconds to Route 53 servers, 5-10 minutes globally

**Test DNS Resolution:**
```bash
# Check DNS resolution
dig dev.nonx.standingtiger.com

# Check directly against Route 53 nameservers
dig dev.nonx.standingtiger.com @ns-123.awsdns-45.com
```

**Expected Output:** Should return CloudFront IP addresses

**Screenshot Verification Points:**
- Record shows `dev.nonx.standingtiger.com` with Type A (Alias)
- Record shows `dev.nonx.standingtiger.com` with Type AAAA (Alias)
- Both point to CloudFront distribution

---

## Phase 5: IAM Setup for GitHub Actions (20 min)

**2026 Best Practice:** Use OIDC (OpenID Connect) instead of long-lived access keys

### Step 5.1: Create OIDC Identity Provider (One-Time Setup)

**Check if OIDC provider already exists:**

**AWS Console Path:**
1. Navigate to: `https://console.aws.amazon.com/iam/`
2. Click "Identity providers" in left sidebar
3. Look for provider: `token.actions.githubusercontent.com`

**If it exists:** Skip to Step 5.2
**If it doesn't exist:** Continue below

**Click "Add provider"**

**Configuration:**
- **Provider type:** OpenID Connect
- **Provider URL:** `https://token.actions.githubusercontent.com`
- **Audience:** `sts.amazonaws.com`

**Click "Get thumbprint"** (auto-fills)

**Click "Add provider"**

### Step 5.2: Create IAM Role for Dev Environment

**AWS Console Path:**
1. IAM Console → Roles → Click "Create role"

**Trusted Entity Type:**
- Select: "Web identity"
- **Identity provider:** token.actions.githubusercontent.com
- **Audience:** sts.amazonaws.com

**Click "Next"**

**Do not attach policies yet** (we'll create custom policy)

**Click "Next"**

**Role Details:**
- **Role name:** `github-actions-nonx-dev`
- **Description:** `GitHub Actions deployment role for NON-X dev environment`

**Click "Create role"**

### Step 5.3: Edit Trust Policy for Dev Role

**Click on newly created role** `github-actions-nonx-dev`

**Click "Trust relationships" tab**

**Click "Edit trust policy"**

**Replace with this policy:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::{YOUR-ACCOUNT-ID}:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com",
          "token.actions.githubusercontent.com:sub": "repo:kstanigar/Xenon_3:ref:refs/heads/dev"
        }
      }
    }
  ]
}
```

**Replace `{YOUR-ACCOUNT-ID}` with your AWS account ID**

**Click "Update policy"**

### Step 5.4: Create and Attach Permissions Policy for Dev

**Click "Permissions" tab**

**Click "Add permissions" → "Create inline policy"**

**Click "JSON" tab**

**Paste this policy:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "S3DevBucketAccess",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::nonx-dev-{YOUR-ACCOUNT-ID}-us-east-2-an",
        "arn:aws:s3:::nonx-dev-{YOUR-ACCOUNT-ID}-us-east-2-an/*"
      ]
    },
    {
      "Sid": "CloudFrontDevInvalidation",
      "Effect": "Allow",
      "Action": [
        "cloudfront:CreateInvalidation",
        "cloudfront:GetInvalidation"
      ],
      "Resource": "arn:aws:cloudfront::{YOUR-ACCOUNT-ID}:distribution/{DEV-DISTRIBUTION-ID}"
    }
  ]
}
```

**Replace:**
- `{YOUR-ACCOUNT-ID}` with your AWS account ID
- `{DEV-DISTRIBUTION-ID}` with your dev CloudFront distribution ID (from Phase 3)

**Click "Next"**

**Policy name:** `nonx-dev-deployment-policy`

**Click "Create policy"**

### Step 5.5: Create IAM Role for Production Environment

**Repeat Steps 5.2-5.4 with these changes:**

**Role name:** `github-actions-nonx-prod`

**Trust policy `sub` condition:**
```json
"token.actions.githubusercontent.com:sub": "repo:kstanigar/Xenon_3:ref:refs/heads/main"
```

**Permissions policy resources:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "S3ProdBucketAccess",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::nonx.standingtiger.com",
        "arn:aws:s3:::nonx.standingtiger.com/*"
      ]
    },
    {
      "Sid": "CloudFrontProdInvalidation",
      "Effect": "Allow",
      "Action": [
        "cloudfront:CreateInvalidation",
        "cloudfront:GetInvalidation"
      ],
      "Resource": "arn:aws:cloudfront::{YOUR-ACCOUNT-ID}:distribution/{PROD-DISTRIBUTION-ID}"
    }
  ]
}
```

**Policy name:** `nonx-prod-deployment-policy`

### Step 5.6: Record IAM Role ARNs

**Dev Role ARN:** `arn:aws:iam::{account-id}:role/github-actions-nonx-dev`
**Prod Role ARN:** `arn:aws:iam::{account-id}:role/github-actions-nonx-prod`

**Screenshot Verification Points:**
- Two roles created: `github-actions-nonx-dev` and `github-actions-nonx-prod`
- Trust policies show GitHub OIDC provider
- Trust policies restrict to specific branches (dev and main)
- Permissions policies show S3 and CloudFront access

---

## Phase 6: GitHub Actions Workflow (30 min)

### Step 6.1: Add GitHub Secrets

**GitHub Console Path:**
1. Go to: `https://github.com/kstanigar/Xenon_3/settings/secrets/actions`
2. Click "New repository secret"

**Add these secrets:**

| Secret Name | Value | Example |
|-------------|-------|---------|
| `AWS_ROLE_DEV` | Dev role ARN | `arn:aws:iam::123456789012:role/github-actions-nonx-dev` |
| `AWS_ROLE_PROD` | Prod role ARN | `arn:aws:iam::123456789012:role/github-actions-nonx-prod` |
| `AWS_REGION` | AWS region | `us-east-2` |
| `DEV_BUCKET_NAME` | Dev S3 bucket | `nonx-dev-123456789012-us-east-2-an` |
| `PROD_BUCKET_NAME` | Prod S3 bucket | `nonx.standingtiger.com` |
| `DEV_DISTRIBUTION_ID` | Dev CloudFront ID | `E1A2B3C4D5E6F7` |
| `PROD_DISTRIBUTION_ID` | Prod CloudFront ID | `E7F6E5D4C3B2A1` |

### Step 6.2: Create Workflow File

**Create file:** `.github/workflows/deploy-aws.yml`

**Full Workflow Content:**
```yaml
name: Deploy to AWS S3 + CloudFront

on:
  push:
    branches:
      - dev
      - main
  workflow_dispatch:

permissions:
  id-token: write
  contents: read

env:
  AWS_REGION: ${{ secrets.AWS_REGION }}

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      # Set deployment target based on branch
      - name: Set deployment target
        id: target
        run: |
          if [ "${{ github.ref }}" == "refs/heads/main" ]; then
            echo "environment=Production" >> $GITHUB_OUTPUT
            echo "bucket=${{ secrets.PROD_BUCKET_NAME }}" >> $GITHUB_OUTPUT
            echo "distribution=${{ secrets.PROD_DISTRIBUTION_ID }}" >> $GITHUB_OUTPUT
            echo "role=${{ secrets.AWS_ROLE_PROD }}" >> $GITHUB_OUTPUT
            echo "url=https://nonx.standingtiger.com" >> $GITHUB_OUTPUT
          else
            echo "environment=Development" >> $GITHUB_OUTPUT
            echo "bucket=${{ secrets.DEV_BUCKET_NAME }}" >> $GITHUB_OUTPUT
            echo "distribution=${{ secrets.DEV_DISTRIBUTION_ID }}" >> $GITHUB_OUTPUT
            echo "role=${{ secrets.AWS_ROLE_DEV }}" >> $GITHUB_OUTPUT
            echo "url=https://dev.nonx.standingtiger.com" >> $GITHUB_OUTPUT
          fi

      # Configure AWS credentials via OIDC
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ steps.target.outputs.role }}
          role-session-name: gha-${{ github.run_id }}
          aws-region: ${{ env.AWS_REGION }}

      # Verify AWS identity
      - name: Verify AWS identity
        run: |
          echo "Deploying to: ${{ steps.target.outputs.environment }}"
          aws sts get-caller-identity

      # Sync files to S3 (excluding unnecessary files)
      - name: Sync to S3 (${{ steps.target.outputs.environment }})
        run: |
          aws s3 sync . s3://${{ steps.target.outputs.bucket }} \
            --exclude ".git/*" \
            --exclude ".github/*" \
            --exclude "docs/*" \
            --exclude "backups/*" \
            --exclude "scripts/*" \
            --exclude "assets/audio/music/*" \
            --exclude "*.md" \
            --exclude ".DS_Store" \
            --exclude ".claude/*" \
            --delete

      # Invalidate CloudFront cache
      - name: Invalidate CloudFront cache
        run: |
          INVALIDATION_ID=$(aws cloudfront create-invalidation \
            --distribution-id ${{ steps.target.outputs.distribution }} \
            --paths "/*" \
            --query 'Invalidation.Id' \
            --output text)
          echo "Invalidation ID: $INVALIDATION_ID"

      # Deployment summary
      - name: Deployment complete
        run: |
          echo "✅ Deployed to ${{ steps.target.outputs.environment }}"
          echo "🔗 URL: ${{ steps.target.outputs.url }}"
          echo "📦 Bucket: ${{ steps.target.outputs.bucket }}"
          echo "🌐 Distribution: ${{ steps.target.outputs.distribution }}"
```

### Step 6.3: Commit and Push Workflow

**Terminal Commands:**
```bash
# Ensure you're on dev branch
git checkout dev

# Add workflow file
git add .github/workflows/deploy-aws.yml

# Commit
git commit -m "feat: add AWS auto-deployment workflow for dev and prod"

# Push to dev branch
git push origin dev
```

### Step 6.4: Monitor First Deployment

**GitHub Console Path:**
1. Go to: `https://github.com/kstanigar/Xenon_3/actions`
2. Click on the running workflow
3. Watch the deployment progress

**Expected Steps:**
1. Checkout code ✓
2. Set deployment target ✓ (should show "Development")
3. Configure AWS credentials ✓
4. Verify AWS identity ✓
5. Sync to S3 ✓
6. Invalidate CloudFront ✓
7. Deployment complete ✓

**Screenshot Verification Points:**
- Workflow runs automatically on push to dev
- All steps complete successfully
- Deployment summary shows dev environment
- URL shows dev.nonx.standingtiger.com

---

## Phase 7: Testing & Verification (20 min)

### Step 7.1: Wait for CloudFront Distribution

**Check distribution status:**
1. CloudFront Console → Distributions
2. Dev distribution status should show date/time (not "Deploying")
3. Wait 5-10 minutes if still deploying

### Step 7.2: Test Dev Environment

**Terminal Test:**
```bash
# Test DNS resolution
dig dev.nonx.standingtiger.com

# Test HTTP redirect
curl -I http://dev.nonx.standingtiger.com

# Test HTTPS
curl -I https://dev.nonx.standingtiger.com
```

**Browser Test:**
1. Open: `https://dev.nonx.standingtiger.com`
2. Verify index.html loads
3. Open browser console (F12)
4. Check for errors
5. Verify all sprites load (no 404s)

### Step 7.3: Test Production Workflow (When Ready)

**Create PR from dev to main:**
```bash
# Make a small test change
git checkout dev
echo "<!-- Test deployment -->" >> index.html
git add index.html
git commit -m "test: verify prod deployment workflow"
git push origin dev

# Create PR via GitHub UI
# After review, merge to main
# Workflow will automatically deploy to production
```

### Step 7.4: Verification Checklist

**Development Environment:**
- [ ] DNS resolves: `dev.nonx.standingtiger.com` → CloudFront IPs
- [ ] HTTPS loads without certificate errors
- [ ] index.html displays correctly
- [ ] All game assets load (check browser console)
- [ ] Firebase/GA4 tracking works
- [ ] Leaderboard loads

**Production Environment:**
- [ ] DNS resolves: `nonx.standingtiger.com` → CloudFront IPs
- [ ] HTTPS loads without certificate errors
- [ ] Game works identically to manual deployment
- [ ] No regressions from automated deployment

**GitHub Actions:**
- [ ] Workflow triggers on push to dev branch
- [ ] Workflow triggers on push to main branch
- [ ] Workflow completes without errors
- [ ] S3 sync shows correct file count
- [ ] CloudFront invalidation creates successfully

---

## Cost Analysis

### Monthly Costs (Both Environments)

**Development Environment:**
| Service | Usage | Cost |
|---------|-------|------|
| S3 Storage | 20 MB | $0.0005/month |
| S3 Requests | <1K GET | $0.0001/month |
| CloudFront Data Transfer | <1 GB | $0 (free tier) |
| CloudFront Requests | <10K | $0 (free tier) |
| Route 53 Queries | 1K alias queries | $0 (free for alias) |
| **Dev Subtotal** | | **~$0.01/month** |

**Production Environment:**
| Service | Usage | Cost |
|---------|-------|------|
| S3 Storage | 20 MB | $0.0005/month |
| S3 Requests | 10K GET | $0.004/month |
| CloudFront Data Transfer | 10 GB | $0 (free tier covers) |
| CloudFront Requests | 100K | $0 (free tier covers) |
| Route 53 Queries | 10K alias queries | $0 (free for alias) |
| **Prod Subtotal** | | **~$0.01/month** |

**Shared Costs:**
| Service | Cost |
|---------|------|
| Route 53 Hosted Zone | $0.50/month |
| ACM SSL Certificate | $0 (free) |
| **Shared Subtotal** | **$0.50/month** |

**Total Monthly Cost:** ~$0.52/month (~$6.24/year)

**Cost Savings vs. Manual:**
- Dev environment costs negligible (<$0.01/month)
- Free tier covers CloudFront for both environments
- Time saved: ~30 min/deployment × 4 deployments/month = 2 hours/month saved

---

## Potential Issues & Solutions

### Issue 1: CloudFront Distribution Takes Long to Deploy
**Symptom:** Distribution status shows "Deploying" for >15 minutes
**Cause:** CloudFront propagates to all edge locations globally
**Solution:** Normal behavior; wait up to 20 minutes for first deployment
**Prevention:** N/A (expected behavior)

### Issue 2: SSL Certificate Error on Dev Domain
**Symptom:** Browser shows "Your connection is not private"
**Cause:** Certificate not issued or doesn't cover dev subdomain
**Solution:**
1. Check ACM certificate includes `dev.nonx.standingtiger.com` or `*.standingtiger.com`
2. Verify certificate is in us-east-1 region
3. Wait for DNS validation to complete (check ACM console)
**Prevention:** Use wildcard certificate `*.standingtiger.com`

### Issue 3: GitHub Actions Workflow Fails with "Could not load credentials"
**Symptom:** Configure AWS credentials step fails
**Cause:** Missing `id-token: write` permission in workflow
**Solution:** Verify workflow has:
```yaml
permissions:
  id-token: write
  contents: read
```
**Prevention:** Copy workflow exactly as provided in Phase 6

### Issue 4: S3 Sync Deletes Unexpected Files
**Symptom:** Music files or other assets missing after deployment
**Cause:** `--delete` flag removes files not in Git repo
**Solution:**
1. If files should persist: Upload once manually and exclude from workflow sync
2. If files should be in Git: Add to repo and commit
**Prevention:** Review `--exclude` patterns in workflow

### Issue 5: CloudFront Shows Old Content After Deployment
**Symptom:** Changes deployed but old version still shows
**Cause:** CloudFront cache not invalidated or invalidation pending
**Solution:**
1. Check GitHub Actions logs for invalidation ID
2. CloudFront Console → Invalidations → Check status
3. Wait for invalidation to complete (1-5 minutes)
**Prevention:** Workflow includes invalidation step (already handled)

### Issue 6: Dev and Prod Show Same Content
**Symptom:** Both environments display identical content
**Cause:** Workflow deploying to wrong bucket or branches not separated
**Solution:**
1. Verify GitHub secrets have different bucket names
2. Check CloudFront origins point to correct S3 buckets
3. Verify workflow conditional logic (`if [ "${{ github.ref }}" == "refs/heads/main" ]`)
**Prevention:** Test dev deployment before merging to main

### Issue 7: IAM Role Assumption Fails
**Symptom:** "User is not authorized to perform: sts:AssumeRoleWithWebIdentity"
**Cause:** Trust policy `sub` claim doesn't match repository or branch
**Solution:**
1. Verify trust policy: `repo:kstanigar/Xenon_3:ref:refs/heads/dev`
2. Check exact repository name (case-sensitive)
3. Verify OIDC provider exists in IAM
**Prevention:** Copy trust policies exactly from Phase 5

### Issue 8: DNS Doesn't Resolve dev.nonx.standingtiger.com
**Symptom:** `dig` returns NXDOMAIN or SERVFAIL
**Cause:** Route 53 record not created or incorrect
**Solution:**
1. Verify Route 53 record exists for `dev.nonx`
2. Check record is Alias type pointing to CloudFront
3. Wait 60 seconds for propagation
**Prevention:** Use alias records (not CNAME) as specified in Phase 4

---

## Rollback Plan

### Emergency Rollback to Manual Deployment

**If auto-deployment breaks production:**

**Step 1: Disable Workflow (2 minutes)**
```bash
# Rename workflow file to prevent execution
mv .github/workflows/deploy-aws.yml .github/workflows/deploy-aws.yml.disabled
git add .
git commit -m "fix: disable auto-deployment workflow"
git push origin main
```

**Step 2: Manual Deployment (5 minutes)**
```bash
# Deploy manually using AWS CLI
aws s3 sync . s3://nonx.standingtiger.com \
  --exclude ".git/*" \
  --exclude ".github/*" \
  --exclude "docs/*" \
  --exclude "backups/*" \
  --exclude "assets/audio/music/*" \
  --exclude "*.md" \
  --exclude ".DS_Store" \
  --delete

# Invalidate CloudFront
aws cloudfront create-invalidation \
  --distribution-id {PROD-DISTRIBUTION-ID} \
  --paths "/*"
```

**Step 3: Debug Issue**
1. Check GitHub Actions logs for error
2. Verify IAM permissions
3. Check S3 bucket policy
4. Test workflow on dev branch first

**Step 4: Re-enable Workflow**
```bash
# After fixing issue
mv .github/workflows/deploy-aws.yml.disabled .github/workflows/deploy-aws.yml
git add .
git commit -m "fix: re-enable auto-deployment workflow"
git push origin dev  # Test on dev first
```

### Rollback Specific Deployment

**If a bad deployment went live:**

```bash
# Option 1: Revert Git commit and push
git revert HEAD
git push origin main  # Triggers re-deployment

# Option 2: Manual rollback to previous version
# S3 versioning must be enabled
aws s3api list-object-versions \
  --bucket nonx.standingtiger.com \
  --prefix index.html

# Copy previous version to current
aws s3api copy-object \
  --bucket nonx.standingtiger.com \
  --copy-source nonx.standingtiger.com/index.html?versionId={VERSION-ID} \
  --key index.html
```

---

## Post-Implementation Tasks

### Update Documentation
- [ ] Mark this plan as COMPLETE
- [ ] Update AWS_DEPLOYMENT_STATUS.md with new dev environment
- [ ] Update README.md with dev URL
- [ ] Document workflow for team members

### Team Communication
- [ ] Share dev environment URL: `https://dev.nonx.standingtiger.com`
- [ ] Document branch strategy (feature → dev → main)
- [ ] Explain PR process for production deployments

### Monitoring Setup
- [ ] Enable CloudWatch alarms for S3 bucket metrics
- [ ] Enable CloudFront access logs (optional)
- [ ] Set up GitHub Actions notifications (Slack/Discord)

---

## Next Steps: Implementing Pink Infinite Level

**Now that dev environment is ready:**

```bash
# 1. Create feature branch from dev
git checkout dev
git pull origin dev
git checkout -b feature/pink-infinite-level

# 2. Develop pink level features
# ... make changes ...

# 3. Push and create PR to dev
git push -u origin feature/pink-infinite-level
# Create PR on GitHub targeting dev branch

# 4. Auto-deployment to dev happens on merge
# Test at: https://dev.nonx.standingtiger.com

# 5. When tested and ready, create PR from dev to main
# This deploys to production: https://nonx.standingtiger.com
```

---

## Success Criteria

**Implementation is successful when:**
- ✅ Dev branch auto-deploys to dev.nonx.standingtiger.com
- ✅ Main branch auto-deploys to nonx.standingtiger.com
- ✅ Both environments accessible via HTTPS (no cert errors)
- ✅ All game features work on both environments
- ✅ No manual S3 syncs required
- ✅ CloudFront invalidations happen automatically
- ✅ Workflow completes in <2 minutes per deployment
- ✅ GitHub Actions shows green checkmarks
- ✅ Firebase and GA4 tracking works on both environments

---

**Status:** Ready for implementation
**Approval Required:** Yes (before starting Phase 1)
**Estimated Total Time:** 3-4 hours
**Blocking Issues:** None (asset paths already fixed)

**Ready to proceed?** Start with Phase 1 and share screenshots at each phase for verification.