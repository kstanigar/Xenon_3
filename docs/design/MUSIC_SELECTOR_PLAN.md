# Music Selector Feature - Implementation Plan

**Status:** Planned (implement AFTER AWS migration)
**Priority:** Post-launch polish feature
**Effort:** 2.5 hours
**Date Created:** April 12, 2026

---

## Overview

Add a music selection system allowing players to choose from 3 background music tracks before starting gameplay. The selector will be located on the How-to Play screen as an accordion under the Difficulty section.

---

## Music Tracks (Option A)

### **Levels 1-12 (Player Choice):**
1. **NonexFullSong.mp3** (4.4MB) - Original, familiar soundtrack
2. **VoidOfEchoes.mp3** (2.6MB) - Atmospheric, darker vibe
3. **Rift.mp3** (3.7MB) - Energetic, upbeat

**Total:** 10.7MB (optimized, reasonable load time)

### **Pink Levels 13-15 (Auto-play):**
- **Ximer_EE.mp3** (2.4MB) - Specialty track for Pink phase

---

## UI/UX Design

### **Location:**
- **Screen:** How-to Play (index.html)
- **Position:** Under "Difficulty" section
- **Format:** Accordion (collapsible section)

### **Accordion Design:**
```
▼ Music Selection
  ○ NonexFullSong (Original) [▶ Preview]
  ○ VoidOfEchoes (Atmospheric) [▶ Preview]
  ○ Rift (Energetic) [▶ Preview]
```

**Collapsed by default** - Player clicks to expand

### **Features:**
- Radio buttons (single selection)
- Preview button plays 10-second clip
- Selection saved to localStorage
- Default: NonexFullSong (original)

---

## Implementation Details

### **Phase 1: Add Accordion to How-to Play Screen** (1.5 hours)

**File:** index.html (How-to Play modal)

**Add after Difficulty section:**
```html
<!-- Music Selection Accordion -->
<div class="accordion-section" style="margin-top: 16px;">
  <button class="accordion-header" onclick="toggleAccordion('musicSelector')">
    <span>🎵 Music Selection</span>
    <span class="accordion-icon">▼</span>
  </button>

  <div id="musicSelector" class="accordion-content" style="display: none;">
    <p style="color: #aaa; margin-bottom: 12px;">
      Choose your background music for gameplay:
    </p>

    <div style="display: flex; flex-direction: column; gap: 12px;">
      <label style="display: flex; align-items: center; gap: 8px; cursor: pointer;">
        <input type="radio" name="bgMusic" value="NonexFullSong" checked>
        <span>NonexFullSong (Original)</span>
        <button
          onclick="previewMusic('NonexFullSong'); event.stopPropagation();"
          style="margin-left: auto; padding: 4px 12px; background: #555; border: none; color: #fff; cursor: pointer; border-radius: 4px;">
          ▶ Preview
        </button>
      </label>

      <label style="display: flex; align-items: center; gap: 8px; cursor: pointer;">
        <input type="radio" name="bgMusic" value="VoidOfEchoes">
        <span>Void of Echoes (Atmospheric)</span>
        <button
          onclick="previewMusic('VoidOfEchoes'); event.stopPropagation();"
          style="margin-left: auto; padding: 4px 12px; background: #555; border: none; color: #fff; cursor: pointer; border-radius: 4px;">
          ▶ Preview
        </button>
      </label>

      <label style="display: flex; align-items: center; gap: 8px; cursor: pointer;">
        <input type="radio" name="bgMusic" value="Rift">
        <span>Rift (Energetic)</span>
        <button
          onclick="previewMusic('Rift'); event.stopPropagation();"
          style="margin-left: auto; padding: 4px 12px; background: #555; border: none; color: #fff; cursor: pointer; border-radius: 4px;">
          ▶ Preview
        </button>
      </label>
    </div>
  </div>
</div>
```

**Accordion Toggle Function:**
```javascript
function toggleAccordion(id) {
  var content = document.getElementById(id);
  var isVisible = content.style.display === 'block';
  content.style.display = isVisible ? 'none' : 'block';

  // Update icon
  var icon = event.target.querySelector('.accordion-icon');
  if (icon) icon.textContent = isVisible ? '▼' : '▲';
}
```

---

### **Phase 2: Preview System** (30 minutes)

