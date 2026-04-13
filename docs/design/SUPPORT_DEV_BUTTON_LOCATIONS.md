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

**Location:** Lines 6781-6793

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

**Documentation:**
- Clear label comment added: "SUPPORT THE DEV BUTTON - Style changes planned"
- JSDoc comment references docs/design/SUPPORT_DEV_BUTTON_LOCATIONS.md

### Active Call Sites (Mobile)
**Status:** ✅ IMPLEMENTED (April 12, 2026)

**Location:** Line 6359 (inside `buildScorecardHTML()` function)

**Implementation:**
```javascript
html += '<div style="margin-top:16px; display:flex; gap:12px; justify-content:center; flex-wrap:wrap;">';
html += buildBugButtonHTML('scorecard');
html += buildKofiButtonHTML('scorecard'); // SUPPORT THE DEV BUTTON - Style changes planned
html += '</div>';
```

**Context:** Scorecard modal footer, matching desktop implementation at line 5755

---

## Style Update Checklist

When updating "Support the Dev" button styling:

- [ ] Update `game.html` line 6105-6107 (function definition)
- [ ] Update `game_mobile.html` function definition (once implemented)
- [ ] Verify scorecard modal displays correctly on desktop
- [ ] Verify scorecard modal displays correctly on mobile
- [ ] Test button click tracking (gtag `kofi_click` event)
- [ ] Update this documentation with new styling details

---

## Related Files

- `MEMORY.md` - Priority 4 documentation
- `game.html` - Desktop implementation
- `game_mobile.html` - Mobile implementation (pending)
- `buildScorecardHTML()` - Modal where button appears

---

## Future Styling (To Be Determined)

**Current:** Cyan background (#00FFFF), black text (#000)
**Future:** TBD - User will specify new styling

When new styling is defined, update this section with:
- New background color
- New text color
- Any other style changes (padding, border, font size, etc.)
- Date of change
- Reason for change