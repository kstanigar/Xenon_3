# NON-X Game Project Memory

## Project Overview
NON-X is a browser-based space shooter game with desktop and mobile versions.
- **Live URL:** https://kstanigar.github.io/Xenon_3/
- **Desktop:** game.html
- **Mobile:** game_mobile.html
- **Index:** index.html (platform selector)
- **Repo:** https://github.com/kstanigar/Xenon_3
- **GA4 Property:** NON-X (Account: NON-X Game), Tracking ID: G-9ECFZ9JBE5

---

## Repository & Git Workflow
- **Branch structure:** `main` (production) → feature branches → PR → merge to main
- **DO NOT use `develop` branch** — caused repeated sync issues
- **CI/CD:** GitHub Actions runs integrity checks on every PR to main
- **GitHub Pages:** auto-deploys from main, takes ~2-3 min after merge
- **Local repo path:** /Users/keithstanigar/Documents/Projects/Xenon_3/

### Critical Workflow Rule
**Always verify files BEFORE committing:**
```bash
python3 -c "
c = open('game_mobile.html').read()
print('Lines:', len(c.splitlines()))
print('Brace diff:', c[c.find('<script>'):].count('{') - c[c.find('<script>'):].count('}'))
print('draw function:', 'function draw(' in c)
"
```
- game.html should be ~5365 lines, brace diff 0
- game_mobile.html should be ~5999 lines, brace diff 0, draw function present

### Commit message tip
Use a single short title line with `-m` to avoid shell quoting issues:
```bash
git commit -m "feat(mobile): short description here"
```

---

## CI Integrity Checks (.github/workflows/integrity-check.yml)
### Required functions — both files:
- function startFromCard
- function playAgain
- function showSurveyBanner
- function collapseSurveyBanner
- function submitSurvey
- function dismissSurvey
- function playerTakeDamage
- function shouldShowSurvey
- function buildBugButtonHTML
- function openBugReport
- function submitBugReport
- function fireEvent
- if (playerBlinking) return
- game_complete
- 'outcome': 'victory'
- 'outcome': 'death'
- 'outcome': 'abandoned'
- bug_report_submitted

### Banned patterns:
- game.html: `buildSurveyHTML`, `'phase'.*'standard'`
- game_mobile.html: `buildSurveyHTML`, `'phase'.*'standard'`

---

## Game Structure
- **12 levels + 3 bosses** across 3 phases:
  - Green phase: Levels 1-4 → Boss 1
  - Red phase: Levels 5-8 → Boss 2
  - Purple phase: Levels 9-12 → Boss 3
- **Power-ups:** Health, Shield, Double Laser, Triple Laser, Quad Laser
- **Music:** A/B test variant (on/off tracked via `ab_music_group`)

---

## Analytics Architecture

### GA4 Custom Dimensions (event-scoped)
Register all of these in GA4 → Admin → Custom definitions → Create custom dimension (event-scoped):

| Parameter | Description | Status |
|-----------|-------------|--------|
| platform | 'desktop' or 'mobile' | ✅ registered |
| level_number | 1-12 | ✅ registered |
| level_reached | highest level in session | ✅ registered |
| boss_id | 1, 2, or 3 | ✅ registered |
| score | player score | ✅ registered |
| phase | 'green', 'red', or 'purple' | ✅ registered |
| outcome | 'victory', 'death', or 'abandoned' | ✅ registered |
| music_variant | 'on' or 'off' | ✅ registered |
| ab_music_group | A/B test group | ✅ registered |
| session_duration_seconds | seconds since game start | ✅ registered |
| powerup_type | type of powerup collected | ✅ registered |
| analytics_version | '2.0' — filter explorations to exclude pre-2.0 QA/test data | ✅ registered |
| rank | leaderboard rank at time of submission | ✅ registered |
| death_phase | phase at time of death: 'green', 'red', or 'purple' | ⚠️ needs registration |
| replay_tier | replay incentive tier applied: 1, 2, 3, or 4 | ⚠️ needs registration |
| bonus_hp | HP bonus granted on replay: 15, 25, or 50 | ⚠️ needs registration |
| continue | true = Continue from Level X, false = Play Again | ⚠️ needs registration |

