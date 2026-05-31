# AWS Multi-Environment Deployment Research Summary - 2026

**Research Date:** May 30, 2026
**Research Agents:** 5 haiku agents (S3, CloudFront, Route 53, GitHub Actions, IAM)
**Purpose:** Current AWS best practices for dev/prod deployment architecture

---

## Executive Summary

Researched current (2026) AWS best practices across 5 key areas to implement professional multi-environment deployment for NON-X game. All findings based on official AWS documentation and 2025-2026 updates.

**Key 2026 Changes:**
- OIDC is now mandatory standard (deprecating long-lived IAM keys)
- Origin Access Control (OAC) replaced Origin Access Identity (OAI)
- CloudFront pricing reduced by 30% (Feb 2026)
- S3 account-regional namespaces introduced
- Route 53 Global Resolver now available

---

## 1. S3 Static Website Hosting (2026)

### Critical Updates

**Account-Regional Namespaces (NEW 2026):**
- Bucket names no longer require global uniqueness
- Format: `{name}-{account-id}-{region}-an`
- Example: `nonx-dev-123456789012-us-east-2-an`
- Simplifies multi-environment setup

**Default Encryption:**
- SSE-S3 enabled by default (no cost)
- No performance impact
- Automatic for all new objects

**Block Public Access:**
- New buckets default to all public access blocked
- Use CloudFront + OAC instead of public buckets
- Direct S3 website hosting discouraged

### Setup Best Practices

**Bucket Configuration:**
```
✅ Enable versioning (rollback capability)
✅ Enable SSE-S3 encryption (default, free)
✅ Block all public access (use CloudFront)
✅ Add environment tags (Environment: dev/prod)
✅ Enable access logging (security audit)
```

