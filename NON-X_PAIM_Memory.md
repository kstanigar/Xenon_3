# NON-X — PAIM Master Memory
### Project AI Model Reference Document
_Last updated: March 14, 2026 (session 4)_
_Merged from: Game Dev Memory + Analytics Memory_

---

## HOW TO USE THIS DOCUMENT

This is the single source of truth for the NON-X project. It is shared with every AI model working on this project (the PAIM — Project AI Model). Before responding to any request, read the relevant sections. Key rules:

1. **Data-first workflow** — before building any visual or metric, confirm data is being captured correctly. Audit as: 🟢 Good / 🟡 Improve / 🔴 Fix.
2. **Never recommend destructive operations** (delete Firebase collections, clear localStorage, reset GA4 properties) without tracing all dependent code first.
3. **Never diagnose a game over screen bug** without asking: what level, what score, first game or replay?
4. **analytics_version = 3.0** — filter ALL GA4 explorations and Looker Studio reports to this version. Bump ONLY when gameplay mechanics change, not for instrumentation fixes.
5. **Pre-launch data (Feb 10 – Mar 9, 2026) is QA/self-testing** — do not draw product conclusions or calibrate benchmarks from it.
6. **Real player baseline starts: ~Mar 10, 2026.**
7. **Investigate and report before making any changes** — always trace root cause first, confirm findings, then implement with comments and revert instructions.

---

## 1. PROJECT OVERVIEW

| Field | Value |
|---|---|
| Game | NON-X — browser-based top-scrolling space shooter |
| Live URL | https://kstanigar.github.io/Xenon_3/ |
| Repo | https://github.com/kstanigar/Xenon_3 |
| Local path | /Users/keithstanigar/Documents/Projects/Xenon_3/ |
| GA4 Property | NON-X (Account: NON-X Game) — ID: G-9ECFZ9JBE5 |
| Files | `index.html` (menu), `game.html` (desktop), `game_mobile.html` (mobile) |

### Game Structure
- 12 levels, 3 phases: **Green** (L1–4) → **Red** (L5–8) → **Purple** (L9–12)
- 3 bosses: spawn at `level >= 4/8/12` + `!bossXDefeated` — NO score threshold gate
- Power-ups: Health, Shield, Double Laser, Triple Laser, Quad Laser
- Win condition: defeat all 3 bosses → `player_won` fires

### Entity Type Taxonomy (Universal Naming Convention)
**CRITICAL:** Always use these exact terms when discussing positioning, spawning, or movement bugs. See Workflow Rule #9.

| Entity Type | Description | Spawn Function | Active Levels | Current Y Position |
|---|---|---|---|---|
| **Main Formation** | Slot rotation morphing formations (grid, diamond, V, circle) | `spawnMorphingFormation()` | 1-12 | 320 |
| **Barriers** | Non-shooting obstacles (circle, orbitingShield, horizontalLine, arrow, dualLines) | `spawnBarrier()` | 1,2,4,6,8,9,10,11,12 | 320 (circle/orbit), 468 (others) |
| **Legacy Formations** | Reserved enemy formations (spiral, pincer, sine wave) | `spawnSpiralFormation()`, `spawnPincerFormation()`, `spawnSineWaveFormation()` | Reserved for pink 13-15 | 320 (ready, dormant) |
| **Boss** | 3 main bosses (green, red, purple) + future pink boss | `spawnBoss()` | 4, 8, 12 (+ future 15) | 245 (settle point) |
| **Boss Minions** | Orbiting enemies around boss | `spawnBossMinion()` | During boss fights | Orbit around boss |
| **Kamikazes** | Enemies that dive at player | `spawnKamikaze()` | Various levels | 320 (center) |

**Key distinctions:**
- **Barriers** = obstacles that don't shoot
- **Spiral Formation** = legacy enemy formation (6 enemies in orbital pattern, shoots at player)
- **Main Formation** = current slot rotation system (levels 1-12)

### Entity Entry Timing Reference (Both Files)

**Formation Entry Mechanics:**
- Formation starts at y=-200 (off-screen above)
- Descends using lerp: `formationCurrentCenterY += (formationTargetCenterY - formationCurrentCenterY) * 0.045`
- Lands at y=320 (mobile) or y=300 (desktop)
- Entry time: **~2.3 seconds** (136 frames @ 60 FPS)

**Morph System:**
- Morph clock starts when `formationEntered = true` (formation lands)
- Morph interval: 2927ms (6 beats @ 123 BPM) = **~2.93 seconds**
- Morphs trigger at: morphCount === 1, 2, 3, etc.

**Timeline from Wave Start (CURRENT - After Barrier Timing Fix):**

| Time | Main Formation | Barriers | Kamikazes | Event |
|---|---|---|---|---|
| **t=0s** | Spawns, descending | — | — | `startWave()` called |
| **t=2.3s** | **Lands** | **Spawn, start descending** | — | `formationEntered = true` |
| **t=4-6.5s** | Static (exploded) | **Fully on-screen** | — | Barriers reach orbit/positions |
| **t=5.2s** | **Collapses** (first morph) | Active | — | `morphCount = 1` |
| **t=8.2s** | Morphing | Active | **Launch** | `morphCount = 2` |
| **t=11.1s** | Morphing | Active | Active | `morphCount = 3`, shield warning hides |

**Per-Level Barrier & Kamikaze Counts:**

| Level | Phase | Formation Count | Barrier Type | Barrier Count | Kamikaze Count |
|---|---|---|---|---|---|
| 1 | Green | 9 | circle | 5 | 2 |
| 2 | Green | 9 | horizontalLine | 5 | 2 |
| 3 | Green | 10 | horizontalLine | 5 | 2 |
| 4 | Green | 9 | arrow | 5 | 2 |
| 5 | Red | 16 | circle | 6 | 2 |
| 6 | Red | 11 | orbitingShield | 6 | 2 |
| 7 | Red | 10 | orbitingShield | 7 | 3 |
| 8 | Red | 10 | dualLines | 8 | 3 |
| 9 | Purple | 16 | orbitingShield | 8 | 3 |
| 10 | Purple | 17 | dualLines | 10 | 4 |
| 11 | Purple | 19 | circle | 8 | 4 |
| 12 | Purple | 22 | arrow | 8 | 5 |

✅ All levels now have barriers (added to levels 3, 5, 7 in Mar 2026 session 5)

---

## 1b. PLANNED FEATURES & ROADMAP

### P1 — High Priority (Next Sprint)

**1. Add Barriers to Levels 3, 5, 7** ✅ **COMPLETED (Mar 14, 2026 session 5)**
- Status: ✅ Implemented
- Implementation: Updated LEVEL_WAVES config in both game.html and game_mobile.html
- Barrier types added:
  - Level 3: horizontalLine (5 barriers) - Simple pattern for green phase
  - Level 5: circle (6 barriers) - Moderate challenge for red phase start
  - Level 7: orbitingShield (7 barriers) - Higher difficulty for mid-red phase
- Files modified: game.html (lines ~2420, 2432, 2444), game_mobile.html (lines ~2676, 2688, 2700)
- Result: All 12 levels now have barrier formations

**2. Horizontal Movement Bonus (1.5x Score Multiplier)**
- Purpose: Incentivize horizontal-only movement, create skill-based scoring tier
- Implementation:
  - Check `localStorage.nonx_movement_preference === 'horizontal'`
  - Apply 1.5x multiplier to all score events (enemy kills, powerups, boss defeats)
  - Display indicator: "BONUS MODE: +50% Score" in UI during gameplay
  - Track in analytics: `score_multiplier` parameter (1.0 or 1.5)
- Analytics impact: New dimension `score_multiplier`, update `game_start` event
- Version bump: analytics_version 3.0 → 3.1 (gameplay mechanic change)

**3. Check Level 12 for Off-Screen Enemies**
- Action: Visual inspection + debug console logs
- Check: Main formation, barriers, boss minions, kamikazes
- Platform: Both desktop and mobile
- Report: Screenshot any off-screen entities with Y coordinates