### Key Events Tracked
| Event | When it fires | Key parameters |
|-------|--------------|----------------|
| session_start | page load | analytics_version |
| first_visit | GA4 auto | — |
| game_start | player starts a new game | analytics_version, is_replay, games_played |
| wave_reached | start of each level's formation wave | level_number, phase, score |
| boss_attempt | player enters boss fight | boss_id, level_reached, score, session_duration_seconds |
| boss_defeated | player beats a boss | boss_id, level_reached, score, session_duration_seconds |
| player_death | player health reaches 0 | level_reached, phase, score, session_duration_seconds |
| player_won | player beats all 3 bosses | score, session_duration_seconds |
| game_complete | every session end regardless of outcome | outcome, level_reached, score, session_duration_seconds |
| powerup_collected | player picks up a powerup | powerup_type, level_reached, score |
| play_again | player clicks Play Again or Continue from Level X | score, level_reached, death_phase, replay_tier, bonus_hp, continue |
| leave_game | player clicks Leave Game | outcome, score, level_reached |
| leaderboard_submit | player submits score to leaderboard | score, rank |
| bug_report_submitted | player submits bug report | — |
| survey_submitted | player submits feedback survey | — |
| music_toggled | player toggles music mid-session | music_variant, score, level_reached |

---

## GA4 Explorations Built

### Filtering for clean data
Apply `Analytics Version exactly matches 3.0` filter to every tab in every exploration and as a report-level filter in Looker Studio.
Dimension will appear in picker 24-48 hours after first live event containing `analytics_version` is received.

**Version history:**
| Version | Status | Notes |
|---------|--------|-------|
| (none) | ❌ discard | Pre-analytics, QA/test data |
| 2.0 | ❌ discard | Boss spawn broken (score threshold gate), indestructible mobile minions, hitbox untuned, movement was random A/B not player choice |
| 3.0 | ✅ use | Current — boss fix, hitbox inset, minion fix, movement as player preference, clean main menu UX |

### Exploration 1: NON-X Completion Funnel (Funnel exploration)
10-step funnel:
1. Session Start
2. Game Start
3. Level 1 (wave_reached, level_number=1)
4. Level 4 (wave_reached, level_number=4)
5. Boss 1 Attempt (boss_attempt, boss_id=1)
6. Level 8 (wave_reached, level_number=8)
7. Boss 2 Attempt (boss_attempt, boss_id=2)
8. Level 12 (wave_reached, level_number=12)
9. Boss 3 Attempt (boss_attempt, boss_id=3)
10. Game Complete (game_complete)

### Exploration 2: NON-X Game Analytics (Free form, 6 tabs)

**Tab 1 — Death Drop-off by Level**
- ROWS: Level Number | COLUMNS: Platform | VALUES: Event count
- FILTER: Event name exactly matches player_death

**Tab 2 — Boss Kill Rate**
- ROWS: Event name + Boss ID (nested) | VALUES: Event count
- FILTER: Event name contains boss

**Tab 3 — Platform Comparison**
- ROWS: Platform | COLUMNS: Event name | VALUES: Event count

**Tab 4 — Music Impact**
- ROWS: Event name | COLUMNS: Music Variant | VALUES: Event count
- FILTER: Event name exactly matches game_complete

**Tab 5 — Session Duration**
- ROWS: Platform | VALUES: Session duration

**Tab 6 — Power-up Usage**
- ROWS: Powerup Type | VALUES: Event count
- FILTER: Event name exactly matches powerup_collected

### Exploration 3: NON-X Replay Funnel (Funnel exploration)
Measures whether the replay incentive system is moving players forward.

**Dimensions to import:** Event name, Replay Tier, Is Replay, Platform
**Metrics to import:** Event count, Active users

**Funnel steps:**
1. **Game Started** — Event name exactly matches `game_start`
2. **Died** — Event name exactly matches `player_death`
3. **Chose to Replay** — Event name exactly matches `play_again`
4. **Started Replay** — Event name exactly matches `game_start`

**Breakdown:** Replay Tier (splits each step by tier — shows drop-off per incentive)
**Filter:** Is Replay exactly matches `true`

Key insight: drop-off between Step 2→3 by tier shows which death contexts most motivate a replay. Drop-off between Step 3→4 should be near zero — if not, something is broken in the flow.

### Exploration 4: NON-X Replay Incentive Breakdown (Free form, 4 tabs)
Answers which tier drives the most replays and whether higher bonuses correlate with better survival.

**Tab 1 — Tier Uptake**
- ROWS: Replay Tier | VALUES: Event count
- FILTER: Event name exactly matches play_again

**Tab 2 — Continue vs Play Again**
- ROWS: Continue | COLUMNS: Replay Tier | VALUES: Event count
- FILTER: Event name exactly matches play_again

**Tab 3 — Bonus HP vs Level Reached**
- ROWS: Bonus HP | COLUMNS: Level Reached | VALUES: Event count
- FILTER: Event name exactly matches game_complete