**Global preview audio object:**
```javascript
var previewAudio = null;

function previewMusic(songName) {
  // Stop current preview
  if (previewAudio) {
    previewAudio.pause();
    previewAudio.currentTime = 0;
  }

  // Play new preview (10 seconds)
  previewAudio = new Audio('assets/audio/music/' + songName + '.mp3');
  previewAudio.volume = 0.5;
  previewAudio.play();

  // Stop after 10 seconds
  setTimeout(() => {
    if (previewAudio) {
      previewAudio.pause();
      previewAudio.currentTime = 0;
    }
  }, 10000);

  // Track preview usage
  fireEvent('music_preview_clicked', {
    song_name: songName
  });
}
```

**Save selection when changed:**
```javascript
document.querySelectorAll('input[name="bgMusic"]').forEach(radio => {
  radio.addEventListener('change', (e) => {
    localStorage.setItem('nonx_selected_music', e.target.value);

    fireEvent('music_selected', {
      song_name: e.target.value
    });
  });
});
```

**Load saved selection on page load:**
```javascript
window.addEventListener('load', () => {
  var savedMusic = localStorage.getItem('nonx_selected_music');
  if (savedMusic) {
    var radio = document.querySelector(`input[name="bgMusic"][value="${savedMusic}"]`);
    if (radio) radio.checked = true;
  }
});
```

---

### **Phase 3: Game Integration** (30 minutes)

**Files:** game.html + game_mobile.html

**Current code (find ~line 857 in game_mobile.html, ~920 in game.html):**
```javascript
var bgMusic = new Audio("assets/audio/music/NonexFullSong.mp3");
```

**Replace with:**
```javascript
// Load player's selected music (defaults to NonexFullSong)
var selectedMusic = localStorage.getItem('nonx_selected_music') || 'NonexFullSong';
var bgMusic = new Audio("assets/audio/music/" + selectedMusic + ".mp3");
```

**Both files updated identically.**

---

### **Phase 4: Pink Level Specialty Track** (15 minutes)

**DEFERRED until Pink Levels (13-15) are implemented**

**Logic to add when ready:**
```javascript
// In advanceLevel() function
if (level === 13 && !pinkPhase) {
  pinkPhase = true;

  // Stop current music
  bgMusic.pause();

  // Switch to Pink level specialty track
  bgMusic = new Audio("assets/audio/music/Ximer_EE.mp3");
  bgMusic.loop = true;
  bgMusic.volume = 0.79;

  if (musicEnabled) {
    bgMusic.play();
  }

  // Analytics
  fireEvent('pink_music_started', {
    level: level,
    tier: currentTier
  });
}
```

---

### **Phase 5: Analytics Tracking** (15 minutes)

**New events to track:**

1. **music_selected** - Player chooses a song
```javascript
{
  song_name: 'NonexFullSong' | 'VoidOfEchoes' | 'Rift',
  analytics_version: '4.3'
}
```

2. **music_preview_clicked** - Player previews a song
```javascript
{
  song_name: 'NonexFullSong' | 'VoidOfEchoes' | 'Rift',
  analytics_version: '4.3'
}
```

3. **pink_music_started** - Pink level music triggered (future)
```javascript
{
  level: 13,
  tier: currentTier,
  analytics_version: '4.3'
}
```

---

## Implementation Timeline

### **Estimated Effort: 2.5 hours**

| Phase | Task | Time |
|-------|------|------|
| 1 | Add accordion to How-to Play | 1.5 hours |
| 2 | Preview system | 30 min |
| 3 | Game integration | 30 min |
| 4 | Pink level track (deferred) | 15 min |
| 5 | Analytics tracking | 15 min |
| **Total** | | **2.5 hours** |

---

## Testing Checklist

### **Pre-Testing:**
- [ ] All 3 music files exist in `assets/audio/music/`
- [ ] File sizes verified (10.7MB total)
- [ ] Ximer_EE.mp3 present (for future Pink levels)

### **Accordion Functionality:**
- [ ] Music Selection accordion appears under Difficulty
- [ ] Accordion collapsed by default
- [ ] Clicking header expands/collapses section
- [ ] Icon changes (▼ ↔ ▲)

