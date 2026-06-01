# GitHub Branch Protection Guide for Solo Developers

**Created:** May 31, 2026
**Last Updated:** May 31, 2026
**Audience:** Solo developers managing single-person repositories
**Status:** Complete Research and Documentation

---

## Executive Summary

GitHub offers two approaches to branch protection in 2026:

1. **Classic Branch Protection Rules** - Traditional, repository-level rules
2. **Repository Rulesets** - Modern, more flexible, and now the recommended approach

### Recommendation for Solo Developers

**Use Repository Rulesets** for new projects. If you already use classic branch protection rules, they continue to work fine, but rulesets offer:
- Easier management (enable/disable without deletion)
- Better transparency (anyone with read access can view active rules)
- More control options
- Ability to layer multiple rules simultaneously

**Key Decision:** For solo developers wanting to prevent accidental direct pushes while maintaining workflow efficiency:
- **Enable:** "Require pull requests" (forces all changes through PR workflow)
- **Enable:** "Require approvals" setting - **BUT keep it UNCHECKED or set to 0 approvals** (allows you to merge your own PRs without external approval)
- **Enable:** "Require status checks to pass" (optional but recommended - ensures CI/CD validation)

---

## Part 1: Classic Branch Protection Rules vs Repository Rulesets

### Detailed Comparison

| Feature | Classic Rules | Rulesets | Winner |
|---------|---------------|----------|--------|
| **Number of Rules Applied** | Only one rule can apply per branch | Multiple rules apply simultaneously | Rulesets |
| **Rule Management** | Must delete and recreate to disable | Enable/disable with toggle status | Rulesets |
| **Scope** | Branches only | Branches, tags, and repository-wide events | Rulesets |
| **Centralization** | Repository-level only | Can be organization-level or repository-level | Rulesets |
| **Transparency** | Requires admin access to view | Anyone with read access can view | Rulesets |
| **Compatibility** | Standalone | Works alongside branch protection rules | Rulesets |
| **Learning Curve** | Simpler, more established | Slightly more options, still intuitive | Slight edge: Classic |

### Key Differences Explained

#### Classic Branch Protection Rules
According to [GitHub Docs on Protected Branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches):

> "You can enforce certain workflows for one or more branches, such as requiring an approving review or passing status checks for all pull requests merged into the protected branch."

- Only one rule pattern can apply to a branch at a time
- Rules are stored at the repository level
- Often duplicated across multiple repositories in an organization
- Well-established interface used by millions of developers

#### Repository Rulesets
According to [GitHub Docs on Rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets):

> "Rulesets help you to control how people can interact with branches and tags in a repository. Unlike protection rules, multiple rulesets can apply at the same time, so you can be confident that every rule targeting a branch in your repository will be evaluated when someone interacts with that branch."

**Key advantage:** Multiple rulesets can apply simultaneously, eliminating ambiguity about which rule will take effect.

### Which Should You Use?

**Choose Rulesets if:**
- Starting a new project
- Want the latest GitHub features (improved required reviewer rule became GA in February 2026)
- Need to scale rules across multiple repositories
- Want cleaner management (enable/disable without deletion)

**Classic Rules are fine if:**
- Already implemented in your project
- Prefer the established, simpler interface
- Don't need advanced features
- Working on an older GitHub plan tier

---

## Part 2: Solo Developer Configuration - The Approval Dilemma

### The Problem

GitHub does not allow developers to approve their own pull requests. The approval dropdown shows "1-6" because GitHub is designed for team workflows where someone else reviews your code.

This creates a dilemma for solo developers:
- **If you enable "Require approvals" and select 1+:** You cannot merge your own PRs (GitHub blocks self-approval)
- **If you leave "Require approvals" unchecked:** You can merge your own PRs, but the dropdown disappears entirely

### The Official Solution