**4. Increase Boss 2 & Boss 3 Difficulty**
- Current issue: Boss 2 kill rate 83%, Boss 3 kill rate 100% (too easy for late game)
- Target: Boss 2 ~70-75%, Boss 3 ~80-85%
- Implementation options (needs user decision):
  - Increase boss health (HP multiplier)
  - Increase bullet speed (faster projectiles)
  - Increase bullet frequency (more shots per volley)
  - Add more minions
  - Faster shield cycling (less vulnerable time)
  - Reduce shield vulnerability window
- Analytics impact: Boss kill rates should drop; track via `boss_defeated` / `boss_attempt` ratio

### P2 — Medium Priority (Future Sprint)

**5. Adaptive Difficulty Control System**
- Purpose: AI-controlled difficulty adjustment based on player performance
- Status: Design phase — needs architecture discussion
- Implementation approach (3 options):

  **Option A: Per-Level Difficulty Multipliers**
  ```javascript
  var DIFFICULTY_CONFIG = {
    enemyCount: 1.0,      // Multiplier for enemy spawn count
    bulletSpeed: 1.0,     // Multiplier for enemy bullet speed
    shieldStrength: 1.0,  // Multiplier for enemy shield hits
    playerDamage: 1.0,    // Multiplier for damage dealt to player
    healthDropRate: 1.0   // Multiplier for health powerup spawn chance
  };
  ```
  - AI adjusts multipliers each level based on player death rate, time to complete, health remaining
  - Values range: 0.7 (easier) to 1.3 (harder)
  - Stored in localStorage, persists across sessions

  **Option B: Phase-Based Difficulty Scaling**
  - Separate configs for green/red/purple phases
  - AI adjusts entire phase difficulty based on completion rate
  - Simpler than per-level, less granular

  **Option C: Real-Time Dynamic Adjustment**
  - AI monitors player health, deaths, time alive
  - Adjusts difficulty mid-level (reduce enemy spawns if player struggling)
  - Most complex, requires careful tuning to avoid feeling "fake"

- Analytics impact: New events `difficulty_adjusted` with parameters: `adjustment_type`, `old_value`, `new_value`, `trigger_reason`
- User testing phase: Manual adjustment first, observe analytics, then enable AI
- Version bump: analytics_version 3.1 → 3.2 (major mechanic change)

**6. Pink Levels — Infinite Mode (Separate HTML Page)**
- Purpose: Endless gameplay for skilled players, easter egg content
- Implementation:
  - New file: `game_pink.html` (separate page to reduce computing load on main game)
  - Structure: Levels 13-15 loop infinitely (13 → 14 → 15 → 13...)
  - No level notifications: Continuous play, no "Level 14" popup
  - Pink boss at level 15: Defeating boss loops back to level 13 (seamless)
  - Unlock condition: Defeat purple boss (level 12) in main game
  - Entry point: Victory screen shows "Continue to Pink Mode" button
  - Legacy formations active: Spiral, pincer, sine wave patterns
  - Difficulty: Hardest in game, bullet speed +40% over purple phase
  - Exit condition: Player death only (no victory screen, just leaderboard submit)

- Analytics impact:
  - New page: `game_pink.html` → new `page_location` value
  - New events: `pink_mode_entered`, `pink_loop_completed` (each time player defeats pink boss)
  - Track: `pink_loops_completed` (how many times player defeated pink boss)
  - Track: `pink_session_duration`, `pink_max_score`
  - Leaderboard: Separate pink mode leaderboard (top score in pink mode only)

- Files to create:
  - `game_pink.html` (clone game_mobile.html or game.html, modify wave loop logic)
  - Update `game.html` and `game_mobile.html` victory screens (add pink mode button)

---

## 1c. ANALYTICS IMPACT SUMMARY

### Version Bumps Required

| Feature | Version Change | Reason |
|---|---|---|
| Barriers added to L3, L5, L7 | 3.0 → 3.0 (no bump) | Difficulty tweak, not mechanic change |
| Horizontal movement bonus (1.5x score) | 3.0 → 3.1 | New scoring mechanic |
| Boss 2 & 3 difficulty increase | 3.1 → 3.1 (no bump) | Balance change, not mechanic change |
| Adaptive difficulty system | 3.1 → 3.2 | Major mechanic change (AI-controlled) |
| Pink mode infinite loop | 3.2 → 3.3 | New game mode, separate page |

### New Events Required

| Event Name | Trigger | Key Parameters | Version |
|---|---|---|---|
| `difficulty_adjusted` | AI changes difficulty mid-session | `adjustment_type`, `old_value`, `new_value`, `trigger_reason`, `level_number` | 3.2+ |
| `pink_mode_entered` | Player clicks "Continue to Pink Mode" on victory screen | `score`, `session_duration_seconds` | 3.3+ |
| `pink_loop_completed` | Player defeats pink boss, loops back to L13 | `loops_completed`, `score`, `session_duration_seconds` | 3.3+ |
| `pink_mode_death` | Player dies in pink mode | `loops_completed`, `level_reached`, `score`, `session_duration_seconds` | 3.3+ |

### New Custom Dimensions Required

| Parameter Name | Type | Source Events | Purpose |
|---|---|---|---|
| `score_multiplier` | Dimension (text) | All score-generating events | Track 1.0 (full movement) vs 1.5 (horizontal-only) |
| `adjustment_type` | Dimension (text) | `difficulty_adjusted` | What was adjusted (enemyCount, bulletSpeed, etc.) |
| `old_value` | Metric (number) | `difficulty_adjusted` | Value before adjustment |
| `new_value` | Metric (number) | `difficulty_adjusted` | Value after adjustment |
| `trigger_reason` | Dimension (text) | `difficulty_adjusted` | Why AI adjusted (high_death_rate, low_health, etc.) |
| `loops_completed` | Metric (number) | `pink_loop_completed`, `pink_mode_death` | How many times player defeated pink boss |

### Existing Events to Update

| Event | New Parameter | Purpose |
|---|---|---|
| `game_start` | `score_multiplier` | Track which scoring tier player is in |
| `wave_reached` | `score_multiplier` | Track scoring tier at each level |
| `player_death` | `score_multiplier` | See if horizontal-only players die more/less |
| `boss_defeated` | `score_multiplier` | Compare boss success rate by movement type |
| `player_won` | `score_multiplier` | Win rate comparison |

### Dashboard Updates Needed

**When horizontal movement bonus launches (v3.1):**
- Add score multiplier filter to all explorations
- Create new exploration: "Movement Type Comparison" (horizontal vs full)
  - Tab 1: Win rate by movement type
  - Tab 2: Avg score by movement type
  - Tab 3: Avg level reached by movement type
  - Tab 4: Death rate by level (separate lines for 1.0x and 1.5x)

**When adaptive difficulty launches (v3.2):**
- Create new exploration: "Difficulty Adjustments"
  - Tab 1: Frequency of adjustments by level
  - Tab 2: Most common adjustment types
  - Tab 3: Player retention before/after adjustment
  - Tab 4: Avg session duration with/without adjustments

**When pink mode launches (v3.3):**
- Create new exploration: "Pink Mode Performance"
  - Tab 1: Entry rate (% of winners who enter pink mode)
  - Tab 2: Loop completion distribution (0 loops, 1 loop, 2 loops, etc.)
  - Tab 3: Avg session duration in pink mode
  - Tab 4: Top scores in pink mode
- Add pink mode filter to global explorations (exclude pink data from main game analysis)

### Data Quality Considerations

**Score Multiplier (v3.1):**
- Historical data (v3.0) has no multiplier → assume 1.0 for pre-v3.1 sessions
- Filter recommendation: `analytics_version = '3.1' OR analytics_version = '3.0'` when comparing score distributions (3.0 = baseline, 3.1 = with multiplier)

**Adaptive Difficulty (v3.2):**
- Pre-v3.2 sessions have static difficulty → not comparable to v3.2+
- Recommendation: Analyze v3.2+ separately, use v3.1 as baseline for "before AI difficulty"
- Risk: If AI makes game too easy, completion rate may spike (not a true skill improvement)

**Pink Mode (v3.3):**
- Completely separate game mode → ALWAYS filter by page_location
- Main game analysis: `page_location CONTAINS 'game.html' OR page_location CONTAINS 'game_mobile.html'` (exclude game_pink.html)
- Pink mode analysis: `page_location CONTAINS 'game_pink.html'` only

