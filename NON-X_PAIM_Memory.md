# NON-X — PAIM Master Memory
### Project AI Model Reference Document
_Last updated: March 12, 2026_
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

---

## 2. REPOSITORY & GIT WORKFLOW

- **Branches:** `main` (production) → feature branches → PR → merge. **Never use `develop`.**
- **CI/CD:** GitHub Actions integrity checks on every PR
- **Deploy:** GitHub Pages, auto-deploys from main, ~2–3 min after merge

### Pre-commit check (always run)
```bash
python3 -c "
c = open('game_mobile.html').read()
print('Lines:', len(c.splitlines()))
print('Brace diff:', c[c.find('<script>'):].count('{') - c[c.find('<script>'):].count('}'))
print('draw function:', 'function draw(' in c)
"
```
- `game.html` → ~6546 lines, brace diff 0
- `game_mobile.html` → ~7441 lines, brace diff 0, draw function present

### CI required functions (both files)
`startFromCard`, `playAgain`, `showSurveyBanner`, `collapseSurveyBanner`, `submitSurvey`, `dismissSurvey`, `playerTakeDamage`, `shouldShowSurvey`, `buildBugButtonHTML`, `openBugReport`, `submitBugReport`, `fireEvent`, `if (playerBlinking) return`, `game_complete`, `'outcome': 'victory'`, `'outcome': 'death'`, `'outcome': 'abandoned'`, `bug_report_submitted`

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
| `play_again` | score, level_reached, death_phase, replay_tier, bonus_hp, continue | Mobile: has tier params. Desktop: port pending. |
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
| `death_phase` | ⚠️ Needs registration | Mobile replay system |
| `replay_tier` | ⚠️ Needs registration | Mobile replay system |
| `bonus_hp` | ⚠️ Needs registration | Mobile replay system |
| `continue` | ⚠️ Needs registration | Mobile replay system |

---

## 6. GA4 EXPLORATIONS BUILT

### 1. NON-X Completion Funnel (Funnel exploration)
10 steps: Session Start → Game Start → Level 1 → Level 4 → Boss 1 Attempt → Level 8 → Boss 2 Attempt → Level 12 → Boss Attempt 3 → Game Complete
⚠️ Step 10 should be changed from `game_complete` → `player_won`

### 2. NON-X Game Analytics (Free form, 6 tabs)
- Death Drop-off: ROWS Level Number | COLUMNS Platform | FILTER player_death
- Boss Kill Rate: ROWS Event name + Boss ID nested | FILTER event contains boss
- Platform Comparison: ROWS Platform | COLUMNS Event name
- Music Impact: ROWS Event name | COLUMNS Music Variant | FILTER game_complete
- Session Duration: ROWS Platform | VALUES Session duration
- Power-up Usage: ROWS Powerup Type | FILTER powerup_collected

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
| Games Won (Looker) | 139 | 🔴 Anomaly — Looker field misconfigured (game_complete vs player_won) |

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

### 🔴 Fix Required
| ID | Issue | Fix |
|---|---|---|
| F2 | "Games Won: 139" Looker field counts `game_complete` not `player_won` | Rewrite Looker calculated field |
| F3 | Funnel step 10 uses `game_complete` not `player_won` | Change in GA4 Explore funnel config |
| F4 | 4 custom dimensions unregistered: `death_phase`, `replay_tier`, `bonus_hp`, `continue` | Register in GA4 Admin |

### 🟡 Watch / Improve
| ID | Issue | Notes |
|---|---|---|
| I1 | Menu bounce — 24.5% of sessions never start a game | 🔴 Now confirmed as #1 drop with real data (37/49 sessions). Cross-ref `menu_view` referrer to identify traffic source. |
| I2 | L2 death spike — 34 deaths vs 8 at L3 | Unexpected. Investigate specific enemy pattern at L2. |
| I3 | Mobile = 81% of all deaths | Platform gap confirmed with real data. Mobile controls are the friction point. |
| I4 | Desktop port of replay incentive system pending | Search `REPLAY INCENTIVES` in game_mobile.html |
| I5 | Boss 2 funnel (50%) vs kill rate (83%) contradiction | Frustration accumulation, not first-attempt wall. Watch as data grows. |

---

## 9. MOBILE-SPECIFIC FEATURES

### Difficulty tuning (affects analytics comparisons)
| Phase | Desktop bullet × | Mobile bullet × |
|---|---|---|
| Green | 1.0 | 1.0 |
| Red | 1.40 | 1.15 |
| Purple | 1.65 | 1.35 |

### Replay Incentive System (mobile only)
**CRITICAL timing:** `isReplay` resets immediately after `game_start` fires. `isReplaySession` must be captured from `isReplay` BEFORE that reset. Without it, Tiers 2–4 never fire.

| Tier | Condition | HP Bonus | Start |
|---|---|---|---|
| 1 | First visit death, any level | +15 | Level 1 |
| 2 | Replay death, green phase levels 2–4 | +15 | Death level |
| 3 | Replay death, red phase | +25 | Level 1 |
| 4 | Replay death, purple phase | +50 | Level 1 |

