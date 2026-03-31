# AI Agent - Advanced Design Ideas (Future Iteration)

**Date:** March 30, 2026
**Status:** 💭 BRAINSTORMING - Not for immediate implementation
**Purpose:** Archive complex system designs discussed during planning session

---

## Summary

During the planning session, we explored several sophisticated approaches to adaptive difficulty:

1. **Speed Gate System** - Bullet speed as one-way ratchet with support parameters
2. **Tier Alignment System** - All parameters must align before speed increases
3. **Phase-Specific Adjustments** - Track performance per phase (green/red/purple)
4. **Staged Adjustment Priority** - Different reduction order when making easier vs harder

These ideas add complexity but could provide more nuanced difficulty adaptation. They're documented here for future consideration after v1.0 is validated.

---

## Advanced Concept 1: Speed Gate + Support Scaffold

### Core Idea
- **Bullet speed** acts as permanent "skill gate" (one-way ratchet)
- **Support params** (shields, counts) flex up/down to help player adapt to new speed
- Once speed increases, it never decreases - player must adapt

### Philosophy
Force skill development in core mechanic (dodging) while providing adjustable support scaffolding.

### Example Progression
```
Player at Speed 5.0, Shields 20, Counts 5 (all maxed at current speed)
→ Speed increases to 6.0, Shields reset to 10 (new speed tier)
→ Player struggles with 6.0 speed
→ Decrease counts: 5→4 (NOT speed - speed stays at 6.0)
→ Still struggling → Decrease shields: 10→5
→ Player adapts to 6.0 over time
→ Increase shields back: 5→10→15→20
→ Increase counts back: 4→5
→ All maxed → Ready for next speed tier (7.0)
```

### Pros
- Forces progressive mastery of core skill
- Prevents regression (speed never decreases)
- Natural learning curve

### Cons
- Complex to implement
- Could frustrate players stuck at speed tier
- Requires careful balancing of support param ranges

---

## Advanced Concept 2: Tier Alignment System

### Core Idea
Each parameter tracks its tier position (e.g., -2, -1, 0, +1, +2). Speed can only increase when all parameters are "aligned" at the same tier.

### Speed Increase Rule
```javascript
if (shields.tier >= speed.tier &&
    counts.tier >= speed.tier) {
  speed.tier++;  // Allowed to increase
  // Reset support params to baseline of new tier
}
```

### Example
```
Speed Tier 0, Shields Tier -1, Counts Tier 0
→ Can't increase speed yet (shields lagging)
→ Complete cycle: Shields +1 tier (now Tier 0)
→ All aligned! Next cycle increases speed to Tier 1
```

### Pros
- Ensures player has "earned" speed increase
- Prevents premature difficulty spikes
- Clear progression milestones

### Cons
- Very complex to explain to players
- Hard to visualize current state
- Requires UI to show tier positions

---

## Advanced Concept 3: Phase-Specific Adjustments

### Core Idea
Track performance separately per phase (green/red/purple) and adjust each independently.

### Data Structure
```javascript
var difficulty = {
  green: { bulletSpeed: 4.0, shieldHits: 10, counts: 3 },
  red: { bulletSpeed: 5.0, shieldHits: 15, counts: 4 },
  purple: { bulletSpeed: 6.0, shieldHits: 20, counts: 5 }
};
```

### Adjustment Logic
```javascript
// Player struggles in red phase only
difficulty.red.counts--;  // Adjust red, leave green/purple alone
```

### Pros
- Most accurate - targets exact problem areas
- Handles uneven skill distribution
- Player feels understood by system

### Cons
- Complex implementation
- Could create weird difficulty curves (red easier than green)
- Harder to persist and sync across sessions

---

## Advanced Concept 4: Staged Adjustment Priority

### Core Idea
Different priority order when making game harder vs easier.

**Making Harder (player excelling):**
1. Increase shields (least noticeable)
2. Increase counts (more noticeable)
3. Increase speed (most noticeable)

**Making Easier (player struggling):**
1. Decrease speed (immediate relief)
2. Decrease counts (reduce pressure)
3. Decrease shields (last resort)

### Rationale
When player needs help, give most impactful change first. When increasing difficulty, ease them in gradually.

### Pros
- Better UX (immediate relief when struggling)
- Gradual escalation when excelling
- Asymmetric design feels more intuitive

### Cons
- Different rules for up vs down (harder to code)
- Could confuse players who expect symmetry
- May not work well with ratchet system

---

## Why These Are "Future Work"

The v1.0 simplified system is:
- ✅ Much easier to implement
- ✅ Easier for players to understand
- ✅ Sufficient for initial testing
- ✅ Can always add complexity later

These advanced ideas should be reconsidered AFTER:
1. v1.0 is implemented and tested
2. We have real player data
3. We identify specific pain points
4. We validate the core adjustment triggers work

---

## Key Learnings from Discussion

1. **Simplicity matters** - Too many rules = confusion
2. **Start simple, iterate** - Add complexity only when needed
3. **Player understanding** - System should be somewhat transparent
4. **Test with real data** - Don't over-engineer without validation

---

## Recommended Next Steps (If/When Revisiting)

1. Implement v1.0 first
2. Collect analytics on:
   - Average cycles to reach each speed tier
   - Death counts per phase
   - Difficulty adjustment frequency
3. Survey players on difficulty curve
4. Identify specific problems (e.g., "too many players stuck at speed 6.0")
5. Apply targeted advanced concept to solve specific problem

**Don't add complexity preemptively!**