According to [GitHub community discussions on approval requirements](https://github.com/orgs/community/discussions/49633), GitHub acknowledges that solo developers face this limitation. The recommended workaround:

**For solo developers wanting to require PRs without approval blockers:**

```
✅ RECOMMENDED CONFIGURATION:

1. Require a pull request before merging: ENABLED
2. Require approvals: UNCHECKED (do not enable)
3. Require status checks before merging: ENABLED (recommended)
   - Configure your CI/CD pipeline to run on all PRs
```

This approach:
- Prevents accidental direct pushes to main/dev
- Forces all changes through the PR workflow (creates audit trail, enables discussion)
- Allows you to merge your own PRs without external approval
- Still validates code quality through automated status checks (tests, linting, etc.)

### Alternative: Auto-Approval GitHub Action

If you want the approval step but automated, you can use a GitHub Action to automatically approve your own PRs:
- [GitHub Repository Self-Approve Action](https://github.com/marketplace/actions/github-repository-self-approve-action)
- [Configurable Required Approvals](https://github.com/marketplace/actions/configurable-required-approvals)

These allow you to maintain the approval workflow structure while automating it. However, most solo developers find the "require PR only" approach cleaner.

---

## Part 3: Step-by-Step Configuration - Classic Branch Protection

This section provides exact UI instructions for configuring classic branch protection rules.

### Prerequisites
- Repository owner or admin permissions
- Branches you want to protect (typically `main` and `dev`)

### Step 1: Access Branch Protection Settings

1. Go to your repository on GitHub
2. Click **Settings** (in the top navigation bar)
3. In the left sidebar, click **Branches**
4. Click **Add rule** button (or edit an existing rule)

### Step 2: Configure Basic Rule Properties

| Setting | Value | Explanation |
|---------|-------|-------------|
| **Branch name pattern** | `main` | Enter the exact branch name (or use wildcards like `release/*`) |
| | `dev` | Run steps 1-5 again for each protected branch |

### Step 3: Require Pull Requests (ALWAYS ENABLE)

#### Checkbox: "Require a pull request before merging"
- **Status:** ☑ ENABLED
- **Purpose:** Prevents direct git pushes to the branch; all changes must go through a pull request
- **Effect:** Blocks commands like `git push origin main`

After checking this box, three sub-options appear:

#### Sub-option 1: "Require approvals"
- **Status:** ☐ UNCHECKED (for solo developers)
- **Why:** Enabling this requires other users to approve your PRs, which blocks solo development
- **Solo Developer Note:** Leaving this unchecked allows you to merge your own PRs immediately after the PR is created
- **Alternative:** If you want approvals, select 1 and use an auto-approval GitHub Action

#### Sub-option 2: "Dismiss stale pull request approvals when new commits are pushed"
- **Status:** ☑ ENABLED (if you use approvals)
- **Purpose:** Re-validates that approvers are reviewing the latest version of your code
- **Effect:** If new commits are pushed to the PR, existing approvals are marked as stale and new approval is required
- **Explanation:** According to [GitHub Docs](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule):

> "When you push a new commit to a branch that has been merged or pushed to, the approving review is dismissed as stale, and the pull request cannot be merged until someone approves the work again."

#### Sub-option 3: "Require review from Code Owners"
- **Status:** ☐ UNCHECKED (for solo developers)
- **Purpose:** Requires approval from specific team members listed in CODEOWNERS file
- **Solo Context:** Only useful if you have defined code owners who should review specific files

### Step 4: Require Status Checks (RECOMMENDED)

#### Checkbox: "Require status checks to pass before merging"
- **Status:** ☑ ENABLED (recommended)
- **Purpose:** Ensures automated tests, linting, and CI/CD pass before merge is allowed
- **Benefit for Solo Devs:** Catches bugs automatically without needing human approval

After checking this box, two sub-options appear:

#### Sub-option 1: "Require branches to be up to date before merging"
- **Status:** ☑ ENABLED
- **Purpose:** Prevents merge if another PR has been merged after this PR was created
- **Effect:** Forces you to rebase/merge with main before completing your PR
- **Reason:** Ensures your code is tested against the latest version of main

#### Sub-option 2: "Select status checks that must pass"
- **Status:** Add any CI/CD checks from your workflow
- **Example:** If you use GitHub Actions, add checks like:
  - `continuous-integration/your-action-name`
  - Tests, linting, builds, etc.
- **If none appear:** Your repository hasn't run any status checks yet. They'll appear automatically after your first workflow run.

### Step 5: Enforce Rules for Administrators

#### Checkbox: "Do not allow bypassing the above settings"
- **Status:** ☑ ENABLED (recommended)
- **Purpose:** Prevents even repository admins from pushing directly or merging without PR/status checks
- **Explanation:** According to [GitHub Changelog on Bypass Permissions](https://github.blog/changelog/2022-08-18-bypass-branch-protections-with-a-new-permission/):

> "When you enable this option, it applies all of your branch protection rules (such as required reviews, status checks, etc.) universally—including to administrators and anyone with bypass permissions."

- **Why Enable:** Prevents "just this once" exceptions that undermine the protection
- **For Solo Devs:** Especially valuable since you're the only one who might be tempted to bypass

### Step 6: Restrict Who Can Push (Optional)

#### Section: "Restrict who can push to matching branches"
- **Status:** Leave empty (for solo developers)
- **Purpose:** Allows you to specify teams/users who can push to the branch
- **Solo Developer Use:** Usually not needed; you have permission anyway as the owner

### Step 7: Review and Save

1. Scroll down and review all settings
2. Click **Create** (for new rule) or **Update** (for existing rule)
3. You should see the rule listed under "Branch protection rules"

### Step 8: Repeat for Additional Branches

Repeat steps 1-7 for each branch you want to protect (typically `dev` if you have it).

---

## Part 4: Step-by-Step Configuration - Repository Rulesets

Repository Rulesets are the modern approach (and recommended for new projects).

### Prerequisites
- Repository owner or admin permissions
- GitHub Free, Pro, Team, or Enterprise plan

### Step 1: Access Rulesets Settings

1. Go to your repository on GitHub
2. Click **Settings**
3. In the left sidebar, click **Rules** > **Rulesets** (or just look for "Rulesets" if the UI has changed)
4. Click **New ruleset** > **New branch ruleset**

### Step 2: Name and Target Your Ruleset

| Setting | Value | Explanation |
|---------|-------|-------------|
| **Ruleset name** | `Main branch protection` | Descriptive name for this ruleset |
| **Include default branch** | ☑ Checked | Applies to your main branch (usually `main`) |
| **OR Bypass branch name** | Leave empty | Or enter specific branches like `main`, `dev`, `release/*` |

For separate rulesets:
- Create one ruleset with "Include default branch" for `main`
- Create another ruleset with branch name `dev` for your dev branch

### Step 3: Configure Rules

Rulesets use individual rule toggles. Enable these:

#### Rule: "Require pull request reviews before merging"
- **Status:** ☑ ENABLED
- **Required reviewers:** Set to 0 (for solo developers)
- **Explanation:** According to [GitHub Docs on Available Ruleset Rules](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets):

> "You can require a certain number of reviews from specific team members before a PR can be merged."

For solo developers, setting this to 0 still enforces the PR workflow without requiring approval.

#### Rule: "Require status checks to pass"
- **Status:** ☑ ENABLED
- **Type:** "Strict" (forces you to rebase with main)
- **Add status checks:** Configure checks from your CI/CD pipeline

#### Rule: "Require conversation resolution before merging"
- **Status:** ☑ ENABLED (optional)
- **Purpose:** Requires that all comments/suggestions are resolved before merge
- **Benefit:** Ensures you address all code review comments

#### Rule: "Dismiss stale pull request approvals when new commits are pushed"
- **Status:** ☑ ENABLED (if you use approvals)
- **Purpose:** Same as in classic rules - re-validates approvals

#### Rule: "Require signed commits"
- **Status:** ☐ UNCHECKED (optional for solo developers)
- **Purpose:** Requires GPG-signed commits (adds security layer)
- **Solo Developer:** Optional; useful if you want to verify commit authenticity

### Step 4: Advanced Options

#### Bypass Options (Optional)

Leave unchecked for maximum protection. If you want an escape hatch:
- **Allow specified actors to bypass** - Leave empty (prevents even you from bypassing)
- **Allows admin to bypass** - Unchecked (prevents admin override)

For solo developers, stricter is better (prevents "just this once" exceptions).

### Step 5: Enable and Save

- Confirm all settings
- Click **Create ruleset** to enable immediately
- Ruleset appears in your ruleset list with a green indicator

### Step 6: Test Your Ruleset

Test that protection works:
```bash
# Try to push directly to main (should fail)
git checkout main
echo "test" > test.txt
git add test.txt
git commit -m "test"
git push origin main

# Expected: Remote rejected with message about branch protection rules
```

---

## Part 5: Understanding All Branch Protection Settings

This section explains every possible checkbox and setting.

### Core Protection Settings

#### "Require a pull request before merging"
- **Type:** Checkbox
- **Default:** Unchecked
- **Enables:** Sub-options below
- **Purpose:** Prevents `git push` to the branch; requires PR workflow
- **Solo Dev:** ✅ ALWAYS ENABLE

#### "Require approvals"
- **Type:** Checkbox with dropdown (1-6)
- **Default:** Unchecked
- **Purpose:** Requires N other users to approve the PR before merge
- **Solo Dev:** ❌ UNCHECK for solo work
- **Why:** Cannot approve own PRs; self-approval is blocked by GitHub
- **Workaround:** Set to 0 (if available) OR use auto-approval GitHub Action

#### "Require review from Code Owners"
- **Type:** Checkbox
- **Default:** Unchecked
- **Purpose:** Requires approval from users/teams listed in `.github/CODEOWNERS`
- **Solo Dev:** ❌ UNCHECK
- **Use Case:** Teams with designated code owners for specific files

#### "Require approval of the most recent reviewable push"
- **Type:** Checkbox (appears if approvals enabled)
- **Default:** Unchecked
- **Purpose:** Most recent commit must be approved by someone other than the person who pushed it
- **Solo Dev:** ❌ SKIP (only matters if approvals enabled)
- **Explanation:** Prevents you from pushing a commit then immediately approving it as reviewer

#### "Dismiss stale pull request approvals when new commits are pushed"
- **Type:** Checkbox (sub-option under "Require approvals")
- **Default:** Unchecked
- **Purpose:** When new commits are pushed to PR, existing approvals are marked stale
- **Solo Dev:** ✅ ENABLE (maintains approval currency)
- **Explanation:** Per [GitHub Docs](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule):

> "GitHub records the state of the diff when a pull request is approved. If the diff changes (for example, because a contributor pushes new changes), the approving review is dismissed as stale, and the pull request cannot be merged until someone approves the work again."

---

### Status Check Settings

#### "Require status checks to pass before merging"
- **Type:** Checkbox
- **Default:** Unchecked
- **Purpose:** Requires configured CI/CD checks to pass before merge
- **Solo Dev:** ✅ HIGHLY RECOMMENDED
- **Benefit:** Automated validation (tests, linting, builds) without human approval

#### "Require branches to be up to date before merging"
- **Type:** Checkbox (sub-option under status checks)
- **Default:** Unchecked
- **Purpose:** PR branch must be rebased with main before merge
- **Solo Dev:** ✅ ENABLE
- **Reason:** Ensures code is tested against latest main branch code
- **Workflow Impact:** Means you must resolve conflicts before merging

#### "Select status checks that must pass"
- **Type:** Multi-select (appears after enabling status checks)
- **Options:** Auto-populated from recent workflow runs
- **Examples:**
  - `build` - Custom build script
  - `continuous-integration/github-actions/pr` - GitHub Actions default
  - `test` - Test suite
  - `lint` - Linter checks
- **Solo Dev:** Add all relevant checks from your CI/CD pipeline

---

### Advanced Protection Settings

#### "Restrict who can push to matching branches"
- **Type:** Team/User search
- **Default:** Empty
- **Purpose:** Whitelist specific teams/users who can push to branch
- **Solo Dev:** Leave empty (you have permission as owner)
- **Use Case:** For teams, restrict to specific developer groups

#### "Require signed commits"
- **Type:** Checkbox
- **Default:** Unchecked
- **Purpose:** All commits must be cryptographically signed with GPG key
- **Solo Dev:** ☐ OPTIONAL
- **Benefit:** Proves commit author identity
- **Setup:** Requires GPG key configuration (out of scope for this guide)

#### "Require up-to-date branches"
- **Type:** Checkbox
- **Same as:** "Require branches to be up to date before merging" (older naming)

#### "Require conversation resolution before merging"
- **Type:** Checkbox
- **Default:** Unchecked
- **Purpose:** All GitHub comments/suggestions must be marked resolved before merge
- **Solo Dev:** ☑ ENABLE (good practice)
- **Benefit:** Ensures you address all feedback/notes

#### "Lock branch"
- **Type:** Checkbox
- **Default:** Unchecked
- **Purpose:** Makes branch read-only; no one can push or merge
- **Solo Dev:** ❌ NEVER ENABLE
- **Use Case:** Temporarily freeze branch during release

#### "Do not allow bypassing the above settings"
- **Type:** Checkbox
- **Default:** Unchecked
- **Purpose:** Enforces ALL rules even for admins
- **Solo Dev:** ✅ ENABLE
- **Explanation:** According to [GitHub Docs](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule):

> "When enabled, this option applies all of your branch protection rules universally—including to administrators."

- **Why Enable:** Prevents "just this once" admin exceptions
- **Common Mistake:** Leaving unchecked defeats the protection (admins can still push directly)

---

## Part 6: Recommended Configurations

### Configuration A: Minimal Protection (Solo Developer)

**Goal:** Prevent accidental direct pushes; allow quick solo merges

**Settings:**
```
☑ Require a pull request before merging
  ☐ Require approvals (UNCHECKED)
  ☐ Dismiss stale approvals
  ☐ Require review from Code Owners

☐ Require status checks before merging
  (GitHub Actions not set up yet)

☑ Do not allow bypassing the above settings

✓ Apply to: main, dev
```

**Workflow:**
1. Create feature branch
2. Make commits
3. Push to GitHub, create PR
4. Merge immediately (no approval needed)
5. Delete feature branch

**Pros:**
- Simple, minimal setup
- No approval bottleneck
- Still creates PR audit trail
- Prevents accidental direct pushes

**Cons:**
- No automated validation
- If you have GitHub Actions, not enforcing them

---

### Configuration B: Balanced Protection (Recommended for Solo Developers)

**Goal:** Prevent accidental pushes AND ensure code quality through CI/CD

**Settings:**
```
☑ Require a pull request before merging
  ☐ Require approvals (UNCHECKED)
  ☐ Dismiss stale approvals
  ☐ Require review from Code Owners

☑ Require status checks before merging
  ☑ Require branches to be up to date
  ✓ Select checks: (all CI/CD checks)
    - Tests
    - Linting
    - Build validation

☑ Require conversation resolution before merging

☑ Do not allow bypassing the above settings

✓ Apply to: main, dev
```

**Prerequisites:**
- GitHub Actions workflow set up
- Workflow files in `.github/workflows/`

**Workflow:**
1. Create feature branch
2. Make commits and push
3. PR automatically runs CI/CD
4. Fix any failing tests/linting
5. Once all checks pass, merge immediately
6. Delete feature branch

**Pros:**
- Automated validation catches bugs
- Still no approval bottleneck
- Professional-grade protection
- Scales as you add features

**Cons:**
- Requires GitHub Actions setup
- Fixes failing checks add time to workflow
- Need to maintain CI/CD configuration

---

### Configuration C: Enterprise-Grade (For Team Transition)

**Goal:** Professional-grade protection; suitable for growing teams

**Settings:**
```
☑ Require a pull request before merging
  ☑ Require approvals: 1
  ☑ Dismiss stale approvals
  ☑ Require approval of most recent push
  ☐ Require review from Code Owners (optional)

☑ Require status checks before merging
  ☑ Require branches to be up to date
  ✓ Select checks: (all CI/CD checks)

☑ Require conversation resolution before merging

☑ Require signed commits

☑ Do not allow bypassing the above settings

Bypass Options:
  ✓ Allow specified actors: (leave empty)
  ☑ Allow admin bypasses: (unchecked)

✓ Apply to: main, dev, release/*
```

**When to Use:**
- Preparing for team collaboration
- High-security requirements
- Open source projects accepting contributions

**Solo Developer Note:** If you're solo, don't use this. The approval requirement will block your PRs. Use Configuration B instead.

---

## Part 7: Common Issues and Troubleshooting

### Issue 1: "Require approvals" Dropdown Shows 1-6, No 0 Option

**Problem:** The dropdown only shows 1-6 approvals, no option for 0.

**Root Cause:** GitHub is designed for team workflows. For solo developers, the checkbox itself becomes the issue.

**Solution:**
- **Option A (Recommended):** Leave the "Require approvals" checkbox **UNCHECKED**
  - This allows you to merge your own PRs
  - PR workflow is still enforced by "Require a pull request before merging"

- **Option B:** Enable it and set to 1, then use auto-approval GitHub Action
  - More complex but maintains approval workflow structure

- **Option C:** If you have collaborators, ask one to approve your PRs
  - Simple but requires coordination

**Recommended:** Go with Option A for solo work.

---

### Issue 2: "Cannot Merge Pull Request - Approval Required" but You're the Only Developer

**Problem:** You created and tried to merge your own PR, but GitHub says approval is required.

**Root Cause:** "Require approvals" checkbox is enabled, and you cannot approve your own PRs.

**Solution:**
1. Uncheck "Require approvals" checkbox
2. OR Set up auto-approval action (more advanced)
3. Re-test: You should now be able to merge

**To Fix:**
1. Go to **Settings > Branches**
2. Click the rule name (e.g., "main")
3. Uncheck "Require approvals"
4. Click **Update**
5. Retry merging PR (may need to refresh browser)

---

### Issue 3: "Branch Protection Doesn't Prevent Direct Pushes"

**Problem:** You or someone can still `git push` directly to main/dev.

**Root Cause:** "Require a pull request before merging" checkbox is not enabled.

**Solution:**
1. Go to **Settings > Branches**
2. Check "Require a pull request before merging" checkbox
3. Also enable "Do not allow bypassing the above settings"
4. Click **Update**
5. Re-test: `git push` should now be rejected

**Test Command:**
```bash
git push origin main
# Should fail with: "remote: error: pushing to protected branch"
```

---

### Issue 4: Branch Protection Rules Not Appearing in Settings

**Problem:** No branch protection rules show up under Settings > Branches.

**Root Cause:** You may not have admin permissions, or branch doesn't exist yet.

**Solution:**
1. Verify you have **admin** permissions (not just write access)
2. Verify the branch exists (push to it first if new)
3. If using Rulesets instead of classic rules, check **Settings > Rules > Rulesets**
4. Contact repo owner if you lack admin access

---

### Issue 5: "Required Status Checks" Doesn't Show Any Checks

**Problem:** The "Select status checks that must pass" dropdown is empty.

**Root Cause:** GitHub hasn't recorded any status checks yet (no recent CI/CD runs).

**Solution:**
1. Make sure your GitHub Actions workflows are configured (`.github/workflows/*.yml`)
2. Create a PR or commit to trigger a workflow run
3. Wait for workflow to complete (successful or failed)
4. Go back to branch protection settings
5. Refresh the page
6. Status checks should now appear in the dropdown

**Timeline:** First status check usually appears within 1-5 minutes of workflow completion.

---

### Issue 6: Cannot Choose Between Classic Rules vs Rulesets

**Problem:** You have both classic branch protection rules and rulesets, unsure which one is actually protecting the branch.

**Root Cause:** GitHub allows both to coexist. They apply simultaneously.

**Solution:**
- **For new projects:** Use only Rulesets (modern approach)
- **For existing projects:** Keep using classic rules (stable, proven)
- **If migrating:** Rulesets and classic rules can run together during transition
- **Recommendation:** Don't use both simultaneously to avoid confusion

**To Check Current Configuration:**
1. **Settings > Branches:** See classic branch protection rules here
2. **Settings > Rules > Rulesets:** See rulesets here
3. If both have rules for `main`, both apply simultaneously

---

### Issue 7: Admin Pushed Directly to Protected Branch

**Problem:** An admin bypassed branch protection and pushed directly to main.

**Root Cause:** "Do not allow bypassing the above settings" was **UNCHECKED**.

**Solution:**
1. Go to **Settings > Branches**
2. Edit the protection rule
3. CHECK "Do not allow bypassing the above settings"
4. Click **Update**
5. Ensure rule has green checkmark indicating it's enforced

**Prevention:** Always enable this for critical branches.

---

## Part 8: Migration Guide - From No Protection to Protected

### Step 1: Evaluate Current State

```bash
# Check if your main branch has any protection
git ls-remote --heads origin main

# If protected, you should get an error when trying to push directly
git push origin main
```

### Step 2: Create Backup Branch (Safety)

Before making changes, create a backup:
```bash
git checkout main
git pull origin main
git checkout -b backup/main-$(date +%Y%m%d)
git push origin backup/main-$(date +%Y%m%d)
```

### Step 3: Set Up CI/CD (If Using Status Checks)

Before enabling status checks, ensure you have:
- `.github/workflows/*.yml` files set up
- At least one successful workflow run
- Workflow should run on `pull_request` event

### Step 4: Enable Basic Branch Protection

1. Go to **Settings > Branches**
2. Click **Add rule**
3. Branch name pattern: `main`
4. Check: "Require a pull request before merging"
5. Check: "Do not allow bypassing the above settings"
6. Click **Create**

### Step 5: Test Protection

```bash
# Create test branch
git checkout -b test/protection-check
echo "test" > test.txt
git add test.txt
git commit -m "test"
git push origin test/protection-check

# Try to push directly to main (should fail)
git push origin test/protection-check:main

# Expected error:
# remote: error: pushing to protected branch
# remote: You can create a pull request instead.
```

### Step 6: Verify PR Workflow Works

1. Go to GitHub
2. You should see a "Compare & pull request" button
3. Click to create PR
4. PR should allow you to merge
5. Click **Merge pull request**
6. Verify merge was successful

### Step 7: Enable Status Checks (If Using CI/CD)

After confirming PR workflow works:
1. Go to **Settings > Branches**
2. Edit the main rule
3. Check: "Require status checks to pass before merging"
4. Check: "Require branches to be up to date before merging"
5. Select your CI/CD checks from the list
6. Click **Update**

### Step 8: Test with Failing Checks

Create a PR that fails CI/CD:
1. Create new feature branch
2. Make a commit that will fail tests
3. Push and create PR
4. Observe: PR shows "required checks failed"
5. Observe: Merge button is disabled
6. Fix the issue, commit, and push
7. Observe: Checks pass, merge button enables

---

## Part 9: Best Practices for Solo Developers

### Best Practice 1: Never Disable Protection to "Get Around It"

**Anti-pattern:**
```
- Enable branch protection
- Hit blocker
- Disable protection
- Push directly
- Re-enable protection
```

**Why:** This defeats the entire purpose. If protection gets in your way, fix your workflow instead.

**Better approach:** Adjust settings to match your workflow (reduce approval requirements, use auto-approval).

---

### Best Practice 2: Use PR Description Template

Even solo, write good PR descriptions:
```markdown
## Description
What does this PR do?

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation

## Testing
How did you test this?

## Checklist
- [ ] Tests pass locally
- [ ] No new linting errors
- [ ] Documentation updated
```

**Benefit:** Forces you to think about changes; creates audit trail.

---

### Best Practice 3: Use Branch Naming Conventions

Make it obvious what each branch is for:
```
feature/user-authentication
bugfix/payment-processing-error
docs/api-documentation
refactor/database-schema
hotfix/critical-production-bug
```

**Benefit:** Easier to track changes; clearly shows PR purpose.

---

### Best Practice 4: Keep Commits Atomic

One logical change per commit:
```bash
# Good
git commit -m "refactor: extract validator function"
git commit -m "feat: add email validation"
git commit -m "docs: update validation readme"

# Bad
git commit -m "stuff and things"
```

**Benefit:** Clean history; easier to revert specific changes.

---

### Best Practice 5: Use Meaningful Commit Messages

Follow conventional commits:
```
feat: add user authentication
fix: resolve payment processing bug
docs: update API documentation
refactor: simplify database queries
test: add unit tests for validator
chore: update dependencies
```

**Benefit:** Automated changelog generation; clear commit history.

---

### Best Practice 6: Delete Merged Branches

After merging, clean up:
```bash
git push origin --delete feature/my-feature
```

**Benefit:** Keeps repo clean; reduces cognitive load.

---

### Best Practice 7: Require Status Checks for Quality Assurance

Don't skip CI/CD:
- **Always** enable status checks
- **Always** require branches to be up to date
- Fix failing checks before merging

**Benefit:** Catches bugs before they reach main; prevents accidental regressions.

---

### Best Practice 8: Review Your Own PRs

Spend 5 minutes reviewing before merge:
1. Click **Files changed** tab
2. Read through your own changes
3. Look for:
   - Accidental debug code
   - Typos
   - Logic errors
   - Inconsistent formatting
4. Then merge

**Benefit:** Fresh eyes catch mistakes; maintains code quality.

---

## Part 10: Reference - All Branch Protection Checkbox Meanings

| Checkbox | Solo Dev | Meaning |
|----------|----------|---------|
| **Require a pull request before merging** | ✅ YES | Prevents `git push` to branch; requires PR |
| **Require approvals** | ❌ NO | Requires N users to approve PR (blocks solo) |
| **Dismiss stale PR approvals when new commits pushed** | ✅ IF USING | Re-validates approvals after new commits |
| **Require review from Code Owners** | ❌ NO | Requires specific users to approve |
| **Require approval of most recent push** | ❌ NO | Pushed code can't be approved by pusher |
| **Require status checks to pass** | ✅ YES | CI/CD checks must pass |
| **Require branches to be up to date** | ✅ YES | PR branch must be rebased with main |
| **Lock branch** | ❌ NO | Makes branch read-only (rarely used) |
| **Require conversation resolution** | ✅ YES | Comments must be resolved before merge |
| **Require signed commits** | ⚠️ OPTIONAL | Commits must be GPG signed |
| **Restrict who can push** | ❌ NO | Whitelist specific users (you're owner) |
| **Do not allow bypassing** | ✅ YES | Admins can't override protection |

---

## Part 11: Related GitHub Features

### GitHub Code Owners

File: `.github/CODEOWNERS`

Automatically request reviews from specific users:
```
# Main code owner
* @username

# Specific files
src/auth/* @auth-maintainer
src/database/* @db-maintainer
docs/* @documentation-maintainer
```

**Solo Dev:** Not typically needed unless planning for team growth.

---

### GitHub Actions Status Checks

Status checks run automatically on PRs:
```yaml
# .github/workflows/tests.yml
name: Tests

on: [pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm install
      - run: npm test
      - run: npm run lint
```

**Solo Dev:** Essential for quality assurance.

---

### GitHub Insights

Monitor branch protection effectiveness:
- **Settings > Insights > Branch protection**
- See attempt to merge/push to protected branch
- Track protection violations over time

---

## Summary for Quick Reference

### TL;DR - Solo Developer Setup

**Step 1: Go to Settings > Branches > Add Rule**

```
Branch pattern: main
☑ Require a pull request before merging
☐ Require approvals (UNCHECKED)
☑ Require status checks to pass before merging
  ☑ Require branches to be up to date before merging
  ✓ Select: (your CI/CD checks)
☑ Do not allow bypassing the above settings
```

**Step 2: Repeat for `dev` branch**

**Step 3: Test PR workflow works**

**Step 4: Done! Your main/dev branches are now protected**

### Your Workflow After Setup

```
1. Create feature branch
   git checkout -b feature/my-feature

2. Make changes and commit
   git commit -m "feat: add new feature"

3. Push to GitHub
   git push origin feature/my-feature

4. Create pull request on GitHub UI
   (button appears automatically)

5. Review your own PR
   Click "Files changed" tab

6. Merge PR
   All checks pass → click "Merge pull request"

7. Delete feature branch
   git push origin --delete feature/my-feature
```

That's it! You've prevented accidental `git push` to main while keeping your solo workflow efficient.

---

## Sources and Official Documentation

- [GitHub Docs: About Protected Branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [GitHub Docs: Managing a Branch Protection Rule](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule)
- [GitHub Docs: About Rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets)
- [GitHub Docs: Available Rules for Rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)
- [GitHub Blog: Required Reviewer Rule Generally Available (February 2026)](https://github.blog/changelog/2026-02-17-required-reviewer-rule-is-now-generally-available/)
- [GitHub Blog: Bypass Branch Protections with New Permission (2022)](https://github.blog/changelog/2022-08-18-bypass-branch-protections-with-a-new-permission/)
- [DEV Community: Branch Protection Rules vs Rulesets](https://dev.to/piyushgaikwaad/branch-protection-rules-vs-rulesets-the-right-way-to-protect-your-git-repos-305m)
- [GitHub Community Discussion: Require Approvals for Solo Developers](https://github.com/orgs/community/discussions/49633)
- [Blog Post: GitHub Branch Protection Deep Dive (March 2026)](https://mcginniscommawill.com/posts/2026-03-24-github-branch-protection-deep-dive/)

---

**Document Version:** 1.0
**Last Updated:** May 31, 2026
**Author:** Research Documentation
**Status:** Complete and Ready for Use