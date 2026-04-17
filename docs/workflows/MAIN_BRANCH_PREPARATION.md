# Main Branch Preparation for Dev Merge

**Created:** April 15, 2026
**Purpose:** Document how to prepare main branch to receive safeguards from dev branch
**Project:** Xenon 3 (NON-X)

---

## ⚠️ CRITICAL WARNING - READ FIRST

**DO NOT merge dev → main until:**
- ✅ AWS staging deployment complete on dev branch
- ✅ Full QA testing passed on AWS staging environment
- ✅ All game features verified working on AWS
- ✅ Performance acceptable on AWS CloudFront
- ✅ SSL certificates working correctly
- ✅ No critical bugs found during staging QA

**Current Status:** Dev branch has safeguards, main does NOT. Branches diverged by 6 commits.

**Workflow:** dev (staging) → AWS deploy → QA test → **THEN** promote to main

**See:** DEV_BRANCH_STRATEGY.md section "Production Promotion" (lines 122-147)

---

## Overview

When dev branch is ready to merge to main (after AWS QA passes), you need to prepare main branch to receive the changes. This document covers:

1. Branch protection updates for main
2. What happens to yml files (automatic via merge)
3. Pre-merge verification checklist
4. Merge procedure
5. Post-merge verification

---

## Current State Analysis

### Dev Branch (6 commits ahead of main)
**Contains:**
- ✅ 4 safeguard files (.claude/hooks, .claude/skills, .claude/rules, docs/workflows)
- ✅ Updated .github/workflows/integrity-check.yml (47 new lines, 5 new checks)
- ✅ Updated docs/workflows/SAFEGUARDS_IMPLEMENTATION_PLAN.md
- ✅ CI checks trigger on `dev` branch
- ✅ Job names removed from workflow (fix for check name mismatch)
- ✅ Console.log check changed to WARNING (allows dev mode logging)

**Branch Protection:**
- ✅ Enforcement: Active
- ✅ Target branch: `dev`
- ✅ Required approvals: 0
- ✅ Required status checks: `check-game-html`, `check-game-mobile-html`

### Main Branch (current production)
**Contains:**
- ❌ No safeguard files
- ❌ Old .github/workflows/integrity-check.yml (only original checks, no new 5 checks)
- ❌ CI checks only trigger on `main` branch (not `dev`)
- ❌ Job names still present in workflow (will cause check name mismatch if not updated)
- ⚠️ Branch protection likely needs updates

**Branch Protection (needs verification):**
- Status: Unknown - needs to be checked and updated
- Required: Same settings as dev branch for consistency

---

## Step 1: Verify Current Main Branch Protection

**Before making changes, document current settings:**

1. **Go to GitHub:**
   - Navigate to: https://github.com/kstanigar/Xenon_3/settings/rules
   - Look for ruleset targeting `main` branch

2. **Check if main branch ruleset exists:**
   - ✅ If exists: Note current settings
   - ❌ If doesn't exist: You'll create one in Step 2

3. **Document current settings** (if ruleset exists):
   ```
   Enforcement: [Active/Disabled/Evaluate]
   Target branch: [main/other]
   Required approvals: [number]
   Required status checks: [list]
   Dismiss stale reviews: [Yes/No]
   Require conversation resolution: [Yes/No]
   Block force pushes: [Yes/No]
   ```

---

## Step 2: Update Main Branch Protection Settings

**Goal:** Match dev branch protection settings for consistency

### Option A: Main Branch Ruleset Already Exists

**Update existing ruleset:**

1. **Go to:** https://github.com/kstanigar/Xenon_3/settings/rules
2. **Find:** Ruleset targeting `main` branch
3. **Click:** Edit (pencil icon)
4. **Update settings to match dev:**

   **Enforcement:**
   - Set to: **Active** (dropdown)

   **Target branches:**
   - Include default branch: ✅ Checked
   - OR Include by pattern: `main` (text field)

   **Branch protections (Require a pull request before merging):**
   - ✅ Enable (toggle)
   - Required approvals: **0** (number field)
     - Reason: Solo developer, can't approve own PRs with >0
   - ✅ Dismiss stale pull request approvals when new commits are pushed

   **Require status checks to pass:**
   - ✅ Enable (toggle)
   - Click "Add checks" button
   - Search for and add:
     - `check-game-html`
     - `check-game-mobile-html`
   - **CRITICAL:** Check names must match workflow job IDs (not job names)

   **Block force pushes:**
   - ✅ Enable (toggle)
   - Reason: Protect production history

   **Require conversation resolution:**
   - ✅ Enable (toggle)
   - Reason: Ensure PR discussions are addressed

5. **Click:** "Save changes"

### Option B: Main Branch Ruleset Does NOT Exist

**Create new ruleset:**

