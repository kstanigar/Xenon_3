# Handoff Protocol Skill

**Purpose:** Standardize session start/end procedures, prevent mistakes, optimize token costs
**Created:** April 13, 2026
**Last Updated:** April 13, 2026

---

## Session Start Procedure (22 minutes)

### 1. Read Last Handoff (5 min)
- Open `~/.claude/projects/.../memory/MEMORY.md`
- Read latest "SESSION HANDOFF SUMMARY"
- Note:
  - Last implementation (what was done)
  - Issues encountered (what went wrong)
  - Next priority (what to do)
  - Recommended model (Haiku/Sonnet/Opus)

**Example:**
```
Last Implementation: "Keep the Lights On" button redesign
Issues: Skipped Phase 2 (lost 2 hours)
Next Priority: Create hooks/skills/rules for better handoffs
Recommended Model: Sonnet (moderate complexity, multi-file creation)
```

### 2. Review Project State (5 min)
- Run `git status` - Check branch and uncommitted changes
- Run `git pull origin main` - Ensure up to date
- Review any uncommitted files
- Verify working directory is clean (or understand changes)

### 3. Confirm Next Priority (2 min)
- **NEVER assume** what to work on
- **ALWAYS ask:** "I see Priority #X is next: [description]. Proceed with this?"
- Get **explicit approval** before starting
- If user changes priority, update MEMORY.md

### 4. Find Task List (10 min)
- Search for documented task list in:
  - Design docs (`docs/design/*.md`)
  - Memory docs (`docs/memory/*.md`, `MEMORY.md`)
  - Conversation transcripts (`.jsonl` files)
- **If not found:** Use multi-agent coordination (3 parallel agents)
- **NEVER proceed without task list**

**User rule:** "No assumptions allowed ever for this user"

---

## Session End Procedure (33 minutes)

### 1. Document Implementation (10 min)
- Update MEMORY.md with new section
- Include:
  - What was accomplished
  - Issues encountered (if any)
  - Files modified
  - Testing status
  - Success criteria met

### 2. Create Handoff Summary (10 min)
- Add to top of MEMORY.md (after PAIM Onboarding Protocol)
- Include:
  - Session ID and date
  - What was done (bullet points)
  - Problems encountered
  - Fixes applied
  - Next session priority
  - Files modified
  - Git status

### 3. Recommend Next Model (5 min)
**NEW:** Analyze next session priority and recommend model

Use Model Selection Decision Matrix below ↓

### 4. Commit Changes (5 min)
- Create feature branch: `git checkout -b feature/descriptive-name`
- Stage files: `git add <files>`
- Commit with detailed message
- Push to remote: `git push -u origin feature/branch-name`

### 5. Update Task List (3 min)
- Mark completed tasks as done
- Document any new tasks discovered
- Update priorities if needed

**Total Session Overhead: ~55 minutes**
**Value:** Prevents 2+ hour mistakes, optimizes costs, ensures continuity

---

## Model Selection Decision Matrix

After creating handoff summary, analyze next session priority and recommend model:

### Use **Haiku** (Fastest, Most Efficient) when:

**Criteria:**
- ✅ Simple bug fixes (typos, single-line edits, obvious errors)
- ✅ Documentation updates only (.md files, no code)
- ✅ Reading/researching code (no changes)
- ✅ Answering questions about codebase
- ✅ Low-risk changes to non-critical files
- ✅ Updating .md files, comments only
- ❌ No multi-agent coordination needed

**Token Cost:** ~$0.25 per million input tokens (Lowest)
**Speed:** Fastest response times

**Example Use Cases:**
- "Update README with new feature documentation"
- "Fix typo in MEMORY.md"
- "Add comments to explain function behavior"
- "Answer: How does the scoring system work?"

**Recommendation Template:**
```
Recommended Model for Next Session: Haiku

Reasoning:
- Task: Update MUSIC_SELECTOR_PLAN.md with final implementation notes
- Complexity: Low (documentation only)
- Risk: Low (no code changes)
- Multi-agent needed: No
- Estimated token usage: Low (~50K tokens)

Use Haiku for maximum efficiency on this simple documentation task.
```

---

### Use **Sonnet** (Balanced, Default) when:

