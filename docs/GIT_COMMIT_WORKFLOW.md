# Git Commit & Merge Workflow for Xenon 3

**Created:** May 31, 2026
**Purpose:** Safe git workflow to prevent accidental merges to main branch
**Project:** Xenon 3 (NON-X)

---

## Critical Rules

### 🚨 Rule #1: NO Co-Author Lines in Commit Messages
**NEVER include co-author attribution lines in commit messages.**

❌ **DO NOT USE:**
```
feat: add new feature

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

✅ **CORRECT FORMAT:**
```
feat: add new feature
```

---

### 🚨 Rule #2: ALWAYS Verify Base Branch Before Merging

**CRITICAL:** The dev branch has branch protection rules that require pull requests. When creating PRs:
1. **GitHub UI defaults to merging into `main`** (DANGEROUS!)
2. **ALWAYS change base branch to `dev`** before creating PR
3. **Double-check base branch** before clicking "Create pull request"

**Why this matters:**
- Merging to `main` triggers production deployment immediately
- Features should be tested on `dev` first
- Production should only receive tested, verified code

---

## Branch Protection Setup ✅ CONFIGURED

**Protected Branches:**
- `main`: ✅ Requires PRs (May 31, 2026)
- `dev`: ✅ Requires PRs (May 31, 2026)

**Configuration Applied:**
- ✅ Require a pull request before merging
- ❌ Require approvals (unchecked for solo developer workflow)
- ✅ Do not allow bypassing the above settings

**What this means:**
- Cannot push directly to `main` or `dev` ✅
- Must create feature branches and PRs ✅
- Can merge your own PRs without external approval ✅
- All commits must go through PR workflow ✅

**Documentation:** See GITHUB_BRANCH_PROTECTION_GUIDE.md for complete setup details

---

## Standard Workflow: Feature Branch → Dev → Main

### Step 1: Create Feature Branch

```bash
# Ensure dev is up to date
git checkout dev
git pull origin dev

# Create feature branch from dev
git checkout -b feature/your-feature-name

# Example:
git checkout -b feature/add-pink-infinite-level
```

**Branch Naming Conventions:**
- `feature/description` - New features
- `fix/description` - Bug fixes
- `refactor/description` - Code refactoring
- `docs/description` - Documentation updates
- `test/description` - Test additions

---

### Step 2: Make Changes and Commit

```bash
# Make your code changes
# ...

# Check status
git status

# Stage specific files (NEVER use "git add .")
git add path/to/file1.html path/to/file2.js

# Commit with clear message (NO co-author line)
git commit -m "feat: add pink infinite level

- Implement infinite scrolling background
- Add pink color theme variants
- Update enemy spawn patterns for infinite mode"
```

**Commit Message Format:**
```
<type>: <short description>

<optional detailed description>
- Bullet point 1
- Bullet point 2
```

**Types:**
- `feat:` - New feature
- `fix:` - Bug fix
- `refactor:` - Code refactoring
- `docs:` - Documentation changes
- `test:` - Test additions
- `chore:` - Maintenance tasks

---

### Step 3: Push Feature Branch

```bash
# Push feature branch to remote
git push -u origin feature/your-feature-name
```

**Output:**
```
remote: Create a pull request for 'feature/your-feature-name' on GitHub by visiting:
remote:      https://github.com/kstanigar/Xenon_3/pull/new/feature/your-feature-name
```

---

### Step 4: Create Pull Request (Terminal Method - RECOMMENDED)

**Using GitHub CLI (Safer than Web UI):**

```bash
# Install gh CLI if not already installed
# brew install gh  (macOS)

# Authenticate (one-time setup)
gh auth login

# Create PR with dev as base branch (CRITICAL!)
gh pr create --base dev --title "feat: your feature title" --body "Description of changes"

# Example:
gh pr create --base dev --title "feat: add pink infinite level" --body "## Summary
- Implement infinite scrolling background
- Add pink color theme variants
- Update enemy spawn patterns

