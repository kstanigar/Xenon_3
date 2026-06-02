# AWS Deployment Plan - NON-X Game
**Date Created:** May 30, 2026
**Status:** 📋 PLANNING
**Priority:** 🔴 CRITICAL - Blocking music selector and production features
**Estimated Effort:** 8-12 hours (spread across 1-2 weeks)

---

## Overview

Migrate NON-X from GitHub Pages to AWS infrastructure for:
- **Custom domain** with professional branding
- **Global CDN** via CloudFront for faster worldwide delivery
- **SSL/HTTPS** with free AWS Certificate Manager
- **Scalability** for future features (API endpoints, backend services)
- **Production-ready** hosting with monitoring and logging

**Current:** `https://kstanigar.github.io/Xenon_3/`
**Target:** `https://non-x.com` (or custom domain of choice)

---

## 🎯 Success Criteria

After migration is complete:
- [ ] Game accessible via custom domain (HTTPS)
- [ ] Global CDN active (CloudFront)
- [ ] SSL certificate valid and auto-renewing
- [ ] GitHub Pages decommissioned or redirected
- [ ] All analytics tracking working
- [ ] Firebase leaderboard functional
- [ ] Load time < 2 seconds (worldwide average)
- [ ] Zero downtime during migration
- [ ] Rollback plan tested and ready

---

## 📋 5-Phase Migration Plan

### **Phase 1: Domain & AWS Account Setup** (2 hours)

#### Prerequisites
- [ ] AWS account created (if not exists)
- [ ] Credit card on file for AWS billing
- [ ] Access to email for domain verification

#### Tasks
1. **Purchase Domain via Route 53**
   - Log into AWS Console → Route 53
   - Search for available domain (suggestions: non-x.com, nonx.io, planonx.com)
   - Purchase domain ($12-15/year typical)
   - Auto-enable privacy protection
   - Wait for registration confirmation (10-60 minutes)

2. **Create Hosted Zone**
   - Route 53 automatically creates hosted zone for new domains
   - Note the 4 nameserver (NS) records for reference
   - Verify hosted zone created successfully

3. **Set Up AWS Billing Alerts**
   - AWS Billing Console → Budgets
   - Create budget: $10/month threshold
   - Alert email: your email address
   - Rationale: Static hosting should cost < $5/month

**Estimated Cost:** $12-15 domain + $1-5/month hosting = ~$25-30/year total

**Checkpoint:** Domain registered, hosted zone created, billing alerts configured

---

### **Phase 2: S3 Bucket Setup** (1 hour)

#### Tasks
1. **Create S3 Bucket**
   - AWS Console → S3 → Create bucket
   - Bucket name: `non-x.com` (exact match to domain)
   - Region: `us-east-1` (required for CloudFront integration)
   - Block all public access: **DISABLED** (we need public read)
   - Bucket versioning: **ENABLED** (for rollback capability)
   - Tags: `Project=NON-X`, `Environment=Production`

2. **Enable Static Website Hosting**
   - Bucket → Properties → Static website hosting → Enable
   - Index document: `index.html`
   - Error document: `index.html` (SPA-style routing)
   - Note the S3 website endpoint URL (e.g., `http://non-x.com.s3-website-us-east-1.amazonaws.com`)

3. **Configure Bucket Policy**
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
   - S3 Console → Bucket → Permissions → Bucket policy → Paste above JSON
   - Replace `non-x.com` with your actual bucket name
   - Save changes

4. **Initial Upload Test**
   ```bash
   # From project directory
   aws s3 sync . s3://non-x.com \
     --exclude ".git/*" \
     --exclude "node_modules/*" \
     --exclude "backups/*" \
     --exclude "docs/*" \
     --exclude "scripts/*" \
     --exclude ".github/*" \
     --exclude "*.md" \
     --exclude ".DS_Store"
   ```
   - Test S3 endpoint URL in browser
   - Verify game loads (no custom domain yet)

**Checkpoint:** S3 bucket hosting game successfully via S3 endpoint URL

---

### **Phase 3: SSL Certificate** (30 minutes + 24hr wait)

