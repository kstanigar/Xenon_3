# Multi-Agent Verification Rules

**Purpose:** Guidelines for when and how to use multi-agent coordination effectively
**Created:** April 13, 2026
**Project:** Xenon 3 (NON-X)

---

## When to Use Multi-Agent Coordination

### ✅ Use Multi-Agent When:

**1. Searching for Task Lists Across Multiple Files**
- Searching docs/design/*.md (10+ files)
- Searching docs/memory/*.md (multiple memory files)
- Searching conversation transcripts (.jsonl files)
- **Launch 3 parallel agents:** Design docs, Memory docs, Transcripts

**2. Verifying Desktop/Mobile Code Parity**
- Comparing game.html vs game_mobile.html
- Finding all instances of a function in both files
- Verifying consistent implementation
- **Launch 2 parallel agents:** 1 for desktop, 1 for mobile

**3. Auditing Large Sections of Code**
- Finding all button locations (8+ buttons across 2 files)
- Verifying all end-game screens (6+ screens)
- Checking all analytics events (20+ events)
- **Launch agents per file or per category**

**4. Finding All Instances of Pattern**
- All uses of specific function (e.g., buildKofiButtonHTML)
- All class names (e.g., class='hazard-flicker')
- All event tracking calls (e.g., fireEvent)
- **Launch agents per search pattern or file**

**5. Researching Complex Questions**
- "How does the scoring system work?" (multiple files involved)
- "What are all the game over screen variants?" (requires exploration)
- "Where is analytics version defined?" (could be many places)
- **Launch agents to explore different aspects**

---

### ❌ Do NOT Use Multi-Agent When:

**1. Reading a Single Specific File**
- ❌ "Read game.html line 5000-5100" → Use Read tool
- ❌ "What's in MEMORY.md?" → Use Read tool

**2. Searching Within 1-2 Known Files**
- ❌ "Find function foo() in game.html" → Use Grep tool
- ❌ "Search for 'score' in game.html and game_mobile.html" → Use Grep tool

**3. Making Simple Edits**
- ❌ "Update line 100 in game.html" → Use Edit tool
- ❌ "Change color from red to blue" → Use Edit tool

**4. When Time is Critical**
- ❌ Quick fixes during emergencies
- ❌ Simple documentation updates
- ⚠️ Multi-agent has overhead (~2-5 min to launch and coordinate)

---

## Verification Protocol

**Before executing findings from multi-agent search:**

### 1. Review All Agent Outputs
- Read each agent's report completely
- Note any discrepancies between agents
- Verify agents actually found what was requested

**Example:**
```
Agent 1 (Desktop): Found 4 buttons at lines 5907, 6232, 6993, 7322
Agent 2 (Mobile): Found 4 buttons at lines 6534, 6882, 7667, 7866
Status: ✅ Counts match, proceed
```

### 2. Cross-Reference with Documentation
- Check findings against previous audits
- Verify counts match documented expectations
- Review design docs for expected locations

**Example:**
```
Earlier audit (April 12): 8 buttons (4 desktop + 4 mobile)
Current findings: 8 buttons (4 desktop + 4 mobile)
Status: ✅ Match confirmed
```

### 3. Verify Counts Match
- If task list says "8 buttons", agents should find 8
- If previous audit found "6 screens", current should find 6
- **If counts don't match:** STOP and investigate

**Example:**
```
Task list: "Update 8 Player Intel & Power buttons"
Agent findings: 10 buttons found
Status: ⚠️ MISMATCH - Investigate before proceeding
Possible reasons: New buttons added? Counting wrong elements?
```

### 4. Document Verification Approach
- Record verification in appropriate .md file
- Explain methodology (which agents, what they searched)
- Document discrepancies and resolutions

**Add to file (e.g., SUPPORT_DEV_BUTTON_LOCATIONS.md):**
```markdown
## Verification Approach (April 13, 2026)

**Method:** Multi-agent coordination
**Agents Launched:** 2 (Desktop + Mobile)
**Findings:** 8 buttons total (4 + 4)
**Cross-Reference:** Matches April 12 audit
**Status:** ✅ Verified
```

### 5. Get User Approval if Findings Contradict Expectations
- If findings don't match task list
- If findings don't match previous documentation
- If agents report conflicting information
- **NEVER assume** - always confirm with user

---

## Task List Discovery Process

**Standard process when task list is not immediately visible:**

### Step 1: Quick Search (2 min)
```bash
# Search design docs
grep -r "task list\|checklist\|21 tasks" docs/design/

# Search memory docs
grep -r "task list\|checklist\|21 tasks" docs/memory/
grep -r "task list\|checklist\|21 tasks" MEMORY.md
```

### Step 2: Multi-Agent Search (5 min)
**If Step 1 fails, launch 3 parallel Explore agents:**

**Agent 1: Search Design Docs**
```
Task: Find task list in docs/design/*.md
Keywords: "task list", "checklist", "Phase 1", "Phase 2"
Report: File location, task count, phases
```

**Agent 2: Search Memory Docs**
```
Task: Find task list in docs/memory/*.md and MEMORY.md
Keywords: "task list", "checklist", "21 tasks", "Phase"
Report: File location, task count, phases
```

**Agent 3: Search Conversation Transcript**
```
Task: Find task list in .jsonl conversation files
Keywords: "Phase 1", "Phase 2", "task", "checklist"
Report: Session ID, task count, phases
```

### Step 3: Report Findings
- Consolidate all agent reports
- Report to user: "Found task list in [location] with [count] tasks across [phases] phases"
- Get user confirmation before proceeding

### Step 4: If Still Not Found - ASK User
- **NEVER assume** what the task list should be
- **ASK:** "I couldn't find a documented task list. Should I create one, or does one exist that I missed?"
- **WAIT** for user response

---

## Cross-Reference Requirement

**For large codebases (Xenon 3 is ~18,000 lines across 3 files):**

### Rule: Always Cross-Reference Current Findings with Previous Audits

**Before making changes:**
1. Check if previous audit exists
2. Compare current findings with previous findings
3. If counts match → Proceed with confidence
4. If counts don't match → Investigate discrepancy

**Example - Button Update:**
```
Previous Audit (April 12, 2026):
- Found 8 "Player Intel & Power" buttons
- 4 in desktop (game.html)
- 4 in mobile (game_mobile.html)

Current Audit (April 13, 2026):
- Found 8 "Player Intel & Power" buttons
- 4 in desktop (game.html)
- 4 in mobile (game_mobile.html)

Status: ✅ MATCH - Proceed with updates
```

**Example - Discrepancy:**
```
Previous Audit: 8 buttons
Current Audit: 10 buttons

Status: ⚠️ STOP - Investigate
Questions:
- Were 2 new buttons added?
- Am I counting different elements?
- Did previous audit miss something?

Action: Cross-reference with documentation, ask user
```

---

## Documentation Requirements

**After multi-agent search, document:**

### In Appropriate .md File
Add verification section:
```markdown
## Multi-Agent Verification (Date)

**Agents Launched:** [count] agents
**Purpose:** [what were we searching for]
**Findings:** [what was found]
**Cross-Reference:** [comparison with previous audits]
**Status:** [verified/discrepancy found]
**Action Taken:** [proceeded/investigated/asked user]
```

### In MEMORY.md (If Significant)
Add to session notes:
```markdown
**Multi-Agent Coordination:**
- Launched 3 agents to find task list
- Agent 1: Found in docs/design/
- Agent 2: Found in MEMORY.md
- Agent 3: Found in conversation transcript
- Verified: All match (21 tasks, 5 phases)
```

---

## Common Mistakes to Avoid

### ❌ Mistake 1: Skipping Verification
**Don't:** Launch agents, get results, immediately make changes
**Do:** Launch agents → Review outputs → Cross-reference → Verify → Then proceed

### ❌ Mistake 2: Ignoring Count Mismatches
**Don't:** "Previous audit found 8, I found 10, close enough, proceed"
**Do:** "Counts don't match - investigate why before proceeding"

### ❌ Mistake 3: Assuming Agent Findings Are Always Correct
**Don't:** "Agent found it, must be right"
**Do:** "Agent found it, let me verify against documentation"

### ❌ Mistake 4: Using Multi-Agent for Everything
**Don't:** "I need to read a file → launch agent"
**Do:** "I need to read a file → use Read tool (faster, simpler)"

---

## Success Metrics

**Multi-agent coordination is successful when:**
- ✅ Finds information that manual search missed
- ✅ Verifies consistency across multiple files
- ✅ Prevents mistakes through cross-referencing
- ✅ Saves time on large-scale audits (>5 files)

**Multi-agent coordination is NOT successful when:**
- ❌ Used for single-file operations (slower than direct tools)
- ❌ Results not verified (defeats purpose)
- ❌ Findings contradicted but not investigated

---

## Related Documentation

- **Pre-Execution Checklist:** Validates task list before changes
- **Handoff Protocol Skill:** Session start/end procedures
- **MEMORY.md:** Project history and previous audits

---

**Last Updated:** April 13, 2026
**Lesson Learned From:** Phase 2 skip incident (April 13, 2026)
**Purpose:** Prevent "assumed instead of researched" mistakes