---

## 2. REPOSITORY & GIT WORKFLOW

- **Branches:** `main` (production) → feature branches → PR → merge. **Never use `develop`.**
- **CI/CD:** GitHub Actions integrity checks on every PR
- **Deploy:** GitHub Pages, auto-deploys from main, ~2–3 min after merge

### Commit message format
```bash
git commit -m "feat(mobile): short description here"
```

### Pre-commit check (always run)
```bash
python3 -c "
c = open('game_mobile.html').read()
print('Lines:', len(c.splitlines()))
print('Brace diff:', c[c.find('<script>'):].count('{') - c[c.find('<script>'):].count('}'))
print('draw function:', 'function draw(' in c)
"
```
- `game.html` → ~6647 lines, brace diff 0
- `game_mobile.html` → ~7512 lines, brace diff 0, draw function present

### CI required functions (both files)
**Core functions (original):**
`startFromCard`, `playAgain`, `showSurveyBanner`, `collapseSurveyBanner`, `submitSurvey`, `dismissSurvey`, `playerTakeDamage`, `shouldShowSurvey`, `buildBugButtonHTML`, `openBugReport`, `submitBugReport`, `fireEvent`, `if (playerBlinking) return`, `game_complete`, `'outcome': 'victory'`, `'outcome': 'death'`, `'outcome': 'abandoned'`, `bug_report_submitted`

**Added Mar 2026 session 5:**
`generateUUID`, `getPlayerId`, `PLAYER_ID`, `updateMorphingFormation`, `spawnMorphingFormation`, `formationEnteredTime`, `spawnBarrier`, `updateBarriers`, `shieldFlashFrames`, `shieldWobble`

**Total checks:** 27 required functions + 10 new checks = 37 checks per file

**Banned patterns (both files):** `buildSurveyHTML`, `'phase'.*'standard'`

---

## 3. ACTIVE A/B TESTS

| Test | Group A | Group B | Primary Metrics |
|---|---|---|---|
| Music default | Music ON (50%) | Music OFF (50%) | Win rate, replay rate, session duration |
| Movement scheme | Horizontal only | Full movement (player choice) | Avg level reached, session duration |

- `ab_music_group` stored in `localStorage.nonx_ab_music_group` — assigned once, never reassigned
- Movement is **player preference** as of v3.0 (was random A/B in v2.0 — discard that data)

---

## 4. ANALYTICS INFRASTRUCTURE

### Event wrappers
| File | Function | Behaviour |
|---|---|---|
| `game.html` | `fireEvent(eventName, params)` | Injects `analytics_version: '3.0'` via Object.assign. Dev mode (Shift+D) suppresses to console. |
| `game_mobile.html` | `fireEvent(eventName, params)` | Identical to game.html |
| `index.html` | `trackEvent(name, data)` | Same injection. Also gates on user consent — suppresses all events if `nonex_analytics = 'off'`, except `analytics_toggled` which always fires. |

### analytics_version history
| Version | Status | Notes |
|---|---|---|
| (none) | ❌ Discard | Pre-analytics / QA |
| 2.0 | ❌ Discard | Broken boss spawn, indestructible mobile minions, untuned hitbox, random movement A/B |
| 3.0 | ✅ Use | Current. Boss fix, hitbox inset, minion fix, movement as player preference. |
| 3.0+ | ✅ Use | Full instrumentation — all events carry version via wrapper. Deploy date: ~Mar 10 2026. Use `date ≥ Mar 10 2026` filter when full event-level coverage required. |

**Instrumentation patches (no version bump — use deploy date to filter):**
| Patch | Date | Change |
|---|---|---|
| v3.0.1 | Mar 12, 2026 | `index.html`: platform value normalised `'computer'` → `'desktop'`. Desktop sessions before this date recorded as `'computer'` in GA4. When analysing platform data, either filter `date ≥ Mar 12 2026` or union `platform = 'desktop' OR platform = 'computer'` for full desktop picture. |

**Convention:** Bump version number for gameplay mechanic changes only. Use deploy date for instrumentation changes.

### All events (game.html + game_mobile.html — 26 each)
| Event | Key Parameters | Notes |
|---|---|---|
| `session_start` | ab_music_group, platform, music_variant | Fires on every page load |
| `first_visit` | ab_music_group, platform, music_variant | Once per browser |
| `returning_user` | ab_music_group, platform, visit_count | |
| `game_start` | ab_music_group, movement_group, is_replay, games_played | |
| `wave_reached` | level_number, phase, score | Start of each level |
| `boss_attempt` | boss_id, level_reached, score, session_duration_seconds | |
| `boss_defeated` | boss_id, level_reached, score, session_duration_seconds | |
| `player_death` | level_reached, phase, score, session_duration_seconds | |
| `player_won` | score, session_duration_seconds | All 3 bosses defeated |
| `game_complete` | outcome (victory/death/abandoned), level_reached, score, session_duration_seconds | Fires on every session end |
| `powerup_collected` | powerup_type, level_reached, score | |
| `play_again` | score, level_reached, death_phase, replay_tier, bonus_hp, continue | Both files fully ported as of Mar 13. |
| `leave_game` | outcome, score, level_reached | |
| `leaderboard_submit` | score, rank | |
| `bug_report_submitted` | — | |
| `survey_submitted` | — | |
| `survey_dismissed` | — | |
| `music_toggled` | music_variant, score, level_reached | |

### Events (index.html — 7 total)
`menu_view`, `play_clicked`, `platform_selected`, `music_toggled`, `movement_toggled`, `analytics_toggled`

---

## 5. GA4 CUSTOM DIMENSIONS

Register in: GA4 Admin → Property → Custom Definitions → Custom Dimensions

| Parameter | Status | Notes |
|---|---|---|
| `platform` | ✅ Registered | ✅ Fixed Mar 12: 'computer' → 'desktop' in index.html v3.0.1. Historical data pre-deploy still shows 'computer' — filter by date when comparing platform metrics. |
| `level_number` | ✅ Registered | |
| `level_reached` | ✅ Registered | |
| `boss_id` | ✅ Registered | |
| `phase` | ✅ Registered | |
| `outcome` | ✅ Registered | victory / death / abandoned |
| `music_variant` | ✅ Registered | |
| `ab_music_group` | ✅ Registered | |
| `powerup_type` | ✅ Registered | |
| `analytics_version` | ✅ Registered | |
| `rank` | ✅ Registered | |
| `score` | ✅ Registered (metric) | |
| `session_duration_seconds` | ✅ Registered (metric) | |
| `death_phase` | ✅ Registered | Replay system — both files |
| `replay_tier` | ✅ Registered | Replay system — both files |
| `bonus_hp` | ✅ Registered | Replay system — both files |
| `continue` | ✅ Registered | Replay system — both files |

---

## 6. GA4 EXPLORATIONS BUILT

### 1. NON-X Completion Funnel (Funnel exploration)
10 steps: Session Start → Game Start → Level 1 → Level 4 → Boss 1 Attempt → Level 8 → Boss 2 Attempt → Level 12 → Boss Attempt 3 → Player Won
✅ Step 10 confirmed as `player_won` — 6 users (12.24%) as of Mar 12, 2026

### 2. NON-X Game Analytics (Free form, 6 tabs)
- Tab 1: Death Drop-off — ROWS: Level Number | COLUMNS: Platform | FILTER: player_death
- Tab 2: Boss Kill Rate — ROWS: Event name + Boss ID (nested) | FILTER: event contains boss
- Tab 3: Platform Comparison — ROWS: Platform | COLUMNS: Event name
- Tab 4: Music Impact — ROWS: Event name | COLUMNS: Music Variant | FILTER: game_complete
- Tab 5: Session Duration — ROWS: Platform | VALUES: Session duration
- Tab 6: Power-up Usage — ROWS: Powerup Type | FILTER: powerup_collected
- **Level Attempts tab** — ROWS: Level Number | VALUES: Event count | FILTER: event_name = wave_reached + analytics_version = 3.0 → exports `level_number, event_count` CSV used for death rate % in dashboard

