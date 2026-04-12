# Adaptive Difficulty System - Design Document
## NON-X Space Shooter Game

**Status:** Stage 1 Complete + Dev Tools + Purple Rebalancing (Mar 29, 2026) - Ready for Testing
**Created:** March 25, 2026
**Last Updated:** March 29, 2026
**Version:** 1.2
**Analytics Version Impact:** 4.0 → 4.2 (purple rebalancing complete)
**Implementation Status:**
- ✅ Stage 1: Multiplier infrastructure (COMPLETE - needs testing)
- ✅ Dev Tools: FPS monitor + bullet speed testing (COMPLETE - Mar 28)
- ✅ Purple Rebalancing: Reduce difficulty + object count (COMPLETE - Mar 29)
- 🎨 Pink Levels: Easter egg levels 13-15 (FUTURE)
- ❌ Stage 2: Static difficulty tiers (SKIPPED - optional)
- ⏳ Stage 3: AI agent (PENDING - next sprint)
- ⏳ Stage 4: ML-based agent (FUTURE)

---

## Table of Contents

1. [Overview & Goals](#1-overview--goals)
2. [Project Rules & Workflow](#2-project-rules--workflow)
3. [Stage 1: Multiplier Infrastructure](#3-stage-1-multiplier-infrastructure)
4. [Stage 2: Static Difficulty Tiers (Optional)](#4-stage-2-static-difficulty-tiers-optional)
5. [Stage 3: AI Agent (Automatic Adjustment)](#5-stage-3-ai-agent-automatic-adjustment)
6. [Stage 4: ML-Based Agent (Advanced)](#6-stage-4-ml-based-agent-advanced)
7. [Implementation Timeline](#7-implementation-timeline)
8. [Analytics Requirements](#8-analytics-requirements)
9. [Testing Strategy](#9-testing-strategy)
10. [Code Locations & Files](#10-code-locations--files)
11. [Rollback Plan](#11-rollback-plan)

---

## 1. Overview & Goals

### Purpose
Create an AI-driven adaptive difficulty system that automatically adjusts game difficulty based on real-time player performance, ensuring optimal challenge and engagement across all skill levels.

### Current Problem
- New players: Game too hard, quit at early levels
- Experienced players: Game too easy after learning patterns
- No middle ground: Static difficulty doesn't adapt to player skill
- High mobile death rate: 81% of deaths on mobile (touch controls harder)

### Solution
Implement a multi-stage adaptive difficulty system:
1. **Infrastructure:** Multiplier-based difficulty control
2. **Static Tiers (Optional):** Manual difficulty selection (Easy/Normal/Hard/Expert)
3. **AI Agent:** Automatic per-level adjustment based on performance metrics
4. **ML-Based (Future):** Personalized difficulty using machine learning

### Success Metrics
- **Retention:** Increase completion rate from 12.2% to 20%+
- **Engagement:** Reduce Level 2 death spike (currently 34 deaths)
- **Balance:** Boss kill rates stabilize at 70-80% (currently 77.8%/83%/100%)
- **Fairness:** Mobile death rate approaches desktop parity (currently 81% vs 19%)

---

## 2. Project Rules & Workflow

### 🚨 CRITICAL WORKFLOW RULES

**Before starting ANY implementation, review these rules:**

#### Rule 1: Data-First Workflow
- Confirm data capture before building any feature
- Audit all metrics: 🟢 Good / 🟡 Improve / 🔴 Fix
- Test analytics events in dev mode before deploying

#### Rule 2: Git Workflow (Protected Main Branch)
**NEVER commit directly to `main`. Always use feature branches.**

```bash
# Correct workflow
git checkout main
git pull origin main
git checkout -b feature/adaptive_difficulty_stage1

# Make changes, test, document

# Commit with proper format
git add [files]
git commit -m "$(cat <<'EOF'
feat(gameplay): implement difficulty multiplier infrastructure

- Add DIFFICULTY_CONFIG object with 6 multipliers
- Apply multipliers to enemy health, speed, bullets
- No gameplay changes (all multipliers = 1.0 baseline)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"

# Push feature branch
git push -u origin feature/adaptive_difficulty_stage1

# Create PR on GitHub
# After merge, delete local branch
git checkout main
git pull origin main
git branch -d feature/adaptive_difficulty_stage1
```

**If you accidentally commit to main:**
```bash
# Create feature branch from current HEAD
git branch feature/your-feature-name

# Switch to feature branch
git checkout feature/your-feature-name

# Reset main to origin/main
git checkout main
git reset --hard origin/main

# Push feature branch
git checkout feature/your-feature-name
git push -u origin feature/your-feature-name
```

#### Rule 3: Pre-Commit Checks (ALWAYS RUN)
```bash
python3 -c "
c = open('game.html').read()
print('game.html:')
print('  Lines:', len(c.splitlines()))
print('  Brace diff:', c[c.find('<script>'):].count('{') - c[c.find('<script>'):].count('}'))
print('  draw function:', 'function draw(' in c)
print()
c = open('game_mobile.html').read()
print('game_mobile.html:')
print('  Lines:', len(c.splitlines()))
print('  Brace diff:', c[c.find('<script>'):].count('{') - c[c.find('<script>'):].count('}'))
print('  draw function:', 'function draw(' in c)
"
```

**Expected output:**
- Brace diff: 0 (both files)
- draw function: True (both files)

#### Rule 4: Documentation Before Code
**Update NON-X_PAIM_Memory.md BEFORE committing code.**

Add to Version History section (~line 1055):
```markdown
- Mar 25 2026 — adaptive difficulty stage 1: multiplier infrastructure, no gameplay changes (both files)
```

Add detailed section with:
- Purpose & problem statement
- Solution approach
- Code changes with line numbers
- Revert instructions
- Analytics impact
- Branch name

#### Rule 5: Never Destructive Operations Without Trace
- Never delete Firebase collections (archive instead)
- Never clear localStorage without documenting impact
- Never reset GA4 properties without backup
- Never modify core game mechanics without testing all dependencies

#### Rule 6: Investigate and Report BEFORE Implementing
- Don't fix bugs blindly — understand root cause first
- Don't optimize without profiling — measure before changing
- Don't add features without understanding existing code flow
- Always report findings to user before making changes

#### Rule 7: Formation Mechanics Are Sacred
**⚠️ CRITICAL:** The morphing + slot rotation system is NON-X's signature mechanic.

Before modifying enemy positioning, timing, or movement:
1. **Read Section 9** of NON-X_PAIM_Memory.md (Formation Morphing + Slot Rotation)
2. **Check debug logs** (enable dev mode with Shift+D)
3. **Report to user** how changes interact with morphing/carousel
4. **Never reset `formationEnteredTime` mid-wave** (breaks morph progression)
5. **Never modify slot assignment** without preserving `(idx + morphCount) % length` pattern

#### Rule 8: Entity Type Taxonomy (Universal Naming)
Always use exact terms when discussing positioning bugs:
- **Main Formation** - Slot rotation morphing formations (grid, diamond, V, circle)
- **Barriers** - Non-shooting obstacles (circle, orbitingShield, horizontalLine, arrow, dualLines)
- **Legacy Formations** - Spiral, pincer, sine wave (reserved for pink levels 13-15)
- **Boss** - Main boss encounters (green, red, purple)
- **Boss Minions** - Orbiting enemies around boss
- **Kamikazes** - Enemies that dive at player

**Do NOT assume "formation" means main formation.** Verify entity type from context.

#### Rule 9: Analytics Version Discipline
**Bump analytics_version ONLY for gameplay mechanic changes.**

Version bump triggers:
- ✅ Difficulty multipliers change gameplay
- ✅ New power-up mechanics
- ✅ Boss behavior changes
- ❌ UI/UX improvements (no bump)
- ❌ Bug fixes that restore intended behavior (no bump)
- ❌ Analytics instrumentation fixes (no bump, use deploy date filter)

Current version: **4.0**
Next version after adaptive difficulty: **4.2**

---

### 🛠️ Development Tools & Skills

#### Local Testing Server
```bash
# Start server for mobile testing
python3 -m http.server 8080 &

# Get local IP for mobile access
ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -1

# Mobile URL: http://[LOCAL_IP]:8080/game_mobile.html
# Desktop URL: http://localhost:8080/game.html

# Stop server when done
pkill -f "python3 -m http.server 8080"
```

#### Developer Mode (Shift+D)
- Toggle on any page (index.html, game.html, game_mobile.html)
- Red pulsing badge shows active state
- Analytics events → console logs (no GA4 firing)
- Debug shortcuts active (Shift+V victory, Shift+G game over, Shift+1-9 jump levels)

#### CI/CD Integrity Checks
GitHub Actions runs on every PR:
- 43 required functions validated per file
- Banned patterns checked (`buildSurveyHTML`, `'phase'.*'standard'`)
- Syntax validation (brace matching, draw function present)

**Add new functions to CI when introducing new systems:**
File: `.github/workflows/integrity-check.yml`

---

## 3. Stage 1: Multiplier Infrastructure

### 3.1 Overview
**Goal:** Create the plumbing for difficulty adjustment without changing gameplay.

**Duration:** 2-3 hours
**Complexity:** Low
**Files:** `game.html`, `game_mobile.html`, `NON-X_PAIM_Memory.md`
**Analytics Impact:** None (all multipliers = 1.0 baseline)
**Version Bump:** None (no gameplay changes yet)

---

### 3.2 Implementation

#### A. Add Difficulty Config Object

**Location:** Both `game.html` (~line 1650) and `game_mobile.html` (~line 1850)

```javascript
// ═══════════════════════════════════════════════════════════════════════════
// ADAPTIVE DIFFICULTY SYSTEM (Mar 2026)
// ═══════════════════════════════════════════════════════════════════════════
// Multiplier-based difficulty control. All values default to 1.0 (baseline).
// Values > 1.0 increase difficulty, values < 1.0 decrease difficulty.
// Adjusted by AI agent each level based on player performance (Stage 3).

var DIFFICULTY_CONFIG = {
  // Enemy durability (hits to destroy shielded enemies)
  // Range: 0.5 (half hits) to 2.0 (double hits)
  enemyHealth: 1.0,

  // Enemy movement speed multiplier
  // Range: 0.7 (30% slower) to 1.4 (40% faster)
  enemySpeed: 1.0,

  // Enemy bullet speed multiplier
  // Range: 0.7 (30% slower) to 1.5 (50% faster)
  bulletSpeed: 1.0,

  // Enemy spawn rate (for wave intervals and boss minions)
  // Range: 0.7 (30% faster spawns) to 1.3 (30% slower spawns)
  // Note: Lower = more enemies, higher = fewer enemies
  spawnRate: 1.0,

  // Damage dealt to player (bullet hits, collisions, boss attacks)
  // Range: 0.6 (40% less damage) to 1.5 (50% more damage)
  playerDamage: 1.0,

  // Health power-up spawn chance multiplier
  // Range: 0.5 (half as frequent) to 2.0 (twice as frequent)
  healthDropRate: 1.0
};

// Track difficulty adjustments for analytics
var difficultyAdjustments = [];
```

#### B. Apply Multipliers to Existing Code

**Location 1: Enemy Shield Hits** (game.html ~line 2680, game_mobile.html ~line 2950)

**Before:**
```javascript
function spawnMorphingFormation(waveData) {
  // ...
  var maxHits = purplePhase ? 25 : 15;
  enemy.maxHits = maxHits;
  enemy.hits = 0;
  // ...
}
```

**After:**
```javascript
function spawnMorphingFormation(waveData) {
  // ...
  var baseHits = purplePhase ? 25 : 15;
  var maxHits = Math.ceil(baseHits * DIFFICULTY_CONFIG.enemyHealth); // Apply difficulty
  enemy.maxHits = maxHits;
  enemy.hits = 0;
  // ...
}
```

**Location 2: Enemy Descent Speed** (game.html ~line 6200, game_mobile.html ~line 7000)

**Before:**
```javascript
// Formation descent (before entered)
if (!formationEntered) {
  formationCurrentCenterY += 1.8; // Fixed descent speed
  // ...
}
```

**After:**
```javascript
// Formation descent (before entered)
if (!formationEntered) {
  var descentSpeed = 1.8 * DIFFICULTY_CONFIG.enemySpeed; // Apply difficulty
  formationCurrentCenterY += descentSpeed;
  // ...
}
```

**Location 3: Enemy Bullet Speed** (game.html ~line 6550, game_mobile.html ~line 7420)

**Before:**
```javascript
function shootEnemyBullet(enemy) {
  var bulletSpeed = redPhase ? 8.05 : 7; // Phase-based speed
  if (purplePhase) bulletSpeed = 9.45;
  // ...
  enemyBullets.push({
    x: enemy.x + enemy.width / 2 - 2,
    y: enemy.y + enemy.height,
    width: 4,
    height: 8,
    speed: bulletSpeed // Fixed speed
  });
}
```

**After:**
```javascript
function shootEnemyBullet(enemy) {
  var baseSpeed = redPhase ? 8.05 : 7; // Phase-based speed
  if (purplePhase) baseSpeed = 9.45;

  var bulletSpeed = baseSpeed * DIFFICULTY_CONFIG.bulletSpeed; // Apply difficulty

  enemyBullets.push({
    x: enemy.x + enemy.width / 2 - 2,
    y: enemy.y + enemy.height,
    width: 4,
    height: 8,
    speed: bulletSpeed
  });
}
```

**Location 4: Boss Minion Spawn Rate** (game.html ~line 6400, game_mobile.html ~line 7250)

**Before:**
```javascript
// Boss minion spawning
if (bossActive && Math.random() < CONFIG.bossMinionSpawnChance) {
  spawnBossMinion();
}
```

**After:**
```javascript
// Boss minion spawning (apply difficulty to spawn rate)
var adjustedSpawnChance = CONFIG.bossMinionSpawnChance / DIFFICULTY_CONFIG.spawnRate;
if (bossActive && Math.random() < adjustedSpawnChance) {
  spawnBossMinion();
}
```

**Location 5: Player Damage** (game.html ~line 4700, game_mobile.html ~line 5300)

**Before:**
```javascript
function playerTakeDamage(damage) {
  if (playerBlinking) return; // Invincibility frames

  // Apply damage
  health -= damage; // Fixed damage
  // ...
}
```

**After:**
```javascript
function playerTakeDamage(damage) {
  if (playerBlinking) return; // Invincibility frames

  // Apply difficulty-adjusted damage
  var adjustedDamage = Math.ceil(damage * DIFFICULTY_CONFIG.playerDamage);
  health -= adjustedDamage;
  // ...
}
```

**Location 6: Health Power-Up Spawn** (game.html ~line 1970, game_mobile.html ~line 2250)

**Before:**
```javascript
function trySpawnPowerup() {
  // ...
  var spawnChance = purplePhase ? 0.4 : (redPhase ? 0.7 : 1.0);
  if (Math.random() < spawnChance) {
    createPowerup('health');
  }
}
```

**After:**
```javascript
function trySpawnPowerup() {
  // ...
  var baseChance = purplePhase ? 0.4 : (redPhase ? 0.7 : 1.0);
  var spawnChance = baseChance * DIFFICULTY_CONFIG.healthDropRate; // Apply difficulty

  if (Math.random() < spawnChance) {
    createPowerup('health');
  }
}
```

---

### 3.3 Testing Stage 1

⚠️ **TESTING STATUS: REQUIRED BEFORE DEPLOY**

All features are implemented but **not yet tested**. Complete testing checklist below before creating PR.

---

#### A. Baseline Testing (No Multiplier Changes)

**Goal:** Verify game plays identically to pre-Stage 1 implementation (all multipliers = 1.0)

**Test Steps:**
1. Start local server: `python3 -m http.server 8080`
2. Open desktop: `http://localhost:8080/game.html`
3. Play through levels 1-4 (green phase)
4. Verify:
   - [ ] Enemies take expected hits (15 hits for levels 1-8)
   - [ ] Bullet speed feels normal (not faster/slower)
   - [ ] Player damage feels normal (25 HP per hit)
   - [ ] Health power-ups appear in cycle (Shield → Laser → Health)
   - [ ] Formation descent speed feels normal
   - [ ] Boss minions spawn at normal rate

5. Repeat on mobile: `http://[LOCAL_IP]:8080/game_mobile.html`

**Expected Result:** Game feels identical to production (no noticeable changes)

---

#### B. Multiplier Console Testing

**Goal:** Verify multipliers actually affect gameplay when adjusted

**Setup:**
1. Enable Developer Mode: Press `Shift+D` on any page
2. Open browser console (F12 or Cmd+Opt+J)
3. Adjust multipliers mid-game

**Test Case 1: Make Game Easier**
```javascript
// In browser console during gameplay
DIFFICULTY_CONFIG.enemyHealth = 0.7;    // Enemies die 30% faster
DIFFICULTY_CONFIG.bulletSpeed = 0.8;    // Bullets 20% slower
DIFFICULTY_CONFIG.playerDamage = 0.7;   // Take 30% less damage
DIFFICULTY_CONFIG.healthDropRate = 1.5; // 50% more health drops
```

**Verify:**
- [ ] Enemy shields break faster (visibly fewer hits needed)
- [ ] Enemy bullets move slower (easier to dodge)
- [ ] Player takes less damage per hit (check HP bar)
- [ ] Health power-ups spawn more often (some cycles spawn 2 health instead of 1)

**Test Case 2: Make Game Harder**
```javascript
// In browser console during gameplay
DIFFICULTY_CONFIG.enemyHealth = 1.3;    // Enemies take 30% more hits
DIFFICULTY_CONFIG.bulletSpeed = 1.2;    // Bullets 20% faster
DIFFICULTY_CONFIG.playerDamage = 1.2;   // Take 20% more damage
DIFFICULTY_CONFIG.healthDropRate = 0.7; // 30% fewer health drops
```

**Verify:**
- [ ] Enemy shields take more hits to break (visibly tankier)
- [ ] Enemy bullets move faster (harder to dodge)
- [ ] Player takes more damage per hit (check HP bar)
- [ ] Health power-ups skip more often (some cycles: Shield → Laser → [skip] → repeat)

**Test Case 3: Reset to Baseline**
```javascript
// Reset all multipliers
DIFFICULTY_CONFIG.enemyHealth = 1.0;
DIFFICULTY_CONFIG.bulletSpeed = 1.0;
DIFFICULTY_CONFIG.playerDamage = 1.0;
DIFFICULTY_CONFIG.healthDropRate = 1.0;
DIFFICULTY_CONFIG.enemySpeed = 1.0;
DIFFICULTY_CONFIG.spawnRate = 1.0;
```

**Verify:**
- [ ] Game returns to normal difficulty (matches baseline testing)

---

#### C. Health Remaining Bonus Testing

**Goal:** Verify health bonus is added to score at victory and tracked in analytics

**Test Case 1: High HP Victory**
1. Enable god mode: `Shift+I` (dev mode)
2. Play through to Level 12 boss
3. Keep health high (180-200 HP)
4. Defeat purple boss
5. **Verify:**
   - [ ] "Victory! You Win!" message appears first (3s)
   - [ ] "Health Bonus: +[amount] pts!" appears 0.2s later (3.2s)
   - [ ] Bonus amount matches remaining HP (e.g., 200 HP → "+200 pts!")
   - [ ] Final score = (game score) + 100 (boss bonus) + [health bonus]
   - [ ] Victory screen shows correct total score

**Test Case 2: Low HP Victory**
1. Play normally (no god mode)
2. Finish purple boss with ~50 HP or less
3. **Verify:**
   - [ ] Health bonus shows smaller amount (e.g., "+47 pts!")
   - [ ] Score calculation still correct

**Test Case 3: Analytics Tracking**
1. Enable GA4 DebugView in browser
2. Defeat purple boss
3. Check `player_won` event in DebugView
4. **Verify:**
   - [ ] Event fires successfully
   - [ ] `health_remaining_bonus` parameter present
   - [ ] Value matches HP remaining (e.g., 127)
   - [ ] Value range: 0-250 (never negative or > maxHealth)

---

#### D. Mobile-Specific Testing

**CRITICAL:** Must test on actual mobile device (not just browser emulation)

**Setup:**
1. Start local server: `python3 -m http.server 8080`
2. Get local IP: `ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -1`
3. Open on mobile: `http://[LOCAL_IP]:8080/game_mobile.html`

**Test:**
- [ ] Baseline gameplay feels normal (all multipliers = 1.0)
- [ ] Console multiplier adjustments work (use mobile browser dev tools)
- [ ] Health bonus appears correctly at victory
- [ ] Health bonus announcement doesn't overlap with touch controls
- [ ] No performance issues (60 FPS maintained)
- [ ] Touch controls remain responsive

---

#### E. Syntax & Build Checks

**Pre-Commit Checks:**
```bash
python3 -c "
c = open('game.html').read()
print('game.html:')
print('  Lines:', len(c.splitlines()))
print('  Brace diff:', c[c.find('<script>'):].count('{') - c[c.find('<script>'):].count('}'))
print('  draw function:', 'function draw(' in c)
print('  DIFFICULTY_CONFIG:', 'DIFFICULTY_CONFIG' in c)
print('  healthBonus:', 'healthBonus' in c)
print()
c = open('game_mobile.html').read()
print('game_mobile.html:')
print('  Lines:', len(c.splitlines()))
print('  Brace diff:', c[c.find('<script>'):].count('{') - c[c.find('<script>'):].count('}'))
print('  draw function:', 'function draw(' in c)
print('  DIFFICULTY_CONFIG:', 'DIFFICULTY_CONFIG' in c)
print('  healthBonus:', 'healthBonus' in c)
"
```

**Expected Output:**
```
game.html:
  Lines: 7731
  Brace diff: 0
  draw function: True
  DIFFICULTY_CONFIG: True
  healthBonus: True

game_mobile.html:
  Lines: 8600
  Brace diff: 0
  draw function: True
  DIFFICULTY_CONFIG: True
  healthBonus: True
```

**Verification:**
- [x] Syntax check passed (completed Mar 26, 2026)
- [ ] Local testing completed (desktop + mobile)
- [ ] Health bonus tested (high HP + low HP scenarios)
- [ ] Analytics verified in DebugView
- [ ] No console errors during gameplay

---

#### F. Analytics Setup Checklist

**Complete BEFORE merging to main:**

**GA4 Configuration:**
- [ ] Register custom dimension: `health_remaining_bonus` (Event-scoped, number)
- [ ] Update existing explorations to include new parameter
- [ ] Test in DebugView (send test event, verify parameter appears)

**Post-Deploy Monitoring (First 48 Hours):**
- [ ] Check `player_won` events in GA4 Realtime report
- [ ] Verify `health_remaining_bonus` values look reasonable (0-250 range)
- [ ] Confirm no errors in browser console logs
- [ ] Monitor for any player reports of scoring issues

**Analytics Questions to Answer (After 1 Week):**
- What's the median health_remaining_bonus? (indicates difficulty balance)
- Do players with higher bonuses have higher total scores? (correlation)
- Desktop vs mobile: Which platform has higher average bonuses?
- Does health bonus correlate with session duration? (fast vs safe play)

---

### Testing Summary

**Status:** ⚠️ NOT TESTED - DO NOT DEPLOY YET

**Completed:**
- ✅ Implementation (Stage 1 multipliers + health bonus)
- ✅ Syntax validation
- ✅ Documentation

**Required Before PR:**
- [ ] Complete Section A: Baseline Testing
- [ ] Complete Section B: Multiplier Console Testing
- [ ] Complete Section C: Health Bonus Testing
- [ ] Complete Section D: Mobile Testing
- [ ] Complete Section E: Final syntax checks
- [ ] Complete Section F: GA4 setup

**Estimated Testing Time:** 2-3 hours (desktop + mobile, all test cases)

---

### 3.4 Documentation Requirements

**Add to NON-X_PAIM_Memory.md Version History (~line 1055):**
```markdown
- Mar 25 2026 — adaptive difficulty stage 1: multiplier infrastructure with 6 config parameters (enemyHealth, enemySpeed, bulletSpeed, spawnRate, playerDamage, healthDropRate). All multipliers default to 1.0 baseline, no gameplay changes. Foundation for AI agent (Stage 3). (both files)
```

**Add detailed section after line 1100:**
```markdown
### Adaptive Difficulty Stage 1: Multiplier Infrastructure (Mar 25, 2026) — Both Files
**Purpose:** Create foundation for AI-driven difficulty adjustment without changing baseline gameplay.

**Implementation:**
- Added `DIFFICULTY_CONFIG` object with 6 multipliers (all default 1.0)
- Applied multipliers to 6 code locations:
  1. Enemy shield hits (spawnMorphingFormation)
  2. Formation descent speed (draw loop)
  3. Enemy bullet speed (shootEnemyBullet)
  4. Boss minion spawn rate (draw loop)
  5. Player damage taken (playerTakeDamage)
  6. Health power-up spawn (trySpawnPowerup)

**Multiplier ranges:**
- enemyHealth: 0.5 to 2.0 (shield hits)
- enemySpeed: 0.7 to 1.4 (movement)
- bulletSpeed: 0.7 to 1.5 (enemy bullets)
- spawnRate: 0.7 to 1.3 (enemy spawns, inverse)
- playerDamage: 0.6 to 1.5 (damage taken)
- healthDropRate: 0.5 to 2.0 (health pickup frequency)

**Files modified:**
- game.html: Lines 1650 (config), 2680, 6200, 6550, 6400, 4700, 1970
- game_mobile.html: Lines 1850 (config), 2950, 7000, 7420, 7250, 5300, 2250

**To revert:** Remove DIFFICULTY_CONFIG object and replace all adjusted values with original hardcoded values.

**Analytics impact:** None (baseline = 1.0, no gameplay changes)

**Next stage:** Stage 3 - AI Agent (automatic adjustment based on performance)

**Branch:** feature/adaptive_difficulty_stage1
```

---

### 3.5 Additional Feature: Health Remaining Bonus (Mar 26, 2026)

**Added during Stage 1 implementation:**

A new scoring mechanic was added alongside the multiplier infrastructure to incentivize health power-up collection and reward skilled play.

**Feature:**
- Defeating purple boss (level 12) adds remaining health points to score (1:1 ratio)
- Example: Finish with 200 HP → +200 bonus points
- Announcement: "Health Bonus: +[amount] pts!" shown 3.2s after victory message

**Analytics Impact:**
- Added `health_remaining_bonus` parameter to `player_won` event
- Requires new GA4 custom dimension (event-scoped, number type)
- Value range: 0-250 (matches CONFIG.maxHealth)

**Strategic Impact:**
- Makes health power-ups dual-purpose (survival + scoring resource)
- Rewards skilled play (fewer hits taken = higher bonus)
- Creates risk/reward decisions (speed vs safety)
- Natural setup for Pink Mode (planned endless mode starting at 200 HP)

**Files Modified:**
- game.html: Boss 3 defeat section (~line 5235-5255), analytics (~5281-5288)
- game_mobile.html: Boss 3 defeat section (~line 5860-5880), analytics (~5930-5937)
- NON-X_PAIM_Memory.md: Full documentation

**Testing Required:**
- [ ] Defeat purple boss with varying HP amounts (25, 100, 200)
- [ ] Verify bonus announcement timing (3.2s delay)
- [ ] Verify correct score calculation (boss bonus + health bonus)
- [ ] Test on both desktop and mobile platforms
- [ ] Verify GA4 parameter appears in DebugView

---

### 3.6 Dev Tools: Performance Monitoring & Testing (Mar 28, 2026)

**Purpose:** Provide real-time bullet speed testing and performance monitoring tools for rebalancing purple phase and validating improvements.

**Status:** ✅ COMPLETE - Ready for testing

---

#### A. Bullet Speed Testing Tool

**Features:**
- Live bullet speed adjustment without code changes
- On-screen display showing effective speed and multiplier
- Phase-aware calculations (green/red/purple baselines)
- Range validation (0.5x to 1.5x)

**Keyboard Shortcuts:**
- `Shift+S` — Toggle speed display on/off
- `[` — Decrease bulletSpeed by 0.05 (min: 0.50x)
- `]` — Increase bulletSpeed by 0.05 (max: 1.50x)
- `Shift+R` — Reset bulletSpeed to 1.0x

**Display Location:** Bottom-right corner (dev mode only)
**Display Format:** `[DEV] Speed: 7.00 (1.00x)`

**Example Usage:**
```
1. Press Shift+D (enable dev mode)
2. Press Shift+S (show speed display)
3. Press [ five times → 0.75x
   Display shows: "Speed: 5.25 (0.75x)" on green level
4. Jump to purple (Shift+0) → Display updates: "Speed: 7.09 (0.75x)"
5. Press ] to increase, test different speeds
6. Press Shift+R to reset to 1.0x
```

**Use Cases:**
- Find optimal min/max bullet speeds for each phase
- Test proposed rebalancing changes before coding
- Validate player feedback about difficulty
- A/B test different speed ranges

**Implementation:**
```javascript
// Variables (both files, ~line 1690 desktop, ~1893 mobile)
var showSpeedDisplay = false; // Toggled with Shift+S

// Keyboard handlers (in keydown event listener)
if (e.key === '[') {
  if (devMode && !gameOver) {
    DIFFICULTY_CONFIG.bulletSpeed = Math.max(0.5, DIFFICULTY_CONFIG.bulletSpeed - 0.05);
    DIFFICULTY_CONFIG.bulletSpeed = Math.round(DIFFICULTY_CONFIG.bulletSpeed * 100) / 100;
    console.log('[DEV MODE] Bullet speed: ' + DIFFICULTY_CONFIG.bulletSpeed + 'x');
  }
}
// Similar for ], Shift+R, Shift+S

// Display rendering (in draw() loop, before requestAnimationFrame)
if (devMode && showSpeedDisplay) {
  var baseSpeed = 7.0; // Green
  if (purplePhase) baseSpeed = 9.45;
  else if (redPhase) baseSpeed = 8.05;

  var effectiveSpeed = baseSpeed * DIFFICULTY_CONFIG.bulletSpeed;
  // Render display in bottom-right corner...
}
```

---

#### B. FPS Counter & Object Count Monitor

**Purpose:** Identify performance bottlenecks, measure purple phase optimization impact.

**Features:**
- Real-time FPS tracking (60-frame rolling average)
- Color-coded performance indicators
- Object count display (enemies + bullets + powerups)
- Console warnings for frame drops
- Automatic in dev mode (no toggle needed)

**Display Location:** Bottom-left corner (dev mode only)
**Display Format:** `[DEV] FPS: 58 | Objects: 45`

**Color Coding:**
- 🟢 **Green** (55-60 FPS): Smooth gameplay
- 🟡 **Yellow** (45-54 FPS): Slight lag
- 🔴 **Red** (<45 FPS): Stuttering/frame drops

**Console Warnings:**
Logs warning when frame time exceeds 33ms (below 30 FPS):
```
[PERF WARNING] Frame took 45ms (22 FPS)
```

**Use Cases:**
- **Baseline purple phase metrics** - Measure current performance
- **Post-rebalancing validation** - Verify improvements
- **Mobile stuttering diagnosis** - Identify exact frame drops
- **Object count optimization** - Track enemy/bullet counts

**Implementation:**
```javascript
// Variables (both files, ~line 1693 desktop, ~1896 mobile)
var fps = 60;
var fpsFrameTimes = [];
var fpsLastTime = Date.now();

// Calculation (in draw() loop, after pause check)
if (devMode) {
  var currentTime = Date.now();
  var deltaTime = currentTime - fpsLastTime;
  fpsLastTime = currentTime;

  fpsFrameTimes.push(deltaTime);
  if (fpsFrameTimes.length > 60) fpsFrameTimes.shift();

  var avgFrameTime = fpsFrameTimes.reduce(function(a, b) { return a + b; }, 0) / fpsFrameTimes.length;
  fps = Math.round(1000 / avgFrameTime);

  // Console warning for drops
  if (deltaTime > 33) {
    console.warn('[PERF WARNING] Frame took ' + deltaTime + 'ms');
  }
}

// Display rendering (in draw() loop, with bullet speed display)
if (devMode) {
  var objectCount = enemies.length + bullets.length + enemyBullets.length + powerups.length;
  // Render FPS with color coding...
  // Render object count...
}
```

---

#### C. URL Parameters for Testing

**Usage:** Jump directly to specific levels without playing through

**Syntax:**
```
http://localhost:8080/game.html?level=11&god=true
```

**Parameters:**
- `level=1-12` - Start at specific level (auto-enables dev mode)
- `god=true` - Enable god mode (invincibility)

**Examples:**
```
# Test purple boss fight
http://localhost:8080/game.html?level=12&god=true

# Test purple level 11 performance
http://localhost:8080/game.html?level=11&god=true

# Test green boss
http://localhost:8080/game.html?level=4&god=true
```

---

#### D. Testing Purple Phase Performance

**Objective:** Establish baseline metrics before rebalancing

**Test Protocol:**
1. Open game with URL: `http://localhost:8080/game.html?level=11&god=true`
2. Press `Shift+D` to enable dev mode (FPS/object display appears)
3. Press `Shift+S` to show bullet speed
4. Play through level 11:
   - Watch FPS color (green/yellow/red)
   - Note object count at peak (formation settled + bullets)
   - Watch for console warnings during powerup collection
   - Test bullet dodging difficulty
5. Record metrics:
   ```
   Level 11 Baseline:
   - FPS: Min ___ / Avg ___ / Max ___
   - Object count: Peak ___
   - Console warnings: ___ during 60s gameplay
   - Bullet speed feels: Too Fast / Just Right / Too Slow
   ```

**Expected Purple Baseline (Before Rebalancing):**
- Object count: ~45-50 objects at peak
- FPS on desktop: 58-60 (stable green)
- FPS on mobile: 45-55 (yellow, occasional red)
- Console warnings: 2-5 during powerup collection on mobile

**Success Criteria After Rebalancing:**
- Object count: ~35-40 objects (10-15 fewer)
- FPS on mobile: 55-60 (stable green)
- Console warnings: 0-1 during powerup events
- Bullet speed: Challenging but fair (8.0 vs current 9.45)

---

#### E. Dev Tools Shortcuts Summary

**Dev Mode Control:**
- `Shift+D` — Toggle dev mode on/off
- `Shift+I` — Toggle god mode (invincibility)

**Navigation:**
- `Shift+V` — Skip to victory screen
- `Shift+G` — Skip to game over screen
- `Shift+1-9` — Jump to levels 1-9
- `Shift+0` — Jump to level 12

**Bullet Speed Testing:**
- `Shift+S` — Toggle speed display
- `[` — Decrease speed by 0.05
- `]` — Increase speed by 0.05
- `Shift+R` — Reset speed to 1.0x

**Performance Monitoring:**
- Always visible in dev mode (FPS + object count)
- Console warnings for frame drops >33ms
- Color-coded FPS (green/yellow/red)

---

### 3.7 Purple Phase Rebalancing (Implemented Mar 29, 2026)

**Status:** ✅ COMPLETE - Ready for testing

See NON-X_PAIM_Memory.md "Purple Phase Rebalancing" section for full details.

**Changes Implemented:**
1. ✅ Removed barriers from levels 9-12 (barrierCount: 0)
   - Level 9: Removed 8 barriers (orbitingShield)
   - Level 10: Removed 10 barriers (dualLines)
   - Level 11: Removed 8 barriers (circle)
   - Level 12: Removed 8 barriers (arrow)
2. ✅ Reduced bullet speeds (both desktop and mobile):
   - Red: 8.05 → 7.5 (multiplier: 1.4 → 1.07)
   - Purple: 9.45 → 8.0 (desktop: 1.65 → 1.14, mobile: 1.35 → 1.14)
3. ✅ Reduced purple boss orbiters: 8 → 6 (completed Mar 28)
4. ✅ Updated analytics_version: 4.0 → 4.2

**Expected Impact:**
- Object count: 59 → 49 (-17% on level 12)
- Max bullet speed with AI: 10.0 (8.0 × 1.25)
- Mobile FPS: Stable 55-60 instead of 45-55
- Difficulty: Challenging but achievable

**Implementation Branch:** feature/dev_tools_fps_bullet_speed (combined with dev tools)

---

### 3.8 Pink Levels Expansion (Future)

**Status:** 🎨 PLANNED - Post-purple rebalancing

Easter egg levels 13-15 with extreme difficulty (0.5-2.5x multiplier range, max bullet speed 17.5).

See NON-X_PAIM_Memory.md "Pink Levels Expansion" section for full design documentation.

**Key Features:**
- Baseline bullet speed: 7.0 (same as green)
- Extended multiplier range: 0.5-2.5x (vs 0.5-1.25x for levels 1-12)
- Legacy formations: Spiral, pincer, sine wave
- Boss 4 encounter at level 15
- Optional content (level 12 victory is canonical ending)

**Implementation Estimate:** ~8 hours

**Priority:** LOW - Implement after Stage 3 AI agent is complete

---

### 3.9 Commit & Push

```bash
# Stage 1 complete workflow
git checkout -b feature/adaptive_difficulty_stage1

# Make code changes...

# Pre-commit check
python3 -c "..." # (syntax validation)

# Update documentation
# Edit NON-X_PAIM_Memory.md (version history + detailed section)

# Stage files
git add game.html game_mobile.html NON-X_PAIM_Memory.md

# Commit
git commit -m "$(cat <<'EOF'
feat(gameplay): add adaptive difficulty multiplier infrastructure

Stage 1 of adaptive difficulty system. Adds DIFFICULTY_CONFIG object
with 6 multipliers (enemyHealth, enemySpeed, bulletSpeed, spawnRate,
playerDamage, healthDropRate). All default to 1.0 baseline.

Applied multipliers to:
- Enemy shield hits (formation spawn)
- Formation descent speed
- Enemy bullet speed
- Boss minion spawn rate
- Player damage taken
- Health power-up spawn chance

No gameplay changes (baseline = 1.0). Foundation for AI agent (Stage 3).

Files modified:
- game.html (7 locations)
- game_mobile.html (7 locations)
- NON-X_PAIM_Memory.md (documentation)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"

# Push
git push -u origin feature/adaptive_difficulty_stage1

# Create PR on GitHub
# Title: feat: adaptive difficulty stage 1 - multiplier infrastructure
# Description: See commit message
```

---

## 4. Stage 2: Static Difficulty Tiers (Optional)

### 4.1 Overview
**Goal:** Predefined difficulty modes players can manually choose.

**Duration:** 3-4 hours
**Complexity:** Medium
**Files:** `index.html`, `game.html`, `game_mobile.html`, `NON-X_PAIM_Memory.md`
**Analytics Impact:** Add `difficulty_tier` parameter to all events
**Version Bump:** 4.0 → 4.1 (gameplay mechanic change)

**⚠️ DECISION POINT:** This stage is **optional**. Most players won't manually adjust difficulty. Consider skipping to Stage 3 (AI agent) for faster time-to-value.

---

### 4.2 Implementation

#### A. Define Difficulty Tiers

**Location:** Both `game.html` and `game_mobile.html` (after DIFFICULTY_CONFIG)

```javascript
// Predefined difficulty tiers (optional manual selection)
var DIFFICULTY_TIERS = {
  easy: {
    enemyHealth: 0.7,      // Enemies die 30% faster
    enemySpeed: 0.8,       // Move 20% slower
    bulletSpeed: 0.85,     // Bullets 15% slower
    spawnRate: 1.2,        // 20% slower spawns (fewer enemies)
    playerDamage: 0.7,     // Take 30% less damage
    healthDropRate: 1.5    // 50% more health drops
  },
  normal: {
    enemyHealth: 1.0,      // Baseline
    enemySpeed: 1.0,
    bulletSpeed: 1.0,
    spawnRate: 1.0,
    playerDamage: 1.0,
    healthDropRate: 1.0
  },
  hard: {
    enemyHealth: 1.3,      // Enemies take 30% more hits
    enemySpeed: 1.15,      // Move 15% faster
    bulletSpeed: 1.2,      // Bullets 20% faster
    spawnRate: 0.85,       // 15% faster spawns (more enemies)
    playerDamage: 1.2,     // Take 20% more damage
    healthDropRate: 0.7    // 30% fewer health drops
  },
  expert: {
    enemyHealth: 1.6,      // Enemies take 60% more hits
    enemySpeed: 1.3,       // Move 30% faster
    bulletSpeed: 1.4,      // Bullets 40% faster
    spawnRate: 0.7,        // 30% faster spawns
    playerDamage: 1.5,     // Take 50% more damage
    healthDropRate: 0.5    // 50% fewer health drops
  }
};
```

#### B. UI Selector (index.html)

**Location:** `index.html` (~line 200, after platform selector)

```html
<!-- Difficulty Selector -->
<div id="difficultySelector" style="margin-top: 20px;">
  <label style="color: #00FFFF; font-size: 16px; display: block; margin-bottom: 10px;">
    Difficulty:
  </label>
  <div style="display: flex; gap: 10px; justify-content: center; flex-wrap: wrap;">
    <button onclick="selectDifficulty('easy')" id="btnEasy"
            style="padding: 10px 20px; background: rgba(0,255,255,0.05); border: 1px solid rgba(0,255,255,0.3); color: #888; cursor: pointer;">
      Easy
    </button>
    <button onclick="selectDifficulty('normal')" id="btnNormal" class="selected"
            style="padding: 10px 20px; background: #00FFFF; border: 1px solid #00FFFF; color: #000; font-weight: bold; cursor: pointer;">
      Normal
    </button>
    <button onclick="selectDifficulty('hard')" id="btnHard"
            style="padding: 10px 20px; background: rgba(0,255,255,0.05); border: 1px solid rgba(0,255,255,0.3); color: #888; cursor: pointer;">
      Hard
    </button>
    <button onclick="selectDifficulty('expert')" id="btnExpert"
            style="padding: 10px 20px; background: rgba(0,255,255,0.05); border: 1px solid rgba(0,255,255,0.3); color: #888; cursor: pointer;">
      Expert
    </button>
  </div>
</div>

<script>
/**
 * Selects a difficulty tier and persists to localStorage.
 * Updates button styling to show selected state.
 * @param {string} tier - 'easy', 'normal', 'hard', or 'expert'
 */
function selectDifficulty(tier) {
  // Update localStorage
  localStorage.setItem('nonx_difficulty', tier);

  // Update button styles
  ['Easy', 'Normal', 'Hard', 'Expert'].forEach(function(t) {
    var btn = document.getElementById('btn' + t);
    if (t.toLowerCase() === tier) {
      btn.style.background = '#00FFFF';
      btn.style.color = '#000';
      btn.style.fontWeight = 'bold';
      btn.classList.add('selected');
    } else {
      btn.style.background = 'rgba(0,255,255,0.05)';
      btn.style.color = '#888';
      btn.style.fontWeight = 'normal';
      btn.classList.remove('selected');
    }
  });

  // Fire analytics event
  trackEvent('difficulty_selected', { tier: tier });
}

// Load saved difficulty on page load
window.addEventListener('DOMContentLoaded', function() {
  var savedDifficulty = localStorage.getItem('nonx_difficulty') || 'normal';
  selectDifficulty(savedDifficulty); // Apply visual state
});
</script>
```

#### C. Load Tier on Game Start

**Location:** Both `game.html` and `game_mobile.html` (in initialization section, ~line 1500)

```javascript
// Load difficulty tier from localStorage (Stage 2 - Static Tiers)
var selectedDifficulty = localStorage.getItem('nonx_difficulty') || 'normal';

// Apply tier multipliers to DIFFICULTY_CONFIG
if (DIFFICULTY_TIERS[selectedDifficulty]) {
  DIFFICULTY_CONFIG = Object.assign({}, DIFFICULTY_TIERS[selectedDifficulty]);
} else {
  // Default to normal if invalid tier stored
  DIFFICULTY_CONFIG = Object.assign({}, DIFFICULTY_TIERS.normal);
  localStorage.setItem('nonx_difficulty', 'normal');
}

console.log('[Difficulty] Tier loaded:', selectedDifficulty, DIFFICULTY_CONFIG);
```

#### D. Analytics Integration

**Add to all gameplay events:**
```javascript
// Example: game_start event
fireEvent('game_start', {
  ab_music_group: userABGroup,
  movement_group: movementABGroup,
  is_replay: isReplay,
  games_played: gamesPlayed,
  difficulty_tier: selectedDifficulty  // NEW PARAMETER
});
```

**Events to update:**
- `game_start`
- `wave_reached`
- `boss_attempt`
- `boss_defeated`
- `player_death`
- `player_won`
- `game_complete`
- `play_again`

---

### 4.3 Testing Stage 2

#### Verification Checklist
- [ ] Difficulty selector appears on main menu
- [ ] Clicking tiers updates visual state (selected button highlighted)
- [ ] Selection persists in localStorage
- [ ] Game loads correct tier on start (check console log)
- [ ] Easy mode: Noticeably easier (fewer hits to kill enemies, slower bullets)
- [ ] Hard mode: Noticeably harder (more hits to kill, faster bullets, more damage)
- [ ] Expert mode: Very challenging (significant difficulty spike)
- [ ] Analytics events include `difficulty_tier` parameter
- [ ] Tier selection tracked in GA4 custom dimension

---

### 4.4 Analytics Configuration

**Register new custom dimension in GA4:**
- Dimension name: `difficulty_tier`
- Scope: Event
- Description: Player-selected difficulty (easy/normal/hard/expert)

**Update all GA4 explorations:**
- Add `difficulty_tier` as secondary dimension
- Filter by tier to compare player performance across difficulties
- Track completion rate by tier

---

### 4.5 Version Bump

**Update analytics_version:**
```javascript
// Both game.html and game_mobile.html
function fireEvent(eventName, params) {
  params = params || {};
  params.analytics_version = '4.1'; // WAS: '4.0'
  // ...
}
```

**Rationale:** Difficulty tiers change gameplay mechanics (enemy health, bullet speed, etc.), requiring version bump for accurate analytics comparisons.

---

## 5. Stage 3: AI Agent (Automatic Adjustment)

### 5.1 Overview
**Goal:** AI automatically adjusts difficulty each level based on player performance metrics.

**Duration:** 5-6 hours
**Complexity:** Medium-High
**Files:** `game.html`, `game_mobile.html`, `NON-X_PAIM_Memory.md`
**Analytics Impact:** New event `difficulty_adjusted`, new parameters
**Version Bump:** 4.1 → 4.2 (or 4.0 → 4.2 if skipping Stage 2)

---

### 5.2 Implementation

#### A. Performance Metrics Tracking

**Location:** Both files, global variables section (~line 1900)

```javascript
// ═══════════════════════════════════════════════════════════════════════════
// ADAPTIVE DIFFICULTY - PERFORMANCE TRACKING (Stage 3)
// ═══════════════════════════════════════════════════════════════════════════
// Tracks per-level player performance to inform AI difficulty adjustments.

var levelPerformance = {
  deaths: 0,              // Number of deaths this level
  healthRemaining: 0,     // HP when level completed
  timeToComplete: 0,      // Seconds from wave start to level end
  damageBlocked: 0,       // Successful shield absorptions
  powerupsCollected: 0,   // Power-ups picked up this level
  levelStartTime: 0,      // Timestamp when level started
  levelStartHealth: 0     // HP at level start
};

// Reset performance tracking (called in advanceLevel)
function resetLevelPerformance() {
  levelPerformance.deaths = 0;
  levelPerformance.healthRemaining = health;
  levelPerformance.timeToComplete = 0;
  levelPerformance.damageBlocked = 0;
  levelPerformance.powerupsCollected = 0;
  levelPerformance.levelStartTime = Date.now();
  levelPerformance.levelStartHealth = health;
}

// Update tracking throughout gameplay
function trackPerformanceMetric(metric, value) {
  if (levelPerformance[metric] !== undefined) {
    if (typeof value === 'number') {
      levelPerformance[metric] += value; // Increment
    } else {
      levelPerformance[metric] = value; // Set
    }
  }
}
```

#### B. Update Tracking Hooks

**Location 1: Player Death** (~line 5100 both files)
```javascript
function playerTakeDamage(damage) {
  // ... existing damage logic ...

  if (health <= 0) {
    // Track death
    trackPerformanceMetric('deaths', 1);
    // ... rest of game over logic
  }
}
```

**Location 2: Shield Absorption** (~line 5150 both files)
```javascript
function playerTakeDamage(damage) {
  // ... existing shield logic ...

  if (hasShield && purplePhase) {
    // Shield absorbed full damage
    trackPerformanceMetric('damageBlocked', 1);
    // ...
  }
}
```

**Location 3: Power-up Collection** (~line 5500 both files)
```javascript
function collectPowerup(powerup) {
  // ... existing collection logic ...

  trackPerformanceMetric('powerupsCollected', 1);
  // ...
}
```

**Location 4: Level Completion** (~line 2500 both files)
```javascript
function advanceLevel() {
  // Calculate time to complete before resetting
  if (levelPerformance.levelStartTime > 0) {
    levelPerformance.timeToComplete = (Date.now() - levelPerformance.levelStartTime) / 1000;
    levelPerformance.healthRemaining = health;
  }

  // Run AI adjustment BEFORE resetting metrics
  adjustDifficultyAI();

  // Reset for next level
  resetLevelPerformance();

  // ... rest of level advancement
}
```

#### C. Performance Score Calculation

**Location:** Both files, after levelPerformance definition (~line 1950)

```javascript
/**
 * Calculates a performance score (0.0 to 1.0) based on level metrics.
 *
 * Score breakdown:
 * - Deaths: 50% weight (fewer deaths = higher score)
 * - Health: 30% weight (more HP remaining = higher score)
 * - Time: 20% weight (faster completion = higher score, levels 5+)
 *
 * @returns {number} Score from 0.0 (struggling) to 1.0 (dominating)
 */
function calculatePerformanceScore() {
  // Death penalty: Each death reduces score by 30%, min 0
  var deathPenalty = Math.max(0, 1 - (levelPerformance.deaths * 0.3));

  // Health bonus: Ratio of health remaining to max health
  var healthBonus = health / CONFIG.maxHealth;

  // Time bonus: Only applies to levels 5+ (early levels have tutorials/learning)
  // Target: 60 seconds per level. Faster = higher bonus, capped at 1.0
  var timeBonus = 1.0;
  if (level >= 5 && levelPerformance.timeToComplete > 0) {
    timeBonus = Math.min(1.0, 60 / levelPerformance.timeToComplete);
  }

  // Weighted score
  var score = (deathPenalty * 0.5) + (healthBonus * 0.3) + (timeBonus * 0.2);

  // Clamp to 0.0-1.0 range
  return Math.max(0, Math.min(1, score));
}
```

#### D. AI Adjustment Logic

**Location:** Both files, after calculatePerformanceScore (~line 2000)

```javascript
/**
 * AI-driven difficulty adjustment based on player performance.
 *
 * Called after each level completion (in advanceLevel).
 * Adjusts DIFFICULTY_CONFIG multipliers by small increments (±3-5%).
 * Tracks adjustments in analytics for tuning.
 *
 * Thresholds:
 * - Score < 0.4: Struggling → Make easier
 * - Score > 0.8: Dominating → Make harder
 * - Score 0.4-0.8: Balanced → No change
 */
function adjustDifficultyAI() {
  var score = calculatePerformanceScore();

  // Skip adjustment for first 2 levels (tutorial/learning period)
  if (level < 3) {
    console.log('[AI Difficulty] Skipping adjustment (tutorial levels)');
    return;
  }

  var adjustment = null;
  var changesMade = [];

  // ── Struggling: Make Easier ──────────────────────────────────────────────
  if (score < 0.4) {
    // Reduce enemy durability
    DIFFICULTY_CONFIG.enemyHealth *= 0.95; // -5%
    changesMade.push('enemyHealth -5%');

    // Slow down bullets
    DIFFICULTY_CONFIG.bulletSpeed *= 0.97; // -3%
    changesMade.push('bulletSpeed -3%');

    // Reduce player damage taken
    DIFFICULTY_CONFIG.playerDamage *= 0.95; // -5%
    changesMade.push('playerDamage -5%');

    // Increase health drops
    DIFFICULTY_CONFIG.healthDropRate *= 1.1; // +10%
    changesMade.push('healthDropRate +10%');

    adjustment = 'easier';
  }

  // ── Dominating: Make Harder ──────────────────────────────────────────────
  else if (score > 0.8) {
    // Increase enemy durability
    DIFFICULTY_CONFIG.enemyHealth *= 1.05; // +5%
    changesMade.push('enemyHealth +5%');

    // Speed up bullets
    DIFFICULTY_CONFIG.bulletSpeed *= 1.03; // +3%
    changesMade.push('bulletSpeed +3%');

    // Increase player damage taken
    DIFFICULTY_CONFIG.playerDamage *= 1.05; // +5%
    changesMade.push('playerDamage +5%');

    // Reduce health drops
    DIFFICULTY_CONFIG.healthDropRate *= 0.9; // -10%
    changesMade.push('healthDropRate -10%');

    adjustment = 'harder';
  }

  // ── Balanced: No Change ──────────────────────────────────────────────────
  else {
    console.log('[AI Difficulty] Balanced (score:', score.toFixed(2), ') - no adjustment');
    return;
  }

  // ── Clamp Multipliers (Prevent Extremes) ─────────────────────────────────
  DIFFICULTY_CONFIG.enemyHealth = Math.max(0.5, Math.min(2.0, DIFFICULTY_CONFIG.enemyHealth));
  DIFFICULTY_CONFIG.bulletSpeed = Math.max(0.7, Math.min(1.5, DIFFICULTY_CONFIG.bulletSpeed));
  DIFFICULTY_CONFIG.playerDamage = Math.max(0.6, Math.min(1.5, DIFFICULTY_CONFIG.playerDamage));
  DIFFICULTY_CONFIG.healthDropRate = Math.max(0.5, Math.min(2.0, DIFFICULTY_CONFIG.healthDropRate));

  // ── Analytics Event ───────────────────────────────────────────────────────
  fireEvent('difficulty_adjusted', {
    level_number: level,
    performance_score: parseFloat(score.toFixed(2)),
    adjustment: adjustment, // 'easier' or 'harder'
    deaths: levelPerformance.deaths,
    health_remaining: levelPerformance.healthRemaining,
    time_to_complete: parseFloat(levelPerformance.timeToComplete.toFixed(1)),
    changes: changesMade.join(', '),
    new_enemy_health: parseFloat(DIFFICULTY_CONFIG.enemyHealth.toFixed(2)),
    new_bullet_speed: parseFloat(DIFFICULTY_CONFIG.bulletSpeed.toFixed(2)),
    new_player_damage: parseFloat(DIFFICULTY_CONFIG.playerDamage.toFixed(2)),
    new_health_drop_rate: parseFloat(DIFFICULTY_CONFIG.healthDropRate.toFixed(2))
  });

  // ── Console Log (Dev Mode) ────────────────────────────────────────────────
  console.log('[AI Difficulty] Adjusted:', adjustment);
  console.log('  Performance Score:', score.toFixed(2));
  console.log('  Changes:', changesMade.join(', '));
  console.log('  Current Config:', DIFFICULTY_CONFIG);
}
```

---

### 5.3 Hybrid Mode (Manual + AI)

**Optional:** Allow players to choose between static tiers and adaptive AI.

**Location:** `index.html` difficulty selector (modify Stage 2 UI)

```html
<button onclick="selectDifficulty('adaptive')" id="btnAdaptive"
        style="padding: 10px 20px; background: rgba(0,255,255,0.05); border: 1px solid rgba(204,0,204,0.5); color: #CC00CC; cursor: pointer;">
  🤖 Adaptive (AI)
</button>
```

**Location:** Both game files, in advanceLevel function

```javascript
function advanceLevel() {
  // ...

  // Only run AI if adaptive mode enabled
  var difficulty = localStorage.getItem('nonx_difficulty') || 'normal';
  if (difficulty === 'adaptive') {
    adjustDifficultyAI(); // Run AI agent
  } else {
    // Static tier: Reload tier multipliers (in case they drifted)
    if (DIFFICULTY_TIERS[difficulty]) {
      DIFFICULTY_CONFIG = Object.assign({}, DIFFICULTY_TIERS[difficulty]);
    }
  }

  // ...
}
```

---

### 5.4 Testing Stage 3

#### Manual Testing Scenarios

**Scenario 1: Intentional Struggling**
1. Start game with Adaptive difficulty
2. Play poorly on purpose:
   - Stand still, take many hits
   - Die 2-3 times per level
   - Don't collect power-ups
3. Check console logs after each level:
   - Performance score should be < 0.4
   - Adjustment: "easier"
   - Enemy health multiplier decreases
   - Bullet speed multiplier decreases
4. Verify gameplay gets easier (enemies die faster, bullets slower)

**Scenario 2: Intentional Domination**
1. Start game with Adaptive difficulty
2. Play perfectly:
   - Don't get hit
   - Complete levels quickly
   - Collect all power-ups
3. Check console logs after each level:
   - Performance score should be > 0.8
   - Adjustment: "harder"
   - Enemy health multiplier increases
   - Bullet speed multiplier increases
4. Verify gameplay gets harder (enemies tankier, bullets faster)

**Scenario 3: Balanced Play**
1. Play normally (some hits, some deaths, moderate speed)
2. Performance score should be 0.4-0.8
3. No adjustments made (console log: "Balanced - no adjustment")
4. Difficulty remains stable

#### Analytics Verification
```javascript
// In browser console, check last adjustment
console.table(difficultyAdjustments);

// Or check GA4 events (DebugView)
// Event: difficulty_adjusted
// Parameters: performance_score, adjustment, level_number, changes
```

---

### 5.5 Analytics Configuration

**Register new event in GA4:**
- Event name: `difficulty_adjusted`
- Custom parameters:
  - `performance_score` (number)
  - `adjustment` (text: easier/harder)
  - `level_number` (number)
  - `deaths` (number)
  - `health_remaining` (number)
  - `time_to_complete` (number)
  - `changes` (text: list of adjustments)
  - `new_enemy_health` (number)
  - `new_bullet_speed` (number)
  - `new_player_damage` (number)
  - `new_health_drop_rate` (number)

**Create GA4 exploration:**
- Name: "Adaptive Difficulty Performance"
- Type: Free form
- Tab 1: Adjustment frequency by level (ROWS: level_number, VALUES: event_count, FILTER: difficulty_adjusted)
- Tab 2: Adjustment direction (ROWS: adjustment, VALUES: event_count)
- Tab 3: Performance score distribution (ROWS: performance_score bins, VALUES: event_count)
- Tab 4: Multiplier trends over time (LINE CHART: new_enemy_health, new_bullet_speed)

---

### 5.6 Version Bump

**Update analytics_version:**
```javascript
// Both game.html and game_mobile.html
function fireEvent(eventName, params) {
  params = params || {};
  params.analytics_version = '4.2'; // WAS: '4.0' or '4.1'
  // ...
}
```

**Rationale:** AI-driven difficulty adjustments fundamentally change gameplay progression, requiring version bump for analytics segmentation.

---

## 6. Stage 4: ML-Based Agent (Advanced)

### 6.1 Overview
**Goal:** Use machine learning to predict optimal difficulty per player based on historical behavior.

**Duration:** 4-6 weeks (includes data collection phase)
**Complexity:** Very High
**Prerequisites:** TensorFlow.js knowledge, Firebase data exports, ML training pipeline
**Status:** Future feature (not critical path)

---

### 6.2 High-Level Approach

#### Phase 1: Data Collection (2-4 weeks)
- Collect player profiles via Firebase
- Export data to CSV/JSON
- Minimum 500+ player sessions for training

```javascript
// Extend player profile tracking
var playerProfile = {
  totalSessions: 0,
  avgLevelReached: 0,
  avgSessionDuration: 0,
  totalDeaths: 0,
  bossWinRate: 0,
  preferredMovement: 'horizontal',
  replayFrequency: 0,
  avgPerformanceScore: 0,
  currentDifficultyMultipliers: {}
};

// Submit to Firebase periodically
function submitPlayerProfile() {
  firebaseSubmitPlayerProfile(playerProfile);
}
```

#### Phase 2: ML Model Training (External)
- Use TensorFlow/Keras to train regression model
- Input features: Player profile metrics
- Output: Optimal difficulty multipliers

```python
# Example training code (Python)
import tensorflow as tf
from tensorflow import keras

# Load player data
data = load_firebase_export('players.csv')

# Feature engineering
X = data[['avg_level_reached', 'boss_win_rate', 'total_sessions']]
y = data[['optimal_enemy_health', 'optimal_bullet_speed']]

# Train model
model = keras.Sequential([
  keras.layers.Dense(64, activation='relu'),
  keras.layers.Dense(32, activation='relu'),
  keras.layers.Dense(2, activation='linear')
])

model.compile(optimizer='adam', loss='mse')
model.fit(X, y, epochs=50)

# Export for TensorFlow.js
model.save('difficulty_model')
```

#### Phase 3: Model Integration
- Load trained model in browser via TensorFlow.js
- Predict optimal multipliers on game start
- Apply predictions to DIFFICULTY_CONFIG

```javascript
// Load model on game start
var difficultyModel;

async function loadDifficultyModel() {
  difficultyModel = await tf.loadLayersModel('model/model.json');
  console.log('[ML] Difficulty model loaded');
}

// Predict optimal difficulty
async function predictOptimalDifficulty(playerProfile) {
  if (!difficultyModel) return;

  var input = tf.tensor2d([
    playerProfile.avgLevelReached / 12,
    playerProfile.bossWinRate,
    playerProfile.totalSessions / 100
  ], [1, 3]);

  var prediction = difficultyModel.predict(input);
  var multipliers = await prediction.data();

  DIFFICULTY_CONFIG.enemyHealth = multipliers[0];
  DIFFICULTY_CONFIG.bulletSpeed = multipliers[1];

  console.log('[ML] Predicted difficulty:', DIFFICULTY_CONFIG);
}
```

---

### 6.3 Considerations

**Pros:**
- Personalized difficulty per player
- Learns from aggregate player behavior
- Can discover non-obvious patterns

**Cons:**
- Complex infrastructure (model training, deployment)
- Requires significant data collection period
- Model may need retraining as game evolves
- Debugging is harder (black box)

**Recommendation:** Only pursue if Stage 3 (simple AI) proves insufficient.

---

## 7. Implementation Timeline

### Recommended Path: Stages 1 + 3 (Skip Stage 2)

| Week | Stage | Tasks | Hours | Deliverable |
|---|---|---|---|---|
| **Week 1** | Stage 1 | Infrastructure | 2-3 | Multiplier system |
| | | Testing & documentation | 1 | PAIM updated |
| | Stage 3 | Performance tracking | 2 | Metrics collection |
| | | AI adjustment logic | 2-3 | adjustDifficultyAI() |
| | | Testing & tuning | 1-2 | Verified adjustments |
| **Week 2** | Deploy | Create PR, merge, monitor | 1-2 | Live on GitHub Pages |
| | Observe | Collect analytics data | - | 1-2 weeks observation |
| **Week 3-4** | Refine | Tune thresholds based on data | 2-3 | Optimized AI |

**Total effort:** 10-13 hours
**Time to production:** 2-3 weeks (including observation)

---

### Alternative Path: All 3 Stages

| Week | Stage | Tasks | Hours |
|---|---|---|---|
| **Week 1** | Stage 1 | Infrastructure | 2-3 |
| | Stage 2 | UI, tiers, testing | 3-4 |
| **Week 2** | Stage 3 | AI agent | 5-6 |
| **Week 3** | Deploy & observe | PR, merge, monitor | 1-2 |

**Total effort:** 13-17 hours
**Benefit:** Players can choose manual tiers OR adaptive AI

---

## 8. Analytics Requirements

### 8.1 New Events

| Event Name | Trigger | Key Parameters |
|---|---|---|
| `difficulty_selected` | Player chooses tier (Stage 2 only) | `tier` (easy/normal/hard/expert/adaptive) |
| `difficulty_adjusted` | AI changes difficulty (Stage 3) | `performance_score`, `adjustment`, `level_number`, `changes`, multipliers |

### 8.2 New Custom Dimensions

| Parameter | Type | Source Events | Purpose |
|---|---|---|---|
| `difficulty_tier` | Text | All gameplay events (Stage 2) | Track manual tier selection |
| `performance_score` | Number | `difficulty_adjusted` | Player skill indicator |
| `adjustment` | Text | `difficulty_adjusted` | Direction of change (easier/harder) |

### 8.3 GA4 Explorations to Build

**1. Difficulty Tier Performance (Stage 2)**
- Rows: difficulty_tier
- Values: completion_rate, avg_level_reached, avg_session_duration
- Filter: analytics_version = 4.1+

**2. Adaptive Difficulty Adjustments (Stage 3)**
- Tab 1: Adjustment frequency by level (ROWS: level_number, VALUES: event_count)
- Tab 2: Adjustment direction distribution (ROWS: adjustment, VALUES: event_count)
- Tab 3: Performance score bins (ROWS: performance_score ranges, VALUES: event_count)
- Tab 4: Multiplier trends (LINE: new_enemy_health, new_bullet_speed over time)
- Filter: analytics_version = 4.2+, difficulty_tier = 'adaptive'

**3. Manual vs Adaptive Comparison**
- Rows: difficulty_tier (normal vs adaptive)
- Values: completion_rate, avg_deaths, avg_session_duration
- Filter: analytics_version = 4.2+

---

## 9. Testing Strategy

### 9.1 Unit Testing (Console)

```javascript
// Test multiplier application
DIFFICULTY_CONFIG.enemyHealth = 0.7;
console.log('Expected shield hits (purple):', Math.ceil(25 * 0.7)); // 18

// Test performance score calculation
levelPerformance.deaths = 2;
levelPerformance.healthRemaining = 150;
levelPerformance.timeToComplete = 45;
console.log('Score:', calculatePerformanceScore()); // Should be ~0.5

// Test AI adjustment
adjustDifficultyAI(); // Check console logs
```

### 9.2 Integration Testing

#### Test Case 1: Stage 1 Infrastructure
- [ ] Set multipliers via console
- [ ] Verify enemy shield hits change
- [ ] Verify bullet speed changes visibly
- [ ] Verify player damage changes
- [ ] Verify health drop frequency changes
- [ ] Syntax check passes

#### Test Case 2: Stage 2 Static Tiers
- [ ] Select "Easy" on main menu
- [ ] Verify gameplay is easier (quick enemy kills, slow bullets)
- [ ] Select "Hard"
- [ ] Verify gameplay is harder (tanky enemies, fast bullets)
- [ ] Check localStorage persistence
- [ ] Verify analytics events include `difficulty_tier`

#### Test Case 3: Stage 3 AI Agent
- [ ] Play poorly (die repeatedly, low health)
- [ ] Check console: performance_score < 0.4, adjustment = "easier"
- [ ] Verify multipliers decreased
- [ ] Play perfectly (no deaths, high health, fast clear)
- [ ] Check console: performance_score > 0.8, adjustment = "harder"
- [ ] Verify multipliers increased
- [ ] Verify `difficulty_adjusted` events fire in GA4 DebugView

### 9.3 Mobile Testing

**Required:** Test on actual mobile device, not just browser emulation.

```bash
# Start local server
python3 -m http.server 8080

# Get local IP
ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -1

# Mobile URL: http://[LOCAL_IP]:8080/game_mobile.html
```

- [ ] Difficulty adjustments work on mobile
- [ ] Performance tracking accurate (deaths, health, time)
- [ ] AI adjustments feel appropriate (not too aggressive)
- [ ] No stuttering or performance issues
- [ ] Touch controls remain responsive

---

## 10. Code Locations & Files

### 10.1 Files Modified per Stage

**Stage 1 (Infrastructure):**
- `game.html` - 7 locations (config + 6 multiplier applications)
- `game_mobile.html` - 7 locations (same)
- `NON-X_PAIM_Memory.md` - Version history + detailed section

**Stage 2 (Static Tiers):**
- `index.html` - UI selector + localStorage logic
- `game.html` - Tier loading, analytics updates (8 events)
- `game_mobile.html` - Same as game.html
- `NON-X_PAIM_Memory.md` - Documentation

**Stage 3 (AI Agent):**
- `game.html` - Performance tracking (3 hooks), score calculation, AI logic
- `game_mobile.html` - Same as game.html
- `NON-X_PAIM_Memory.md` - Documentation

---

### 10.2 Line Number References (Approximate)

**game.html:**
- Config object: ~1650
- Enemy shield hits: ~2680
- Formation descent: ~6200
- Enemy bullet speed: ~6550
- Boss minion spawn: ~6400
- Player damage: ~4700
- Health drop: ~1970
- Level advancement: ~2500
- Analytics wrapper: ~1100

**game_mobile.html:**
- Config object: ~1850
- Enemy shield hits: ~2950
- Formation descent: ~7000
- Enemy bullet speed: ~7420
- Boss minion spawn: ~7250
- Player damage: ~5300
- Health drop: ~2250
- Level advancement: ~2780
- Analytics wrapper: ~1300

**index.html:**
- Difficulty selector: ~200 (after platform selector)
- Analytics tracking: ~450

---

## 11. Rollback Plan

### 11.1 If Stage 1 Breaks Game

**Symptoms:** Game freezes, enemies don't spawn, bullets don't fire

**Quick fix:**
```javascript
// In browser console
DIFFICULTY_CONFIG.enemyHealth = 1.0;
DIFFICULTY_CONFIG.enemySpeed = 1.0;
DIFFICULTY_CONFIG.bulletSpeed = 1.0;
DIFFICULTY_CONFIG.spawnRate = 1.0;
DIFFICULTY_CONFIG.playerDamage = 1.0;
DIFFICULTY_CONFIG.healthDropRate = 1.0;
```

**Full revert:**
```bash
# Revert to previous commit
git revert HEAD
git push origin main

# Or reset branch
git reset --hard HEAD~1
git push --force origin feature/adaptive_difficulty_stage1
```

---

### 11.2 If Stage 3 AI is Too Aggressive

**Symptoms:** Difficulty swings wildly, game becomes too easy/hard too fast

**Tuning options:**
1. **Reduce adjustment magnitude:**
   ```javascript
   // In adjustDifficultyAI()
   DIFFICULTY_CONFIG.enemyHealth *= 0.98; // Was 0.95 (-5% → -2%)
   DIFFICULTY_CONFIG.bulletSpeed *= 0.99;  // Was 0.97 (-3% → -1%)
   ```

2. **Tighten thresholds:**
   ```javascript
   if (score < 0.3) { /* was 0.4 */ }  // Only adjust if really struggling
   if (score > 0.9) { /* was 0.8 */ }  // Only adjust if dominating
   ```

3. **Add cooldown:**
   ```javascript
   var lastAdjustmentLevel = 0;
   function adjustDifficultyAI() {
     // Only adjust every 2 levels
     if (level - lastAdjustmentLevel < 2) return;
     // ... rest of logic
     lastAdjustmentLevel = level;
   }
   ```

---

### 11.3 Emergency Disable (Production)

**If AI causes critical issues post-deploy:**

1. **Quick patch (no code change):**
   ```bash
   # Update index.html via GitHub web UI
   # Remove "Adaptive" option from difficulty selector
   # Users default to "Normal" static tier
   ```

2. **Code disable:**
   ```javascript
   // In game.html and game_mobile.html
   function adjustDifficultyAI() {
     console.log('[AI Difficulty] Temporarily disabled');
     return; // Early exit, no adjustments
   }
   ```

3. **Hotfix PR:**
   - Create branch: `hotfix/disable_adaptive_difficulty`
   - Add return statement to adjustDifficultyAI()
   - Update NON-X_PAIM_Memory.md with incident notes
   - PR, merge, deploy (~5 min)

---

## 12. Success Criteria

### 12.1 Stage 1 Complete When:
- [x] DIFFICULTY_CONFIG object exists in both files
- [x] 6 multipliers applied to 6 code locations each
- [x] Syntax check passes (0 brace errors)
- [x] Manual console testing confirms multipliers work
- [x] Documentation added to PAIM
- [x] PR merged to main

### 12.2 Stage 2 Complete When:
- [x] Difficulty selector appears on main menu
- [x] 4 tiers functional (easy/normal/hard/expert)
- [x] Selection persists in localStorage
- [x] Gameplay difficulty changes are noticeable
- [x] Analytics events include `difficulty_tier`
- [x] GA4 custom dimension registered
- [x] Version bumped to 4.1
- [x] Documentation updated

### 12.3 Stage 3 Complete When:
- [x] Performance tracking hooks functional (deaths, health, time)
- [x] Performance score calculation tested
- [x] AI adjustment logic working (easier/harder)
- [x] Multipliers stay within bounds (0.5-2.0 range)
- [x] Analytics events fire correctly
- [x] Manual testing confirms appropriate adjustments
- [x] Mobile testing passed
- [x] Version bumped to 4.2
- [x] Documentation updated

---

## 13. Future Enhancements

### 13.1 Per-Phase Tuning
Instead of global multipliers, apply different adjustments per phase:
```javascript
var DIFFICULTY_CONFIG_BY_PHASE = {
  green: { enemyHealth: 1.0, bulletSpeed: 1.0, ... },
  red: { enemyHealth: 1.1, bulletSpeed: 1.05, ... },
  purple: { enemyHealth: 1.2, bulletSpeed: 1.1, ... }
};
```

### 13.2 Player Skill Profile
Track long-term player skill across sessions:
```javascript
var playerSkillProfile = {
  gamesPlayed: 0,
  avgLevelReached: 0,
  bossWinRate: 0,
  recommendedDifficulty: 1.0
};
```

### 13.3 Difficulty Achievements
Reward players for completing game on higher difficulties:
- "Beat game on Easy" → Bronze medal
- "Beat game on Hard" → Silver medal
- "Beat game on Expert" → Gold medal
- "Beat game on Adaptive (avg multiplier > 1.3)" → Platinum medal

---

## 14. Future Enhancement: Tier-Based Scoring System

### 14.1 Overview

**Status:** 🎨 DEFERRED - Implement after Pink Levels (13-15) + Survey Triple Laser
**Created:** March 30, 2026
**Implementation Priority:** LOW (Phase 2 of AI agent)
**Design Philosophy:** Silent system - no tier displays to players, scoring adjustments happen behind-the-scenes

---

### 14.2 Problem Statement

After bullet speed reduction (4.0/5.0/6.0), game became too easy. Tester achieved #1 leaderboard on first completion. New baseline (Tier 0) needs to be 5.0/6.0/7.0, but this creates leaderboard fairness issue:

**Issue:** If AI agent lowers difficulty for struggling players, they could complete game on easier settings and dominate leaderboard.

**Solution:** Implement tier-based score multipliers that:
- Reduce scoring for lower tiers (easier = fewer points)
- Increase scoring for higher tiers (harder = more points)
- Maintain leaderboard competitiveness
- Keep system transparent in design docs but silent to players

---

### 14.3 Adjusted Score Multiplier Table

**User Feedback:** Expert 2.0x is too generous, adjusted to 1.75x with proportional scaling.

| Tier | Name | Difficulty | Final Score Multiplier | Reasoning |
|------|------|------------|----------------------|-----------|
| **-3** | Tutorial | Easiest | **0.50x** | Learning mode, not competitive |
| **-2** | Beginner | Very Easy | **0.65x** | Needs significant help |
| **-1** | Easy | Easy | **0.80x** | Below baseline |
| **0** | Normal | Baseline | **1.00x** | New baseline (5.0/6.0/7.0 speeds) |
| **+1** | Challenging | Hard | **1.20x** | Above baseline (was 1.25x) |
| **+2** | Veteran | Very Hard | **1.45x** | Expert play (was 1.50x) |
| **+3** | Expert | Extreme | **1.75x** | Top tier mastery (was 2.00x) |

**Key Adjustment:** Reduced top-tier multipliers to prevent score inflation while maintaining competitive advantage for skilled players.

---

### 14.4 Bonus Structure by Tier

#### Lower Tiers (-3 to -1): Reduced Bonuses
```javascript
// No replay bonus multipliers
var replayBonus = 1; // Disabled (normally 2x/3x/4x/5x)

// No level completion bonuses
var levelBonus = 0; // Disabled (normally +50/+100/+150/+200)

// Base scoring still active
// - Enemy kills: ✅
// - Powerups: ✅
// - Boss defeat base points: ✅
```

**Rationale:** Prevents easy mode from dominating leaderboard via replay farming or completion bonuses.

#### Tier 0 (Normal): Standard Bonuses
```javascript
// All bonuses active (current implementation)
var replayBonus = Math.min(gamesWon + 2, 5); // 2x/3x/4x/5x
var levelBonus = getLevelCompletionBonus(level); // +50/+100/+150/+200
```

#### Higher Tiers (+1 to +3): Enhanced Bonuses
```javascript
// Standard replay bonus PLUS tier completion bonus
var tierCompletionBonus = {
  '1': 500,   // Challenging: +500 points
  '2': 1000,  // Veteran: +1000 points
  '3': 2000   // Expert: +2000 points
};

// Added when player defeats final boss
if (gameCompleted && currentTier > 0) {
  score += tierCompletionBonus[currentTier];
}
```

**Rationale:** Reward skilled players with flat bonus + multiplier for completing harder difficulties.

---

### 14.5 Example Score Calculations

**Scenario:** Player completes game with 10,000 base points

| Tier | Base Points | Bonuses | Subtotal | Multiplier | Final Score | Leaderboard Position |
|------|-------------|---------|----------|------------|-------------|---------------------|
| -3 Tutorial | 10,000 | 0 (disabled) | 10,000 | 0.50x | **5,000** | Bottom 25% |
| -1 Easy | 10,000 | 0 (disabled) | 10,000 | 0.80x | **8,000** | Bottom 40% |
| 0 Normal | 10,000 | +5,000 | 15,000 | 1.00x | **15,000** | Middle 50% |
| +1 Challenge | 10,000 | +5,500 | 15,500 | 1.20x | **18,600** | Top 30% |
| +2 Veteran | 10,000 | +6,000 | 16,000 | 1.45x | **23,200** | Top 15% |
| +3 Expert | 10,000 | +7,000 | 17,000 | 1.75x | **29,750** | Top 5% |

**Result:** Expert tier player earns 1.98x more than Normal tier player (not 2.0x, per user feedback). Lower tier players unlikely to reach top 25.

---

### 14.6 Implementation Pseudocode

```javascript
// ═══════════════════════════════════════════════════════════════════════════
// TIER-BASED SCORING SYSTEM (DEFERRED - Phase 2)
// ═══════════════════════════════════════════════════════════════════════════

/**
 * Score multiplier lookup table
 * Applied to final score after all bonuses
 */
var TIER_MULTIPLIERS = {
  '-3': 0.50,  // Tutorial
  '-2': 0.65,  // Beginner
  '-1': 0.80,  // Easy
  '0': 1.00,   // Normal (baseline)
  '1': 1.20,   // Challenging (adjusted from 1.25)
  '2': 1.45,   // Veteran (adjusted from 1.50)
  '3': 1.75    // Expert (adjusted from 2.00)
};

/**
 * Tier completion bonuses (only for positive tiers)
 */
var TIER_COMPLETION_BONUS = {
  '1': 500,    // Challenging
  '2': 1000,   // Veteran
  '3': 2000    // Expert
};

/**
 * Check if bonuses are enabled for current tier
 * Lower tiers (-3 to -1) have bonuses disabled
 */
function areBonusesEnabled() {
  return currentTier >= 0;
}

/**
 * Calculate final score with tier adjustments
 * Called when submitting to leaderboard
 */
function calculateFinalScore(baseScore, replayCount, gameCompleted) {
  var finalScore = baseScore;

  // Apply replay bonus if enabled
  if (areBonusesEnabled() && replayCount > 0) {
    var replayMultiplier = Math.min(replayCount + 2, 5); // 2x/3x/4x/5x
    finalScore *= replayMultiplier;
  }

  // Add tier completion bonus for higher tiers
  if (gameCompleted && currentTier > 0) {
    var tierBonus = TIER_COMPLETION_BONUS[currentTier.toString()] || 0;
    finalScore += tierBonus;
  }

  // Apply tier multiplier (main balancing factor)
  var tierMultiplier = TIER_MULTIPLIERS[currentTier.toString()] || 1.0;
  finalScore = Math.floor(finalScore * tierMultiplier);

  return finalScore;
}
```

---

### 14.7 Silent System Design (No Player-Facing UI)

**User Decision:** Keep scoring system behind-the-scenes to avoid overwhelming players.

**What players DON'T see:**
- ❌ No tier badges or labels during gameplay
- ❌ No "Difficulty: 🟠 Challenge (1.20x)" display
- ❌ No tier selection UI (AI adjusts silently)
- ❌ No multiplier notifications on game over screen

**What players DO experience:**
- ✅ Game feels appropriately challenging (AI adjusts difficulty)
- ✅ Scores reflect their actual skill level (multipliers applied silently)
- ✅ Leaderboard rankings are fair (lower tier scores naturally lower)
- ✅ Replay bonuses and completion bonuses work as expected (if tier allows)

**Internal tracking only:**
- Store `currentTier` in localStorage
- Submit tier to Firebase with leaderboard entry
- Track tier in GA4 analytics
- Never display tier value to players

---

### 14.8 Firebase Schema Update

```javascript
// Leaderboard submission includes tier metadata
{
  player_id: "uuid-here",
  instagram: "PlayerName",
  score: 18600,              // Already multiplied by tier
  tier: 1,                   // NEW: Difficulty tier when score achieved
  raw_score: 15500,          // NEW: Score before tier multiplier (optional)
  platform: "mobile",
  movement_group: "A",
  date: timestamp
}
```

**Note:** `tier` field only used for analytics and debugging, never displayed to players.

---

### 14.9 Analytics Events

```javascript
// Add tier to existing game_complete event
fireEvent('game_complete', {
  final_score: 18600,
  difficulty_tier: 1,           // NEW: Current tier at completion
  tier_multiplier: 1.20,        // NEW: Multiplier applied
  bonuses_enabled: true,        // NEW: Were bonuses active?
  tier_completion_bonus: 500    // NEW: Flat bonus added
});
```

---

### 14.10 Why Defer Implementation?

**Reasons to implement later:**
1. **Current Priority:** Fix bugs first (green boss shield, pause music toggle, curving bullets)
2. **Baseline Needs Validation:** Need real player data on new Tier 0 (5.0/6.0/7.0) before adding multipliers
3. **AI Agent v1.0 First:** Simple tier adjustment system needs testing before adding score complexity
4. **Pink Levels Integration:** Scoring system should launch with levels 13-15 (expanded content)
5. **Survey Triple Laser:** Natural milestone to introduce scoring changes alongside new reward

**Implementation Timeline:**
```
Phase 1 (Current):
- Fix P1 bugs ✅
- Implement AI agent v1.0 (simple tier adjustment)
- Validate new baseline difficulty (Tier 0)
- Collect 2-4 weeks of player data

Phase 2 (Future - with Pink Levels):
- Implement levels 13-15 (pink phase)
- Add survey triple laser unlock
- Implement tier-based scoring system
- Launch all features together as "Easter Egg Update"
```

---

### 14.11 User Concern: Player Confusion

**User Feedback:** "Players will see their tier but may not understand why they are in a lower tier. Some players will leave the game if they are in a lower tier with no explanation."

**Solution:** Don't show tier to players at all.

**Design Decision:**
- AI adjusts difficulty silently in background
- Players never see "You are in Tier -1"
- Players just experience game getting easier/harder naturally
- Score multipliers applied invisibly at game over
- No explanation needed because system is transparent to players

**Alternative (if transparency desired later):**
- Add "How-To" section explaining adaptive difficulty
- Simple message: "Game adjusts to your skill level for best experience"
- No mention of tiers, multipliers, or scoring penalties

---

### 14.12 Integration with AI Agent v1.0

**AI Agent adjusts tier based on cross-session deaths:**

```javascript
// Persistent tracking across playthroughs
var persistentStats = {
  deathsInGreen: 0,
  deathsInRed: 0,
  deathsInPurple: 0,
  cyclesCompleted: 0,
  currentTier: 0  // Starts at Tier 0 (Normal)
};

// Phase-weighted thresholds
var DEATH_THRESHOLDS = {
  green: 3,   // Can continue from level, less punishing
  red: 2,     // Back to L1, help faster
  purple: 1   // Back to L1 from late game, help immediately
};

// On game over, track deaths and adjust tier
function onGameOver() {
  var deathPhase = getCurrentPhase();
  persistentStats['deathsIn' + capitalize(deathPhase)]++;

  // Check threshold for current phase
  if (persistentStats.deathsInPurple >= 1) {
    currentTier = Math.max(-3, currentTier - 1); // Decrease difficulty
    persistentStats.deathsInPurple = 0;
  }
  // Similar for red/green

  // Apply tier parameters (bullet speed, shield hits, enemy counts)
  applyTierParameters();

  // Save to localStorage
  savePersistentStats();
}

// On cycle complete (beat all 3 bosses)
function onCycleComplete() {
  currentTier = Math.min(3, currentTier + 1); // Increase difficulty
  persistentStats.cyclesCompleted++;

  applyTierParameters();
  savePersistentStats();
}
```

**When scoring system is implemented:**
- `currentTier` already tracked by AI agent
- Just apply multipliers during score calculation
- No additional tracking needed

---

### 14.13 Testing Checklist (When Implemented)

**Tier Multiplier Tests:**
- [ ] Tier -3: Score multiplied by 0.50x
- [ ] Tier 0: Score multiplied by 1.00x (no change)
- [ ] Tier +3: Score multiplied by 1.75x

**Bonus Disable Tests:**
- [ ] Tier -1: Replay bonus disabled (1x, not 2x/3x/4x)
- [ ] Tier -1: Level completion bonus disabled (0 pts, not +50/+100)
- [ ] Tier 0: All bonuses active

**Tier Completion Bonus Tests:**
- [ ] Tier +1: +500 bonus added at victory
- [ ] Tier +2: +1000 bonus added at victory
- [ ] Tier +3: +2000 bonus added at victory

**Leaderboard Tests:**
- [ ] Lower tier scores appear lower on leaderboard
- [ ] Higher tier scores appear higher (even with same base points)
- [ ] Tier field submitted to Firebase correctly
- [ ] Analytics events include tier metadata

**Silent System Tests:**
- [ ] No tier badges visible during gameplay
- [ ] No tier labels on game over screen
- [ ] No tier multiplier notifications
- [ ] Players unaware of tier adjustments

---

### 14.14 Multiplier Adjustment Rationale

**Original proposal vs User feedback:**

| Tier | Original | Adjusted | Reason |
|------|----------|----------|--------|
| +1 Challenge | 1.25x | **1.20x** | Reduce score inflation |
| +2 Veteran | 1.50x | **1.45x** | Prevent excessive advantage |
| +3 Expert | 2.00x | **1.75x** | User: "2.0x is too high" |

**Impact:**
- Expert player still earns 1.98x more than Normal player (was 2.27x)
- Maintains competitive advantage without excessive score inflation
- Leaderboard top 5 still dominated by high-tier players
- More balanced progression between tiers

---

### 14.15 Summary

**What:** Tier-based score multipliers that silently adjust final scores based on difficulty tier.

**Why:** Maintain leaderboard fairness when AI agent lowers difficulty for struggling players.

**When:** Deferred until after Pink Levels (13-15) + Survey Triple Laser implementation.

**How:** Apply multipliers to final score calculation, disable bonuses for lower tiers, enhance bonuses for higher tiers.

**Philosophy:** Keep system silent to players (no tier displays), scoring adjustments happen behind-the-scenes.

**Next Steps:**
1. Implement AI agent v1.0 (simple tier adjustment)
2. Validate new baseline (Tier 0: 5.0/6.0/7.0)
3. Collect 2-4 weeks of player data
4. Implement Pink Levels + Survey Triple Laser
5. Add tier-based scoring system
6. Launch all as "Easter Egg Update"

---

## 15. Contact & Support

**For questions about this implementation:**
- Review NON-X_PAIM_Memory.md Section 13 (Workflow Rules)
- Check DOCUMENTATION_PROGRESS.md for code documentation status
- Consult AB_TESTING_GUIDE.md for analytics best practices

**GitHub Repository:**
- https://github.com/kstanigar/Xenon_3

**Deployment:**
- GitHub Pages: https://kstanigar.github.io/Xenon_3/

---

**Document Version:** 1.1
**Last Updated:** March 30, 2026
**Author:** Claude Sonnet 4.5 + Keith Stanigar
**Status:** Stage 1 Complete + Dev Tools + Purple Rebalancing, Stage 3 (AI Agent) Pending, Tier-Based Scoring Deferred