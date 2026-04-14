# Support the Dev Button - Code Locations Reference

**Date Created:** April 12, 2026
**Purpose:** Document all locations where "Support the Dev" (Ko-fi) button styling exists for future style changes

---

## ⚠️ IMPORTANT: Style Changes Planned

The "Support the Dev" button will undergo style changes soon. This document tracks all locations where the button code exists to ensure updates are applied consistently across desktop and mobile.

---

## Desktop Implementation (game.html)

### Function Definition
**Location:** game.html lines 6105-6107

```javascript
function buildKofiButtonHTML(source) {
  return "<a href='https://ko-fi.com/raginats' target='_blank' onclick=\"if(typeof gtag !== 'undefined') gtag('event', 'kofi_click', {location: '" + source + "' });\" style='display: inline-block; padding: 10px 20px; font-size: 14px; border-radius: 4px; border: none; background: #00FFFF; color: #000; cursor: pointer; text-decoration: none; font-weight: bold;'>☕ Support the Dev</a>";
}
```

**Current Styling (Desktop):**
- Background: `#00FFFF` (cyan)
- Text color: `#000` (black)
- Padding: `10px 20px`
- Font size: `14px`
- Border radius: `4px`
- Font weight: `bold`

### Active Call Sites (Desktop)
1. **Line 5755** - Scorecard modal footer (`buildScorecardHTML()` function)
   - Context: Called with `buildKofiButtonHTML('scorecard')`
   - Active: ✅ Currently in use

### Commented Out Call Sites (Desktop)
These were removed during button consolidation (April 2026):
- Line 5902 - Victory screen (commented out)
- Line 6228 - Rebuild game over (commented out)
- Line 6990 - Normal game over (commented out)
- Line 7312 - Dev mode game over (commented out)

---

## Mobile Implementation (game_mobile.html)

### Function Definition
**Status:** ✅ IMPLEMENTED (April 12, 2026)
**Last Updated:** April 13, 2026 (location audit)

**Location:** Lines 6808-6810

```javascript
function buildKofiButtonHTML(source) {
  return "<a href='https://ko-fi.com/raginats' target='_blank' onclick=\"if(typeof gtag !== 'undefined') gtag('event', 'kofi_click', {location: '" + source + "'});\" style='display: inline-block; padding: 10px 20px; font-size: 14px; border-radius: 4px; border: none; background: #00FFFF; color: #000; cursor: pointer; text-decoration: none; font-weight: bold;'>☕ Support the Dev</a>";
}
```

**Current Styling (Mobile):**
- Background: `#00FFFF` (cyan) - Matches desktop ✅
- Text color: `#000` (black) - Matches desktop ✅
- Padding: `10px 20px` - Matches desktop ✅
- Font size: `14px` - Matches desktop ✅
- Border radius: `4px` - Matches desktop ✅
- Font weight: `bold` - Matches desktop ✅
- Label: `☕ Support the Dev` - Matches desktop ✅

**Documentation:**
- Clear label comment added: "SUPPORT THE DEV BUTTON - Style changes planned"
- JSDoc comment references docs/design/SUPPORT_DEV_BUTTON_LOCATIONS.md
- Full JSDoc at lines 6797-6807

### Active Call Sites (Mobile)
**Status:** ✅ IMPLEMENTED (April 12, 2026)

**Location:** Line 6354 (inside `buildScorecardHTML()` function)

**Implementation:**
```javascript
html += '<div style="margin-top:16px; display:flex; gap:12px; justify-content:center; flex-wrap:wrap;">';
html += buildBugButtonHTML('scorecard');
html += buildKofiButtonHTML('scorecard'); // SUPPORT THE DEV BUTTON - Style changes planned
html += '</div>';
```

**Context:** Scorecard modal footer, matching desktop implementation at line 5755

### Removed Call Sites (Mobile)
These were removed during button consolidation (April 2026):
- Line 6527 - Victory screen (documentation comment)
- Line 6873 - Normal game over (documentation comment)
- Line 7661 - Rebuild game over (documentation comment)

---

## "Keep the Lights On" Button Redesign Plan

**Priority:** #1 (Next Session)
**Target Implementation:** April 13-14, 2026

### New Design Specification

**Label Change:**
- Current: `☕ Support the Dev`
- New: `⚡ Keep the Lights On`

**Color Palette:**
- Current: Cyan `#00FFFF`
- New: Hazard Yellow `#FFD700`

**Animation:**
- Add "dying neon" flicker effect with box-shadow transitions
- Opacity range: 65%-100% (subtle brownout, not blackout)
- Timing: 3 flickers in 1.5s, then stable 6.5s (8s loop)
- Stepped transitions (no soft fades)

**Hover State:**
- Animation pauses (stabilizes)
- Increased glow on hover

### Style Update Checklist

When implementing "Keep the Lights On" button:

