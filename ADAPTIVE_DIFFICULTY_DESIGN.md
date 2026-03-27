# Adaptive Difficulty System - Design Document
## NON-X Space Shooter Game

**Status:** Design Phase
**Created:** March 25, 2026
**Version:** 1.0
**Analytics Version Impact:** 4.1 → 4.2

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

#### Manual Console Testing
```javascript
// In browser console, adjust multipliers mid-game (dev mode)

// Make game easier
DIFFICULTY_CONFIG.enemyHealth = 0.7;    // Enemies die 30% faster
DIFFICULTY_CONFIG.bulletSpeed = 0.8;    // Bullets 20% slower
DIFFICULTY_CONFIG.playerDamage = 0.7;   // Take 30% less damage
DIFFICULTY_CONFIG.healthDropRate = 1.5; // 50% more health drops

// Make game harder
DIFFICULTY_CONFIG.enemyHealth = 1.3;    // Enemies take 30% more hits
DIFFICULTY_CONFIG.bulletSpeed = 1.2;    // Bullets 20% faster
DIFFICULTY_CONFIG.playerDamage = 1.2;   // Take 20% more damage
DIFFICULTY_CONFIG.healthDropRate = 0.7; // 30% fewer health drops

// Reset to baseline
DIFFICULTY_CONFIG.enemyHealth = 1.0;
DIFFICULTY_CONFIG.bulletSpeed = 1.0;
DIFFICULTY_CONFIG.playerDamage = 1.0;
DIFFICULTY_CONFIG.healthDropRate = 1.0;
```

#### Verification Checklist
- [ ] Enemy shields take more/fewer hits (test with console adjustment)
- [ ] Enemy bullets move faster/slower visibly
- [ ] Player health drops by adjusted amounts
- [ ] Health power-ups spawn more/less frequently
- [ ] Formation descent speed changes
- [ ] Boss minions spawn more/less frequently
- [ ] Syntax check passes (0 brace errors)
- [ ] Game plays normally at baseline (1.0 multipliers)

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

### 3.5 Commit & Push

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

## 14. Contact & Support

**For questions about this implementation:**
- Review NON-X_PAIM_Memory.md Section 13 (Workflow Rules)
- Check DOCUMENTATION_PROGRESS.md for code documentation status
- Consult AB_TESTING_GUIDE.md for analytics best practices

**GitHub Repository:**
- https://github.com/kstanigar/Xenon_3

**Deployment:**
- GitHub Pages: https://kstanigar.github.io/Xenon_3/

---

**Document Version:** 1.0
**Last Updated:** March 25, 2026
**Author:** Claude Sonnet 4.5 + Keith Stanigar
**Status:** Ready for Implementation