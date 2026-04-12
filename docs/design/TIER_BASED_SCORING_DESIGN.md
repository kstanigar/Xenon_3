# Tier-Based Scoring System (AI Agent Phase 2)
**Date:** April 1, 2026
**Status:** Ready for Implementation
**Priority:** HIGH - Prevent easy-mode leaderboard exploitation

---

## **Problem Statement**

With AI Agent v1.0, players can decrease to easier tiers (Tutorial/Beginner/Easy) for significantly slower bullets and reduced challenge. Without scoring adjustments, a player on **Tier -3 (Tutorial)** with:
- 3.5 bullet speed (30% slower than Normal)
- 0 shield hits (instant enemy kills)
- 2/3/4 boss orbiters (50% fewer than Normal)

...could dominate the leaderboard by playing on easy mode, defeating the purpose of having difficulty tiers.

**User Quote:**
> "I don't want for players on tier -3 or -2 to be the #1 player in the top 25"

---

## **Solution: Score Multipliers by Tier**

Apply a **per-tier score multiplier** to all scoring events. Higher tiers earn more points, incentivizing skilled play.

---

## **Multiplier Table**

| Tier | Name | Bullet Speed | Score Multiplier | Effective Score Example |
|------|------|--------------|------------------|-------------------------|
| **-3** | Tutorial | 3.5 | **0.50×** | 10,000 pts → 5,000 pts |
| **-2** | Beginner | 4.0 | **0.70×** | 10,000 pts → 7,000 pts |
| **-1** | Easy | 4.5 | **0.85×** | 10,000 pts → 8,500 pts |
| **0** | Normal | 5.0 | **1.00×** ✨ | 10,000 pts → 10,000 pts (baseline) |
| **+1** | Challenge | 5.5 | **1.20×** | 10,000 pts → 12,000 pts |
| **+2** | Veteran | 6.0 | **1.40×** | 10,000 pts → 14,000 pts |
| **+3** | Expert | 6.5 | **1.75×** | 10,000 pts → 17,500 pts |

**Design Notes:**
- **Tier 0 (Normal)** is the baseline (1.00×)
- **Tutorial** is heavily penalized (0.50×) - half points
- **Expert** earns 75% more points (1.75×)
- Multipliers scale with difficulty increase
- **User feedback (Mar 30):** Originally 2.0× for Expert, reduced to 1.75× per user request

---

## **Implementation Design**

### **1. Add Multiplier Lookup**

Add to TIER_CONFIG in both game files:

```javascript
var TIER_CONFIG = {
  '-3': { bulletSpeed: 3.5, shieldHits: 0,  bossOrbiters: [2,3,4], minionRate: 0,   scoreMultiplier: 0.50 },
  '-2': { bulletSpeed: 4.0, shieldHits: 5,  bossOrbiters: [3,4,5], minionRate: 0.5, scoreMultiplier: 0.70 },
  '-1': { bulletSpeed: 4.5, shieldHits: 10, bossOrbiters: [3,4,5], minionRate: 1.0, scoreMultiplier: 0.85 },
  '0':  { bulletSpeed: 5.0, shieldHits: 15, bossOrbiters: [4,5/6], minionRate: 1.0, scoreMultiplier: 1.00 },
  '1':  { bulletSpeed: 5.5, shieldHits: 18, bossOrbiters: [4,6,7], minionRate: 1.5, scoreMultiplier: 1.20 },
  '2':  { bulletSpeed: 6.0, shieldHits: 20, bossOrbiters: [5,6,8], minionRate: 1.5, scoreMultiplier: 1.40 },
  '3':  { bulletSpeed: 6.5, shieldHits: 25, bossOrbiters: [5,7,9], minionRate: 2.0, scoreMultiplier: 1.75 }
};
```

---

### **2. Apply Multiplier to All Scoring Events**

**Scoring Events to Multiply:**
1. ✅ **Enemy kills** - Base 5 pts (formation/kamikaze)
2. ✅ **Power-up collection** - Base 5 pts
3. ✅ **Boss defeat** - Base 500 pts (varies by boss)
4. ✅ **Victory bonuses** - Health remaining, replay bonuses

**How to Apply:**