### 3. NON-X Replay Funnel (Funnel exploration)
game_start → player_death → play_again → game_start | Breakdown: Replay Tier | Filter: is_replay = true

### 4. NON-X Replay Incentive Breakdown (Free form, 4 tabs)
Tier Uptake / Continue vs Play Again / Bonus HP vs Level Reached / Death Phase Distribution

### 5. NON-X Phase Retention (Free form)
ROWS Death Phase | COLUMNS Is Replay | FILTER player_death

---

## 7. QA DATA BASELINE (Feb 10 – Mar 9, 2026)

> ⚠️ **This dataset is QA/self-testing only.** ~38 "unique users" were primarily the developer testing across incognito sessions and cache clears. Do NOT calibrate benchmarks or draw product conclusions from this data. Use for pipeline validation only.
> **Real player baseline: Mar 10, 2026 onward.**

| Metric | Value | Assessment |
|---|---|---|
| Total Sessions | 136 | ⚠️ QA sessions |
| Total Unique Users | 38 | ⚠️ Developer cache clears |
| Sessions per User | 3.58 | ⚠️ Not a replay signal |
| Engagement Rate | 79.41% | ⚠️ Developer knows the game |
| Avg Session Time | 8:07 | ⚠️ Not representative of new players |
| Games Won (Looker) | 28 (with Last 28 days default) | ⚠️ Includes QA data — always filter to Mar 10+ for real player count |

### Completion funnel (pipeline validation only)
Session Start 38 → Game Start 28 (73.7%) → L1 22 (57.9%, -40.9%) → L4 13 (34.2%) → Boss 1 8 (21.1%) → L8 6 (15.8%) → Boss 2 6 (15.8%, -50%) → L12 3 (7.9%) → Boss 3 3 (7.9%) → Complete 3 (7.9%)

### Boss kill rate (developer skill — not new player benchmark)
Boss 1: 46/63 = 73% | Boss 2: 23/26 = 88.5% | Boss 3: 19/19 = 100%

---

## 7b. REAL PLAYER BASELINE (Mar 10 – Mar 12, 2026)

> ✅ **This is the first real player dataset.** 49 sessions from organic users. Small sample — do not over-index on individual metrics, but use for directional signals and pipeline validation. Benchmarks will sharpen as data accumulates.

### Completion funnel (49 session starts)
| Step | Users | % of Start | Drop |
|---|---|---|---|
| Session Start | 49 | 100% | — |
| Game Start | 37 | 75.5% | 🔴 -24.5% (menu bounce — biggest single drop) |
| Level 1 | 31 | 63.3% | -12.2% |
| Level 4 | 22 | 44.9% | -18.4% |
| Boss 1 Attempt | 17 | 34.7% | -10.2% |
| Level 8 | 15 | 30.6% | -4.1% |
| Boss 2 Attempt | 15 | 30.6% | 0% |
| Level 12 | 9 | 18.4% | -12.2% |
| Boss 3 Attempt | 6 | 12.2% | -6.1% |
| Player Won | 6 | 12.2% | 0% |

### Deaths by level (133 total)
L1=0, L2=34, L3=8, L4=45, L5=12, L6=11, L7=0, L8=9, L9=2, L10=5, L11=2, L12=5
- **L4 is the death hotspot** (45 deaths) — Boss 1 gate, not a pure level difficulty issue
- **L2 spike** (34 deaths) warrants investigation — specific enemy pattern?
- **L7 zero deaths** — only level in red phase with none; players who reach it have learned red phase patterns
- **Mobile = 81% of all deaths** (108 of 133)

### Boss kill rates (real data — healthy)
| Boss | Attempts | Defeats | Kill Rate | Assessment |
|---|---|---|---|---|
| Boss 1 | 99 | 77 | 77.8% | ✅ Healthy difficulty |
| Boss 2 | 47 | 39 | 83% | ✅ Strong pass rate |
| Boss 3 | 25 | 25 | 100% | ✅ Survivorship reward — only skilled players reach here |

### Key insights
1. **Menu bounce is #1 problem** — 24.5% drop Session Start → Game Start, larger than any in-game drop
2. **Boss difficulty is healthy** — 77.8% / 83% / 100% kill rates; not a balance problem
3. **Mobile dominates deaths** — platform gap is significant; mobile controls are the friction point
4. **Boss 3 100% kill rate** — not an anomaly, it's survivorship; only committed players reach L12

---

## 8. ACTIVE ISSUES

### ✅ Resolved
| ID | Issue | Resolution |
|---|---|---|
| F1 | Platform values fragmented (`computer`, `desktop`, `mobile`, `not_set`) | ✅ Fixed Mar 12 — `computer` → `desktop` in index.html v3.0.1. Historical sessions pre-deploy still show `computer`. |
| F2 | "Games Won" Looker scorecard showing 28/139 | ✅ Fixed Mar 12 — not a formula bug. Root cause: default "Last 28 days" date range included QA data (Feb 10–Mar 9). Fix: set Looker date range to Mar 10, 2026 → today → shows 6 (correct). |
| F3 | Funnel step 10 uses `game_complete` not `player_won` | ✅ Non-issue Mar 12 — GA4 Explore funnel step 10 already reads `player_won` (6 users, 12.24%). No change needed. |
| F4 | 4 custom dimensions unregistered: `death_phase`, `replay_tier`, `bonus_hp`, `continue` | ✅ Fixed Mar 2 — all registered in GA4 Admin. |
| F5 | Mobile L4 V-formation: 2 enemies appearing after formation stops | ✅ Fixed Mar 13 — `flyingVExploded` spacing reduced from 0.5 → 0.34 in `game_mobile.html`. See Section 9 for details. |
| F6 | Purple phase replay button showing "+25 HP" instead of "+50 HP" | ✅ Fixed Mar 13 — root cause: `redPhase` flag stays `true` through purple phase, so `redPhase` check fired before `purplePhase` check. Fixed in both files by switching button logic to use `deathPhase` string. Combined with replay incentive simplification (see Section 9). |
| F7 | Desktop replay incentive system not ported | ✅ Fixed Mar 13 — full tier system ported to `game.html`, matching mobile. Both files now use identical simplified logic. |
| F8 | Mobile spiral formation partially off-screen | ✅ Fixed Mar 14 (session 4) — `spawnSpiralFormation` `targetY` raised from 150 → 320 to align with main formations and barriers. |
| F9 | Desktop formation snaps/jumps to collapsed position at first morph | ✅ Fixed Mar 13 (session 2) — `morphStartTime` and `lastMorphTime` now reset inside `formationEntered = true` block, matching existing mobile behaviour. See Section 9 Fix 4. |
| F10 | Mobile barriers off-screen (levels 1, 6, 9, 11) | ✅ Fixed Mar 14 (session 4) — Barrier orbit center moved from y=160 → y=320. Affects circle and orbitingShield barrier types only. See Version History for full details. |

### 🟡 Watch / Improve
| ID | Issue | Notes |
|---|---|---|
| I1 | Menu bounce — 24.5% of sessions never start a game | 🔴 Now confirmed as #1 drop with real data (37/49 sessions). Cross-ref `menu_view` referrer to identify traffic source. |
| I2 | L2 death spike — 34 deaths vs 8 at L3 | Unexpected. Investigate specific enemy pattern at L2. |
| I3 | Mobile = 81% of all deaths | Platform gap confirmed with real data. Mobile controls are the friction point. |
| I5 | Boss 2 funnel (50%) vs kill rate (83%) contradiction | Frustration accumulation, not first-attempt wall. Watch as data grows. |

---

## 9. GAMEPLAY CHANGES (Mar 13, 2026)

### Fix 1 — Mobile L4 V-formation pop-in (`game_mobile.html` only)
**Problem:** In `flyingVExploded`, the outermost arm enemies (index 4 and 8) had natural X positions of -65px and 495px on the 480px-wide mobile canvas — fully off-screen during the entire descent. When the formation stopped and X-clamping activated, they snapped visibly to the screen edges, appearing to "pop in." Player saw 7 enemies enter, 2 appear suddenly.