**Tab 4 — Death Phase Distribution**
- ROWS: Death Phase | COLUMNS: Platform | VALUES: Event count
- FILTER: Event name exactly matches play_again

### Exploration 5: NON-X Phase Retention (Free form)
Answers where players drop off across phases and whether replaying changes that. Most direct measure of whether the incentive system is getting players into red and purple phases.

- ROWS: Death Phase
- COLUMNS: Is Replay
- VALUES: Event count
- FILTER: Event name exactly matches player_death

---

## Mobile-Only Features (game_mobile.html)

### Difficulty Tuning (vs desktop)
Enemy bullet speed multipliers reduced to ease late-game difficulty on touch controls:
- Red phase: ×1.15 (desktop: ×1.40)
- Purple phase: ×1.35 (desktop: ×1.65)
- Green phase: unchanged (base CONFIG.enemyBulletSpeed = 5)

arrowheadExploded explode multiplier: 1.6 (desktop: 2.4) — outer enemies were spawning off-screen on L12.

### Mobile Enemy Counts
| Level | Phase | Count |
|-------|-------|-------|
| 1–4 | Green | 9, 9, 10, 9 |
| 5 | Red | 14 |
| 6 | Red | 11 |
| 7 | Red | 10 |
| 8 | Red | 10 |
| 9 | Purple | 16 |
| 10 | Purple | 17 |
| 11 | Purple | 19 |
| 12 | Purple | 22 |

### Personal Best Callout (mobile only)
- **Game over:** `🏆 New personal best!` if new record, otherwise `Your best: X — Y away`
- **Victory:** `🏆 New personal best!` if new record, otherwise `Your best: X`
- **First game:** no callout (nothing to compare against yet)
- `prevBest` is read from `highScores[0]` before the new score is added

### Replay Incentive System (mobile only)
**To port to desktop:** search `REPLAY INCENTIVES` in game_mobile.html — each comment identifies exactly what to copy and where it goes in game.html. Port as a matched set:

- **Variables** (declare near `isReplay`): `isReplaySession`, `deathPhase`, `continueFromLevelNum`
- **Functions**: `continueFromLevel()`, updated `playAgain()` tier logic
- **Game start reset**: `replayBonusHP` tier logic + set `isReplaySession = isReplay` BEFORE `isReplay = false`
- **Both game over screens**: `var wasReplay = isReplaySession` capture + tier button blocks

**CRITICAL**: `isReplay` is a one-shot flag reset immediately after `game_start` fires. `isReplaySession` is set from it before the reset and stays `true` for the full run. Without it, Tiers 2-4 never fire.

| Tier | Condition | Button | HP bonus | Start level |
|------|-----------|--------|----------|-------------|
| 1 | First visit death, any level | ▶ Play Again (+15 HP) | +15 | Level 1 |
| 2 | Replay death, levels 2–4 | ↩ Resume Level X (+15 HP) | +15 | Death level |
| 3 | Replay death, red phase | ▶ Play Again (+25 HP) | +25 | Level 1 |
| 4 | Replay death, purple phase | ▶ Play Again (+50 HP) | +50 | Level 1 |

**Key behaviours:**
- Tier 2 shows only Continue + Leave Game — no plain Play Again option
- Tier eligibility is based on `deathPhase` at moment of death, not session history — a player who reached red phase, replayed, and died at level 3 gets Tier 2
- Score always resets to 0
- `deathPhase` captured at moment of death in both game over paths
- `continueFromLevelNum` set by `continueFromLevel()`, applied at game start, then cleared
- `isReplay` already tracked; determines Tier 1 vs Tiers 2-4

---

## GA4 Property Reset Plan
Use `analytics_version = 2.0` filter on explorations to exclude pre-2.0 QA data — no reset needed.

If a full reset is ever required:
1. GA4 → Admin → Create Property → name `NON-X`
2. Replace `G-9ECFZ9JBE5` with new measurement ID in both game files (2 places each: `gtag('config',...)` and `gtag/js?id=...`)
3. Deploy via PR, rebuild all explorations in new property

---

## Known Issues / History
- game_mobile.html: missing `function playAgain`, broken shield block, truncated file, quote syntax error, missing survey/blink functions — all fixed
- Embedded `buildSurveyHTML` survey replaced with slide-down banner matching desktop — now banned in CI for both files
- `analytics_version: '2.0'` added to `session_start` and `game_start` in both files
- Deferred analytics implemented in both files: `play_again`, `music_toggled`, `rank` on `leaderboard_submit`
- Mobile difficulty tuned: bullet speeds, enemy counts, arrowheadExploded formation fix
- Personal best callout added to all mobile end screens
- Tiered replay incentive system added to mobile (Tiers 1-4) with full analytics and porting comments; `isReplaySession` introduced to fix timing bug (isReplay resets before death screen renders); Tier 2 button label shortened to "↩ Resume Level X (+15 HP)"
- **analytics_version bumped to 3.0** across game.html, game_mobile.html, and index.html — filters all explorations and Looker Studio to exclude 2.0 data (broken boss spawn, indestructible minions, untuned hitbox, random movement A/B)

