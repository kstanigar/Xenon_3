# Testing & Analytics Checklist
## Adaptive Difficulty Stage 1 + Health Remaining Bonus

**Implementation Date:** March 26, 2026
**Last Updated:** March 27, 2026 (invincibility frames increased to 1 second)
**Status:** ✅ CODE COMPLETE - ⚠️ TESTING IN PROGRESS
**Branch:** `feature/adaptive_difficulty_stage1`

**Recent Changes:**
- Mar 27, 2026: Invincibility frames increased from 30 frames (0.5s) to 60 frames (1s) for better shield cooldown feel (both files)

---

## 🚨 CRITICAL: DO NOT DEPLOY WITHOUT COMPLETING THIS CHECKLIST

---

## ⚠️ MANDATORY MOBILE DEVICE TESTING REQUIREMENT

**ALL TESTS MUST BE PERFORMED ON ACTUAL MOBILE DEVICES**

- ❌ Browser emulation/responsive mode is NOT sufficient
- ❌ Desktop browser with mobile viewport is NOT sufficient
- ✅ Testing on real iPhone/Android device is REQUIRED
- ✅ Use local IP address for mobile testing (e.g., `http://192.168.x.x:8080/game_mobile.html`)

**Rationale:** 81% of player deaths occur on mobile. Touch controls, performance, and timing behave differently on real devices vs emulation.

---

## 📋 PART 1: REQUIRED TESTING (Before PR)

### A. Baseline Testing - Verify No Gameplay Changes
**Goal:** Confirm game plays identically to production (all multipliers = 1.0)

**Desktop Testing:**
- [ ] Start local server: `python3 -m http.server 8080`
- [ ] Open `http://localhost:8080/game.html`
- [ ] Play through levels 1-4
- [ ] Verify enemy shields take 15 hits (not more/less)
- [ ] Verify bullet speed feels normal
- [ ] Verify player damage feels normal (25 HP per hit)
- [ ] Verify power-ups cycle: Shield → Laser → Health
- [ ] No console errors

**Mobile Testing:**
- [ ] Get local IP: `ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -1`
- [ ] Open on real device: `http://[LOCAL_IP]:8080/game_mobile.html`
- [ ] Play through levels 1-4
- [ ] Verify all behaviors match desktop
- [ ] Touch controls responsive
- [ ] 60 FPS maintained

**✅ Pass Criteria:** Game feels identical to production version

---

### B. Multiplier Console Testing - Verify Adjustments Work
**Goal:** Confirm multipliers actually affect gameplay when changed

**Setup:**
1. Press `Shift+D` to enable Developer Mode
2. Open browser console (F12 or Cmd+Opt+J)
3. Play to level 2 or 3

**Test 1: Make Game Easier**
```javascript
// Paste in console during gameplay:
DIFFICULTY_CONFIG.enemyHealth = 0.7;
DIFFICULTY_CONFIG.bulletSpeed = 0.8;
DIFFICULTY_CONFIG.playerDamage = 0.7;
DIFFICULTY_CONFIG.healthDropRate = 1.5;
```

**Verify:**
- [ ] Enemies die noticeably faster (fewer hits needed)
- [ ] Bullets move slower (easier to dodge)
- [ ] Player takes less damage per hit
- [ ] More health power-ups appear

**Test 2: Make Game Harder**
```javascript
// Paste in console:
DIFFICULTY_CONFIG.enemyHealth = 1.3;
DIFFICULTY_CONFIG.bulletSpeed = 1.2;
DIFFICULTY_CONFIG.playerDamage = 1.2;
DIFFICULTY_CONFIG.healthDropRate = 0.7;
```

**Verify:**
- [ ] Enemies take more hits to kill (tankier)
- [ ] Bullets move faster (harder to dodge)
- [ ] Player takes more damage per hit
- [ ] Fewer health power-ups appear

**Test 3: Reset to Normal**
```javascript
// Paste in console:
DIFFICULTY_CONFIG.enemyHealth = 1.0;
DIFFICULTY_CONFIG.bulletSpeed = 1.0;
DIFFICULTY_CONFIG.playerDamage = 1.0;
DIFFICULTY_CONFIG.healthDropRate = 1.0;
```

**Verify:**
- [ ] Game returns to normal difficulty

**✅ Pass Criteria:** All 6 multipliers visibly affect gameplay

---

### C. Health Remaining Bonus Testing
**Goal:** Verify health bonus added at victory and displayed correctly

**Test 1: High HP Victory (200 HP)**
1. Enable god mode: `Shift+I` in dev mode
2. Play through to Level 12 boss
3. Keep health at 200 HP
4. Defeat purple boss