**Fix:** Reduced `flyingVExploded` spacing from `0.5` → `0.34`. Value 0.34 is the maximum that keeps all 9 enemies within the existing 20px canvas margin (outermost enemies land at x≈25 and x≈405). The collapsed `flyingV` shape retains its original spacing of `0.25`.

**To revert:** Change `var spacing = 0.34` back to `var spacing = 0.5` in `flyingVExploded`. Comment marker: `BUG FIX (Mar 2026)`.

**Analytics impact:** None — no events or parameters affected.

---

### Fix 2 — Replay incentive simplification (both files)
**Problem (display):** Button display logic used `redPhase` / `purplePhase` boolean flags. Since `redPhase` is set to `true` at Boss 1 defeat and **never reset during gameplay**, it remains `true` through all of purple phase. The if/else chain checked `redPhase` before `purplePhase`, so purple deaths always showed "+25 HP" instead of "+50 HP". The HP was actually being applied correctly (+50) via `deathPhase` — only the label was wrong.

**Problem (design):** The `!isReplaySession` gate meant first-time deaths in red or purple phase only received +15 HP, regardless of how far the player had progressed. This worked against the retention goal of the incentive system.

**Fix:** Simplified to universal phase-based rules in all 10 affected locations (3 button display blocks + 1 HP application block + 1 analytics block per file). Button display and HP application now both use `deathPhase` string (correctly set as `purplePhase ? 'purple' : redPhase ? 'red' : 'green'`).

**New rules (both files, all sessions):**
| Death phase | Button label | HP applied |
|---|---|---|
| Purple (L9–12) | Play Again (+50 HP) | +50 |
| Red (L5–8) | Play Again (+25 HP) | +25 |
| Green replay (L2–4) | Resume Level X (+15 HP) | +15 |
| Green (L1) | Play Again (+15 HP) | +15 |

**To revert:** Search `SIMPLIFIED (Mar 2026)` in either file — 5 marked locations per file. Restore `!isReplaySession` as first branch and `redPhase`/`purplePhase` flag checks per the revert instructions in each comment.

**Analytics impact:** `replay_tier` and `bonus_hp` values in `play_again` events now correctly reflect the simplified tiers. First-time red/purple deaths will now log tier 3/4 instead of tier 1. No version bump needed — this is a UX fix, not a mechanic change.

---

### Fix 3 — Mobile spiral formation off-screen (`game_mobile.html` only)
**Problem:** `spawnSpiralFormation()` hardcoded `targetY = 150` as both the descent target and orbit center Y (`spiralCenterY`). The orbit radius is 80px with a ±30% breathing pulse, meaning the top of the arc reached y ≈ 46px — clipping against the top edge of the canvas. Players saw the circle cut off.

**Fix:** Raised `targetY` from `150` → `220` in `spawnSpiralFormation()`. At 220 the full orbit sits between y ≈ 116 (top arc) and y ≈ 324 (bottom arc), fully visible with comfortable margins. `spiralCenterY` is derived from `targetY` so it moves automatically — one value to change.

**To revert:** Change `var targetY = 220` back to `var targetY = 150` in `spawnSpiralFormation()`. Comment marker: `ORBIT CENTER Y — BUG FIX (Mar 2026)`.

**Analytics impact:** None.

---

### Fix 4 — Desktop formation snaps to collapsed position at first morph (`game.html` only)
**Problem:** `morphStartTime` was set to `Date.now()` inside `startWave()` — 3.33 seconds before the formation finished entering the screen. The morph interval is only 2.93 seconds (6 beats at 123 BPM), so the first morph transition fired 407ms *before* the formation reached `formationTargetCenterY`. Enemies were still mid-descent when `updateMorphingFormation` triggered the first shape change — they snapped to the collapsed positions instead of transitioning smoothly from a held exploded state.

**Root cause was a missing fix mobile already had.** Mobile resets `morphStartTime = Date.now()` inside the `formationEntered = true` block so the dance only begins once the formation is fully on screen. Desktop was missing those two lines.

**Fix:** Added `morphStartTime = Date.now()` and `lastMorphTime = Date.now()` inside the `formationEntered = true` block in `game.html`. The existing `morphStartTime = Date.now()` in `startWave()` remains as an initial value — the new lines simply overwrite it at the correct moment. No gameplay change — the formation dances identically, it just waits until it has landed to start.

**To revert:** Delete the two added lines inside the `formationEntered = true` block in `game.html`. Comment marker: `MORPH CLOCK RESET — BUG FIX (Mar 2026)`.

**Analytics impact:** None.

---

### ⚠️ CRITICAL GAME MECHANIC: Formation Morphing + Slot Rotation System
**Status: ✅ IMPLEMENTED AND WORKING — DO NOT MODIFY WITHOUT EXTREME CARE**

This is the signature "drone-like" movement that defines NON-X's visual identity. Two interlocking systems work together:

#### **System 1: Shape Morphing**
Formations cycle through different geometric shapes every ~2.93 seconds (6 beats at 123 BPM):
- **Shapes:** grid3x3 → diamond → grid3x3 → diamond (loops)
- **Each shape has two states:** collapsed (tight) and exploded (spread out)
- **Timing:** Controlled by `formationEnteredTime` (NOT `morphStartTime` — see Fix 5 below)
- **Interpolation:** Uses `easeInOutCubic()` for smooth 1-second transitions between shapes

#### **System 2: Slot Rotation (Carousel)**
On each morph, enemies cycle to the next position in the formation:
- **Implementation:** `var rotatedIndex = (idx + morphCount) % newPositions.length;`
- **Effect:** Enemy at slot 0 moves to slot 1, slot 1 → slot 2, etc. (carousel)
- **Visual result:** Enemies appear to "orbit" through the formation while it morphs
- **Location:** `updateMorphingFormation()` — lines ~2954 (game.html), ~3188 (game_mobile.html)

#### **Why These Systems Are Fragile**

**⚠️ CRITICAL TIMING DEPENDENCY:**
- `formationEnteredTime` MUST be set EXACTLY ONCE when `formationEntered = true`
- Morph clock starts at 0 when formation lands, preventing snap from exploded → collapsed
- Resetting `formationEnteredTime` mid-wave breaks morph progression (shapes stop cycling)
- `morphCount` increments each shape change — drives slot rotation

**⚠️ CRITICAL POSITION DEPENDENCY:**
- Slot rotation relies on modulo arithmetic: `(idx + morphCount) % newPositions.length`
- Changing position assignment logic breaks carousel effect
- Enemy positions interpolated using `startPos`, `targetPos`, `currentPos` (do not modify)

#### **Debug Console Logging**
Both files include debug logs for troubleshooting (currently active):
- **Morph state:** Logs every 1 second — `timeSinceStart`, `newShapeIndex`, `currentMorphShape`
- **Shape changes:** Logs when morph fires — new shape name + first 3 enemies' target positions
- **Enemy positions:** Logs every 1 second — first 3 enemies' `currentPos` + screen coordinates

**To use debug logs:**
1. Open browser console
2. Start a level
3. Watch for `Morph check:`, `Shape changed to`, and `Enemy positions:` logs
4. Verify `timeSinceStart` increases steadily, `newShapeIndex` increments every ~2927ms
5. Verify `targetPos` values change each morph (confirms slot rotation)
6. Verify `screenXY` values transition smoothly (confirms interpolation)

**Debug logs are dev-mode only** — wrapped in `localStorage.getItem('nonx_dev_mode') === 'true'` conditionals (Mar 2026 session 5). Zero performance impact in production. Enable with Shift+D in-game.

---

### Fix 5 — Formation Entry Snap Bug (Mar 13, session 3) — BOTH FILES
**Problem:** Formations jumped from exploded (entry) state to collapsed state immediately upon landing. The morph timer (`morphStartTime`) was set in `startWave()` — 3.33 seconds before the formation finished entering the screen. Since morph interval is 2.93 seconds, by the time formations landed, `newShapeIndex` was already 1, triggering an instant morph to the collapsed state.

