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

**Last Updated:** April 13, 2026
**Reason Created:** Prevent 2-hour mistake from Phase 2 skip (April 13, 2026 session)