#### Tasks
1. **Request Certificate via ACM**
   - AWS Console → Certificate Manager (ACM)
   - **CRITICAL:** Switch region to `us-east-1` (CloudFront requires this)
   - Request certificate → Request a public certificate
   - Domain name: `non-x.com`
   - Add another name: `www.non-x.com`
   - Validation method: **DNS validation** (recommended)
   - Click "Request"

2. **Add DNS Validation Records**
   - ACM will show CNAME records needed for validation
   - Option 1 (Easy): Click "Create records in Route 53" button
   - Option 2 (Manual): Copy CNAME name/value to Route 53 hosted zone
   - Wait for validation (5 minutes - 24 hours, typically 10-20 minutes)

3. **Verify Certificate Status**
   - ACM Console → Certificate status should show "Issued"
   - If pending after 30 minutes, check Route 53 records
   - Certificate auto-renews every year (no action needed)

**Checkpoint:** SSL certificate issued and valid

---

### **Phase 4: CloudFront CDN Setup** (2 hours)

#### Tasks
1. **Create CloudFront Distribution**
   - AWS Console → CloudFront → Create distribution

   **Origin Settings:**
   - Origin domain: Select your S3 bucket from dropdown
   - Origin path: leave blank
   - Name: `S3-non-x.com`
   - Origin access: **Origin access control settings (recommended)**
   - Create new OAC → Create

   **Default Cache Behavior:**
   - Viewer protocol policy: **Redirect HTTP to HTTPS**
   - Allowed HTTP methods: **GET, HEAD, OPTIONS**
   - Cache policy: **CachingOptimized**
   - Origin request policy: **CORS-S3Origin**

   **Settings:**
   - Price class: **Use all edge locations** (best performance)
   - Alternate domain names (CNAMEs): `non-x.com`, `www.non-x.com`
   - Custom SSL certificate: Select your ACM certificate
   - Default root object: `index.html`
   - Standard logging: **Enabled** (optional but recommended)
   - IPv6: **Enabled**

   - Click "Create distribution"
   - **Wait 10-20 minutes for deployment** (status: "Deploying" → "Enabled")

2. **Update S3 Bucket Policy for CloudFront**
   - CloudFront will show a banner "S3 bucket policy needs update"
   - Click "Copy policy" → Go to S3 bucket → Permissions → Bucket policy
   - Replace old policy with CloudFront policy
   - This allows CloudFront to access S3 while keeping bucket private

3. **Configure Custom Error Responses (Optional)**
   - CloudFront distribution → Error pages → Create custom error response
   - HTTP error code: 403, 404
   - Customize error response: Yes
   - Response page path: `/index.html`
   - HTTP response code: 200
   - Rationale: SPA-style routing (all routes serve index.html)

4. **Test CloudFront Distribution**
   - Copy CloudFront domain name (e.g., `d1234abcd.cloudfront.net`)
   - Open in browser: `https://d1234abcd.cloudfront.net`
   - Verify game loads with HTTPS
   - Check Network tab: Response headers should show `X-Cache: Hit from cloudfront`

**Checkpoint:** CloudFront serving game with SSL, cache working

---

### **Phase 5: DNS Configuration & Go-Live** (30 minutes + DNS propagation)

#### Tasks
1. **Create Route 53 A Records (Alias)**
   - Route 53 → Hosted zones → your domain → Create record

   **Record 1 (Root domain):**
   - Record name: leave blank (creates `non-x.com`)
   - Record type: **A - IPv4 address**
   - Alias: **Yes**
   - Route traffic to: **Alias to CloudFront distribution**
   - Select your CloudFront distribution from dropdown
   - Routing policy: Simple routing
   - Create record

   **Record 2 (WWW subdomain):**
   - Record name: `www`
   - Record type: **A - IPv4 address**
   - Alias: **Yes**
   - Route traffic to: **Alias to CloudFront distribution**
   - Select your CloudFront distribution from dropdown
   - Routing policy: Simple routing
   - Create record

2. **Wait for DNS Propagation**
   - Typically 5-60 minutes
   - Check status: `dig non-x.com` or `nslookup non-x.com`
   - Should resolve to CloudFront IP addresses