**Fix:** Track formation entry time separately from wave start time.
- **Added:** `var formationEnteredTime = 0;` global variable
- **Reset in `startWave()`:** `formationEnteredTime = 0;` (not entered yet)
- **Set when landing:** `formationEnteredTime = Date.now();` inside `formationEntered = true` block (only once)
- **Updated timing:** `timeSinceStart = formationEnteredTime > 0 ? (time - formationEnteredTime) : 0;`

**Result:** Morph clock doesn't start until formation lands. First morph happens ~2.93 seconds AFTER landing (smooth). Slot rotation preserved (still uses `morphCount` which increments normally).

**To revert:** Change `time - formationEnteredTime` back to `time - morphStartTime` in `updateMorphingFormation()`. Remove `formationEnteredTime` variable and initialization code.

**Analytics impact:** None — visual fix only.

**Code locations:**
- game.html: Lines ~1998 (variable), ~2497 (reset), ~6242 (set), ~2874 (timing calc)
- game_mobile.html: Lines ~2248 (variable), ~2778 (reset), ~7051 (set), ~3113 (timing calc)

---

### ⚠️ Formation Rotation (Angular Spin) — NOT IMPLEMENTED
**Note:** This is DIFFERENT from slot rotation (carousel). Formation rotation would spin the entire formation like a pinwheel while it morphs and carousels.

**Background:** `formationRotation` and `targetFormationRotation` variables exist in both files but are **dead variables** — never applied to position calculations. The current system has NO angular rotation, only slot rotation (carousel).

**If ever implementing angular rotation:**
- Apply 2D rotation matrix to normalized positions before scaling by `spreadRadius`
- Must preserve slot rotation (carousel) — rotation is additive, not replacement
- Test extensively — two simultaneous rotation systems (angular + carousel) may be visually confusing

**Current status:** Not needed. Slot rotation (carousel) alone creates sufficient visual interest.

---

## 10. MOBILE-SPECIFIC FEATURES

### Difficulty tuning (affects analytics comparisons)
| Phase | Desktop bullet × | Mobile bullet × |
|---|---|---|
| Green | 1.0 | 1.0 |
| Red | 1.40 | 1.15 |
| Purple | 1.65 | 1.35 |

`arrowheadExploded` explode multiplier: 1.6 mobile (vs 2.4 desktop)

Enemy counts per level:
- Green L1–4: 9, 9, 10, 9
- Red L5–8: 14, 11, 10, 10
- Purple L9–12: 16, 17, 19, 22

### Replay Incentive System (both files as of Mar 13)
**CRITICAL timing:** `isReplay` resets immediately after `game_start` fires. `isReplaySession` must be captured from `isReplay` BEFORE that reset. Without it, green-phase resume (Tier 2) never fires.

**Simplified tier rules (Mar 13):**
| Tier | Condition | HP Bonus | Start |
|---|---|---|---|
| 1 | Green phase death, level 1 (any session) | +15 | Level 1 |
| 2 | Green phase death, levels 2–4 (replay only) | +15 | Death level |
| 3 | Red phase death, any session | +25 | Level 1 |
| 4 | Purple phase death, any session | +50 | Level 1 |

---

## 11. SENSITIVE CODE — DO NOT MODIFY WITHOUT FULL TRACE

### ⚠️ Leaderboard Submit (`buildLeaderboardSubmitHTML`)
- `submittedScore` MUST be captured BEFORE `addHighScore()` runs — timing bug caused a 2.5 hr regression
- Gate: `score > submittedScore` only — no other gates
- Called in 3 places per file: main death, `rebuildGameOverScreen`, dev mode death
- **NEVER delete the Firebase `leaderboard` collection** — archive instead

### ⚠️ Boss Spawn (`advanceLevel`)
- Triggers at `level >= 4/8/12` + `!bossXDefeated` — no score threshold
- `boss.shieldStartTime` resets when `boss.entering = false`

### ⚠️ Mobile Boss Minions (`updateBossMinions`)
- Must NOT be inserted into `SpatialGrid` — causes indestructible minions + infinite score ticks

### ⚠️ `isReplay` / `isReplaySession` timing
- `isReplaySession` must be captured from `isReplay` BEFORE `game_start` fires — see Tier system above

### ⚠️ `redPhase` flag behaviour
- `redPhase` is set to `true` when Boss 1 is defeated and **never reset to false during gameplay**
- It remains `true` through all of purple phase (`redPhase=true` AND `purplePhase=true` simultaneously at levels 9–12)
- Always use `deathPhase` string ('green'/'red'/'purple') for phase-conditional logic, NOT the boolean flags
- `deathPhase` is correctly set as `purplePhase ? 'purple' : redPhase ? 'red' : 'green'` at moment of death

---

## 12. DASHBOARD & TOOLING

### HTML Analytics Dashboard (`nonx-analytics-dashboard.html`)
- 6 tabs: Overview, Funnel, Boss Analysis, A/B Tests, Platform, Looker Guide
- CSV drag-and-drop loader — auto-detects report type, filters `analytics_version ≠ 3.0`
- Chip tracker shows which CSVs are loaded (FUNNEL / DEATHS / BOSS / ATTEMPTS / A/B MUSIC / PLATFORM / DEATHS MOBILE)
- Wave drop-off chart: all 12 levels + 3 boss bars always rendered (zero-death levels show faint placeholder bar)
- Boss bars computed live from boss CSV data — load order independent
- **Data loaded (as of Mar 12):** FUNNEL ✅ DEATHS ✅ BOSS ✅ ATTEMPTS ✅ | A/B MUSIC ⏳ PLATFORM ⏳ (pending platform fix propagation in GA4)
- Ctrl+S session persistence: planned, not yet built — re-drop CSVs each session

### CSV load order (each session)
1. Deaths — `Death_Dropoff.csv` (`level_reached` × platform pivot)
2. Boss — `boss_kill_rate.csv` (`event_name` + `boss_id` + `event_count`)
3. Funnel — `Funnel_Completion.csv` (GA4 funnel export)
4. Attempts — `Level_Attempts.csv` (`level_number` + `event_count`, filtered to `wave_reached`) — unlocks death rate % table and platform toggle on wave drop-off chart

### Wave drop-off platform toggle
ALL / MOBILE / DESKTOP toggle in the Wave Drop-off card header. Switches both bar chart and death rate table simultaneously. Guard: Mobile/Desktop buttons show a toast and stay on ALL if Deaths CSV not loaded. Death rate table label updates: ALL PLATFORMS / MOBILE ONLY / DESKTOP ONLY.

### Smart Signal System (planned — next major feature)
Two-layer design:

**Layer 1 — Contextual Benchmark Tooltips (on every chart)**
Hover any data point to see: metric + value / benchmark range / status / what it means / what to watch next week. No grades on charts. No badges. Context only.

Example tooltip:
```
Boss 2 Abandonment — 50%
────────────────────────────────────
Benchmark: 25–35% is healthy at this stage
Status: ⚠ Above threshold

What this means: Players are reaching Boss 2 but quitting
after multiple failed attempts — frustration wall, not a
skill cliff.

Watch: Does this improve as sample grows, or persist?
Cross-check with avg attempts/user.
```

**Layer 2 — Report Card Tab (dedicated weekly summary)**
Every metric as a table row: Value | Grade (A–F) | Δ Week (↑↓→~) | One-liner interpretation
Weighted overall grade at top with single priority callout.

Example rows:
```
Metric           | Value  | Grade | Δ Week  | One-liner
Win Rate         | 7.9%   |  C    | ↑ +1.7pp| Low but improving — watch L1 drop
L1 Abandonment   | 40.9%  |  D    | → stable| Biggest retention leak — priority fix
Boss 1 Kill Rate | 73.0%  |  A    | ↑ +4pp  | Healthy. Difficulty well-tuned.
Replay Rate      | 3.58x  |  B    | → stable| Strong. Music A/B test primary signal.
```

Grade scale: A = at/above target | B = acceptable | C = below target | D = needs attention | F = critical/anomaly
Delta: ↑ green = improving | ↓ red = worsening | → grey = stable | ~ yellow = anomaly

**Sample size guardrails:**
- n < 20 game_starts: suppress all grades — show "Insufficient data — Report Card activates at 20+ game starts"
- n 20–50: grades shown with "Low confidence" label, delta arrows suppressed
- n > 50: full Report Card active with deltas