1. **Go to:** https://github.com/kstanigar/Xenon_3/settings/rules
2. **Click:** "New branch ruleset" (green button)
3. **Configure:**

   **Ruleset Name:**
   - Enter: `main-branch-protection`

   **Enforcement status:**
   - Select: **Active** (dropdown)

   **Target branches:**
   - Include default branch: ✅ Check this
   - Should show: `main` as target

   **Branch protections:**
   - ✅ Require a pull request before merging
   - Required approvals: **0**
   - ✅ Dismiss stale pull request approvals when new commits are pushed

   **Require status checks to pass:**
   - ✅ Enable
   - Click "Add checks"
   - Add: `check-game-html`
   - Add: `check-game-mobile-html`

   **Additional protections:**
   - ✅ Block force pushes
   - ✅ Require conversation resolution before merging

4. **Click:** "Create" (green button at bottom)

---

## Step 3: Understand What Happens to YML Files

### Important: YML Files Update AUTOMATICALLY via Merge

**You do NOT need to manually update yml files on main branch.**

**Why:**
- The updated `.github/workflows/integrity-check.yml` exists on dev branch
- When you merge dev → main via PR, the updated yml file will be included
- GitHub will start using the new workflow immediately after merge

**What the merge will bring to main:**
1. **5 new CI checks** (console.log, debugger, TODO/FIXME, file sizes, parity)
2. **Trigger on both branches** (`branches: [ main, dev ]`)
3. **Job name fix** (removed `name:` fields to use job IDs)
4. **Console.log changed to WARNING** (allows dev mode logging)

**Current main yml** (before merge):
```yaml
on:
  push:
    branches: [ main ]  # Only triggers on main
  pull_request:
    branches: [ main ]

jobs:
  check-game-html:
    runs-on: ubuntu-latest
    name: Verify game.html functions  # Has name field (causes mismatch)
    # No new checks (console.log, debugger, etc.)
```

**Updated yml** (after dev merge):
```yaml
on:
  push:
    branches: [ main, dev ]  # Triggers on both
  pull_request:
    branches: [ main, dev ]

jobs:
  check-game-html:
    runs-on: ubuntu-latest
    # No name field - uses job ID (fixes mismatch)
    # Has 5 new checks (console.log, debugger, TODO/FIXME, etc.)
```

---

## Step 4: Pre-Merge Verification Checklist

**Before creating PR from dev → main, verify:**

### AWS Staging QA Complete
- [ ] Game deployed to AWS staging on dev branch
- [ ] S3 bucket serving files correctly
- [ ] CloudFront CDN caching working
- [ ] Route 53 DNS pointing to staging environment
- [ ] SSL certificate valid and working
- [ ] Desktop game loads without errors
- [ ] Mobile game loads without errors
- [ ] All 12 levels playable
- [ ] Leaderboard submission working
- [ ] Analytics tracking working
- [ ] Audio playback working
- [ ] Performance acceptable (no lag/stutter)

### Branch Protection Configured
- [ ] Main branch ruleset exists and is ACTIVE
- [ ] Required status checks added: `check-game-html`, `check-game-mobile-html`
- [ ] Required approvals set to 0 (solo developer)
- [ ] Force pushes blocked
- [ ] Conversation resolution required

### Git State Clean
- [ ] Dev branch up to date: `git checkout dev && git pull origin dev`
- [ ] No uncommitted changes: `git status` shows clean
- [ ] All commits pushed: `git log origin/dev..dev` shows nothing
- [ ] Main branch up to date: `git checkout main && git pull origin main`

### CI Checks Passing on Dev
- [ ] Latest dev branch CI checks passed (green checkmarks)
- [ ] No empty black squares (check name mismatch resolved)
- [ ] Both jobs completed: `check-game-html`, `check-game-mobile-html`
- [ ] Console.log warnings acceptable (not failing build)

---

## Step 5: Create PR from Dev to Main

**Only after Step 4 checklist is complete:**

### Via GitHub Web UI (Recommended)

1. **Go to:** https://github.com/kstanigar/Xenon_3
2. **Click:** "Pull requests" tab
3. **Click:** "New pull request" (green button)
4. **Configure PR:**
   - Base: `main` (left dropdown)
   - Compare: `dev` (right dropdown)
   - Should show: "6 commits" and file changes
5. **Review changes:**
   - Verify 4 new safeguard files appear
   - Verify .github/workflows/integrity-check.yml shows 47 new lines
   - Verify no unexpected file changes
