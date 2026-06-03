# Dev Branch Strategy

**Created:** April 13, 2026
**Purpose:** Staging environment workflow for safe production deployments
**Project:** Xenon 3 (NON-X)

---

## Overview

The `dev` branch serves as a **staging environment** for all changes before they reach production (`main`).

**Philosophy:** Test everything in staging before promoting to production.

---

## Branch Structure

```
main (production)
  ↑
  │ PR after QA passes
  │
dev (staging)
  ↑
  │ PR for each feature
  │
feature/name (development)
```

**Protection Rules:**
- `main`: Highly protected (no direct commits, requires review)
- `dev`: Protected (requires review, allows rebasing)
- `feature/*`: Unprotected (free development)

---

## Workflow

### 1. Feature Development

**Create feature branch from `dev` (NOT main):**
```bash
# Ensure dev is up to date
git checkout dev
git pull origin dev

# Create feature branch
git checkout -b feature/descriptive-name

# Example branch names:
# - feature/music-selector
# - feature/aws-migration
# - fix/button-animation
# - docs/update-readme
```

**Develop feature:**
- Make changes
- Test locally
- Commit frequently with clear messages

**Push to remote:**
```bash
git push -u origin feature/descriptive-name
```

---

### 2. Merge to Dev (Staging)

**Create PR to merge into `dev` (NOT main):**
1. Go to GitHub
2. Create Pull Request
3. Base: `dev` ← Compare: `feature/descriptive-name`
4. Title: Clear description of feature
5. Description: What was changed, why, testing done
6. Request review (if applicable)
7. Wait for CI checks to pass
8. Merge to `dev`

**After merge:**
```bash
# Switch to dev
git checkout dev

# Pull latest (including your merge)
git pull origin dev

# Delete feature branch (cleanup)
git branch -d feature/descriptive-name
git push origin --delete feature/descriptive-name
```

---

### 3. QA Testing on Dev

**Deploy `dev` branch to staging environment:**
- **Staging URL:** TBD (AWS staging environment)
- **Deploy trigger:** Automatic on push to `dev` (configured in CI/CD)
- **Purpose:** Full QA testing before production

**QA Checklist:**
- [ ] Feature works as expected
- [ ] No console errors
- [ ] Desktop + mobile tested
- [ ] No regressions (existing features still work)
- [ ] Analytics tracking works
- [ ] Performance acceptable
- [ ] Accessible (screen readers, keyboard navigation)

**If issues found:**
1. Create new `fix/issue-name` branch from `dev`
2. Fix issue
3. PR back to `dev`
4. Re-test
5. Repeat until QA passes

---

### 4. Production Promotion

**Only after `dev` passes complete QA:**

**Create PR from `dev` to `main`:**
```bash
# Ensure dev is up to date
git checkout dev
git pull origin dev

# Create PR on GitHub
# Base: main ← Compare: dev
```

**PR Requirements for Main:**
- ✅ All CI checks passing
- ✅ QA testing complete on staging
- ✅ At least 1 reviewer approval
- ✅ No merge conflicts
- ✅ All conversations resolved

**After merge to main:**
- Production deployment triggered automatically
- Monitor production for issues
- Be ready to rollback if needed

---

## Branch Protection Rules

### `main` Branch (Production)

**Settings → Branches → Add rule for `main`:**
- ✅ **Require pull request reviews:** 1 reviewer minimum
- ✅ **Require status checks to pass:** All CI checks must pass
- ✅ **Require conversation resolution:** All PR comments resolved
- ✅ **Include administrators:** Even admins must follow rules
- ✅ **Do not allow bypassing:** No exceptions
- ❌ **Allow force pushes:** DISABLED
- ❌ **Allow deletions:** DISABLED

**Result:** Cannot push directly to main, must use PR from dev

---

### `dev` Branch (Staging)

**Settings → Branches → Add rule for `dev`:**
- ✅ **Require pull request reviews:** 1 reviewer minimum
- ✅ **Require status checks to pass:** All CI checks must pass
- ⚠️ **Allow force pushes:** ENABLED (for rebasing only - use carefully)
- ❌ **Allow deletions:** DISABLED

**Result:** Must use PR for features, but can force-push if needed for cleanup

---

## AWS Deployment Configuration

### Staging Environment (dev branch)

**AWS Services:**
- S3 bucket: `xenon3-staging` (or similar)
- CloudFront distribution: Staging URL
- Route 53: `staging.xenon3.com` (or subdomain)
- Certificate Manager: SSL cert for staging

**Deploy Trigger:** Push to `dev` branch

