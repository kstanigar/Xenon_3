# Black Background Implementation Plan
**Date:** April 12, 2026
**Status:** ✅ COMPLETE - Implemented April 12, 2026
**Effort:** 5 minutes

---

## Overview
Add semi-transparent black backgrounds to game over and victory screens for better readability and visual polish.

---

## Implementation

### Files to Modify
1. `game.html` - Desktop CSS
2. `game_mobile.html` - Mobile CSS

### CSS Changes

**#gameOver styling (both files):**
```css
#gameOver {
  display: none;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 24px;
  color: #00FFFF;
  text-shadow: 0 0 10px #00FFFF;
  text-align: center;
  line-height: 1.6;
  background: rgba(0, 0, 0, 0.92);  /* Semi-transparent black */
  padding: 40px;                     /* Breathing room */
  border-radius: 12px;               /* Rounded corners */
  box-shadow: 0 0 30px rgba(0, 255, 255, 0.2);  /* Subtle cyan glow */
}
```

**#victory styling (both files):**
```css
#victory {
  display: none;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 18px;
  color: #00FFFF;
  text-shadow: 0 0 15px #00FFFF;
  z-index: 3;
  text-align: center;
  line-height: 1.4;
  max-width: 90%;
  width: 90%;
  padding: 40px;                     /* Match game over */
  background: rgba(0, 0, 0, 0.92);  /* Match game over */
  border-radius: 12px;               /* Match game over */
  box-shadow: 0 0 30px rgba(0, 255, 255, 0.2);  /* Match game over */
}
```

---

## Design Decisions

**Opacity: 92% (rgba 0.92)**
- Not fully opaque - allows subtle game canvas visibility
- Maintains sense of depth
- Better than 95% (too dark) or 85% (too transparent)
- Optimal for text readability + aesthetic

**Border Radius: 12px**
- Modern, polished look
- Not too rounded (maintains professional feel)
- Matches game's sci-fi aesthetic

**Box Shadow: Cyan Glow**
- Subtle `0 0 30px rgba(0, 255, 255, 0.2)`
- Matches existing cyan theme
- Adds depth without being distracting

**Padding: 40px**
- Prevents text from touching edges
- Creates clean, spacious layout
- Consistent with scorecard modal spacing

---

## Locations

**game.html:**
- Line ~343-353: #gameOver
- Line ~451-465: #victory

**game_mobile.html:**
- Same selectors (different line numbers)

---

## Testing Checklist
- [ ] Desktop game over screen (normal death) - **Requires manual browser testing**
- [ ] Desktop game over screen (dev mode Shift+G) - **Requires manual browser testing**
- [ ] Desktop victory screen - **Requires manual browser testing**
- [ ] Mobile game over screen (normal death) - **Requires manual browser testing**
- [ ] Mobile game over screen (dev mode Shift+G) - **Requires manual browser testing**
- [ ] Mobile victory screen - **Requires manual browser testing**
- [ ] Verify leaderboard displays correctly - **Requires manual browser testing**
- [ ] Verify scorecard modal displays correctly - **Requires manual browser testing**
- [ ] Check on different screen sizes - **Requires manual browser testing**

**Implementation Status (Apr 12, 2026):**
- ✅ CSS syntax validated (no diagnostics errors)
- ✅ game.html #gameOver updated (lines 353-357)
- ✅ game.html #victory updated (lines 469-473)
- ✅ game_mobile.html #gameOver updated
- ✅ game_mobile.html #victory updated
- ⏳ Manual browser testing pending

---

## Rollback
If issues occur, remove these properties:
- `background`
- `border-radius`
- `box-shadow`
- Adjust `padding` back to original (victory had 20px, game over had none)