6. **Click:** "Create pull request"
7. **Fill in PR details:**

   **Title:**
   ```
   chore: merge safeguards implementation from dev to main
   ```

   **Description:**
   ```
   ## Summary
   Merge safeguards implementation from dev branch to main after successful AWS staging QA.

   ## Changes Included
   - 4 safeguard files (hooks, skills, rules, dev branch strategy)
   - Enhanced CI/CD integrity checks (5 new production quality checks)
   - Updated workflow triggers (now runs on both main and dev)
   - CI check name mismatch fix (removed job names)
   - Console.log check changed to warning (allows dev mode logging)

   ## Testing
   - ✅ AWS staging deployment successful
   - ✅ Full QA testing passed on staging environment
   - ✅ CI checks passing on dev branch
   - ✅ Branch protection configured on main

   ## Files Changed
   - `.claude/hooks/pre-execution-checklist.md` (new)
   - `.claude/skills/handoff-protocol.md` (new)
   - `.claude/rules/multi-agent-verification.md` (new)
   - `docs/workflows/DEV_BRANCH_STRATEGY.md` (new)
   - `.github/workflows/integrity-check.yml` (updated, +47 lines)
   - `docs/workflows/SAFEGUARDS_IMPLEMENTATION_PLAN.md` (updated)

   ## Post-Merge Steps
   - Monitor CI checks on main branch
   - Verify production deployment (if auto-deploy configured)
   - Update MEMORY.md with merge completion
   ```

8. **Click:** "Create pull request"

### Via Command Line (Alternative)

```bash
# Ensure dev is up to date
git checkout dev
git pull origin dev

# Ensure main is up to date
git checkout main
git pull origin main

# Create PR using GitHub CLI (if installed)
gh pr create --base main --head dev --title "chore: merge safeguards from dev to main" --body "See description in GitHub UI"

# If gh CLI not installed, use web UI method above
```

---

## Step 6: Review and Merge PR

### Review Checklist

**Before clicking "Merge pull request":**

1. **Verify CI checks passed:**
   - [ ] `check-game-html` - Green checkmark
   - [ ] `check-game-mobile-html` - Green checkmark
   - [ ] No empty black squares (name mismatch resolved)
   - [ ] No failed checks

2. **Review file changes one more time:**
   - [ ] 4 new safeguard files look correct
   - [ ] integrity-check.yml changes look correct (47 new lines)
   - [ ] No unexpected deletions
   - [ ] No merge conflicts

3. **Verify branch protection working:**
   - [ ] Cannot merge without status checks passing
   - [ ] Required approvals is 0 (shows "Approved" or allows merge)
   - [ ] Conversation resolution not blocking (no unresolved comments)

### Merge the PR

1. **Click:** "Merge pull request" (green button)
2. **Merge method:** Choose "Create a merge commit" (default)
   - Reason: Preserves full history, shows clear promotion point
   - Alternative: "Squash and merge" (cleaner history, loses individual commits)
