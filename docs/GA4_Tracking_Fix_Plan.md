# GA4 Tracking Fix Plan — `death_phase` + `is_replay`

**Created:** June 27, 2026
**Author:** Session 12 — non-x_analytics P-5 Security Audit smoke test investigation
**Status:** 🔴 PENDING IMPLEMENTATION — awaiting user approval

---

## Problem Summary

Two GA4 custom dimensions are registered but returning `(not set)` in the NON-X Analytics dashboard:

| Dimension | GA4 Parameter Key | Registered | Impact |
|-----------|------------------|------------|--------|
| Death Phase | `death_phase` | Mar 2, 2026 | Death Triggers chart empty |
| Is Replay | `is_replay` | Feb 27, 2026 | Replay Rate shows `—` |

---

## Root Causes

### Fix 1 — `death_phase` (wrong parameter name)

**Problem:** `player_death` event sends `'phase'` (maps to the "Game Phase" custom dimension), but the Death Triggers chart queries `customEvent:death_phase` (the "Death Phase" custom dimension). These are two separate registered dimensions — `phase` and `death_phase` are different GA4 parameter keys.

**Evidence:** GA4 Data API returns `customEvent:death_phase = "(not set)"` for all `player_death` events. The `phase` parameter IS being sent correctly (the "Game Phase" dimension has data). `death_phase` is never populated.

**Fix:** Add `'death_phase'` alongside the existing `'phase'` parameter in both `player_death` fireEvent calls, using the same ternary value.

---

### Fix 2 — `is_replay` (boolean falsy value dropped by gtag)

**Problem:** `game_start` sends `'is_replay': isReplay` where `isReplay` is a JavaScript boolean. gtag() drops falsy parameter values — boolean `false` is never sent to GA4, resulting in `(not set)` for all non-replay game starts. Only when `isReplay = true` (on replay) does the value reach GA4.

**Evidence:** GA4 Data API returns `customEvent:is_replay = "(not set)"` for 12/13 game_start events; only 1 row shows a value. The `isReplay` variable is correctly maintained in game logic — this is purely a gtag/boolean type issue.

**Fix:** Convert boolean to string: `'is_replay': isReplay ? 'true' : 'false'`
This ensures gtag always receives a non-empty string and GA4 records every game start as either `'true'` or `'false'`.

---

## Exact Code Changes

### Change 1A — `game.html` line 7035 (`player_death`, desktop)

**File:** `/Users/ks2026/Documents/Projects/2026/Xenon_3/game.html`
**Lines:** 7030–7040

**Before (lines 7030–7040):**
```javascript
fireEvent('player_death', {
  'ab_music_group': userABGroup,
  'movement_group': movementABGroup,
  'platform': 'desktop',
  'level_reached': level,
  'phase': purplePhase ? 'purple' : redPhase ? 'red' : 'green',
  'score': score,
  'music_variant': localStorage.getItem('nonex_music') !== 'off' ? 'on' : 'off',
  'session_duration_seconds': gameSessionStart ? Math.round((Date.now() - gameSessionStart) / 1000) : null,
  'score_multiplier': scoreMultiplier
});
```

**After:**
```javascript
fireEvent('player_death', {
  'ab_music_group': userABGroup,
  'movement_group': movementABGroup,
  'platform': 'desktop',
  'level_reached': level,
  'phase': purplePhase ? 'purple' : redPhase ? 'red' : 'green',
  'death_phase': purplePhase ? 'purple' : redPhase ? 'red' : 'green',
  'score': score,
  'music_variant': localStorage.getItem('nonex_music') !== 'off' ? 'on' : 'off',
  'session_duration_seconds': gameSessionStart ? Math.round((Date.now() - gameSessionStart) / 1000) : null,
  'score_multiplier': scoreMultiplier
});
```

**What changed:** Added line `'death_phase': purplePhase ? 'purple' : redPhase ? 'red' : 'green',` after the existing `'phase'` line (line 7036 becomes line 7036, new `death_phase` is line 7037).

---

### Change 1B — `game_mobile.html` line 7706 (`player_death`, mobile)

**File:** `/Users/ks2026/Documents/Projects/2026/Xenon_3/game_mobile.html`
**Lines:** 7701–7711

**Before (lines 7701–7711):**
```javascript
fireEvent('player_death', {
  'ab_music_group': userABGroup,
  'movement_group': movementABGroup,
  'platform': 'mobile',
  'level_reached': level,
  'phase': purplePhase ? 'purple' : redPhase ? 'red' : 'green',
  'score': score,
  'music_variant': localStorage.getItem('nonex_music') !== 'off' ? 'on' : 'off',
  'session_duration_seconds': gameSessionStart ? Math.round((Date.now() - gameSessionStart) / 1000) : null,
  'score_multiplier': scoreMultiplier
});
```

