# Hero Ship Color Purchase Feature

**Created:** June 1, 2026
**Status:** Planned
**Priority:** High
**Replaces:** Music Selector feature (marked irrelevant)

---

## Concept

**In-game purchase system allowing players to buy different hero ship colors.**

### Core Mechanic
- Players can purchase alternate hero ship skins/colors
- Shield color automatically matches hero ship color
- Maintains visual consistency (purple hero = purple shield)

### Current State
- **Default:** Blue hero ship + blue hero shield
- **System:** Shield color already coded to match ship in game logic

---

## Planned Color Options

### Purchasable Colors (TBD)
1. Purple hero ship + purple shield
2. Red hero ship + red shield
3. Green hero ship + green shield
4. Gold/Yellow hero ship + gold shield
5. Additional colors as designed

### Technical Requirements
- New .webp assets for each hero ship color variant
- Shield rendering already supports color matching
- Purchase system (Ko-fi integration or in-game currency)
- localStorage to save purchased colors
- Color selection UI (settings or shop menu)

---

## Implementation Notes

### Asset Creation
- Follow existing naming convention: `player_[color].webp`
- Match existing dimensions and sprite format
- Ensure consistent visual style with current blue hero

### Code Changes
- Add color selection to settings/shop
- Load appropriate hero sprite based on selection
- Shield color logic already exists (matches hero)
- Save selection to localStorage

### Monetization
- Ko-fi donation tiers could unlock colors
- Or in-game currency earned through gameplay
- Or one-time purchase unlock all colors

---

## Why This Replaces Music Selector

**Music Selector Issues:**
- Required 6 music files (large download)
- Limited player interest in music customization
- Most players use own music/mute game audio

**Hero Ship Colors Advantages:**
- Visual customization (more engaging)
- Monetization opportunity (support development)
- Smaller asset size (images vs audio files)
- More player expression/identity

---

## Priority Ranking

**High Priority** - Implements:
1. Player customization
2. Monetization path
3. Visual variety
4. Engagement feature

**Depends On:**
- Pink Infinite Level completion (higher priority)
- Phase 7 AWS deployment completion
- Security audit completion

---

## Related Features

### Shield Color Matching (Already Implemented)
**Current System:**
- Blue hero → blue shield (default)
- System can support any color combination
- Code location: game.html shield rendering logic

**Enhancement Needed:**
- Ensure shield color automatically updates when hero color changes
- Test all color combinations for visual clarity
- Verify shield visibility against all enemy colors (red, purple)

---

## Next Steps (When Ready to Implement)

1. Design color palette (5-7 colors)
2. Create hero ship .webp assets for each color
3. Test shield color rendering with new colors
4. Build color selection UI
5. Integrate with Ko-fi or payment system
6. Add to settings menu
7. Test localStorage persistence
8. Deploy to dev for testing

---

**Status:** Awaiting prioritization after Pink Infinite Level and security audit
**Estimated Effort:** Medium (2-3 sessions including asset creation)
**Impact:** High (monetization + player engagement)