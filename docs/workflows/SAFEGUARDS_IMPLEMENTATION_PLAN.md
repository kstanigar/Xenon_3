# Safeguards Implementation Plan - Option A

**Status:** ✅ Phase 1 Complete - Files Created (Tasks #33-35, #37)
**Priority:** CRITICAL - Must complete before AWS migration
**Estimated Total Time:** 2 hours 35 minutes (155 minutes)
**Created:** April 13, 2026
**Updated:** April 13, 2026 (Added token efficiency / model selection recommendation)
**Phase 1 Completed:** April 13, 2026 - All 4 safeguard files created in parallel

---

## Purpose

Implement process safeguards to prevent costly mistakes during AWS migration and future development. Last session lost ~2 hours due to skipped Phase 2 (no task list verification). This plan ensures all future implementations follow documented processes without errors.

---

## Task List Overview

**Total Tasks:** 8
**Task IDs:** #33-#40
**Phases:** 3 (Create Safeguards → Implement Infrastructure → Test & Document)

---

## Phase 1: Create Safeguard Files (80 minutes)

### Task #33: Create Pre-Execution Checklist Hook
**Time:** 30 minutes
**File:** `.claude/hooks/pre-execution-checklist.md`
**Purpose:** Triggered before ANY code changes to validate prerequisites

**Checklist Contents:**
```markdown
# Pre-Execution Checklist

Before making ANY code changes, verify:

## 1. Task List Verification
- [ ] Task list exists (in .md file or documented in conversation)
- [ ] Task list has been reviewed and understood
- [ ] All tasks are numbered and specific
- [ ] Dependencies between tasks are identified

## 2. Documentation Review
- [ ] MEMORY.md handoff summary read
- [ ] Relevant design docs reviewed
- [ ] Previous session issues understood
- [ ] No assumptions being made

## 3. Testing Plan
- [ ] Testing approach documented
- [ ] QA checklist created
- [ ] Rollback plan ready
- [ ] Success criteria defined

## 4. Multi-Agent Coordination
- [ ] If needed, agents have clear objectives
- [ ] Agent findings will be verified
- [ ] Cross-reference plan documented

**If ANY checkbox is unchecked, STOP and address it before proceeding.**
```

---

### Task #34: Create Handoff Protocol Skill (UPDATED)
**Time:** 35 minutes (updated from 30 min)
**File:** `.claude/skills/handoff-protocol.md`
**Purpose:** Standardize session start/end procedures + optimize token costs with model recommendations

**Skill Contents:**
```markdown
# Handoff Protocol Skill

## Session Start Procedure

1. **Read Last Handoff (5 min)**
   - Open MEMORY.md
   - Read latest handoff summary
   - Note: Last implementation, issues encountered, next priority

2. **Review Project State (5 min)**
   - Check git status
   - Review uncommitted changes
   - Verify branch is up to date

3. **Confirm Next Priority (2 min)**
   - Ask user: "I see Priority #X is next. Proceed with this?"
   - Get explicit approval before starting

4. **Find Task List (10 min)**
   - Search for documented task list
   - If not found, use multi-agent coordination
   - NEVER proceed without task list

## Session End Procedure

1. **Document Implementation (10 min)**
   - Update MEMORY.md with what was accomplished
   - Note any issues encountered
   - Document files modified

2. **Create Handoff Summary (10 min)**
   - What was done
   - What worked well
   - What needs improvement
   - Next session priority

3. **Commit Changes (5 min)**
   - Create feature branch
   - Commit with detailed message
   - Push to remote

4. **Update Task List (5 min)**
   - Mark completed tasks
   - Document any new tasks discovered
   - Update priorities if needed

5. **Recommend Next Model (5 min)**
   - Analyze next session priority
   - Recommend Haiku, Sonnet, or Opus
   - Document recommendation in handoff summary
   - Consider: complexity, risk, multi-agent needs, token efficiency

**Total Session Overhead: ~55 minutes (worth it to prevent 2+ hour mistakes + optimize costs)**

## Model Selection Decision Matrix

After creating handoff summary, analyze next session priority and recommend model:

### Use **Haiku** (Fastest, Most Efficient) when:
- ✅ Simple bug fixes (typos, single-line edits)
- ✅ Documentation updates only
- ✅ Reading/researching code (no changes)
- ✅ Answering questions about codebase
- ✅ Low-risk changes to non-critical files
- ✅ Updating .md files only
- ❌ No multi-agent coordination needed

**Token Cost:** Lowest (~$0.25 per million input tokens)
**Use Case:** "Update README with new feature documentation"

### Use **Sonnet** (Balanced, Default) when:
- ✅ Standard feature implementation
- ✅ Multi-file changes (2-5 files)
- ✅ Moderate complexity (following existing patterns)
- ✅ Multi-agent coordination needed
- ✅ Code reviews and audits
- ✅ Testing and QA guidance
- ✅ Most day-to-day development tasks

**Token Cost:** Medium (~$3 per million input tokens)
**Use Case:** "Implement music selector feature (5 phases, 2.5 hours)"

### Use **Opus** (Most Capable, Most Expensive) when:
- ✅ Critical infrastructure changes (AWS migration, CI/CD)
- ✅ High-risk production deployments
- ✅ Complex architectural decisions
- ✅ Large-scale refactoring (10+ files)
- ✅ Debugging critical production issues
- ✅ Security-sensitive changes
- ✅ When mistakes could break production

**Token Cost:** Highest (~$15 per million input tokens)
**Use Case:** "Migrate entire application to AWS infrastructure"

## Recommendation Format

Add to handoff summary:
```markdown
**Recommended Model for Next Session:** [Haiku/Sonnet/Opus]

**Reasoning:**
- Task: [Brief description of next priority]
- Complexity: [Low/Medium/High]
- Risk: [Low/Medium/High]
- Multi-agent needed: [Yes/No]
- Estimated token usage: [Low/Medium/High]

**Recommendation:** Use [Model] because [specific reason based on criteria above]
```

## Example Recommendations

**Example 1 - Haiku:**
```
Recommended Model: Haiku
Reasoning: Next priority is updating MEMORY.md documentation (low complexity, no code changes, low risk)
```

**Example 2 - Sonnet:**
```
Recommended Model: Sonnet
Reasoning: Implement music selector feature (moderate complexity, 5 phases, multi-agent for testing, medium risk)
```

**Example 3 - Opus:**
```
Recommended Model: Opus
Reasoning: AWS migration (high complexity, critical infrastructure, production deployment, high risk, ~6 hours work)
```
```

---

### Task #35: Create Multi-Agent Verification Rules
**Time:** 20 minutes
**File:** `.claude/rules/multi-agent-verification.md`
**Purpose:** Rules for when and how to use multi-agent coordination

**Rules Contents:**
```markdown
# Multi-Agent Verification Rules

## When to Use Multi-Agent Coordination

**Use multi-agent when:**
- Searching for task lists across multiple .md files
- Verifying desktop/mobile code parity (2 agents, 1 per file)
- Auditing large sections of code for consistency
- Finding all instances of a function/pattern
- Researching complex questions requiring multiple sources

**Do NOT use multi-agent when:**
- Reading a single specific file (use Read tool)
- Searching within 1-2 known files (use Grep tool)
- Making simple edits (use Edit tool directly)

## Verification Protocol

**Before executing findings:**
1. Review all agent outputs
2. Cross-reference findings with documentation
3. Verify counts match (e.g., "8 buttons found" should match task list)
4. Document verification in .md file
5. Get user approval if findings contradict expectations

## Task List Discovery Process

**If task list not immediately visible:**
1. Launch 3 parallel Explore agents:
   - Agent 1: Search design docs (docs/design/*.md)
   - Agent 2: Search memory docs (docs/memory/*.md, MEMORY.md)
   - Agent 3: Search conversation transcript (.jsonl)
2. Report findings to user
3. If still not found, ASK user (do not assume)

## Cross-Reference Requirement

**Large codebase rule:**
- Always cross-reference current findings with previous audits
- Document verification approach in appropriate .md file
- If counts don't match, investigate before proceeding
- Example: "Earlier audit: 8 buttons. Current: 10 buttons. ⚠️ STOP and investigate."
```

---

## Phase 2: Implement Infrastructure (70 minutes)

### Task #36: Update CI/CD Integrity Checks
**Time:** 45 minutes
**File:** `.github/workflows/integrity-check.yml`
**Purpose:** Add automated validation to prevent production issues

**Changes to Add:**

```yaml
# Add after existing function checks

    # Check for debug code in production
    - name: Check for console.log statements
      run: |
        if grep -r "console\.log" game.html game_mobile.html index.html; then
          echo "❌ ERROR: console.log found in production code"
          exit 1
        fi
        echo "✅ No console.log statements found"

    # Check for debugger statements
    - name: Check for debugger statements
      run: |
        if grep -r "debugger" game.html game_mobile.html index.html; then
          echo "❌ ERROR: debugger statement found in production code"
          exit 1
        fi
        echo "✅ No debugger statements found"

    # Check for TODO/FIXME comments
    - name: Check for unresolved TODO/FIXME
      run: |
        TODO_COUNT=$(grep -r "TODO\|FIXME" game.html game_mobile.html index.html | wc -l)
        if [ $TODO_COUNT -gt 0 ]; then
          echo "⚠️ WARNING: $TODO_COUNT TODO/FIXME comments found"
          grep -r "TODO\|FIXME" game.html game_mobile.html index.html
        fi
        echo "ℹ️ TODO/FIXME check complete"

    # Check file sizes
    - name: Check large asset files
      run: |
        find assets/ -type f -size +5M -exec ls -lh {} \; | while read line; do
          echo "⚠️ WARNING: Large file detected: $line"
        done
        echo "✅ File size check complete"

    # Verify desktop/mobile parity for critical functions
    - name: Verify desktop/mobile function parity
      run: |
        DESKTOP_FUNCTIONS=$(grep -o "function [a-zA-Z_][a-zA-Z0-9_]*" game.html | sort | uniq | wc -l)
        MOBILE_FUNCTIONS=$(grep -o "function [a-zA-Z_][a-zA-Z0-9_]*" game_mobile.html | sort | uniq | wc -l)
        echo "Desktop functions: $DESKTOP_FUNCTIONS"
        echo "Mobile functions: $MOBILE_FUNCTIONS"
        DIFF=$((DESKTOP_FUNCTIONS - MOBILE_FUNCTIONS))
        DIFF=${DIFF#-}  # absolute value
        if [ $DIFF -gt 5 ]; then
          echo "⚠️ WARNING: Desktop and mobile function counts differ by $DIFF"
        fi
        echo "✅ Desktop/mobile parity check complete"
```

---

### Task #37: Create Dev Branch Strategy Document
**Time:** 15 minutes
**File:** `docs/workflows/DEV_BRANCH_STRATEGY.md`
**Purpose:** Document staging workflow

**Document Contents:**
```markdown
# Dev Branch Strategy

## Overview

The `dev` branch serves as a staging environment for all changes before they reach production (`main`).

## Workflow

### Feature Development
1. Create feature branch from `dev`: `git checkout -b feature/name`
2. Implement feature
3. Create PR to merge into `dev` (NOT main)
4. After PR approval, merge to `dev`

### QA Testing
1. Deploy `dev` branch to staging environment
2. Run full QA checklist
3. Fix any issues found (create new feature branches from `dev`)
4. Repeat until QA passes

### Production Promotion
1. Create PR from `dev` to `main`
2. Require additional review for main promotion
3. After approval, merge to `main`
4. Deploy `main` to production

## Branch Protection Rules

### `main` branch
- ✅ Require pull request reviews (1 reviewer)
- ✅ Require status checks to pass
- ✅ Require conversation resolution
- ✅ No force push
- ✅ No deletions

### `dev` branch
- ✅ Require pull request reviews (1 reviewer)
- ✅ Require status checks to pass
- ⚠️ Allow force push (for rebasing only)
- ✅ No deletions

## AWS Deployment

### Staging (dev branch)
- URL: TBD (AWS staging environment)
- Deploy trigger: Push to `dev`
- Purpose: QA testing before production

### Production (main branch)
- URL: TBD (AWS production environment)
- Deploy trigger: Push to `main`
- Purpose: Live player-facing deployment

## Rollback Procedures

### If dev deployment fails:
1. Revert problematic PR in `dev`
2. Redeploy `dev`
3. Fix in new feature branch

### If main deployment fails:
1. Emergency: Revert merge commit in `main`
2. Redeploy `main` (returns to last working state)
3. Fix issue in `dev`, re-test, then re-promote

## Benefits

- ✅ Catch issues in staging before production
- ✅ Safer AWS migration (test on dev first)
- ✅ Faster rollbacks (dev can be reset easily)
- ✅ Clear promotion path (dev → main)
```

---

### Task #38: Create Dev Branch from Main
**Time:** 10 minutes
**Action:** Create and configure `dev` branch

**Commands:**
```bash
# Create dev branch
git checkout main
git pull origin main
git checkout -b dev
git push -u origin dev
```

**GitHub Configuration:**
1. Go to Settings → Branches
2. Add branch protection rule for `dev`
3. Enable: Require pull request reviews
4. Enable: Require status checks to pass
5. Save changes

---

## Phase 3: Test & Document (30 minutes)

### Task #39: Test Safeguards Implementation
**Time:** 20 minutes
**Purpose:** Verify all safeguards are working

**Test Checklist:**
- [ ] `.claude/hooks/pre-execution-checklist.md` exists and is readable
- [ ] `.claude/skills/handoff-protocol.md` exists and is readable
- [ ] `.claude/rules/multi-agent-verification.md` exists and is readable
- [ ] `.github/workflows/integrity-check.yml` updated with new checks
- [ ] `docs/workflows/DEV_BRANCH_STRATEGY.md` created
- [ ] `dev` branch created and pushed
- [ ] GitHub branch protection configured
- [ ] Run `git status` - should show main branch, clean
- [ ] Run CI checks locally (if possible)

**Verification Commands:**
```bash
# Verify files exist
ls -la .claude/hooks/pre-execution-checklist.md
ls -la .claude/skills/handoff-protocol.md
ls -la .claude/rules/multi-agent-verification.md
ls -la docs/workflows/DEV_BRANCH_STRATEGY.md

# Verify dev branch
git branch -a | grep dev

# Verify CI file updated
git diff main -- .github/workflows/integrity-check.yml
```

---

### Task #40: Document Safeguards in MEMORY.md
**Time:** 10 minutes
**Purpose:** Record safeguards implementation for future sessions

**Add to MEMORY.md:**
```markdown
## ✅ COMPLETE - Safeguards Implementation (April 13, 2026)

**STATUS:** ✅ Complete - Process safeguards in place before AWS migration

**PURPOSE:**
Prevent costly mistakes during AWS migration and future development. Last session lost ~2 hours due to skipped Phase 2. These safeguards ensure documented processes are followed.

**IMPLEMENTED:**

**Hooks:**
- `.claude/hooks/pre-execution-checklist.md` - Validates prerequisites before code changes

**Skills:**
- `.claude/skills/handoff-protocol.md` - Standardizes session start/end procedures

**Rules:**
- `.claude/rules/multi-agent-verification.md` - Guidelines for multi-agent coordination

**CI/CD:**
- Updated `.github/workflows/integrity-check.yml`:
  - Check for console.log/debugger
  - Check for TODO/FIXME
  - File size validation
  - Desktop/mobile parity checks

**Infrastructure:**
- Created `dev` branch as staging environment
- Documented workflow in `docs/workflows/DEV_BRANCH_STRATEGY.md`
- Configured branch protection rules

**SUCCESS CRITERIA MET:**
- ✅ Pre-execution validation in place
- ✅ Handoff protocol documented
- ✅ Multi-agent rules defined
- ✅ CI/CD enhanced
- ✅ Dev branch workflow established

**NEXT STEP:** AWS migration (can proceed with confidence)

**TIME INVESTED:** 2.5 hours
**TIME SAVED:** Prevents 2+ hour mistakes in future sessions
**ROI:** Positive within first prevented mistake
```

---

## Success Criteria

**Before marking complete, verify:**
- [ ] All 8 tasks completed (#33-#40)
- [ ] All files created and committed
- [ ] Dev branch pushed and protected
- [ ] CI/CD checks passing
- [ ] Documentation updated
- [ ] User review and approval

---

## Next Step After Completion

**AWS Migration:**
- Proceed with confidence using safeguards
- Test on `dev` branch first
- Promote to `main` only after QA passes
- Reference: Follow AWS migration plan (TBD)

---

## Rollback Plan

If safeguards cause issues:
```bash
# Remove files
rm .claude/hooks/pre-execution-checklist.md
rm .claude/skills/handoff-protocol.md
rm .claude/rules/multi-agent-verification.md

# Revert CI changes
git checkout main -- .github/workflows/integrity-check.yml

# Delete dev branch
git branch -D dev
git push origin --delete dev
```

**Low risk** - These are documentation and process files, not code changes.

---

## Estimated Timeline

**Start:** Now
**Phase 1 (Create):** 85 minutes (updated: +5 min for model selection)
**Phase 2 (Implement):** 70 minutes
**Phase 3 (Test):** 30 minutes
**Total:** 2 hours 35 minutes (155 minutes)
**Completion:** ~2.5 hours from start

**Then:** AWS migration with safeguards in place

---

**Document Status:** Ready for review
**Awaiting:** User approval to proceed