---

## 10. SENSITIVE CODE — DO NOT MODIFY WITHOUT FULL TRACE

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

---

## 11. DASHBOARD & TOOLING

### HTML Analytics Dashboard (`nonx-analytics-dashboard.html`)
- 6 tabs: Overview, Funnel, Boss Analysis, A/B Tests, Platform, Looker Guide
- CSV drag-and-drop loader — auto-detects report type, filters `analytics_version ≠ 3.0`
- Chip tracker shows which CSVs are loaded (FUNNEL / DEATHS / BOSS / A/B MUSIC / PLATFORM / DEATHS MOBILE)
- Load order each session: Deaths CSV → Boss CSV → Funnel CSV
- Wave drop-off chart: all 12 levels + 3 boss bars always rendered (zero-death levels show faint placeholder bar)
- Boss bars computed live from boss CSV data — load order independent
- **Data loaded (as of Mar 12):** FUNNEL ✅ DEATHS ✅ BOSS ✅ | A/B MUSIC ⏳ PLATFORM ⏳ (pending platform fix deploy)
- Ctrl+S session persistence: planned, not yet built — re-drop CSVs each session

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

Grade scale: A = at/above target | B = acceptable | C = below target | D = needs attention | F = critical/anomaly
Delta: ↑ green = improving | ↓ red = worsening | → grey = stable | ~ yellow = anomaly

⚠️ Do NOT calibrate grade thresholds until real organic user data accumulates (post Mar 10, 2026)

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

### Documents produced
- `NON-X_Analytics_Export_Guide.docx` — full GA4 + Looker Studio setup guide
- `nonx-analytics-dashboard.html` — interactive 6-tab dashboard with CSV loader

---

## 12. WORKFLOW RULES

1. **Data-first:** Confirm capture before building any visual. Audit: Good / Improve / Fix.
2. **Every metric gets a G/I/F audit** before being added to the dashboard.
3. **Share updated files after each commit** — AI applies fixes to the new version.
4. **Dashboard:** Weekly GA4 CSV → drag-and-drop → Ctrl+S.
5. **Looker = real-time ops. HTML dashboard = polished weekly + portfolio.**
6. **Data sharing:** Screenshots + CSV exports (no direct GA4/Looker access possible).
7. **Claude rule:** Never recommend destructive operations without full dependency trace.
8. **Claude rule:** Never diagnose game over bugs without asking level + score + context first.
9. **Practice runs:** QA data is valid for workflow practice — builds readiness for real data launch.

---

## 13. KNOWN HISTORY & POST-MORTEMS

### Leaderboard Submission Bug (~2.5 hrs lost, March 2026)
Deleting Firebase collection → submit form stopped appearing. Root cause: `addHighScore(score)` ran before `buildLeaderboardSubmitHTML()`. Fix: capture `submittedScore` before `addHighScore()` runs. Claude incorrectly diagnosed the `level >= 2` gate and made 3 bad fixes in a row.

### Mobile Fixes (all resolved)
Missing `playAgain`, broken shield block, truncated file, quote syntax error, missing survey/blink functions — all fixed. `buildSurveyHTML` replaced with slide-down banner — now banned in CI.

### Version History
- v2.0 → v3.0: Boss spawn fix, hitbox inset, mobile minion fix, movement as player preference
- v3.0 full instrumentation: Mar 10 2026 — `analytics_version` injected on all events via wrapper
- v3.0.1 instrumentation patch: Mar 12 2026 — `index.html` platform dimension `'computer'` → `'desktop'`

---

## 14. NEXT ACTIONS

| Priority | Action | Owner |
|---|---|---|
| ✅ Done | Normalise platform: `computer` → `desktop` in index.html | Deployed Mar 12 |
| 🔴 P1 | Fix "Games Won" Looker field → `player_won` only | User |
| 🔴 P1 | Change funnel step 10: `game_complete` → `player_won` | User in GA4 |
| 🔴 P1 | Register 4 pending GA4 dimensions: `death_phase`, `replay_tier`, `bonus_hp`, `continue` | User |
| 🟡 P2 | Load Platform CSV once `computer` → `desktop` fix propagates in GA4 (~1–2 days post-deploy) | User |
| 🟡 P2 | Investigate L2 death spike — specific enemy pattern? | User |
| 🟡 P2 | Cross-ref `menu_view` referrer vs 24.5% menu bounce rate | — |
| 🟡 P2 | Port replay incentive system (Tiers 1–4) to desktop | User |
| 🟡 P2 | Build Ctrl+S session persistence for dashboard | Claude |
| 🟢 P3 | Build Smart Signal System — Report Card tab + benchmark tooltips | Claude (after real data accumulates) |
| 🟢 P3 | Build music A/B comparison once v3.0 organic data accumulates (~Mar 24+) | — |
| 🟢 P3 | Build 6-page Looker Studio portfolio dashboard | After F2 + F3 fixes |
| 🟢 P3 | Song choice feature on victory screen | Pending audio assets |