3. **Confirm merge**
4. **Delete feature branch?** NO - keep `dev` branch (it's your staging environment)

---

## Step 7: Post-Merge Verification

**Immediately after merge:**

### 1. Verify Main Branch Updated

```bash
# Switch to main
git checkout main

# Pull latest (includes merge commit)
git pull origin main

# Verify safeguard files exist
ls -la .claude/hooks/pre-execution-checklist.md
ls -la .claude/skills/handoff-protocol.md
ls -la .claude/rules/multi-agent-verification.md
ls -la docs/workflows/DEV_BRANCH_STRATEGY.md

# Verify yml file updated
git log -1 --stat .github/workflows/integrity-check.yml
# Should show recent merge commit with +47 lines
```

### 2. Verify CI Checks on Main

1. **Go to:** https://github.com/kstanigar/Xenon_3/actions
2. **Check:** Latest workflow run on main branch
3. **Verify:** Both jobs passing
   - `check-game-html` - Green checkmark
   - `check-game-mobile-html` - Green checkmark
4. **If checks fail:**
   - Review GitHub Actions logs
   - Check for unexpected issues
   - May need to create hotfix PR

### 3. Verify Production Deployment (if auto-deploy configured)

**If GitHub Pages auto-deploys from main:**

1. Wait 2-5 minutes for deployment
2. Visit: https://kstanigar.github.io/Xenon_3/
3. Verify game still works
4. Check browser console for errors
5. Test basic functionality:
   - Game loads
   - Can start playing
   - Audio works
   - No JS errors

**If AWS auto-deploys from main:**

1. Wait for AWS deployment to complete (check CI/CD logs)
2. Visit production AWS URL
3. Verify same functionality as staging
4. Monitor CloudWatch logs for errors

### 4. Update Dev Branch (Sync with Main)

**After merging to main, sync dev branch:**

```bash
# Switch to dev
git checkout dev

# Pull latest dev (should be same as before merge)
git pull origin dev

# Merge main back into dev (keeps them in sync)
git merge main

# Should say "Already up to date" (fast-forward merge)

# Push to remote (if any updates)
git push origin dev
```

**Why sync dev with main:**
- Keeps dev branch clean for next feature
- Prevents merge conflicts on next dev → main PR
- Ensures both branches have same safeguards

---

## Step 8: Document Merge Completion

**Update MEMORY.md:**

Add a new section documenting the merge:

```markdown
## ✅ COMPLETE - Safeguards Promoted to Main (April XX, 2026)

**STATUS:** ✅ Complete - Main branch now has safeguards
**MERGE DATE:** April XX, 2026
**PR:** #XXX (dev → main)

### Promotion Summary

Successfully promoted safeguards implementation from dev to main after AWS staging QA passed.

**Changes Merged:**
- 4 safeguard files (hooks, skills, rules, dev branch strategy)
- Enhanced CI/CD integrity checks (5 new production quality checks)
- Updated workflow triggers (now runs on both main and dev)
- CI check name mismatch fix (removed job names)
- Console.log check changed to warning (allows dev mode logging)

**Verification:**
- ✅ CI checks passing on main branch
- ✅ Production deployment successful
- ✅ Game functionality verified
- ✅ No regressions detected

**Git State:**
- Main branch: 6 commits updated (now matches dev)
- Dev branch: Synced with main, ready for next feature
- Both branches: Have safeguards, CI checks, branch protection

**Next Steps:**
- Continue with next feature development on dev branch
- Follow DEV_BRANCH_STRATEGY.md workflow for future releases
```

---

## Common Issues & Solutions

### Issue 1: Status Checks Not Appearing

**Symptom:** Can't add `check-game-html` or `check-game-mobile-html` to required checks

**Cause:** Checks haven't run on main branch yet (only exist on dev)

**Solution:**
```bash
# Option A: Create empty PR to trigger checks on main
git checkout main
git checkout -b trigger-checks
git commit --allow-empty -m "chore: trigger CI checks"
git push -u origin trigger-checks

# Create PR to main, let checks run, then close PR without merging
```

**Solution B:** Add checks after dev → main merge (checks will be available once yml file is on main)

### Issue 2: "Authors Can't Approve Own PRs"

**Symptom:** PR shows "Review required" but you can't approve it

**Solution:** Set "Required approvals" to **0** in branch protection settings

### Issue 3: Merge Conflicts

**Symptom:** PR shows "This branch has conflicts that must be resolved"

**Cause:** Main branch changed since dev branch was created

**Solution:**
```bash
# Update dev with latest main
git checkout dev
git pull origin dev
git merge main

# Resolve any conflicts
# Edit conflicting files
git add <resolved-files>
git commit -m "chore: merge main into dev, resolve conflicts"
git push origin dev

# PR should now show "No conflicts"
```

### Issue 4: Empty Black Squares (Check Name Mismatch)

**Symptom:** CI checks show empty black squares, never complete

**Cause:** Job `name:` field doesn't match ruleset expectations

**Verification:**
```bash
# Check if yml file has name fields
grep "name: Verify" .github/workflows/integrity-check.yml

# Should return nothing (if fixed)
# If returns matches, job names still present (need to remove)
```

**Solution:** Already fixed on dev branch (name fields removed). Will auto-fix when dev merges to main.

---

## Timeline Estimate

**Total time:** ~30-45 minutes

| Step | Task | Time |
|------|------|------|
| 1 | Verify current main protection | 5 min |
| 2 | Update branch protection | 10 min |
| 3 | Understand yml files (read) | 5 min |
| 4 | Pre-merge verification | 10 min |
| 5 | Create PR | 5 min |
| 6 | Review and merge | 5 min |
| 7 | Post-merge verification | 10 min |
| 8 | Document completion | 5 min |

**Note:** Does NOT include AWS staging QA time (4-6 hours) - that's prerequisite

---

## Summary Checklist

**Before creating dev → main PR:**
- [ ] AWS staging QA complete and passed
- [ ] Main branch protection configured
- [ ] Main branch up to date
- [ ] Dev branch up to date
- [ ] CI checks passing on dev
- [ ] No uncommitted changes

**During PR review:**
- [ ] File changes look correct
- [ ] CI checks passing
- [ ] No merge conflicts
- [ ] PR description complete

**After merge:**
- [ ] Main branch updated locally
- [ ] CI checks passing on main
- [ ] Production deployment successful (if applicable)
- [ ] Dev branch synced with main
- [ ] MEMORY.md updated with merge completion

---

## Related Documentation

- **DEV_BRANCH_STRATEGY.md** - Staging workflow and promotion process
- **SAFEGUARDS_IMPLEMENTATION_PLAN.md** - What was implemented
- **MEMORY.md** - Project history and handoff summaries

---

**Document Created:** April 15, 2026
**Last Updated:** April 15, 2026
**Purpose:** Prepare main branch for safeguards merge after AWS staging QA
**Important:** Only merge after AWS QA passes completely