3. **Test Production Domain**
   - Open `https://non-x.com` in browser
   - Open `https://www.non-x.com` in browser
   - Verify SSL certificate valid (no warnings)
   - Test game functionality:
     - [ ] Index menu loads
     - [ ] Platform selection works
     - [ ] Game launches (desktop + mobile)
     - [ ] Leaderboard loads from Firebase
     - [ ] Analytics tracking fires (GA4 DebugView)
     - [ ] Music/SFX play correctly
     - [ ] All images load

4. **Update External References**
   - Update `README.md` live demo link
   - Update Firebase leaderboard allowed domains
   - Update GA4 allowed referrers (if configured)
   - Update any social media links
   - Update portfolio site links

**Checkpoint:** Production domain live and fully functional

---

## 🚀 Deployment Workflow (Post-Migration)

### Option 1: Manual S3 Sync (Simple)
```bash
# From project directory
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

# Invalidate CloudFront cache (forces immediate update)
aws cloudfront create-invalidation \
  --distribution-id E1234ABCD5678 \
  --paths "/*"
```

### Option 2: GitHub Actions (Automated)
Create `.github/workflows/deploy-aws.yml`:

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

**Required GitHub Secrets:**
- `AWS_ACCESS_KEY_ID` - IAM user access key
- `AWS_SECRET_ACCESS_KEY` - IAM user secret key
- `CLOUDFRONT_DISTRIBUTION_ID` - CloudFront distribution ID

---

## 🔐 Security Best Practices

### IAM User Setup (For CI/CD)
1. Create IAM user: `github-actions-deploy`
2. Attach policy:
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
3. Generate access keys → Store in GitHub Secrets
4. **NEVER commit AWS credentials to git**

### Security Headers (CloudFront Function)
Optional but recommended - add security headers via CloudFront Function:

```javascript
function handler(event) {
  var response = event.response;
  var headers = response.headers;

  headers['strict-transport-security'] = { value: 'max-age=63072000' };
  headers['x-content-type-options'] = { value: 'nosniff' };
  headers['x-frame-options'] = { value: 'SAMEORIGIN' };
  headers['x-xss-protection'] = { value: '1; mode=block' };
  headers['referrer-policy'] = { value: 'strict-origin-when-cross-origin' };

  return response;
}
```

---

## 💰 Cost Estimate

### Monthly Costs (Estimated)
- **Route 53 Hosted Zone:** $0.50/month
- **S3 Storage:** ~$0.10/month (100 MB game assets)
- **S3 Requests:** ~$0.01/month (low traffic)
- **CloudFront Data Transfer:** $0.50-2.00/month (1,000-5,000 plays)
- **CloudFront Requests:** ~$0.10/month
- **ACM SSL Certificate:** **FREE**

**Total: $1-3/month** (plus $12-15/year domain)

### Annual Cost
- **Year 1:** ~$50-75 (domain + hosting)
- **Year 2+:** ~$30-50/year

**Much cheaper than dedicated hosting!**

---

## 📊 Monitoring & Logging

### CloudWatch Alarms (Optional)
1. **High Error Rate Alarm**
   - Metric: CloudFront 4xx/5xx errors
   - Threshold: > 5% error rate
   - Action: Email notification

2. **High Cost Alarm**
   - Already configured in Phase 1 (billing alert)

### CloudFront Logs
- Enable standard logging (Phase 4)
- Logs stored in S3 bucket (separate bucket recommended)
- Analyze with Athena or download for local analysis
- Useful for debugging CDN cache issues

### S3 Versioning
- Already enabled in Phase 2
- Allows rollback to previous versions
- Retain last 10 versions (lifecycle policy)

---

## 🔄 Rollback Plan

### If AWS Migration Fails
1. **Immediate Rollback:**
   - Keep GitHub Pages active during migration
   - Don't update DNS until fully tested
   - CloudFront failure → Remove DNS records, traffic stays on GitHub Pages

2. **Partial Rollback:**
   - Remove Route 53 A records → Traffic back to GitHub Pages
   - Keep S3/CloudFront for testing
   - Fix issues, retry DNS cutover later

