# Pre-Execution Checklist

**Trigger:** Before making ANY code changes
**Purpose:** Prevent Phase 2-style mistakes by validating prerequisites

---

## ✅ Checklist (All Must Be Complete)

### 1. Task List Verification
- [ ] Task list exists (in .md file or documented in conversation)
- [ ] Task list has been reviewed and understood completely
- [ ] All tasks are numbered and specific (e.g., "Task 2.1: Remove animation from desktop victory button")
- [ ] Dependencies between tasks are identified (e.g., "Phase 2 depends on Phase 1")
- [ ] Total task count is known (e.g., "21 tasks across 5 phases")

**If task list not found:** Use multi-agent coordination to search docs/design/, docs/memory/, and conversation transcripts

### 2. Documentation Review
- [ ] MEMORY.md handoff summary has been read
- [ ] Relevant design docs have been reviewed (e.g., SUPPORT_DEV_BUTTON_LOCATIONS.md)
- [ ] Previous session issues are understood
- [ ] NO ASSUMPTIONS are being made about requirements

**User requirement:** "No assumptions allowed ever for this user"

### 3. Testing Plan
- [ ] Testing approach is documented
- [ ] QA checklist has been created
- [ ] Rollback plan is ready (if things go wrong)
- [ ] Success criteria are defined

**Example:** "Testing required: Desktop victory (static button), Mobile victory (static button), Animation quality (4 flickers, not gimmicky)"

### 4. Multi-Agent Coordination (If Needed)
- [ ] Agents have clear, specific objectives
- [ ] Agent findings will be cross-referenced with documentation
- [ ] Verification plan is documented
- [ ] If counts don't match previous audits, investigation is required

---

## 🚫 Stop Conditions

**If ANY checkbox is unchecked, STOP and address it before proceeding.**

### Common Violations to Avoid:
❌ "I'll just start coding and figure it out" → Find task list first
❌ "The task list is probably similar to last time" → NO ASSUMPTIONS
❌ "I'll skip Phase 2, it's probably not important" → Follow ALL phases
❌ "Testing can happen later" → Define testing plan NOW

---

## ⏱️ Time Investment

**Time to complete checklist:** 5-10 minutes
**Time saved by preventing mistakes:** 2+ hours (based on last session)

**ROI:** 12x-24x return on time invested

---

## 📚 Related Documentation

- **Handoff Protocol Skill:** Session start/end procedures
- **Multi-Agent Verification Rules:** When/how to use agents
- **MEMORY.md:** Project history and handoff summaries

---

## Example Usage

**Scenario:** User requests "Implement music selector feature"

**Checklist Execution:**
1. ✅ Task list found in MUSIC_SELECTOR_PLAN.md (5 phases, 2.5 hours)
2. ✅ Documentation reviewed: Plan includes accordion UI, preview system, game integration
3. ✅ Testing plan exists: 30+ item checklist in plan
4. ⏸️ Multi-agent not needed for this task
5. ✅ **Proceed with implementation**

**Scenario:** User requests "Fix the buttons"

**Checklist Execution:**
1. ❌ Task list NOT found - which buttons? what's wrong?
2. 🔍 Launch multi-agent search for task list
3. ✅ Found 21-task checklist in conversation transcript
4. ✅ Documentation reviewed: Phase 2 was skipped last time
5. ✅ **Now proceed with all phases**

---

## 🔄 Git Commit Operations Checklist

**Trigger:** When message contains: "commit", "push", "merge", "PR", "pull request", "git"

**MANDATORY: Read docs/GIT_COMMIT_WORKFLOW.md IMMEDIATELY before any git operation**

### Git Operations Checklist
- [ ] Read docs/GIT_COMMIT_WORKFLOW.md (REQUIRED)
- [ ] Verify Rule #1: NO co-author lines in commit message
- [ ] Verify Rule #2: Base branch is correct (dev, not main)
- [ ] Confirm using feature branch workflow (not pushing directly to dev/main)
- [ ] Branch protection requires PRs for dev and main
- [ ] Commit message follows format: `<type>: <description>` (no co-author)

### Feature Branch Workflow (REQUIRED)
```bash
# 1. Create feature branch from dev
git checkout -b feature/description

# 2. Commit changes (NO co-author line)
git commit -m "type: description"

# 3. Push feature branch
git push -u origin feature/description

# 4. Create PR to dev (NOT main)
gh pr create --base dev --title "title" --body "description"

# 5. Merge PR
gh pr merge --squash --delete-branch

# 6. Pull updated dev
git checkout dev && git pull origin dev
```

### 🚨 Critical Rules (NEVER VIOLATE)
1. **NO co-author lines** - Never add "Co-Authored-By:" to commits
2. **Always use feature branches** - Never push directly to dev or main
3. **Base branch = dev** - PRs go to dev first, not main
4. **Read workflow first** - Check GIT_COMMIT_WORKFLOW.md before ANY git operation

### Stop Conditions
**If ANY of these are true, STOP immediately:**
- ❌ About to add co-author line to commit
- ❌ About to push directly to dev or main
- ❌ About to create PR with base branch = main (should be dev)
- ❌ Haven't read GIT_COMMIT_WORKFLOW.md yet

---

**Last Updated:** June 3, 2026
**Reason Created:** Prevent 2-hour mistake from Phase 2 skip (April 13, 2026 session)
**Updated:** Added Git Commit Operations checklist (June 3, 2026) - Prevent co-author violations and workflow mistakes
