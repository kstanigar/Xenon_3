# AWS Deployment Status

**Last Updated:** May 30, 2026
**Status:** ✅ LIVE - Manual deployment active

## Live Infrastructure

### Production URL
**Domain:** https://nonx.standingtiger.com
**Status:** Active
**Deployment Date:** April 16, 2026

### AWS Services

| Service | Resource | Status |
|---------|----------|--------|
| **Route 53** | standingtiger.com hosted zone | ✅ Active |
| **Route 53** | nonx subdomain A record | ✅ Active → CloudFront |
| **S3** | nonx.standingtiger.com bucket | ✅ Active (20 objects) |
| **CloudFront** | Distribution d3lvcv... | ✅ Active |
| **ACM** | SSL certificate | ✅ Valid (auto-renewing) |
| **Lambda** | non-x-analytics-api | ✅ Active (Node.js 22.x) |

### Current Deployment Method
**Type:** Manual S3 sync
**Last Upload:** April 16, 2026
**Files:** 20 objects (assets/, HTML, sprites)

## Auto-Deployment Status

**GitHub Actions Workflow:** ❌ Not configured
**GitHub Secrets:** ❌ Not configured
**Target:** Create `.github/workflows/deploy-aws.yml`

**Implementation Docs:**
- AUTO_DEPLOYMENT_ANALYSIS.md (786 lines)
- DEPLOYMENT_QUICK_REFERENCE.md (282 lines)
- WORKFLOW_IMPLEMENTATION_GUIDE.md (608 lines)

**Estimated Setup:** 1.5-2 hours (reduced - asset paths already fixed)

## Next Actions

1. ✅ Archive outdated docs - COMPLETE (May 30, 2026)
2. ✅ Update README.md with AWS URL - COMPLETE (May 30, 2026)
3. ✅ Fix asset paths in game.html - COMPLETE (April 2026, commit fd7d0d6)
4. ✅ Verify live site functionality - COMPLETE (May 30, 2026)
5. ⏳ Configure GitHub Actions auto-deployment - READY (no blockers)
6. ⏳ Update Firebase/GA4 allowed domains - PENDING

## Migration Timeline

| Date | Event |
|------|-------|
| Apr 16, 2026 | Assets uploaded to S3 |
| Apr 16, 2026 | Asset paths updated in code (commit fd7d0d6) |
| Apr 17, 2026 | AWS migration PR merged (PR #107) |
| Apr 30, 2026 | Lambda analytics bridge deployed |
| May 30, 2026 | Documentation updated, archive created, asset paths verified |

## Cost Summary

**Monthly:** $1-3 (S3 storage, CloudFront data transfer, Route 53 hosted zone)
**Annual:** ~$40-60 (hosting + domain renewal)

## Rollback Plan

GitHub Pages still available as backup:
- Legacy URL: https://kstanigar.github.io/Xenon_3/
- Can redirect DNS back if needed
- Recovery time: 5-60 minutes (DNS propagation)