- [ ] Update CSS @keyframes hazard-flicker (add box-shadow transitions)
- [ ] Update `game.html` line 6105-6107 (function definition)
- [ ] Update `game_mobile.html` line 6808-6810 (function definition)
- [ ] Change label: "☕ Support the Dev" → "⚡ Keep the Lights On"
- [ ] Change colors: cyan (#00FFFF) → yellow (#FFD700)
- [ ] Add hover stabilization logic
- [ ] Verify scorecard modal displays correctly on desktop
- [ ] Verify scorecard modal displays correctly on mobile
- [ ] Test flicker animation in browser
- [ ] Test button click tracking (gtag `kofi_click` event)
- [ ] Update this documentation with final styling details
- [ ] Update MEMORY.md with narrative rationale

---

## Related Files

- `MEMORY.md` - Priority 4 documentation
- `game.html` - Desktop implementation
- `game_mobile.html` - Mobile implementation (pending)
- `buildScorecardHTML()` - Modal where button appears

---

## Planned Styling - "Keep the Lights On" Narrative

**Current (April 13, 2026):**
- Background: `#00FFFF` (cyan)
- Text: `#000` (black)
- Label: `☕ Support the Dev`
- Animation: hazard-flicker (opacity only)

**Planned (Target: April 13-14, 2026):**
- Background: `rgba(255, 215, 0, 0.15)` (hazard yellow, 15% opacity)
- Text: `#FFD700` (gold)
- Border: `2px solid #FFD700`
- Label: `⚡ Keep the Lights On`
- Animation: hazard-flicker with box-shadow transitions (65%-100% opacity range)
- Hover: Animation pause, increased glow

**Design Rationale:**
The "Keep the Lights On" redesign creates a narrative-driven UI where the button's visual state reflects the real-world project status. The "dying neon" flicker effect transforms the tip request from a static transaction into an immersive experience where the player feels they are literally providing the "electricity" needed to keep the software running.

**Animation Specification:**
```css
@keyframes hazard-flicker {
  0%, 100% {
    opacity: 1;
    box-shadow: 0 0 15px rgba(255, 215, 0, 0.3);
  }
  12.5% {
    opacity: 0.75;
    box-shadow: 0 0 8px rgba(255, 215, 0, 0.15);
  }
  13% {
    opacity: 1;
    box-shadow: 0 0 15px rgba(255, 215, 0, 0.3);
  }
  14.5% {
    opacity: 0.7;
    box-shadow: 0 0 5px rgba(255, 215, 0, 0.1);
  }
  15% {
    opacity: 1;
    box-shadow: 0 0 15px rgba(255, 215, 0, 0.3);
  }
  16.5% {
    opacity: 0.65;
    box-shadow: 0 0 3px rgba(255, 215, 0, 0.05);
  }
  17% {
    opacity: 1;
    box-shadow: 0 0 15px rgba(255, 215, 0, 0.3);
  }
}
```

**Narrative Elements:**
- "Almost going out" opacity (65% minimum, not aggressive)
- Stepped transitions (electrical arcing, not soft fades)
- Hover stabilization (player attention "fixes" the power issue)
- Precision-engineered aesthetic (sharp, intentional)

**Implementation Date:** TBD
**Reason:** Create emotional connection through "power failure" metaphor and environmental storytelling

---

## ✅ Phase 2 Implementation Complete (April 13, 2026)

**Status:** ✅ COMPLETE - All 8 "Player Intel & Power" buttons now static (no animation)

**Implementation Date:** April 13, 2026
**Task:** Remove animation from all 8 "Player Intel & Power" buttons per 21-task checklist Phase 2

### Changes Applied:

**Desktop (game.html) - 4 Buttons:**
- ✅ Line 5907 - Victory screen button - Removed `class='hazard-flicker'` and `animation: hazard-flicker 8s infinite steps(1)`
- ✅ Line 6232 - Rebuild game over button - Removed `class='hazard-flicker'` and `animation: hazard-flicker 8s infinite steps(1)`
- ✅ Line 6993 - Normal game over button - Removed `class='hazard-flicker'` and `animation: hazard-flicker 8s infinite steps(1)`
- ✅ Line 7322 - Dev mode game over button - Removed `class='hazard-flicker'` and `animation: hazard-flicker 8s infinite steps(1)`

**Mobile (game_mobile.html) - 4 Buttons:**
- ✅ Line 6534 - Victory screen button - Removed `class='hazard-flicker'` and `animation: hazard-flicker 8s infinite steps(1)`
- ✅ Line 6882 - Rebuild game over button - Removed `class='hazard-flicker'` and `animation: hazard-flicker 8s infinite steps(1)`
- ✅ Line 7667 - Normal game over button - Removed `class='hazard-flicker'` and `animation: hazard-flicker 8s infinite steps(1)`
- ✅ Line 7866 - Dev mode game over button - Removed `class='hazard-flicker'` and `animation: hazard-flicker 8s infinite steps(1)`

### Result:

**Player Intel & Power Buttons (8 total):**
- ✅ Completely static (no animation)
- ✅ Yellow theme preserved (#FFD700 color, golden background, golden border)
- ✅ Professional, clean appearance

**Ko-fi "Keep the Lights On" Buttons (2 total):**
- ✅ Animated with 4 aggressive flickers (30%-100% opacity)
- ✅ Box-shadow transitions for "dying neon" effect
- ✅ Hover stabilization (animation pauses)

### Design Rationale:

**Visual Narrative:**
- **Player Intel & Power** = Static warning (early alert, no urgency)
- **Keep the Lights On** = Animated critical state (power failure, urgent action needed)

**Result:** Clear visual separation between warning (static) and critical (animated) states creates intuitive user experience and emotional connection to "keep the software running" narrative.

### Testing Required:

- [ ] Desktop: Victory screen - Verify Player Intel button is static
- [ ] Desktop: Game over screens (normal/rebuild/dev mode) - Verify Player Intel button is static
- [ ] Desktop: Scorecard modal - Verify Ko-fi button is animated
- [ ] Mobile: Victory screen - Verify Player Intel button is static
- [ ] Mobile: Game over screens (normal/rebuild/dev mode) - Verify Player Intel button is static
- [ ] Mobile: Scorecard modal - Verify Ko-fi button is animated
- [ ] Animation quality: 4 flickers, not too gimmicky, 30%-100% opacity
- [ ] Hover stabilization works on Ko-fi button