**Verify:**
- [ ] "Victory! You Win!" message appears (3s)
- [ ] "Health Bonus: +200 pts!" appears 0.2s later (3.2s)
- [ ] Final score increases by 200 points
- [ ] Victory screen shows correct total score

**Test 2: Low HP Victory (50 HP)**
1. Play normally (no god mode)
2. Defeat purple boss with ~50 HP

**Verify:**
- [ ] "Health Bonus: +[~50] pts!" appears
- [ ] Score calculation correct

**Test 3: Edge Case - Very Low HP (10 HP)**
1. Intentionally take damage before final hit
2. Defeat boss with 5-15 HP

**Verify:**
- [ ] Small bonus shown (e.g., "+12 pts!")
- [ ] No errors in console
- [ ] Score calculation still correct

**✅ Pass Criteria:** Health bonus works at all HP ranges (10-200)

---

### D. Mobile-Specific Testing
**🚨 CRITICAL: Must test on ACTUAL MOBILE DEVICE (not browser emulation)**

**Why This Matters:**
- 81% of player deaths occur on mobile (from analytics)
- Touch latency, performance, and visual timing differ on real devices
- Browser emulation does NOT accurately represent mobile gameplay
- Invincibility frames timing critical for mobile touch controls

**Setup:**
- [ ] Start server: `python3 -m http.server 8080`
- [ ] Get local IP: `ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -1`
- [ ] Ensure Mac and mobile device on SAME WiFi network
- [ ] Open on real mobile device: `http://[LOCAL_IP]:8080/game_mobile.html`
- [ ] Example: `http://192.168.72.93:8080/game_mobile.html`

**Test on Real Device:**
- [ ] Baseline gameplay feels normal
- [ ] Invincibility frames work correctly (1 second blink after hit)
- [ ] Shield cooldown works (1 second between shield hits)
- [ ] Health bonus displays correctly at victory
- [ ] Bonus text doesn't overlap with touch controls
- [ ] No lag or performance issues
- [ ] All multipliers work via mobile browser console

**✅ Pass Criteria:** All features work on mobile as expected

---

### E. Final Syntax Check
```bash
python3 -c "
c = open('game.html').read()
print('game.html:')
print('  Brace diff:', c[c.find('<script>'):].count('{') - c[c.find('<script>'):].count('}'))
print('  DIFFICULTY_CONFIG:', 'DIFFICULTY_CONFIG' in c)
print('  healthBonus:', 'healthBonus' in c)
print()
c = open('game_mobile.html').read()
print('game_mobile.html:')
print('  Brace diff:', c[c.find('<script>'):].count('{') - c[c.find('<script>'):].count('}'))
print('  DIFFICULTY_CONFIG:', 'DIFFICULTY_CONFIG' in c)
print('  healthBonus:', 'healthBonus' in c)
"
```

**Expected:**
- [ ] Brace diff: 0 (both files)
- [ ] DIFFICULTY_CONFIG: True (both files)
- [ ] healthBonus: True (both files)

**✅ Pass Criteria:** All checks return expected values

---

## 📊 PART 2: REQUIRED ANALYTICS SETUP (Before Deploy)

### A. Register GA4 Custom Dimension
**Location:** Google Analytics 4 → Admin → Custom Definitions → Custom Dimensions

**Steps:**
1. [ ] Click "Create custom dimension"
2. [ ] Fill in:
   - **Dimension name:** `health_remaining_bonus`
   - **Scope:** Event
   - **Description:** "Health points remaining when player defeats purple boss (level 12). Used to track victory health bonus feature."
   - **Event parameter:** `health_remaining_bonus`
3. [ ] Click "Save"
4. [ ] Wait 24 hours for dimension to process

---

### B. Verify in GA4 DebugView
**Steps:**
1. [ ] Open game in Chrome
2. [ ] Enable GA4 DebugView (install extension if needed)
3. [ ] Play through to victory (use god mode for speed)
4. [ ] Defeat purple boss
5. [ ] Check DebugView for `player_won` event
6. [ ] Confirm `health_remaining_bonus` parameter appears
7. [ ] Verify value matches HP remaining (e.g., 127)
8. [ ] Verify value range: 0-250 (never negative)

**✅ Pass Criteria:** Parameter appears in DebugView with correct value

---

### C. Update GA4 Explorations (Optional but Recommended)

**Create New Exploration: "Victory Health Bonus Analysis"**
1. [ ] GA4 → Explore → Create New Exploration
2. [ ] Name: "Victory Health Bonus Analysis"
3. [ ] Filter: `event_name = player_won`

**Tab 1: Average Bonus by Platform**
- Rows: `platform`
- Values: `avg(health_remaining_bonus)`
- Secondary dimension: `score_multiplier`

**Tab 2: Bonus Distribution**
- Rows: `health_remaining_bonus` (create bins: 0-50, 51-100, 101-150, 151-200+)
- Values: `event_count`