---

## Pending / Deferred
- ⚠️ Register 4 new GA4 custom dimensions: `death_phase`, `replay_tier`, `bonus_hp`, `continue`
- ⚠️ Update `analytics_version = 3.0` filter on all explorations and Looker Studio dashboard (replaces 2.0)
- Port replay incentive system to game.html (search `REPLAY INCENTIVES` in game_mobile.html)
- Song choice feature on victory screen replay (pending audio asset decisions)

---

## Post-Mortem: Leaderboard Submission Bug (March 2026, ~2.5 hrs lost)

### What happened
Asking "how do I reset the leaderboard?" led to advice to delete the Firebase collection. That triggered a cascade:
1. Deleting the collection caused `showLeaderboard()` to return empty — "No scores yet" on every game over screen
2. The submit form stopped appearing. Root cause was a **timing bug**: `addHighScore(score)` ran *before* `buildLeaderboardSubmitHTML()`, so `highScores[0]` already equalled the current score, making `score > submittedScore` always false
3. Claude misdiagnosed the cause as the `level >= 2` gate (without asking what level the player was on) and removed it prematurely
4. Then over-corrected `getEffectiveSubmittedScore()` by stripping the `highScores` comparison — wrong fix
5. Three bad fixes in a row, each masking the previous one

### Actual fix
Capture `submittedScore = getEffectiveSubmittedScore()` **before** `addHighScore(score)` runs, then pass it as a parameter into `buildLeaderboardSubmitHTML(submittedScore)`. The timing was the only bug.

### Communication rules going forward
- **Always state level + score + first game or replay** when reporting a game over screen bug
- **When something breaks after a specific action**, lead with that action: *"I deleted X and now Y is broken"* — the sequence is the clue
- **Claude rule**: never recommend a destructive operation (deleting collections, clearing localStorage, resetting properties) without first tracing all code that depends on it and documenting what will break
- **Claude rule**: never diagnose a game over screen bug without first asking what level the player was on and what action preceded the bug
- **Claude rule**: the Firebase collection deletion was Claude's bad advice — the recommendation said "it will auto-recreate, no code changes needed" which was incorrect. Responsibility for that cascade sits with Claude, not the user

---

## Sensitive Code — Do Not Modify Without Full Trace

The following areas have caused multi-hour regressions. Treat as high-risk — always read the full function and its call sites before changing anything:

### ⚠️ Leaderboard Submit Form (`buildLeaderboardSubmitHTML`)
- `submittedScore` MUST be captured before `addHighScore()` runs — passed as parameter, never fetched internally
- `getEffectiveSubmittedScore()` reads only `nonx_submitted_score` (Firebase submitted) — not `highScores[]`
- Gate is `score > submittedScore` only — no level or score minimum gates
- Called in 3 places per file: main death, `rebuildGameOverScreen`, dev mode death
- The Firebase `leaderboard` collection must exist (even with one dummy doc) for `showLeaderboard()` to work
- **Never delete the Firebase collection** — archive instead (export first, then delete individual docs)

### ⚠️ Boss Spawn Trigger (`advanceLevel`)
- Boss spawns when `level >= 4/8/12` and `!boss1/2/3Defeated` — NO score threshold gate
- Score threshold was removed because levels 1-4 only yield ~370 pts max, causing boss to never spawn
- `boss.shieldStartTime` resets when `boss.entering = false` — not at spawn time
- Bullet collision checks `!boss.entering` guard — bullets must not damage boss while off-screen

### ⚠️ Mobile Boss Minions (`updateBossMinions`)
- Minions must NOT be inserted into `SpatialGrid` — they have their own collision loop
- Inserting them causes bullets consumed by grid path (looks them up in `enemies[]`), making minions indestructible and causing infinite score ticks

### ⚠️ Analytics Version
- Current version: `3.0` — filter ALL explorations and Looker Studio to `analytics_version = 3.0`
- Bump version whenever gameplay mechanics change (hitbox, boss logic, scoring)
- Set in: `session_start` + `game_start` in both game files; `menu_view` + `play_clicked` in index.html