### **Music Selection:**
- [ ] 3 radio buttons display correctly
- [ ] Only 1 radio button selectable at a time
- [ ] Default: NonexFullSong checked
- [ ] Selection saved to localStorage
- [ ] Selection persists after page refresh

### **Preview System:**
- [ ] Clicking "Preview" plays 10-second clip
- [ ] Preview stops after 10 seconds
- [ ] Clicking new preview stops current preview
- [ ] Preview volume at 0.5 (not too loud)
- [ ] Preview doesn't affect main menu music (if any)

### **Game Integration (Desktop):**
- [ ] Desktop game loads selected music
- [ ] Music loops correctly
- [ ] Music volume at 0.79
- [ ] Pause button works
- [ ] Mute toggle works
- [ ] Selection persists across game sessions

### **Game Integration (Mobile):**
- [ ] Mobile game loads selected music
- [ ] Music loops correctly
- [ ] Music volume at 0.79
- [ ] Pause button works
- [ ] Mute toggle works
- [ ] Selection persists across game sessions

### **Analytics:**
- [ ] `music_selected` event fires when selection changed
- [ ] `music_preview_clicked` event fires on preview click
- [ ] Events appear in GA4 DebugView
- [ ] analytics_version: '4.3' included

### **Cross-Browser:**
- [ ] Works in Chrome
- [ ] Works in Firefox
- [ ] Works in Safari
- [ ] Works on mobile browsers

---

## localStorage Schema

```javascript
// Music selection
nonx_selected_music: 'NonexFullSong' | 'VoidOfEchoes' | 'Rift'

// Default if not set
if (!localStorage.getItem('nonx_selected_music')) {
  localStorage.setItem('nonx_selected_music', 'NonexFullSong');
}
```

---

## File Structure

```
assets/audio/music/
├── NonexFullSong.mp3    # 4.4MB - Original (always available)
├── VoidOfEchoes.mp3     # 2.6MB - Atmospheric (always available)
├── Rift.mp3             # 3.7MB - Energetic (always available)
├── Ximer_EE.mp3         # 2.4MB - Pink Levels 13-15 (auto-play)
├── SystemOverload.mp3   # 3.3MB - (unused, reserved for future)
└── VastUniverse.mp3     # 3.5MB - (unused, reserved for future)
```

**Note:** SystemOverload and VastUniverse reserved for potential unlock system or additional content.

---

## Future Enhancements (Not in Scope)

**Unlock System (Option for later):**
- VoidOfEchoes - Unlocks at Tier +1 cycle completion
- Rift - Unlocks at Tier +2 cycle completion
- Additional songs unlock at higher tiers

**Additional Features:**
- Volume slider for music
- Separate volume for SFX vs music
- "Random" option (picks random song each session)
- "Shuffle" option (changes song every level)

---

## Rollback Plan

If music selector causes issues:

```bash
# Revert index.html changes
git checkout main -- index.html

# Revert game file changes
git checkout main -- game.html game_mobile.html

# Commit revert
git add index.html game.html game_mobile.html
git commit -m "revert: remove music selector feature"
```

**Low risk** - Feature is isolated and doesn't affect core gameplay.

---

## Dependencies

- ✅ File reorganization complete (assets/audio/music/ structure)
- ✅ Music files compressed and optimized
- ✅ Analytics version 4.3 active
- ⏳ AWS migration (implement after)
- ⏳ Pink levels 13-15 (Ximer_EE.mp3 waits for this)

---

## Success Criteria

Post-implementation, verify:
- [ ] Players can select from 3 music tracks
- [ ] Preview system works smoothly
- [ ] Selected music plays during gameplay
- [ ] Selection persists across sessions
- [ ] No performance impact on game load
- [ ] Analytics tracking works
- [ ] Mobile + desktop parity
- [ ] No console errors

---

## Notes

- **Simple scope** - No unlock complexity, just player choice
- **Post-launch feature** - Implement AFTER AWS migration complete
- **Low risk** - Easy to test, easy to revert
- **High value** - Player personalization, professional feel
- **Scalable** - Easy to add more songs or unlock system later
- **File size acceptable** - 10.7MB for 3 songs (optimized)

---

## Implementation Date

**Target:** 1-2 weeks after AWS migration complete
**Branch:** `feature/music-selector`
**Estimated completion:** End of April 2026