```javascript
// Helper function to get current tier multiplier
function getTierMultiplier() {
  var tierConfig = TIER_CONFIG[currentTier.toString()];
  return tierConfig ? tierConfig.scoreMultiplier : 1.0; // Default 1.0 if not found
}

// Example: Enemy kill
function addScore(basePoints) {
  var multiplier = getTierMultiplier();
  var earnedPoints = Math.round(basePoints * multiplier);
  score += earnedPoints;
  updateUI();
}

// Usage:
// OLD: score += 5;
// NEW: addScore(5);
```

---

### **3. Track Tier History for Session**

**Challenge:** Player's tier can change during gameplay. Which tier's multiplier applies?

**Solution Options:**

#### **Option A: Real-Time Current Tier (Recommended)**
- Use `currentTier` at moment of scoring event
- If player is on Tier +3 when killing enemy → 1.75× multiplier
- If player drops to Tier +2 later → future kills use 1.40× multiplier

**Pros:**
- Simple implementation
- Fair - rewards difficulty at moment of achievement
- Encourages maintaining higher tiers

**Cons:**
- Score can "slow down" if tier decreases mid-game

---

#### **Option B: Session Average Tier**
- Track weighted average tier across session
- Calculate final multiplier at victory screen

**Pros:**
- Smoother scoring experience
- Prevents "tier gaming"

**Cons:**
- Complex calculation
- Less transparent to players

---

#### **Option C: Highest Tier Reached**
- Use highest tier achieved during session

**Pros:**
- Rewards peak performance
- Simple to track

**Cons:**
- Could enable "tier gaming" (increase tier briefly, then drop)
- Less fair

---

**Recommendation: Use Option A (Real-Time Current Tier)**

Simple, fair, and incentivizes consistent high-tier play.

---

### **4. Display Multiplier to Player**

**Option 1: Silent System (Recommended)**
- Don't show multiplier to player
- Apply behind-the-scenes
- Final score reflects adjusted value

**Pros:**
- Less UI clutter
- Players focus on gameplay, not math
- Leaderboard "just works" fairly

**Cons:**
- Less transparency
- Players might not understand why scores differ

---

**Option 2: Show in AI Mode (Dev Testing)**
- Display multiplier when AI Mode is enabled (Shift+A)
- Hidden in normal gameplay

**Pros:**
- Transparent for testing
- Doesn't clutter regular gameplay

**Cons:**
- Players might discover via dev mode

---

**Option 3: Show in Pause Menu / Victory Screen**
- Display "Current Tier: +2 (Veteran) - Score Multiplier: 1.40×"

**Pros:**
- Full transparency
- Players understand scoring

**Cons:**
- UI design needed
- Might confuse casual players

---

**Recommendation: Option 2 (Show in AI Mode Only)**

Keep it silent for normal gameplay, but show multiplier in AI Mode display for testing/verification.

---

### **5. Victory Screen Display**

**Show final score with subtle tier indicator:**

```
━━━━━━━━━━━━━━━━━━━━━━━━
🎉 VICTORY! 🎉
━━━━━━━━━━━━━━━━━━━━━━━━

Final Score: 12,450
(Completed on Challenge difficulty)

Health Remaining Bonus: +205
Replay Bonus: +50

TOTAL: 12,705

[Submit to Leaderboard]
[Play Again]
```

**Don't show multiplier explicitly**, but indicate tier name for transparency.

---

### **6. Leaderboard Display**

**Option 1: Show Tier with Score**
```
Rank | Player | Score | Tier
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1    | Alice  | 15,200 | Expert
2    | Bob    | 14,800 | Veteran
3    | Carol  | 12,100 | Challenge
```

**Option 2: Hide Tier (Silent)**
```
Rank | Player | Score
━━━━━━━━━━━━━━━━━━━━━━━━
1    | Alice  | 15,200
2    | Bob    | 14,800
3    | Carol  | 12,100
```

**Recommendation: Option 2 (Hide Tier)**

Keep leaderboard simple. Scoring adjustments happen behind-the-scenes.

---

## **Implementation Steps**

### **Phase 1: Add Multiplier Lookup (~20 min)**
1. Add `scoreMultiplier` field to TIER_CONFIG (7 tiers × 2 files)
2. Create `getTierMultiplier()` helper function
3. Test multiplier lookup in AI Mode

