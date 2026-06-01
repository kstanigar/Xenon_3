# Deployment Workflow Exclusion Audit - Findings

**Audit Date:** June 1, 2026
**Status:** CRITICAL ISSUE IDENTIFIED

---

## TL;DR

The deployment workflow excludes `assets/audio/music/*`, which breaks the game because:

1. **NonexFullSong.mp3** (currently used) is NOT deployed to S3
2. Game code loads this file from `assets/audio/music/NonexFullSong.mp3`
3. File doesn't exist in production → no music plays → broken UX

**Solution:** Delete the line `--exclude "assets/audio/music/*"` from `.github/workflows/deploy-aws.yml` (line 66)

---

## Problem Files

### File: `.github/workflows/deploy-aws.yml`

**Lines 61-69 (Current):**
```yaml
--exclude ".git/*"
--exclude ".github/*"
--exclude "docs/*"
--exclude "backups/*"
--exclude "scripts/*"
--exclude "assets/audio/music/*"   # ← DELETE THIS LINE
--exclude "*.md"
--exclude ".DS_Store"
--exclude ".claude/*"
```

**Lines 61-68 (Fixed):**
```yaml
--exclude ".git/*"
--exclude ".github/*"
--exclude "docs/*"
--exclude "backups/*"
--exclude "scripts/*"
--exclude "*.md"
--exclude ".DS_Store"
--exclude ".claude/*"
```

---

## Assets Affected

### BREAKING THE GAME NOW
- `assets/audio/music/NonexFullSong.mp3` (4.58 MB)
  - Currently hardcoded in game.html (line ~920)
  - Currently hardcoded in game_mobile.html (line ~857)
  - Will break when Music Selector feature is implemented

### WILL BREAK WHEN MUSIC SELECTOR LAUNCHES
- `assets/audio/music/VoidOfEchoes.mp3` (2.75 MB)
- `assets/audio/music/Rift.mp3` (3.89 MB)
- `assets/audio/music/SystemOverload.mp3` (3.41 MB)
- `assets/audio/music/VastUniverse.mp3` (3.71 MB)
- `assets/audio/music/Ximer_EE.mp3` (2.57 MB)

See: `docs/archive/planning/MUSIC_SELECTOR_PLAN.md`

---

## All Other Exclusions Are Correct

| Pattern | Safe? | Reason |
|---------|-------|--------|
| `.git/*` | ✅ Yes | Git metadata, not needed in production |
| `.github/*` | ✅ Yes | Workflows, not needed in production |
| `docs/*` | ✅ Yes | Documentation, not needed in production |
| `backups/*` | ✅ Yes | Archived files, not needed in production |
| `scripts/*` | ✅ Yes | Build scripts, not needed in production |
| `*.md` | ✅ Yes | Documentation files, not needed in production |
| `.DS_Store` | ✅ Yes | macOS metadata, not needed in production |
| `.claude/*` | ✅ Yes | AI agent config, not needed in production |

---

## Evidence

### Game Code References (game.html, ~line 920)
```javascript
var bgMusic = new Audio("assets/audio/music/NonexFullSong.mp3");
```

### Game Code References (game_mobile.html, ~line 857)
```javascript
var bgMusic = new Audio("assets/audio/music/NonexFullSong.mp3");
```

### Planned Feature (docs/archive/planning/MUSIC_SELECTOR_PLAN.md)
```javascript
// Will be added post-AWS migration:
var selectedMusic = localStorage.getItem('nonx_selected_music') || 'NonexFullSong';
var bgMusic = new Audio("assets/audio/music/" + selectedMusic + ".mp3");
```

---

## Impact

### Current (Live)
- Background music doesn't play in-game
- All players with music enabled are affected
- Silent failure (no console errors)

### Future (Post-Music Selector Implementation)
- Feature becomes completely non-functional
- Players selecting alternate tracks get 404 errors
- Music selector feature cannot launch

---

## Assets Actually Required for Deployment

### Images (16 files, not excluded)
- player.webp, enemy.webp, enemy2.webp, enemy3.webp, enemy4.webp
- Boss.webp, enemy1_Red.webp, enemy2_Red.webp, enemy3_Red.webp
- enemy4_Red.webp, boss_Red.webp, enemy1_purple.webp, enemy2_purple.webp
- enemy3_purple.webp, enemy4_purple.webp, boss_purple.webp

### SFX Audio (6 files, not excluded)
- assets/audio/sfx/playerBullet.mp3
- assets/audio/sfx/playerHit.mp3
- assets/audio/sfx/playerDead.mp3
- assets/audio/sfx/enemyDead.mp3
- assets/audio/sfx/bossIntro.mp3
- assets/audio/sfx/powerUp.mp3

### Music Audio (6 files, INCORRECTLY EXCLUDED)
- assets/audio/music/NonexFullSong.mp3 (REQUIRED NOW)
- assets/audio/music/VoidOfEchoes.mp3 (Required when feature launches)
- assets/audio/music/Rift.mp3 (Required when feature launches)
- assets/audio/music/SystemOverload.mp3 (Required when feature launches)
- assets/audio/music/VastUniverse.mp3 (Required when feature launches)
- assets/audio/music/Ximer_EE.mp3 (Required when feature launches)

---

## Audit Files Checked

1. `.github/workflows/deploy-aws.yml` - Exclusion patterns
2. `game.html` - Audio references and dependencies
3. `game_mobile.html` - Audio references and dependencies
4. `index.html` - Assets and dependencies
5. `docs/archive/planning/MUSIC_SELECTOR_PLAN.md` - Future feature requirements
6. `assets/audio/music/` directory - Actual files present
7. `assets/audio/sfx/` directory - SFX files (correctly deployed)
8. Project root - Image asset files

---

## Next Steps

1. **Delete line 66** from `.github/workflows/deploy-aws.yml`
2. **Test deployment** to verify music files appear in S3
3. **Verify CloudFront** properly caches music paths
4. **Test game** with music enabled to verify audio plays
5. **Monitor GA4** for music-related metrics

---

**Full audit report:** See `/tmp/DEPLOYMENT_EXCLUSION_AUDIT_REPORT.md` for comprehensive analysis.