**Tab 3: Correlation Analysis**
- Scatter chart: X = `health_remaining_bonus`, Y = `score`
- Shows: Do higher bonuses = higher total scores?

**✅ Pass Criteria:** Exploration created and shows data after 48 hours

---

## 📈 PART 3: POST-DEPLOY MONITORING (First 48 Hours)

### A. Realtime Verification
- [ ] GA4 → Reports → Realtime
- [ ] Filter: `event_name = player_won`
- [ ] Verify events appear with `health_remaining_bonus` parameter
- [ ] Check value range: 0-250
- [ ] Typical values: 50-150 (most players don't finish at full HP)

### B. Error Monitoring
- [ ] Check browser console logs (no errors during gameplay)
- [ ] Check GA4 for anomalies (e.g., negative values, values > 250)
- [ ] Monitor Discord/support channels for player reports

### C. Data Quality Check (After 1 Week)
**Key Questions to Answer:**
1. [ ] What's the median `health_remaining_bonus`? (indicates difficulty balance)
2. [ ] Desktop vs mobile: Which platform has higher average bonuses?
3. [ ] Does `health_remaining_bonus` correlate with `score`? (higher bonus = higher score?)
4. [ ] Does `health_remaining_bonus` correlate with `session_duration_seconds`? (fast vs safe play?)

---

## 📁 FILES MODIFIED (This Branch)

**Code Changes:**
- ✅ `game.html` - Stage 1 multipliers (7 locations) + health bonus (4 lines)
- ✅ `game_mobile.html` - Stage 1 multipliers (7 locations) + health bonus (4 lines)

**Documentation:**
- ✅ `NON-X_PAIM_Memory.md` - Full feature documentation + testing notes
- ✅ `ADAPTIVE_DIFFICULTY_DESIGN.md` - Updated with implementation status + testing guide
- ✅ `TESTING_CHECKLIST.md` - This file (handoff document)

---

## 🎯 SUMMARY FOR NEXT SESSION

### What Was Completed (Mar 26, 2026):
1. ✅ **Stage 1: Multiplier Infrastructure**
   - Added `DIFFICULTY_CONFIG` object with 6 multipliers
   - Applied to 6 code locations in both files
   - All multipliers default to 1.0 (no gameplay changes)

2. ✅ **Health Remaining Bonus Feature**
   - Victory adds remaining HP to score (1:1 ratio)
   - Visual announcement: "Health Bonus: +[amount] pts!"
   - Analytics tracking: `health_remaining_bonus` parameter

3. ✅ **Documentation Complete**
   - NON-X_PAIM_Memory.md updated
   - ADAPTIVE_DIFFICULTY_DESIGN.md updated
   - Testing checklist created

### What Needs to Be Done:
1. ⏸️ **Complete all testing** (Parts 1A-1E above) - ~2-3 hours
2. ⏸️ **Set up GA4 analytics** (Part 2) - ~15 minutes
3. ⏸️ **Create PR and merge** (after testing passes)
4. ⏸️ **Monitor post-deploy** (Part 3) - First 48 hours

### Branch Status:
- **Branch:** `feature/adaptive_difficulty_stage1`
- **Uncommitted changes:** None (if committed) OR 3 files (if not committed)
- **Ready for:** Testing → PR → Deploy

### Estimated Time to Complete:
- Testing: 2-3 hours (includes desktop + mobile)
- GA4 setup: 15 minutes
- PR creation: 5 minutes
- **Total:** ~3 hours

---

## 🤖 FOR NEXT AI SESSION

**Quick Start Checklist:**
1. Read this file (TESTING_CHECKLIST.md)
2. Read NON-X_PAIM_Memory.md (Health Remaining Bonus section)
3. Review ADAPTIVE_DIFFICULTY_DESIGN.md Section 3.3 (detailed testing guide)
4. Start with Part 1A (Baseline Testing)
5. Work through checklist sequentially
6. Report any test failures to user immediately

**Key Files to Review:**
- `/Users/keithstanigar/Documents/Projects/Xenon_3/TESTING_CHECKLIST.md` (this file)
- `/Users/keithstanigar/Documents/Projects/Xenon_3/NON-X_PAIM_Memory.md` (lines ~1197-1350)
- `/Users/keithstanigar/Documents/Projects/Xenon_3/ADAPTIVE_DIFFICULTY_DESIGN.md` (Section 3.3)

**Testing Command:**
```bash
# Start local server for testing
cd /Users/keithstanigar/Documents/Projects/Xenon_3
python3 -m http.server 8080

# Get local IP for mobile testing
ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -1
```

---

**Last Updated:** March 26, 2026
**Next Session:** Testing & Analytics Setup
**Estimated Completion:** 3 hours