### **Phase 2: Apply to Scoring Events (~45 min)**
4. Find all scoring locations:
   - Enemy kills (formation, kamikaze, orbiters, minions)
   - Power-up collection
   - Boss defeats (3 bosses)
   - Victory bonuses (health, replay)
5. Replace `score += X` with `addScore(X)` using multiplier
6. Test scoring at different tiers

### **Phase 3: Display in AI Mode (~15 min)**
7. Update AI Mode indicator to show multiplier
8. Update AI Mode console logs to show multiplier

### **Phase 4: Victory Screen Update (~10 min)**
9. Add tier name to victory message (subtle indicator)
10. Don't show multiplier explicitly

### **Phase 5: Testing (~30 min)**
11. Test scoring at Tier -3 (Tutorial) - expect 50% of normal
12. Test scoring at Tier +3 (Expert) - expect 175% of normal
13. Test tier changes mid-game (verify real-time multiplier)
14. Verify final scores on leaderboard

**Total Time: ~2 hours**

---

## **Example Score Comparison**

**Scenario:** Player completes game with 10,000 base points

| Tier | Multiplier | Raw Score | Final Score | Rank Impact |
|------|------------|-----------|-------------|-------------|
| **-3 (Tutorial)** | 0.50× | 10,000 | **5,000** | #50+ (bottom) |
| **-1 (Easy)** | 0.85× | 10,000 | **8,500** | #30-40 |
| **0 (Normal)** | 1.00× | 10,000 | **10,000** | #15-25 ✅ |
| **+2 (Veteran)** | 1.40× | 10,000 | **14,000** | #5-10 |
| **+3 (Expert)** | 1.75× | 10,000 | **17,500** | #1-3 🏆 |

**Result:** Expert players earn 3.5× more points than Tutorial players for same base performance.

---

## **Edge Cases**

### **1. Tier changes mid-game**
- **Solution:** Use current tier at moment of scoring event
- Example: Kill enemy at Tier +3 (1.75×), drop to +2, next kill at 1.40×

### **2. Player at Tier -3 scores 20,000 base points**
- **Calculation:** 20,000 × 0.50 = 10,000 final
- **Result:** Still lower than Tier 0 player with 12,000 base (12,000 × 1.0 = 12,000)

### **3. Leaderboard shows adjusted or raw score?**
- **Answer:** Show **final adjusted score**
- Firebase stores final score (already multiplied)
- No need to store base score separately

### **4. Multiplier visible to players?**
- **Answer:** Only in AI Mode (Shift+A)
- Normal gameplay: silent
- Victory screen: show tier name only ("Completed on Expert")

---

## **Analytics Tracking**

Track tier distribution at victory:

```javascript
fireEvent('player_won', {
  score: finalScore,
  tier: currentTier,
  tier_multiplier: getTierMultiplier(),
  base_score: baseScore, // Optional: track for analysis
  // ... other params
});
```

Allows analysis:
- Are players exploiting easy tiers?
- What's the average tier at victory?
- Does multiplier system incentivize harder tiers?

---

## **Success Criteria**

✅ Tutorial/Beginner players **cannot** reach top 10 with low skill
✅ Expert players **earn significantly more** points for same performance
✅ Tier 0 (Normal) remains fair baseline
✅ Multiplier **encourages** harder tier play
✅ Scoring system **feels balanced** across all tiers
✅ No leaderboard exploitation via easy-mode dominance

---

## **Rollback Plan**

If scoring system causes issues:

**Quick disable:**
```javascript
function getTierMultiplier() {
  return 1.0; // Disable all multipliers
}
```

**Full revert:**
- Remove `scoreMultiplier` field from TIER_CONFIG
- Remove `getTierMultiplier()` function
- Restore direct `score += X` assignments
- Remove tier indicator from victory screen

---

## **User Approval**

**User Quote:**
> "We should implement a scoring system based off which tier the players are performing in. I don't want for players on tier -3 or -2 to be the #1 player in the top 25"

**Status:** Approved for implementation
**Priority:** HIGH - Implement before AI Agent deployment

---

**Implementation Date:** April 1, 2026 (scheduled)
**Estimated Time:** 2 hours
**Files Modified:** game.html, game_mobile.html