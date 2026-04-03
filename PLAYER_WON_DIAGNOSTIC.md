# player_won Event Diagnostic Report
**Date:** April 3, 2026
**Issue:** player_won event not appearing in GA4 DebugView
**Status:** Diagnostic logging added, awaiting test results

---

## Problem Summary

During GA4 DebugView testing, the following events were observed:
- ✅ `ai_difficulty_adjusted` events firing correctly (2 occurrences)
- ✅ `game_complete` events firing correctly (2 occurrences)
- ❌ `player_won` event NOT appearing in DebugView

**Expected behavior:** When player defeats all 3 bosses, both `player_won` and `game_complete` should fire in sequence.

---

## Code Analysis

### Location: showVictory() function
- **game_mobile.html:** Lines 6219-6230 (player_won), Line 6233 (game_complete)
- **game.html:** Lines 5592-5603 (player_won), Line 5607 (game_complete)

### Event Firing Sequence:
```javascript
// 1. Calculate tier multipliers
var tierMult = getTierMultiplier();           // 0.50 to 1.75
var effectiveMult = tierMult * scoreMultiplier; // Combined multiplier

// 2. Fire player_won event
fireEvent('player_won', {
  'tier': currentTier,
  'tier_multiplier': tierMult,
  'movement_multiplier': scoreMultiplier,
  'effective_multiplier': effectiveMult,
  // ... other parameters
});

// 3. Fire game_complete event (14 lines later)
fireEvent('game_complete', {
  'outcome': 'victory',
  // ... other parameters
});
```

**Key Finding:** Both events fire sequentially with no conditional logic between them. If `game_complete` appears in GA4, then `player_won` must have been called first.

---

## Possible Causes

### 1. JavaScript Error in player_won Parameters
- **Symptom:** Invalid parameter value causes silent failure
- **Likely culprits:**
  - `tierMult` = undefined (if TIER_CONFIG missing current tier)
  - `effectiveMult` = NaN (if scoreMultiplier undefined)
  - `gameSessionStart` = null causing calculation error

### 2. GA4 Event Rejection
- **Symptom:** Event sent to GA4 but rejected server-side
- **Possible reasons:**
  - Event name "player_won" flagged by spam filters
  - Parameter value exceeds GA4 limits
  - Rate limiting or sampling

### 3. Dev Mode Enabled
- **Symptom:** Events logged to console instead of GA4
- **Check:** Dev mode suppresses all fireEvent calls (line 1063-1070)
- **Note:** This doesn't match user observation (other events appear in DebugView)

### 4. Timing Issue
- **Symptom:** Event fires but DebugView not actively monitoring
- **Note:** Unlikely since ai_difficulty_adjusted from same session appeared

---

## Diagnostic Changes Made (Apr 3, 2026)

Added console logging around player_won event in both game files:

```javascript
// Before player_won fireEvent
console.log('[VICTORY] About to fire player_won event');
console.log('[VICTORY] tierMult:', tierMult, 'scoreMultiplier:', scoreMultiplier, 'effectiveMult:', effectiveMult);

fireEvent('player_won', { /* parameters */ });

// After player_won fireEvent
console.log('[VICTORY] player_won event fired successfully');
```

**Commit:** `0673e65` - "debug: add console logging for player_won event diagnostics"
**Branch:** feature/ai_agent_v1

---

## Next Steps for User

### Step 1: Deploy Diagnostic Version
Since this is a feature branch, you need to merge to main or test directly from feature branch:

**Option A: Test on feature branch (faster)**
```bash
# If GitHub Pages supports branch deployment
# Navigate to: Settings → Pages → Source → feature/ai_agent_v1
```

**Option B: Merge to main (recommended)**
```bash
git checkout main
git merge feature/ai_agent_v1
git push origin main
```

### Step 2: Open Browser Console
1. Open the game URL in Chrome
2. Press **F12** or **Cmd+Option+I** (Mac) to open DevTools
3. Click **Console** tab
4. Keep console open during gameplay

### Step 3: Play Through to Victory
1. Start a new game
2. Use god mode (Shift+I) to beat all 3 bosses quickly
3. When victory screen appears, check console for logs

### Step 4: Analyze Console Output

**Expected output (if working correctly):**
```
[VICTORY] About to fire player_won event
[VICTORY] tierMult: 1.2 scoreMultiplier: 1.25 effectiveMult: 1.5
[VICTORY] player_won event fired successfully
```

**If you see JavaScript errors:**
- Copy the full error message
- Note which line number it occurs on
- This tells us exactly what's failing

**If you see NaN or undefined values:**
- This explains why GA4 rejects the event
- We'll need to fix the calculation

**If you DON'T see the logs at all:**
- The showVictory() function isn't being called
- Or there's an earlier error preventing code execution

### Step 5: Check DebugView Again
1. Keep DebugView open: **Admin → Property settings → Data display → DebugView**
2. Play through to victory (with console open)
3. Check if player_won appears now

### Step 6: Check Dev Mode Status
In console, type:
```javascript
localStorage.getItem('nonx_dev_mode')
```

**Result:**
- `'true'` → Dev mode is ON (all events suppressed!)
- `'false'` or `null` → Dev mode is OFF (events sent to GA4)

**If dev mode is ON, turn it OFF:**
1. Press **Shift+D** twice (toggle off, then on shows indicator)
2. Verify badge disappears from top-left
3. Or manually clear: `localStorage.removeItem('nonx_dev_mode')`

---

## What This Will Tell Us

| Console Output | DebugView Result | Diagnosis |
|----------------|------------------|-----------|
| ✅ All logs appear, valid values | ❌ No player_won | **GA4 rejection** - event sent but filtered |
| ✅ Logs appear, NaN/undefined | ❌ No player_won | **Invalid parameters** - need to fix calculation |
| ❌ No logs at all | ❌ No player_won | **Code not executing** - earlier error in showVictory() |
| ✅ [DEV MODE] suppressed logs | ❌ No player_won | **Dev mode enabled** - turn off and retry |
| ✅ All logs appear, valid values | ✅ player_won appears | **Issue resolved!** |

---

## If Issue Persists After Diagnostic

### Fallback Option: Rename Event
If GA4 is filtering "player_won", try alternative names:
- `victory_complete`
- `game_victory`
- `boss_all_defeated`

### Check GA4 Event Registration
Navigate to: **Admin → Data display → Events**
- Check if "player_won" appears in event list
- If not, it might need manual registration

### Verify gtag Installation
In console, type:
```javascript
typeof gtag
```

**Expected:** `"function"`
**If undefined:** gtag not loaded, analytics broken entirely

---

## Files Modified

- ✅ `game_mobile.html` - Added diagnostic logging (lines 6220-6222, 6232)
- ✅ `game.html` - Added diagnostic logging (lines 5595-5597, 5605)

---

## Related Documentation

- GA4 Custom Dimensions: See NON-X_PAIM_Memory.md Section 21
- AI Agent Implementation: See /Users/keithstanigar/.claude/plans/quiet-brewing-deer.md
- Tier-Based Scoring: See TIER_BASED_SCORING_DESIGN.md

---

**Next Update:** After user runs diagnostic test and provides console output