**After:**
```javascript
fireEvent('player_death', {
  'ab_music_group': userABGroup,
  'movement_group': movementABGroup,
  'platform': 'mobile',
  'level_reached': level,
  'phase': purplePhase ? 'purple' : redPhase ? 'red' : 'green',
  'death_phase': purplePhase ? 'purple' : redPhase ? 'red' : 'green',
  'score': score,
  'music_variant': localStorage.getItem('nonex_music') !== 'off' ? 'on' : 'off',
  'session_duration_seconds': gameSessionStart ? Math.round((Date.now() - gameSessionStart) / 1000) : null,
  'score_multiplier': scoreMultiplier
});
```

**What changed:** Added `'death_phase'` line after the existing `'phase'` line — identical to Change 1A, `'platform': 'mobile'` only difference.

---

### Change 2A — `game.html` line 8574 (`game_start`, desktop)

**File:** `/Users/ks2026/Documents/Projects/2026/Xenon_3/game.html`
**Lines:** 8569–8577

**Before (line 8574):**
```javascript
'is_replay': isReplay,
```

**After (line 8574):**
```javascript
'is_replay': isReplay ? 'true' : 'false',
```

**Context (full block):**
```javascript
fireEvent('game_start', {
  'ab_music_group': userABGroup,
  'movement_group': movementABGroup,
  'platform': 'desktop',
  'music_variant': localStorage.getItem('nonex_music') !== 'off' ? 'on' : 'off',
  'is_replay': isReplay ? 'true' : 'false',
  'games_played': parseInt(localStorage.getItem('nonx_game_count') || '0', 10) + 1,
  'score_multiplier': scoreMultiplier
});
```

---

### Change 2B — `game_mobile.html` line 9451 (`game_start`, mobile)

**File:** `/Users/ks2026/Documents/Projects/2026/Xenon_3/game_mobile.html`
**Lines:** 9446–9454

**Before (line 9451):**
```javascript
'is_replay': isReplay,
```

**After (line 9451):**
```javascript
'is_replay': isReplay ? 'true' : 'false',
```

---

## CI/CD Safety Assessment

| Check | Risk | Reason |
|-------|------|--------|
| test.yml — required files | ✅ None | No files added/removed |
| test.yml — GA4 tracking present | ✅ None | fireEvent calls untouched except parameter additions |
| test.yml — ab_music_group present | ✅ None | Not touching ab_music_group |
| integrity-check.yml — `fireEvent` function exists | ✅ None | Function not modified |
| integrity-check.yml — `getCurrentPhase` function exists | ✅ None | Function not modified |
| integrity-check.yml — banned pattern `'phase'.*'standard'` | ✅ None | New values are `'purple'`/`'red'`/`'green'` only |
| integrity-check.yml — desktop/mobile parity | ✅ None | Changes are identical in both files |
| Jest / unit tests | ✅ None | No test files exist in project |

**Risk level: ZERO** — parameter additions to fireEvent() calls are invisible to all CI checks.

---

## Branch & Deploy Workflow

```bash
# Step 1: Create feature branch from dev
git checkout dev
git pull origin dev
git checkout -b feature/ga4-fix-death-phase-is-replay

# Step 2: Make the 4 changes (2 files × 2 fixes each)

# Step 3: Commit
git add game.html game_mobile.html
git commit -m "fix: add death_phase param to player_death; fix is_replay boolean → string"

# Step 4: Push to remote feature branch
git push origin feature/ga4-fix-death-phase-is-replay

# Step 5: Open PR → dev (not main)
# CI/CD runs on PR — confirm all checks pass
# Merge to dev after CI passes

# Step 6: Test on dev/staging
# Play game → die → check GA4 DebugView for death_phase and is_replay values
# Confirm: death_phase: 'green'/'red'/'purple', is_replay: 'true'/'false'

# Step 7: After 24-48h GA4 data propagation — confirm dashboard Death Triggers chart populates

# Step 8: PR dev → main when confirmed working
```

---

## Testing & Validation

**Immediate (DebugView — same day):**
1. GA4 → Admin → Data display → DebugView
2. Open NON-X game, play until death in green phase
3. Click `player_death` event in stream → Parameters tab
4. Confirm: `death_phase: 'green'` ✅ (and `phase: 'green'` still present)
5. Start a fresh game → click `game_start` → Parameters tab
6. Confirm: `is_replay: 'false'` ✅
7. Die and use Play Again → start new game → `game_start`
8. Confirm: `is_replay: 'true'` ✅

**Dashboard (24–48h after deploy):**
- Death Triggers chart populates with green/red/purple breakdown
- Replay Rate shows a percentage instead of `—`

---

## Possible Errors

| Error | Cause | Solution |
|-------|-------|---------|
| CI parity check warns on diff | Mobile/desktop have different function counts | Warning only — not a blocker; changes are identical |
| `death_phase` still `(not set)` after deploy | GA4 processing lag (24-48h) | Wait and re-query; verify DebugView shows value immediately |
| `is_replay` shows `'false'` for all events | No replays in dataset yet | Expected — need actual replay plays to see `'true'` |

---

## Files Changed

- `game.html` — 2 line changes (lines 7036, 8574)
- `game_mobile.html` — 2 line changes (lines 7706, 9451)

**No other files need changes.** The GA4 custom dimensions are already registered. The dashboard parser already handles these values correctly. No Lambda/API changes needed.

---

**User Approval Required Before Implementation**