**Persistence:** On each CSV load, previous DATA object saved as DATA_PREV embedded in HTML. Ctrl+S saves both DATA (current week) and DATA_PREV (last week) — file is self-archiving. Delta: relative = (current − prev) / prev × 100, absolute = current − prev. No localStorage, no server required.

⚠️ Do NOT calibrate grade thresholds until real organic user data accumulates (post Mar 24, 2026)

### Benchmark Reference (to calibrate with real data)
| Metric | Healthy range | Grade A |
|---|---|---|
| Win rate | 10–20% | >15% |
| L1 abandonment | <25% | <20% |
| Boss 1 kill rate | 65–80% | 70%+ |
| Boss 2 kill rate | 70–85% | 75%+ |
| Boss 3 kill rate | 75–90% | 80%+ |
| Menu → game start | >80% | >85% |
| Avg session duration | >5 min | >8 min |
| Replay rate | >2.5x | >3.5x |
| Leaderboard submit | >10% | >15% |

### Looker Studio
- Real-time ops and portfolio sharing
- Apply `analytics_version = 3.0` as report-level filter first
- Theme: `#0D1B2A` bg, `#00B4C8` cyan, `#CC00CC` magenta, Space Mono + Exo 2 fonts

⚠️ **Date range warning:** Default "Last 28 days" includes QA data (Feb 10–Mar 9) until ~Mar 24, 2026 when it fully rolls out of the window. Always set date range manually to **Mar 10, 2026 → today** for clean organic-only numbers. After Mar 24, the default is safe to use.

### Documents produced
- `NON-X_Analytics_Export_Guide.docx` — full GA4 + Looker Studio setup guide
- `nonx-analytics-dashboard.html` — interactive 6-tab dashboard with CSV loader

---

## 13. WORKFLOW RULES

1. **Data-first:** Confirm capture before building any visual. Audit: Good / Improve / Fix.
2. **Every metric gets a G/I/F audit** before being added to the dashboard.
3. **Share updated files after each commit** — AI applies fixes to the new version.
4. **Dashboard:** Weekly GA4 CSV → drag-and-drop → Ctrl+S.
5. **Looker = real-time ops. HTML dashboard = polished weekly + portfolio.**
6. **Data sharing:** Screenshots + CSV exports (no direct GA4/Looker access possible).
7. **Claude rule:** Never recommend destructive operations without full dependency trace.
8. **Claude rule:** Never diagnose game over bugs without asking level + score + context first.
9. **Claude rule:** When fixing positioning bugs, ALWAYS clarify which enemy/entity type needs adjustment:
   - **Main Formation** (slot rotation formations: grid, diamond, V, circle) - levels 1-12, targetY in `spawnMorphingFormation()`
   - **Barriers** (circle, orbitingShield, horizontalLine, arrow, dualLines) - separate positioning per type
   - **Legacy Formations** (spiral, pincer, sine wave) - reserved for pink levels, separate positioning
   - **Boss/Kamikazes/Boss Minions** - separate positioning systems
   - Do NOT assume "formation" means main formation - verify which entity type from screenshots/context
10. **Claude rule:** Investigate and report findings before making any code changes.
11. **Practice runs:** QA data is valid for workflow practice — builds readiness for real data launch.
12. **🚨 CRITICAL — Formation mechanics:** The morphing + slot rotation system is NON-X's signature visual identity. When adjusting enemy positioning, timing, or movement:
    - **READ Section 9 (Formation Morphing + Slot Rotation System) FIRST** — understand both systems before ANY changes
    - **CHECK debug console logs** — verify `timeSinceStart`, `newShapeIndex`, `morphCount`, and `targetPos` values
    - **REPORT to user BEFORE implementing** — explain how changes will interact with morphing/carousel
    - **TEST thoroughly** — formations must morph smoothly, enemies must carousel through slots
    - **NEVER reset `formationEnteredTime` mid-wave** — breaks morph progression
    - **NEVER modify slot assignment without preserving `(idx + morphCount) % length` pattern** — breaks carousel

---

## 14. KNOWN HISTORY & POST-MORTEMS

### Leaderboard Submission Bug (~2.5 hrs lost, March 2026)
Deleting Firebase collection → submit form stopped appearing. Root cause: `addHighScore(score)` ran before `buildLeaderboardSubmitHTML()`. Fix: capture `submittedScore` before `addHighScore()` runs. Claude incorrectly diagnosed the `level >= 2` gate and made 3 bad fixes in a row.

### Mobile Fixes (all resolved)
Missing `playAgain`, broken shield block, truncated file, quote syntax error, missing survey/blink functions — all fixed. `buildSurveyHTML` replaced with slide-down banner — now banned in CI.

### Barrier Positioning Bug (~30 min confusion, March 14, 2026)
User reported enemies off-screen in levels 1, 6, 9 (screenshots). Claude initially misidentified as main formation positioning issue and attempted to adjust `targetY` in `spawnMorphingFormation()` multiple times. User clarified the highlighted enemies were **barriers** (circular/orbiting obstacles), NOT main formation enemies. Root cause: Barrier orbit center at y=160 was too high. Fix: moved to y=320. **Lesson:** Always clarify which enemy/entity type (main formation vs barriers vs legacy formations) before adjusting positioning - added as Workflow Rule #9.

### Purple Replay Button Bug (Mar 13, 2026)
Button showed "+25 HP" for purple deaths because `redPhase` stays `true` through purple phase and was checked before `purplePhase` in the if/else chain. HP application was actually correct all along (used `deathPhase` string). Display-only bug. Fixed by switching all button logic to use `deathPhase`. Combined with replay incentive simplification.

### Version History
- v2.0 → v3.0: Boss spawn fix, hitbox inset, mobile minion fix, movement as player preference
- v3.0 full instrumentation: Mar 10 2026 — `analytics_version` injected on all events via wrapper
- v3.0.1 instrumentation patch: Mar 12 2026 — `index.html` platform dimension `'computer'` → `'desktop'`
- Mar 13 2026 — gameplay fixes: L4 V-formation pop-in (mobile), replay incentive simplification + purple button bug (both files)
- Mar 13 2026 (session 2) — formation fixes: spiral orbit center Y 150→220 (mobile), morph clock reset at formationEntered (desktop)
- Mar 13 2026 (session 3) — formation morphing + slot rotation system: fixed entry snap bug (both files), added `formationEnteredTime` tracking, comprehensive documentation
- Mar 14 2026 (session 4) — mobile barrier positioning fix: circular/orbiting barriers moved from y=160 → y=320, spiral formation aligned to y=320
- Mar 14 2026 (session 5) — barrier spawn timing fix: barriers now spawn at formation landing (t=2.3s) instead of first morph (t=5.2s), reducing action lull from 7-9s to 2.3s (both files)
- Mar 14 2026 (session 5) — added barriers to levels 3, 5, 7: horizontalLine (L3, 5 count), circle (L5, 6 count), orbitingShield (L7, 7 count) — all 12 levels now have barriers (both files)
- Mar 14 2026 (session 5) — updated CI integrity checks: added 10 new function checks (Player ID system, formation morphing, barriers, shield feedback) — total 37 checks per file
- Mar 14 2026 (session 5) — wrapped all debug console.log in dev mode conditionals: zero performance impact in production, enable with Shift+D (both files)

### Debug Logging Performance Fix (Mar 14, 2026 session 5) — Both Files
**Problem:** Debug console.log statements (3 groups per file) running every 1-3 seconds added ~0.5-1ms overhead per second on mobile devices, even with dev tools closed. Over 5-minute sessions, this meant 300-600 unnecessary function calls.

**Fix:** Wrapped all debug logging in dev mode conditionals:
```javascript
if (localStorage.getItem('nonx_dev_mode') === 'true') {
  console.log(...); // Only runs when dev mode active
}
```

**Affected debug logs (both files):**
- Morph state check (every 1 second)
- Shape change logging (every 2.93 seconds)
- Enemy position tracking (every 1 second)

**Result:**
- Production: Zero performance impact, zero console.log calls
- Dev mode (Shift+D): Full debug logging available for troubleshooting