**Bucket Policy (CloudFront OAC):**
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": {
      "Service": "cloudfront.amazonaws.com"
    },
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::bucket-name/*",
    "Condition": {
      "StringEquals": {
        "AWS:SourceArn": "arn:aws:cloudfront::account:distribution/ID"
      }
    }
  }]
}
```

### Pricing (20MB Static Site)

| Component | Cost/Month |
|-----------|------------|
| Storage (20 MB) | $0.0005 |
| GET requests (<1K) | $0.0001 |
| Data transfer to CloudFront | Free |
| **Total** | **~$0.001** |

**Sources:** [AWS S3 Documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/WebsiteHosting.html), [S3 Pricing 2026](https://www.cloudzero.com/blog/s3-pricing/)

---

## 2. CloudFront Distribution Setup (2026)

### Origin Access Control (OAC) - Mandatory

**OAC vs OAI:**
| Feature | OAI (Legacy) | OAC (Current) |
|---------|--------------|---------------|
| Status | Deprecated | ✅ Recommended |
| SSE-KMS Support | ❌ No | ✅ Yes |
| All AWS Regions | Limited | ✅ All regions |
| Security | Basic | ✅ Enhanced (SigV4) |

**OAC Setup:**
1. CloudFront auto-creates OAC during distribution creation
2. CloudFront provides S3 bucket policy to copy
3. Bucket policy uses `AWS:SourceArn` condition (prevents confused deputy attacks)

### Multi-Environment Strategy

**Recommended: Separate Distributions**
```
Dev Environment:
- Distribution ID: E123DEV...
- Origin: nonx-dev-{account}-us-east-2.s3.amazonaws.com
- CNAME: dev.nonx.standingtiger.com

Prod Environment:
- Distribution ID: E456PROD...
- Origin: nonx.standingtiger.com.s3.amazonaws.com
- CNAME: nonx.standingtiger.com
```

### Cache Invalidation Strategies

**Tier 1: Versioned URLs (FREE - Recommended)**
- Use build hashes in filenames: `app.a3f2c9d1.js`
- CloudFront fetches new version automatically
- Zero invalidation costs
- Best performance

**Tier 2: Explicit Invalidations (1,000 free/month)**
- Wildcard: `/*` = 1 path = $0.005
- Cache tags (NEW April 2026): surgical invalidations
- First 1,000 paths free, then $0.005/path

**Tier 3: Cache-Control Headers**
- `Cache-Control: no-cache` - always revalidate
- `Cache-Control: max-age=3600` - cache 1 hour
- No additional costs

### SSL/TLS Certificate Requirements

**CRITICAL:** ACM certificates MUST be in us-east-1 region

**Setup:**
1. AWS Console → Certificate Manager (us-east-1 only)
2. Request certificate for `*.standingtiger.com` or specific subdomain
3. Validation: DNS (recommended - auto-renews)
4. Attach to CloudFront distribution

### Pricing (20MB Site, Moderate Traffic)

| Component | Usage | Cost |
|-----------|-------|------|
| Data Transfer | 1 TB/month | $0 (free tier) |
| Requests | 10M/month | $0 (free tier) |
| Invalidations | <1,000 paths | $0 (free tier) |
| **Total** | | **$0/month** |

**Note:** CloudFront free tier covers most small-to-medium sites

**Sources:** [CloudFront OAC Guide 2026](https://oneuptime.com/blog/post/2026-02-12-cloudfront-origin-access-control-oac-s3/view), [CloudFront Pricing 2026](https://blog.blazingcdn.com/en-us/aws-cloudfront-pricing-explained)

---

## 3. Route 53 DNS Configuration (2026)

### Alias Records vs CNAME

**Always Use Alias Records for CloudFront**

| Aspect | Alias | CNAME |
|--------|-------|-------|
| Pricing | ✅ FREE | Charged per query |
| Zone Apex | ✅ Supported | ❌ Not allowed |
| Performance | Faster | Slower (extra lookup) |
| CloudFront | ✅ Recommended | ❌ Not recommended |

### Subdomain Configuration

**Single Hosted Zone (Recommended):**
```
standingtiger.com (hosted zone - $0.50/month)
├── dev.nonx.standingtiger.com (A alias → CloudFront)
├── nonx.standingtiger.com (A alias → CloudFront)
└── www.standingtiger.com (A alias → CloudFront)
```

**Cost:** $0.50/month total (single zone covers all subdomains)

**Separate Zones (Only for Multi-Account):**
- Use only if environments in different AWS accounts
- Cost: $0.50/zone/month (higher cost)
- Small latency penalty on first query

### Setup Steps

**Console Path:**
1. Route 53 → Hosted zones → Select zone
2. Create record
3. Configuration:
   - Name: `dev.nonx` (for dev.nonx.standingtiger.com)
   - Type: **A - IPv4 address**
   - Alias: **Toggle ON**
   - Route traffic to: **Alias to CloudFront distribution**
   - Select distribution from dropdown
4. Repeat for AAAA (IPv6) if enabled

**Propagation:** 60 seconds to Route 53 servers, 5-10 minutes globally

### 2026 Updates

**February 2026: Query Pricing Reduction (30%)**
- Standard queries: $0.40/million (was $0.57/million)
- Makes Route 53 more cost-competitive

**March 2026: Route 53 Global Resolver**
- Internet-reachable anycast DNS resolver
- Available across 30 AWS regions
- Useful for hybrid/multi-cloud scenarios

### Pricing

| Component | Cost |
|-----------|------|
| Hosted zone (standingtiger.com) | $0.50/month |
| Alias queries to CloudFront | **FREE** |
| Standard queries (if used) | $0.40/million |
| **Total (with alias)** | **$0.50/month** |

**Sources:** [Route 53 Alias Records 2026](https://oneuptime.com/blog/post/2026-02-12-route-53-alias-records-vs-cname/view), [Route 53 Pricing Reduction](https://aws.amazon.com/route53/pricing/)

---

## 4. GitHub Actions AWS Deployment (2026)

### OIDC - Current Best Practice

**2026 Standard: Use OIDC, NOT Access Keys**

**Why OIDC:**
- ✅ No long-lived credentials stored
- ✅ Temporary tokens (5-15 minute TTL)
- ✅ Automatic expiration after workflow
- ✅ CloudTrail audit trail with workflow ID
- ✅ No credential rotation needed
- ✅ Reduced blast radius if compromised

**Access Keys (Deprecated):**
- ❌ Long-lived credentials in GitHub secrets
- ❌ Manual rotation required (30-90 days)
- ❌ Higher breach risk
- ❌ No workflow-level audit trail

### OIDC Setup

**Step 1: Create OIDC Provider (One-Time)**
```bash
aws iam create-open-id-connect-provider \
  --url https://token.actions.githubusercontent.com \
  --client-id-list sts.amazonaws.com
```

**Step 2: IAM Role Trust Policy**
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": {
      "Federated": "arn:aws:iam::ACCOUNT:oidc-provider/token.actions.githubusercontent.com"
    },
    "Action": "sts:AssumeRoleWithWebIdentity",
    "Condition": {
      "StringEquals": {
        "token.actions.githubusercontent.com:aud": "sts.amazonaws.com",
        "token.actions.githubusercontent.com:sub": "repo:ORG/REPO:ref:refs/heads/main"
      }
    }
  }]
}
```

**Step 3: Workflow Configuration**
```yaml
permissions:
  id-token: write  # Required for OIDC
  contents: read

jobs:
  deploy:
    steps:
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::ACCOUNT:role/github-actions-role
          aws-region: us-east-1
```

### Multi-Environment Deployment

**Branch-Based Conditional Deployment:**
```yaml
- name: Set deployment target
  run: |
    if [ "${{ github.ref }}" == "refs/heads/main" ]; then
      echo "bucket=prod-bucket" >> $GITHUB_OUTPUT
    else
      echo "bucket=dev-bucket" >> $GITHUB_OUTPUT
    fi
```

**Separate Roles Per Environment:**
- Dev role: `github-actions-dev` (trusts `refs/heads/dev`)
- Prod role: `github-actions-prod` (trusts `refs/heads/main`)

### Latest Action Version

**aws-actions/configure-aws-credentials:**
- Current version: v4 (v6.1.1 released May 5, 2026)
- Use semantic versioning tags
- OIDC support since v2

### 2026 Security Updates

**April 2026: Subject Claim Enhancement**
- GitHub now appends owner/repo IDs to OIDC subject claims
- Prevents name-reuse attacks
- Applies to repos created after June 18, 2026
- Update trust policies accordingly

**Sources:** [GitHub Actions OIDC AWS 2026](https://oneuptime.com/blog/post/2026-02-02-github-actions-oidc-aws/view), [AWS Blog: GitHub Actions IAM Roles](https://aws.amazon.com/blogs/security/use-iam-roles-to-connect-github-actions-to-actions-in-aws/)

---

## 5. IAM Policies for Dev/Prod Separation (2026)

### Recommended Architecture

**Separate Roles Per Environment (Best Practice)**
```
github-actions-dev (trusts dev branch)
├── S3: nonx-dev-* (read/write/delete)
├── CloudFront: DEV_DISTRIBUTION_ID (invalidate)
└── Session: 15 minutes max

github-actions-prod (trusts main branch)
├── S3: nonx.standingtiger.com (read/write/delete)
├── CloudFront: PROD_DISTRIBUTION_ID (invalidate)
├── Explicit deny: destructive operations
└── Session: 15 minutes max
```

### Least-Privilege Policy Examples

**Development Environment (Broader Permissions):**
```json
{
  "Statement": [{
    "Sid": "S3DevAccess",
    "Effect": "Allow",
    "Action": [
      "s3:GetObject",
      "s3:PutObject",
      "s3:DeleteObject",
      "s3:ListBucket"
    ],
    "Resource": [
      "arn:aws:s3:::nonx-dev-*",
      "arn:aws:s3:::nonx-dev-*/*"
    ]
  }, {
    "Sid": "CloudFrontDevInvalidation",
    "Effect": "Allow",
    "Action": ["cloudfront:CreateInvalidation"],
    "Resource": "arn:aws:cloudfront::ACCOUNT:distribution/DEV_ID"
  }]
}
```

**Production Environment (Restrictive):**
```json
{
  "Statement": [{
    "Sid": "S3ProdAccess",
    "Effect": "Allow",
    "Action": [
      "s3:GetObject",
      "s3:PutObject",
      "s3:ListBucket"
    ],
    "Resource": [
      "arn:aws:s3:::nonx.standingtiger.com",
      "arn:aws:s3:::nonx.standingtiger.com/*"
    ]
  }, {
    "Sid": "CloudFrontProdInvalidation",
    "Effect": "Allow",
    "Action": ["cloudfront:CreateInvalidation"],
    "Resource": "arn:aws:cloudfront::ACCOUNT:distribution/PROD_ID"
  }, {
    "Sid": "ExplicitDenyDelete",
    "Effect": "Deny",
    "Action": ["s3:DeleteBucket"],
    "Resource": "*"
  }]
}
```

### Policy Condition Examples

**Time-Based Restrictions (Production Only):**
```json
{
  "Condition": {
    "DateGreaterThan": {"aws:CurrentTime": "2026-05-30T09:00:00Z"},
    "DateLessThan": {"aws:CurrentTime": "2026-05-30T17:00:00Z"}
  }
}
```

**IP-Based Restrictions (CI/CD Only):**
```json
{
  "Condition": {
    "IpAddress": {
      "aws:SourceIp": ["203.0.113.0/24"]
    }
  }
}
```

### 2025-2026 Security Best Practices

**1. Eliminate Long-Lived Credentials**
- Phase out IAM user access keys
- Use OIDC or STS temporary credentials
- Rotate any remaining keys every 90 days

**2. Use Service Control Policies (Multi-Account)**
- Prevent account-level IAM user creation
- Enforce MFA for production access
- Block destructive operations organization-wide

**3. Enable Comprehensive Logging**
- CloudTrail logs every IAM action
- Ship logs to separate security account
- Enable GuardDuty for anomaly detection

**4. Policy Validation in CI/CD**
- Validate policies before deployment
- Block overly permissive policies
- Automated security scans

**Sources:** [IAM Best Practices 2026](https://akshayghalme.com/blogs/aws-iam-best-practices-least-privilege/), [IAM Security Guide 2026](https://dev.to/karaniph/aws-iam-security-best-practices-in-2026-a-complete-guide-o14)

---

## Cost Summary: Complete Multi-Environment Setup

### Monthly Costs

**Development Environment:**
| Service | Cost |
|---------|------|
| S3 storage + requests | $0.001 |
| CloudFront (free tier) | $0 |
| Route 53 alias queries | $0 |
| **Dev Total** | **$0.001** |

**Production Environment:**
| Service | Cost |
|---------|------|
| S3 storage + requests | $0.005 |
| CloudFront (free tier) | $0 |
| Route 53 alias queries | $0 |
| **Prod Total** | **$0.005** |

**Shared Services:**
| Service | Cost |
|---------|------|
| Route 53 hosted zone | $0.50 |
| ACM SSL certificates | $0 |
| IAM roles/policies | $0 |
| **Shared Total** | **$0.50** |

**Grand Total:** ~$0.51/month (~$6.12/year)

**Cost Comparison:**
- Current (manual): ~$0.50/month (single environment)
- With dev environment: ~$0.51/month (both environments)
- **Additional cost:** $0.01/month for dev environment

---

## Implementation Timeline

| Phase | Task | Duration |
|-------|------|----------|
| 1 | Create dev branch | 5 min |
| 2 | S3 dev bucket setup | 15 min |
| 3 | CloudFront distribution | 30 min |
| 4 | Route 53 subdomain | 10 min |
| 5 | IAM OIDC + roles | 20 min |
| 6 | GitHub Actions workflow | 30 min |
| 7 | Testing & verification | 20 min |
| **Total** | | **2h 10min** |

**Buffer:** +30-60 min for AWS propagation delays and troubleshooting

---

## Key Takeaways for 2026

### What's Changed Since 2024-2025

1. **OIDC is Standard:** Long-lived IAM keys deprecated for CI/CD
2. **OAC Replaced OAI:** Origin Access Identity no longer recommended
3. **Pricing Improvements:** CloudFront 30% cheaper, Route 53 queries reduced
4. **Account-Regional S3 Buckets:** Easier multi-environment naming
5. **Enhanced Security:** Default encryption, OIDC subject claims, GuardDuty improvements

### Critical Requirements

**Do This:**
- ✅ Use OIDC for GitHub Actions authentication
- ✅ Use Origin Access Control (OAC) for CloudFront → S3
- ✅ Use alias records in Route 53 (free queries)
- ✅ Enable S3 versioning (rollback capability)
- ✅ Separate IAM roles per environment
- ✅ Block public S3 access (use CloudFront only)

**Don't Do This:**
- ❌ Store AWS access keys in GitHub secrets
- ❌ Use Origin Access Identity (OAI) - deprecated
- ❌ Use CNAME records for CloudFront (charged, slower)
- ❌ Allow direct S3 public access
- ❌ Use wildcard IAM policies (`Resource: "*"`)
- ❌ Create ACM certificates outside us-east-1 for CloudFront

---

## Complete Source List

### AWS Official Documentation
- [S3 Static Website Hosting](https://docs.aws.amazon.com/AmazonS3/latest/userguide/WebsiteHosting.html)
- [CloudFront Private Content Access](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html)
- [Route 53 Alias Records](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resource-record-sets-choosing-alias-non-alias.html)
- [IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)

### 2026 Updates & Guides
- [S3 Account-Regional Namespaces](https://dev.to/aws-builders/amazon-s3-introduces-account-regional-namespaces-for-buckets-4m2f)
- [CloudFront OAC Setup 2026](https://oneuptime.com/blog/post/2026-02-12-cloudfront-origin-access-control-oac-s3/view)
- [Route 53 Pricing Reduction Feb 2026](https://aws.amazon.com/route53/pricing/)
- [GitHub Actions OIDC AWS 2026](https://oneuptime.com/blog/post/2026-02-02-github-actions-oidc-aws/view)
- [IAM Security Best Practices 2026](https://dev.to/karaniph/aws-iam-security-best-practices-in-2026-a-complete-guide-o14)

### Pricing Information
- [S3 Pricing 2026](https://www.cloudzero.com/blog/s3-pricing/)
- [CloudFront Pricing Explained 2026](https://blog.blazingcdn.com/en-us/aws-cloudfront-pricing-explained)
- [Route 53 Pricing](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/Route53Pricing.html)

---

**Research Complete:** May 30, 2026
**Next Step:** Review DEV_PROD_DEPLOYMENT_PLAN.md for implementation
**Confidence Level:** High (all findings from official 2026 documentation)