## Testing
- Tested on dev environment
- All existing levels still functional"
```

**Advantages of Terminal Method:**
- Explicitly specify base branch (no UI mistakes)
- Faster workflow
- Scriptable and repeatable
- No risk of clicking wrong base branch

---

### Step 4 Alternative: Create Pull Request (Web UI Method)

**If using GitHub web interface:**

1. **Navigate to PR creation URL** (provided by git push output)

2. **🚨 CRITICAL: CHECK BASE BRANCH FIRST**
   - Look at top left: `base: main ← compare: feature/your-feature-name`
   - **Click "base: main" dropdown**
   - **Select "dev"** from dropdown
   - Verify it now shows: `base: dev ← compare: feature/your-feature-name`

3. **Fill in PR details:**
   - Title: `feat: your feature title`
   - Description: Summary of changes
   - DO NOT include co-author line

4. **Double-check base branch again** (paranoia is good!)

5. **Click "Create pull request"**

**Common Mistake:**
```
❌ WRONG: base: main ← compare: feature/your-feature-name
✅ RIGHT: base: dev ← compare: feature/your-feature-name
```

---

### Step 5: Merge Pull Request (Terminal Method - RECOMMENDED)

**Using GitHub CLI:**

```bash
# View PR details
gh pr view

# Check PR status and base branch
gh pr view --json baseRefName,headRefName,title

# Merge PR (will merge into base branch specified during creation)
gh pr merge --squash --delete-branch

# Alternative: Merge and keep branch
gh pr merge --squash
```

**Merge Options:**
- `--squash` - Squash all commits into one (recommended for feature branches)
- `--merge` - Standard merge commit (keeps all individual commits)
- `--rebase` - Rebase and merge (linear history)
- `--delete-branch` - Delete feature branch after merge

---

### Step 5 Alternative: Merge Pull Request (Web UI Method)

**If using GitHub web interface:**

1. **Navigate to PR page**

2. **🚨 FINAL CHECK: Verify base branch**
   - Look at PR title section
   - Should show: "wants to merge 1 commit into **dev** from feature/your-feature-name"
   - If it shows "into **main**", STOP and close the PR
   - Create new PR with correct base branch

3. **Click "Merge pull request"**

4. **Click "Confirm merge"**

5. **Optional: Delete branch**
   - Click "Delete branch" button after merge

---

### Step 6: Clean Up Local Branches

```bash
# Switch back to dev
git checkout dev

# Pull latest changes (includes your merged PR)
git pull origin dev

# Delete local feature branch
git branch -d feature/your-feature-name

# Verify branch is deleted
git branch
```

---

## Automatic Deployment Triggers

### When Commits Are Merged:

**Dev Branch → Dev Environment**
- **Trigger:** Any merge to `dev` branch
- **Deployment:** https://dev.nonx.standingtiger.com
- **S3 Bucket:** nonx-dev-032614958698-us-east-2-an
- **CloudFront:** E1Q496KLUYVM0Z
- **IAM Role:** github-actions-nonx-dev
- **Duration:** ~13 seconds

**Main Branch → Production Environment**
- **Trigger:** Any merge to `main` branch
- **Deployment:** https://nonx.standingtiger.com
- **S3 Bucket:** nonx.standingtiger.com
- **CloudFront:** ED9CRAIN93YRS
- **IAM Role:** github-actions-nonx-prod
- **Duration:** ~13 seconds

**⚠️ WARNING:** Merging to `main` deploys to production IMMEDIATELY!

---

## Emergency: Accidentally Merged to Wrong Branch

### If you accidentally merged to main instead of dev:

**Option 1: Revert the merge commit (SAFEST)**

```bash
# Find the merge commit hash
git log --oneline main -n 5

# Revert the merge commit
git revert -m 1 <merge-commit-hash>

# Push the revert
git push origin main
```

**Option 2: Force push (DANGEROUS - only if no one else has pulled)**

```bash
# Reset main to previous commit
git checkout main
git reset --hard HEAD~1

# Force push (requires admin permissions)
git push --force origin main
```

**⚠️ DO NOT use force push if:**
- Anyone else has pulled the main branch
- The commit has been deployed to production
- You're not 100% certain of what you're doing

**Option 3: Ask for help**
- Stop immediately
- Document what happened
- Ask team lead or senior developer for assistance

---

## Deploying to Production: Dev → Main

**Only deploy to production when dev is fully tested.**

### Step 1: Verify Dev Environment

```bash
# Ensure dev is up to date
git checkout dev
git pull origin dev