**Criteria:**
- ✅ Standard feature implementation (following existing patterns)
- ✅ Multi-file changes (2-5 files)
- ✅ Moderate complexity (not trivial, not critical)
- ✅ Multi-agent coordination needed
- ✅ Code reviews and audits
- ✅ Testing and QA guidance
- ✅ Most day-to-day development tasks
- ✅ Bug fixes requiring investigation

**Token Cost:** ~$3 per million input tokens (Medium)
**Speed:** Balanced

**Example Use Cases:**
- "Implement music selector feature (5 phases, 2.5 hours)"
- "Fix mobile button animation issue (requires multi-agent search)"
- "Add new analytics event tracking"
- "Refactor function to improve readability"

**Recommendation Template:**
```
Recommended Model for Next Session: Sonnet

Reasoning:
- Task: Implement music selector feature (MUSIC_SELECTOR_PLAN.md)
- Complexity: Medium (5 phases, accordion UI, preview system, game integration)
- Risk: Medium (affects gameplay UX)
- Multi-agent needed: Yes (desktop/mobile parity verification)
- Estimated token usage: Medium (~200K tokens)

Use Sonnet for balanced capability and cost on this standard feature implementation.
```

---

### Use **Opus** (Most Capable, Most Expensive) when:

**Criteria:**
- ✅ Critical infrastructure changes (AWS migration, database changes)
- ✅ High-risk production deployments
- ✅ Complex architectural decisions
- ✅ Large-scale refactoring (10+ files, complex dependencies)
- ✅ Debugging critical production issues (game broken, data loss)
- ✅ Security-sensitive changes (authentication, payment, PII)
- ✅ When mistakes could break production for real users

**Token Cost:** ~$15 per million input tokens (Highest)
**Speed:** Slower but most thorough

**Example Use Cases:**
- "Migrate entire application to AWS infrastructure"
- "Implement tier-based scoring system (prevents leaderboard exploits)"
- "Debug production issue: players losing save data"
- "Refactor entire game loop for performance (20+ files)"

**Recommendation Template:**
```
Recommended Model for Next Session: Opus

Reasoning:
- Task: AWS migration (deploy to S3, CloudFront, Route 53, Certificate Manager)
- Complexity: High (infrastructure, DNS, SSL, multiple AWS services)
- Risk: High (production deployment, could break live game)
- Multi-agent needed: Likely (verification, testing)
- Estimated token usage: High (~500K tokens, 4-6 hours work)

Use Opus for maximum capability on this critical infrastructure change.
Mistakes could cause game downtime affecting real players.
```

---

## Cost Comparison Examples

### Scenario 1: Documentation Update
- **Haiku:** ~50K tokens × $0.25/M = **$0.0125** ✅
- **Sonnet:** ~50K tokens × $3/M = **$0.15**
- **Opus:** ~50K tokens × $15/M = **$0.75**
- **Savings:** $0.7375 by using Haiku

### Scenario 2: Feature Implementation
- **Haiku:** ~200K tokens × $0.25/M = **$0.05** (too simple, might make mistakes)
- **Sonnet:** ~200K tokens × $3/M = **$0.60** ✅
- **Opus:** ~200K tokens × $15/M = **$3.00**
- **Savings:** $2.40 by using Sonnet (appropriate complexity)

### Scenario 3: AWS Migration
- **Haiku:** ~500K tokens × $0.25/M = **$0.125** (too risky!)
- **Sonnet:** ~500K tokens × $3/M = **$1.50** (risky for critical infrastructure)
- **Opus:** ~500K tokens × $15/M = **$7.50** ✅
- **Cost:** Worth it to prevent production downtime

---

## Monthly Cost Optimization Potential

**If this skill prevents 10 wrong model choices per month:**
- 5 × (Opus → Haiku): Save ~$7.50 each = **$37.50/month**
- 3 × (Opus → Sonnet): Save ~$6 each = **$18/month**
- 2 × (Sonnet → Haiku): Save ~$0.50 each = **$1/month**

**Total Savings:** ~$56.50/month = **$678/year**

---

## Related Documentation

- **Pre-Execution Checklist:** Validates prerequisites before code changes
- **Multi-Agent Verification Rules:** When/how to use multi-agent coordination
- **MEMORY.md:** Project history and handoff summaries

---

**Last Updated:** April 13, 2026
**Created By:** Safeguards Implementation Plan (Option A)
**Purpose:** Prevent mistakes, optimize costs, ensure continuity between AI sessions