### ⚠️ `isReplay` / `isReplaySession` timing (mobile)
- `isReplay` is a one-shot flag reset immediately after `game_start` fires
- `isReplaySession` captured from `isReplay` BEFORE the reset — persists for the full run
- Without `isReplaySession`, Tiers 2-4 of the replay incentive system never fire

---

## Code Comments Debt
The codebase has grown rapidly and comments are inconsistent. A dedicated comments pass is needed. Priority areas:
- Leaderboard submission flow (timing, gates, parameter passing)
- Boss spawn and shield logic
- Replay incentive tier system (`isReplay` vs `isReplaySession`)
- Analytics event firing (what fires where, version tagging)
- Mobile SpatialGrid exclusions
- Player hitbox inset (`isCollidingPlayer`)

---

## ✅ DONE: How-To-Play Screen Updates

Both `game.html` and `game_mobile.html` introCard updated with:
- **Controls** — desktop: mouse/arrow keys + Full Movement toggle note; mobile: tap/drag + auto-fire + Full Movement toggle note
- **Global Leaderboard** — top 10 on main menu, submit on game over, cyan highlight, one submission per personal best
- **Settings** — Music, Full Movement (with on/off description), Analytics, all auto-save

---

## Next Session: Analytics Dashboard Build (Portfolio)

Build a public-facing Looker Studio dashboard connected to GA4 that tells the full player journey story. Goal: demonstrate product analytics skills to recruiters and collaborators.

### Dashboard Pages

**Page 1 — Overview (headline numbers)**
- Total sessions, unique players, avg session duration (scorecards)
- Platform split: desktop vs mobile (donut chart)
- Play sessions over time (daily line chart)
- Game complete outcomes: victory / death / abandoned (stacked bar or donut)
- Key callout: % of sessions that reach Boss 1 (funnel entry rate)

**Page 2 — Player Funnel**
- Full 10-step completion funnel visualised as a waterfall/bar
- Drop-off % at each stage — annotate the single biggest drop-off point
- Side-by-side: desktop funnel vs mobile funnel (segment comparison)
- Boss kill rate table: boss_attempt vs boss_defeated per boss_id (Boss 1/2/3)
- Callout: overall victory rate (player_won / game_start)

**Page 3 — Difficulty & Level Analysis**
- Deaths by level (horizontal bar chart) — where do players struggle most?
- Average score at death by level (line chart overlay)
- Level reached distribution: how far do most players get? (histogram)
- Phase drop-off: % of players who reach green → red → purple (3 scorecards)

**Page 4 — Engagement & Retention**
- Replay rate: avg game_start events per session (are players coming back?)
- Session duration distribution (histogram, bucket by minute)
- Music on vs off: compare avg level_reached and session_duration_seconds
- movement_group comparison: Full Movement vs Horizontal Only — avg score and level_reached
- Replay tier breakdown: which tier drives the most replays? (bar chart)

**Page 5 — Leaderboard & Score Analysis**
- leaderboard_submit count over time (line chart)
- Score distribution at submission (histogram — what scores make the leaderboard?)
- Platform comparison: avg score desktop vs mobile (scorecard pair)
- Rank distribution at submission (bar chart — are most submissions rank 10 or rank 1?)

**Page 6 — Feature & Settings Usage**
- Power-up collection by type (donut chart)
- Analytics opt-in rate (% of sessions with consent = on) — scorecard
- movement_toggled event count (how many players change from the default?)
- music_toggled event count (mid-session music changes)
- Bug reports over time (quality/stability signal)

### Key Metrics to Highlight for Portfolio
These are the most compelling numbers to feature prominently — they tell the strongest product story:

| Metric | How to calculate | Why it matters |
|--------|-----------------|----------------|
| Funnel completion rate | boss_attempt(1) / game_start | Core engagement depth |
| Boss kill rate | boss_defeated / boss_attempt per boss_id | Difficulty balance signal |
| Replay rate | play_again / player_death | Retention / game feel signal |
| Platform parity | level_reached desktop vs mobile avg | UX equity signal |
| Music impact | session_duration music_on vs music_off | A/B test result |
| Movement preference | % Full Movement vs Horizontal Only | Player behaviour insight |
| Victory rate | player_won / game_start | Ultimate completion rate |

### Looker Studio Setup Notes
- Data source: GA4 property G-9ECFZ9JBE5
- Apply `analytics_version = 2.0` filter at report level to exclude all QA/test data
- Use date range control on every page (default: last 28 days)
- Add platform filter control so viewers can drill down by desktop/mobile
- Use NON-X colour palette: #00FFFF (cyan) primary, #000 background, #FF0055 accent for deaths, #00FF88 accent for victories
- Host dashboard publicly and link from portfolio/GitHub README