**Purpose:**
- QA testing before production
- Test AWS configuration
- Verify CloudFront caching
- Test SSL certificates

---

### Production Environment (main branch)

**AWS Services:**
- S3 bucket: `xenon3-production` (or similar)
- CloudFront distribution: Production URL
- Route 53: `xenon3.com` (or custom domain)
- Certificate Manager: SSL cert for production

**Deploy Trigger:** Push to `main` branch

**Purpose:**
- Live player-facing deployment
- Maximum reliability
- Monitored for errors

---

## Rollback Procedures

### If Dev Deployment Fails (Staging)

**Low risk - easy to fix:**
```bash
# Option 1: Revert the problematic PR
git checkout dev
git revert [commit-hash]
git push origin dev

# Option 2: Reset dev to last working commit (more aggressive)
git checkout dev
git reset --hard [last-good-commit]
git push --force origin dev  # Force push allowed on dev
```

**Then:**
1. Fix issue in new feature branch
2. PR back to dev
3. Re-test

---

### If Main Deployment Fails (Production) 🚨

**High risk - must be fast:**

**Emergency Rollback:**
```bash
# Revert the merge commit
git checkout main
git revert -m 1 [merge-commit-hash]
git push origin main

# Production redeploys automatically to last working state
```

**Then:**
1. Investigate issue in dev
2. Fix in feature branch
3. Test thoroughly in dev staging
4. Re-promote to main when confident

**Prevent future issues:**
- More thorough QA in staging
- Add automated tests
- Test edge cases
- Monitor production carefully after deploys

---

## Benefits of Dev Branch Strategy

### ✅ Safety
- Catch issues in staging before production
- Test AWS configuration without risk
- Rollback dev freely without affecting users

### ✅ Speed
- Deploy to staging for quick QA
- Iterate rapidly in dev
- Promote to production with confidence

### ✅ Quality
- Full QA cycle before production
- Multiple review opportunities
- Reduces production bugs

### ✅ AWS Migration
- Test AWS setup in staging first
- Verify S3, CloudFront, Route 53 work
- Practice deployment process
- Move to production when ready

---

## Common Workflows

### Workflow 1: Simple Feature

```bash
# 1. Create from dev
git checkout dev
git checkout -b feature/new-button

# 2. Develop + test
git add button.html
git commit -m "feat: add new button"
git push -u origin feature/new-button

# 3. PR to dev → Merge

# 4. Test on staging
# Visit staging.xenon3.com
# Verify button works

# 5. If QA passes, PR dev → main

# 6. Production deploy
# Visit xenon3.com
# Verify button works in production
```

---

### Workflow 2: AWS Migration

```bash
# 1. Create from dev
git checkout dev
git checkout -b feature/aws-migration

# 2. Configure AWS (S3, CloudFront, etc.)
# Update deployment scripts
git add .github/workflows/deploy.yml
git commit -m "feat: add AWS deployment"

# 3. PR to dev → Merge

# 4. Deploy to AWS staging
# Test staging.xenon3.com thoroughly
# Verify all features work
# Check performance

# 5. If staging works perfectly, PR dev → main

# 6. Production AWS deploy
# Visit xenon3.com on AWS
# Monitor carefully
```

---

### Workflow 3: Hotfix

```bash
# Emergency fix needed in production

# 1. Create from main (not dev!)
git checkout main
git pull origin main
git checkout -b hotfix/critical-bug

# 2. Fix bug
git add fix.html
git commit -m "fix: resolve critical bug"

# 3. PR to main → Emergency review → Merge

# 4. Backport to dev
git checkout dev
git cherry-pick [hotfix-commit]
git push origin dev

# Result: Both main and dev have the fix
```

---

## Deployment Checklist

### Before Promoting Dev → Main:

- [ ] All features tested on staging
- [ ] Desktop + mobile verified
- [ ] No console errors
- [ ] Analytics working
- [ ] Performance acceptable
- [ ] No regressions
- [ ] Team approval
- [ ] CI checks passing
- [ ] Ready to monitor production

---

## Next Steps (After AWS Migration)

**Future Enhancements:**
1. Automated tests (run on every PR)
2. Performance budgets (fail if too slow)
3. Visual regression tests (screenshots)
4. Automated staging deploys
5. Slack notifications on deploy
6. Error monitoring (Sentry, LogRocket)

---

## Related Documentation

- **Safeguards Implementation Plan:** Process improvements
- **AWS Migration Plan:** TBD (detailed AWS setup)
- **MEMORY.md:** Project history

---

**Last Updated:** April 13, 2026
**Created By:** Safeguards Implementation Plan (Task #37)
**Purpose:** Enable safe AWS migration with staging environment