# Test dev site
# Visit: https://dev.nonx.standingtiger.com
# Verify all features work correctly
```

**Manual Testing Checklist:**
- [ ] Site loads without errors
- [ ] All game levels functional
- [ ] Leaderboard displays correctly
- [ ] Settings toggles work
- [ ] Mobile version works (game_mobile.html)
- [ ] No console errors
- [ ] Analytics tracking verified

---

### Step 2: Create PR from Dev to Main (Terminal Method)

```bash
# Ensure you're on dev branch
git checkout dev
git pull origin dev

# Create PR to merge dev into main
gh pr create --base main --head dev --title "chore: deploy dev to production" --body "## Summary
Deploying tested features from dev environment to production.

## Changes Included
- [List major features/fixes being deployed]

## Testing
- ✅ All features tested on dev.nonx.standingtiger.com
- ✅ No errors in console
- ✅ Mobile version verified
- ✅ Analytics tracking confirmed

## Deployment
This will trigger automatic deployment to:
- URL: https://nonx.standingtiger.com
- CloudFront: ED9CRAIN93YRS
- S3: nonx.standingtiger.com"
```

---

### Step 3: Review and Merge

```bash
# View the PR
gh pr view

# Check what commits will be merged
gh pr diff

# If everything looks good, merge
gh pr merge --squash --delete-branch
```

**What Happens:**
1. PR merged to `main` branch
2. GitHub Actions workflow triggers automatically
3. Deployment to production starts (~13 seconds)
4. Files synced to S3 production bucket
5. CloudFront cache invalidated
6. Production site updated: https://nonx.standingtiger.com

---

## Hotfix Workflow: Emergency Production Fix

**Use this workflow ONLY for critical production bugs.**

### Step 1: Create Hotfix Branch from Main

```bash
# Create hotfix branch from main
git checkout main
git pull origin main
git checkout -b hotfix/critical-bug-description

# Example:
git checkout -b hotfix/fix-leaderboard-crash
```

---

### Step 2: Make Fix and Commit

```bash
# Make minimal changes to fix the bug
# ...

# Commit the fix
git commit -m "fix: resolve leaderboard crash on game over

- Add null check for player score
- Prevent undefined access in submitScore function"
```

---

### Step 3: Push and Create PR to Main

```bash
# Push hotfix branch
git push -u origin hotfix/critical-bug-description

# Create PR to main (hotfix goes directly to production)
gh pr create --base main --title "hotfix: critical bug description" --body "## Critical Bug Fix

**Issue:** [Describe the production bug]

**Fix:** [Describe the fix applied]

**Testing:** [How you verified the fix]

**Urgency:** Production hotfix - requires immediate deployment"
```

---

### Step 4: Merge and Deploy

```bash
# Merge hotfix to main
gh pr merge --squash

# IMPORTANT: Also merge hotfix to dev to keep branches in sync
git checkout dev
git pull origin dev
git merge hotfix/critical-bug-description
git push origin dev

# Clean up
git branch -d hotfix/critical-bug-description
git push origin --delete hotfix/critical-bug-description
```

---

## Common Mistakes and How to Avoid Them

### ❌ Mistake 1: Merging to Main Instead of Dev

**Prevention:**
- Use terminal commands with explicit `--base dev`
- Always double-check base branch in GitHub UI
- Test on dev first, deploy to main later

---

### ❌ Mistake 2: Including Co-Author Line

**Prevention:**
- Remember: Rule #1 is NO co-author lines
- Review commit message before committing
- Use git commit templates if needed

---

### ❌ Mistake 3: Using "git add ."

**Prevention:**
- Always stage specific files: `git add path/to/file`
- Review `git status` before staging
- Avoid accidentally committing sensitive files (.env, credentials, etc.)

---

### ❌ Mistake 4: Force Pushing to Protected Branches

**Prevention:**
- NEVER use `git push --force` on `main` or `dev`
- Protected branches should never need force push
- Use revert commits instead of rewriting history

---

### ❌ Mistake 5: Not Testing Before Production Deploy

**Prevention:**
- ALWAYS test on dev environment first
- Use the checklist in "Deploying to Production" section
- Never merge dev → main without verification

---

## Git Command Quick Reference

### Branch Operations
```bash
# List all branches
git branch -a

