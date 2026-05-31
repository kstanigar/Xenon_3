# Difficulty Toggle Discussion
**Date:** April 1, 2026
**Status:** Deferred - Keep AI Agent only for now
**Decision:** Manual difficulty selection not needed at launch

---

## **Context**

After implementing AI Agent v1.0 (7-tier adaptive difficulty), user asked:
> "Should we implement a difficulty toggle for players that complete 1 cycle?"

This document captures the discussion and rationale for deferring manual difficulty controls.

---

## **Options Considered**

### **Option A: Manual Tier Selector (Post-Victory Screen)**
After beating Boss 3, show difficulty selector for next cycle.

**Pros:**
- Player has full control over difficulty
- Clear expectations before starting
- Respects scoring multiplier

**Cons:**
- Removes AI adaptation element
- Could enable easy-mode exploitation if no scoring multiplier

---

### **Option B: Pause Menu Tier Adjustment**
Add "Difficulty" option in pause menu (P key).

**Pros:**
- Accessible anytime during gameplay
- Combines with AI Agent (manual override)

**Cons:**
- Could feel like "cheating" if adjustable mid-level
- Might reduce AI Agent's purpose

---

### **Option C: Hybrid System**
Keep AI Agent primary, add victory screen choice + pause override.

**Pros:**
- Best of both worlds (manual + automatic)
- Respects player agency
- AI still provides adjustments

**Cons:**
- More complex UI
- Need to design victory screen modal

---

## **Decision: Keep AI Agent Only**

**Rationale:**
1. AI Agent already implemented and working
2. Players can access Easy mode after first cycle (Tier -1 minimum with speed lock)
3. Tier-based scoring multiplier (Phase 2) will naturally incentivize harder tiers
4. Can gather player feedback before adding manual controls
5. Simpler UX - less cognitive load for players

**Next Steps:**
- Implement tier-based scoring system (prevents easy-mode leaderboard dominance)
- Monitor player feedback for 2-4 weeks
- Re-evaluate manual difficulty toggle if players request it

---

## **Future Consideration**

If manual control becomes necessary:
- **Victory screen tier selector** recommended (one-time choice per cycle)
- Keep AI Agent active during gameplay (automatic adjustments)
- Optional pause menu override for manual tier changes
- Preserve speed ratchet (min Tier -1 after first cycle)

---

**User Quote:**
> "Yes, let's go with what is already here. But document the discussion."

**Implementation Date:** Not planned - deferred indefinitely
**Review Date:** After 2-4 weeks of player feedback