3. **Full Rollback:**
   - Delete CloudFront distribution
   - Delete S3 bucket
   - Keep Route 53 domain (redirect to GitHub Pages with CNAME)

### Recovery Time
- **DNS rollback:** 5-60 minutes (DNS propagation)
- **GitHub Pages reactivation:** Instant (if kept enabled)

---

## ✅ Pre-Launch Checklist

### Before Phase 5 (DNS Cutover)
- [ ] S3 bucket serving game correctly
- [ ] CloudFront distribution deployed and enabled
- [ ] SSL certificate issued and valid
- [ ] Test CloudFront URL loads game perfectly
- [ ] Firebase leaderboard working via CloudFront URL
- [ ] GA4 analytics tracking via CloudFront URL
- [ ] All assets loading (images, audio, sprites)
- [ ] Mobile responsive on CloudFront URL
- [ ] Performance acceptable (load time < 3s)
- [ ] Rollback plan documented and understood

### After DNS Cutover
- [ ] Production domain loads with HTTPS
- [ ] WWW subdomain redirects correctly
- [ ] SSL certificate shows valid (no warnings)
- [ ] All game features working
- [ ] Analytics tracking with new domain
- [ ] Firebase leaderboard working
- [ ] GitHub Pages disabled or redirected
- [ ] Update all external links
- [ ] Monitor for 24 hours

---

## 🎓 AWS CLI Setup (If Not Installed)

### macOS Installation
```bash
# Install AWS CLI
brew install awscli

# Configure credentials
aws configure

# Enter when prompted:
# AWS Access Key ID: [from IAM user]
# AWS Secret Access Key: [from IAM user]
# Default region: us-east-1
# Default output format: json

# Verify installation
aws s3 ls
```

### Generate IAM User Credentials
1. AWS Console → IAM → Users → Create user
2. User name: `cli-deploy`
3. Attach policy: `AmazonS3FullAccess`, `CloudFrontFullAccess`
4. Create access key → Download credentials
5. **Store securely, never commit to git**

---

## 📚 Reference Documentation

### AWS Documentation
- [S3 Static Website Hosting](https://docs.aws.amazon.com/AmazonS3/latest/userguide/WebsiteHosting.html)
- [CloudFront Getting Started](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/GettingStarted.html)
- [Route 53 Domain Registration](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/domain-register.html)
- [ACM Certificate Request](https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-request-public.html)

### Troubleshooting Resources
- [CloudFront Invalidation](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Invalidation.html)
- [S3 Bucket Policy Examples](https://docs.aws.amazon.com/AmazonS3/latest/userguide/example-bucket-policies.html)
- [Route 53 DNS Troubleshooting](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/troubleshooting-route-53.html)

---

## 🚦 Next Steps After Migration

Once AWS migration is complete:

1. **Implement Music Selector** (2.5 hours)
   - See `docs/design/MUSIC_SELECTOR_PLAN.md`
   - Blocked by AWS migration (file size concerns)

2. **Pink Levels 13-15 Activation** (4-6 hours)
   - Legacy formations ready
   - Requires balancing and testing

3. **Performance Optimization**
   - Analyze CloudFront cache hit rates
   - Optimize asset compression
   - Consider WebP for all sprites

4. **Advanced Features**
   - API Gateway for leaderboard backend
   - Lambda functions for server-side logic
   - DynamoDB for advanced analytics

---

## 📝 Session Notes

**Created:** May 30, 2026
**Author:** Claude Sonnet 4.5
**Purpose:** Comprehensive AWS migration plan for NON-X game

**Key Decisions:**
- Chose Route 53 for domain (AWS ecosystem integration)
- Chose S3 + CloudFront over EC2 (static site, lower cost)
- Chose ACM over third-party SSL (free, auto-renewing)
- DNS validation over email (faster, more reliable)
- us-east-1 region (CloudFront/ACM requirement)

**Estimated Timeline:**
- Phase 1: 2 hours
- Phase 2: 1 hour
- Phase 3: 30 min + 24hr wait
- Phase 4: 2 hours
- Phase 5: 30 min + DNS propagation

**Total: 6 hours active work + 24-48 hours waiting**

---

**Status:** Ready to begin Phase 1 when approved