**Code locations:**
- game_mobile.html: Lines ~3212, ~3263, ~3283, ~3330
- game.html: Lines ~2975, ~3028, ~3049, ~3092

---

### CI/CD Integrity Check Update (Mar 14, 2026 session 5)
**Purpose:** Ensure critical new functions added in recent sessions are validated in CI pipeline.

**New checks added (10 total):**
- **Player ID System:** `generateUUID`, `getPlayerId`, `PLAYER_ID` (leaderboard security)
- **Formation Morphing:** `updateMorphingFormation`, `spawnMorphingFormation`, `formationEnteredTime` (signature mechanic)
- **Barrier System:** `spawnBarrier`, `updateBarriers` (all 12 levels use barriers)
- **Shield Visual Feedback:** `shieldFlashFrames`, `shieldWobble` (player feedback)

**File:** `.github/workflows/integrity-check.yml`

**Result:** CI now validates 37 required functions per file (was 27), ensuring recent features are tested on every PR.

---

### Barrier Addition to Levels 3, 5, 7 (Mar 14, 2026 session 5) — Both Files
**Purpose:** Complete barrier coverage across all 12 levels for consistent difficulty progression.

**Barriers added:**
- **Level 3** (Green): `horizontalLine`, 5 barriers - Simple side-to-side movement pattern
- **Level 5** (Red): `circle`, 6 barriers - Circular orbit pattern for red phase start
- **Level 7** (Red): `orbitingShield`, 7 barriers - Faster orbit for increased mid-red challenge

**Implementation:** Updated `LEVEL_WAVES` configuration in both files
- game.html: Lines 2420, 2432, 2444
- game_mobile.html: Lines 2676, 2688, 2700
- Total change: 6 lines (2 per level - barrier type + count)

**Result:** All 12 levels now have barrier formations. No more barrier-less levels.

**Analytics impact:** None - no version bump needed (difficulty balance tweak, not mechanic change).

---

### Barrier Spawn Timing Fix (Mar 14, 2026 session 5) — Both Files
**Problem:** Wave start pacing had a 7-9 second lull where nothing happened. Formation descended (2.3s), then sat static in exploded state (2.9s), then morphed and barriers spawned (t=5.2s), then barriers descended (1.8-4.2s more) before being fully on-screen. Players were just watching for 7-9 seconds before meaningful action started.

**Root cause:** Barrier spawn was triggered at first morph (`morphCount === 1`) which happens 2.93 seconds after formation lands. This delayed barrier entry unnecessarily.

**Fix:** Moved barrier spawn trigger from `morphCount === 1` to `formationEntered = true` block.
- Barriers now spawn immediately when formation lands (t=2.3s from wave start)
- Barriers still descend smoothly from off-screen (1.8-4.2s depending on type)
- Player sees continuous action (barriers descending) during formation's static phase
- Total lull reduced: 7-9 seconds → 2.3 seconds (68-74% reduction)

**Timeline comparison:**
| Event | Before | After | Change |
|---|---|---|---|
| Formation lands | t=2.3s | t=2.3s | No change |
| Barriers spawn | t=5.2s | t=2.3s | -2.9s (spawn immediately) |
| Barriers on-screen | t=7-9s | t=4-6.5s | -3s (visible earlier) |
| Kamikazes launch | t=8.2s | t=8.2s | No change |

**Code locations:**
- game.html: Line ~6310 (barrier spawn added to formationEntered block), Line ~2999 (old morphCount trigger removed)
- game_mobile.html: Line ~7127 (barrier spawn added to formationEntered block), Line ~3235 (old morphCount trigger removed)

**To revert:** Move barrier spawn code from `formationEntered = true` block back to `morphCount === 1` conditional. See comment markers in both files.

**Analytics impact:** None — no events or timing changes, just visual pacing improvement.

---

### Barrier Orbit Positioning Fix (Mar 14, 2026 session 4) — Mobile Only
**Problem:** Circular and orbiting shield barriers (levels 1, 6, 9, 11) were positioned too high on screen. Orbit center at y=160 with vertical radius 108px caused top of orbit to reach y≈27px, clipping barriers off-screen at the top edge. User screenshots showed 2-4 barriers clearly above visible area.

**Root cause confusion:** Initially misidentified as main formation positioning issue. After clarification, identified as separate barrier orbit positioning bug affecting only `'circle'` and `'orbitingShield'` barrier types.

**Fix:** Moved barrier orbit center from y=160 → y=320 in `spawnBarrier()` function (game_mobile.html line ~3331).
- Aligns barrier orbit with main formation center (both at y=320)
- Top of orbit: 320 - 108 = 212px (safe margin)
- Bottom of orbit: 320 + 108 = 428px (well within 1040px canvas)

**Affected levels:**
- Level 1 (Green): `'circle'` barrier (5 barriers) - orbit moved down 160px
- Level 6 (Red): `'orbitingShield'` barrier (6 barriers) - orbit moved down 160px
- Level 9 (Purple): `'orbitingShield'` barrier (8 barriers) - orbit moved down 160px
- Level 11 (Purple): `'circle'` barrier (8 barriers) - orbit moved down 160px

**Unaffected levels:** Levels 2, 4, 8, 10, 12 use different barrier types (`horizontalLine`, `arrow`, `dualLines`) with different Y positioning (y=468px), unchanged by this fix.

**Code location:** game_mobile.html lines ~3324-3351 (spawnBarrier function, circle/orbitingShield case)

**To revert:** Change `var orbitCenterY = 320;` back to `160` (both inline calculation and enemy property)

---

## 15. NEXT ACTIONS

| Priority | Action | Owner |
|---|---|---|
| ✅ Done | Normalise platform: `computer` → `desktop` in index.html | Deployed Mar 12 |
| ✅ Done | Wave drop-off: ATTEMPTS CSV support + death rate % table | Mar 12 |
| ✅ Done | Wave drop-off: ALL / MOBILE / DESKTOP platform toggle | Mar 12 |
| ✅ Done | "Games Won" Looker scorecard — date range fix, filter Mar 10+ | Mar 12 |
| ✅ Done | Funnel step 10 — already `player_won`, no change needed | Mar 12 |
| ✅ Done | Fix L4 mobile V-formation pop-in (flyingVExploded spacing 0.5→0.34) | Mar 13 |
| ✅ Done | Fix purple replay button showing +25 instead of +50 | Mar 13 |
| ✅ Done | Port + simplify replay incentive system to desktop | Mar 13 |
| ✅ Done | Fix mobile spiral formation clipping top of screen (targetY 150→220) | Mar 13 session 2 |
| ✅ Done | Fix desktop formation snap-to-position at first morph (morph clock reset) | Mar 13 session 2 |
| ✅ Done | Implement slot rotation carousel + fix formation entry snap bug (both files) | Mar 13 session 3 |
| ✅ Done | Document critical formation mechanics in PAIM + inline comments (both files) | Mar 13 session 3 |
| 🟡 P1 | Formation angular rotation — confirm design choice (continuous spin vs beat-snapped) | NOT NEEDED — slot rotation sufficient |
| 🟡 P2 | Load Platform CSV once `computer` → `desktop` propagates in GA4 (~1–2 days post Mar 12 deploy) | User |
| 🟡 P2 | Investigate L2 death spike — specific enemy pattern? | User |
| 🟡 P2 | Cross-ref `menu_view` referrer vs 24.5% menu bounce rate | — |
| 🟡 P2 | Build Ctrl+S session persistence for dashboard | Claude |
| 🟢 P3 | Build Smart Signal System — Report Card tab + benchmark tooltips | Claude (after ~Mar 24 data) |
| 🟢 P3 | Build music A/B comparison once v3.0 organic data accumulates (~Mar 24+) | — |
| 🟢 P3 | Build 6-page Looker Studio portfolio dashboard | After platform CSV loaded |
| 🟢 P3 | Song choice feature on victory screen | Pending audio assets |
| 🟢 P3 | Pink levels 13–15 + impossible boss / forever play mode | Future session |
| 🟢 P3 | Increase difficulty: Red boss, Purple boss, Red level 7 | Future session |