# Create new branch
git checkout -b feature/name

# Switch branches
git checkout branch-name

# Delete local branch
git branch -d branch-name

# Delete remote branch
git push origin --delete branch-name
```

### Viewing Changes
```bash
# View status
git status

# View commit history
git log --oneline -n 10

# View changes in working directory
git diff

# View changes in staging area
git diff --staged

# View file history
git log --follow -- path/to/file
```

### Undoing Changes
```bash
# Unstage file
git restore --staged path/to/file

# Discard local changes
git restore path/to/file

# Amend last commit (only if not pushed!)
git commit --amend -m "new message"

# Revert commit (creates new commit)
git revert commit-hash
```

### Remote Operations
```bash
# View remotes
git remote -v

# Fetch remote changes (no merge)
git fetch origin

# Pull remote changes (fetch + merge)
git pull origin branch-name

# Push to remote
git push origin branch-name

# Force push (DANGEROUS - avoid on protected branches)
git push --force origin branch-name
```

---

## GitHub CLI (gh) Quick Reference

### Authentication
```bash
# Login to GitHub
gh auth login

# Check auth status
gh auth status
```

### Pull Requests
```bash
# Create PR
gh pr create --base dev --title "title" --body "description"

# List PRs
gh pr list

# View PR details
gh pr view PR_NUMBER

# View PR in browser
gh pr view --web

# Check PR status
gh pr status

# Merge PR
gh pr merge PR_NUMBER --squash

# Close PR
gh pr close PR_NUMBER
```

### Repository Info
```bash
# View repo in browser
gh repo view --web

# View issues
gh issue list

# View actions/workflows
gh workflow list

# View recent workflow runs
gh run list
```

---

## Troubleshooting

### Problem: "failed to push some refs" (branch protection)

**Solution:** You're trying to push directly to a protected branch. Use the PR workflow instead.

```bash
# Create feature branch
git checkout -b feature/your-feature

# Push feature branch
git push -u origin feature/your-feature

# Create PR
gh pr create --base dev
```

---

### Problem: Merge conflict during PR

**Solution:** Rebase your feature branch on latest dev.

```bash
# Update dev
git checkout dev
git pull origin dev

# Rebase feature branch
git checkout feature/your-feature
git rebase dev

# Resolve conflicts (if any)
# Edit files, then:
git add path/to/resolved-file
git rebase --continue

# Force push (feature branch only!)
git push --force origin feature/your-feature
```

---

### Problem: Accidentally committed sensitive data

**Solution:** Remove from history immediately.

```bash
# If not pushed yet:
git reset --soft HEAD~1
git restore --staged path/to/sensitive-file

# If already pushed (requires force push):
# 1. Remove from latest commit
git rm --cached path/to/sensitive-file
git commit --amend -m "remove sensitive data"

# 2. Force push (dangerous!)
git push --force origin branch-name

# 3. Rotate/invalidate the exposed credentials immediately
```

---

### Problem: Need to undo a merge to main

**Solution:** Revert the merge commit (safest).

```bash
# Find merge commit
git log --oneline main -n 5

# Revert merge
git revert -m 1 <merge-commit-hash>

# Push revert
git push origin main
```

---

## Best Practices Summary

### ✅ DO:
- Always work on feature branches
- Use descriptive branch names
- Write clear commit messages
- Stage specific files (never `git add .`)
- Test on dev before deploying to main
- Use terminal commands for critical operations
- Double-check base branch before creating PRs
- Keep commits focused and atomic
- Pull latest changes before creating new branches

### ❌ DON'T:
- Never include co-author lines in commits
- Never push directly to `main` or `dev`
- Never use `git add .` (stage specific files)
- Never merge to main without testing on dev
- Never force push to protected branches
- Never commit sensitive data (.env, credentials)
- Never assume GitHub UI has correct base branch
- Never skip the PR review process

---

## Related Documentation

- **DEV_PROD_DEPLOYMENT_PLAN.md** - Overall deployment architecture
- **DEPLOYMENT_PROGRESS.md** - Phase-by-phase implementation tracking
- **GitHub Actions Workflow** - .github/workflows/deploy-aws.yml

---

**Last Updated:** May 31, 2026
**Maintained By:** Project team
**Review Frequency:** After any git workflow changes