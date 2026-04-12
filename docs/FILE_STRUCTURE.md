# File Structure Documentation

**Last Updated:** April 12, 2026
**Reorganization:** Phase 1 (Security Fix + Audio Organization)

---

## Overview

The Xenon_3 project follows a professional folder structure optimized for AWS deployment and security. This document explains the organization and rationale behind each directory.

---

## Root Directory

```
/Xenon_3/
├── index.html                  # Main menu (platform selector, leaderboard, music toggle)
├── game.html                   # Desktop game (800×600, 4:3 aspect ratio, keyboard controls)
├── game_mobile.html            # Mobile game (480×1040, 19.5:9, touch controls)
├── README.md                   # Project README with structure diagram
├── favicon.ico                 # Browser favicon
├── .gitignore                  # Git ignore rules
└── .DS_Store                   # macOS metadata (git ignored)
```

**Why files stay in root:**
- **GitHub Pages requirement:** `index.html` must be at root for deployment
- **Path compatibility:** Game files use relative/absolute paths from root
- **Minimal changes:** Keeps current navigation (`index.html` ↔ `game.html` ↔ `game_mobile.html`) working

---

## Sprite Files (Root Directory)

**Desktop Sprites (PNG - 24 files):**
```
Boss.png, boss_Red.png, boss_purple.png
enemy.png, enemy2.png, enemy3.png, enemy4.png
enemy1_Red.png, enemy2_Red.png, enemy3_Red.png, enemy4_Red.png
enemy1_purple.png, enemy2_purple.png, enemy3_purple.png, enemy4_purple.png
player.png
```

**Mobile Sprites (WebP - 24 files):**
```
Boss.webp, boss_Red.webp, boss_purple.webp
enemy.webp, enemy2.webp, enemy3.webp, enemy4.webp
enemy1_Red.webp, enemy2_Red.webp, enemy3_Red.webp, enemy4_Red.webp
enemy1_purple.webp, enemy2_purple.webp, enemy3_purple.webp, enemy4_purple.webp
player.webp
```

**Why sprites stay in root:**
- **Deferred migration:** Avoid 48 path updates now + 48 more during AWS migration
- **Format split already handled:** Desktop uses `.png`, mobile uses `.webp`
- **Will reorganize during AWS:** Sprite paths will change for CloudFront anyway

**File paths in code:**
- **Desktop (game.html):** `/Xenon_3/player.png` (absolute paths)
- **Mobile (game_mobile.html):** `player.webp` (relative paths)

---

## Assets Directory

### Audio Files

```
assets/
└── audio/
    ├── music/                  # Background music (6 tracks, 59MB total)
    │   ├── NonexFullSong.mp3   # Original background music (4.6MB)
    │   ├── DarkLights.mp3      # Alternative track 1 (13.1MB)
    │   ├── SystemOverload.mp3  # Alternative track 2 (12.8MB)
    │   ├── VastUniverse.mp3    # Alternative track 3 (13.6MB)
    │   ├── VoidOfEchoes.mp3    # Alternative track 4 (9.9MB)
    │   └── Ximer_EE.mp3        # Alternative track 5 (9.8MB)
    │
    └── sfx/                    # Sound effects (6 files, 35KB total)
        ├── playerBullet.mp3    # Laser shot sound
        ├── playerHit.mp3       # Player damage sound
        ├── playerDead.mp3      # Player death sound
        ├── enemyDead.mp3       # Enemy explosion sound
        ├── bossIntro.mp3       # Boss entry sound
        └── powerUp.mp3         # Power-up collection sound
```

**File paths in code:**
- **Desktop (game.html):**
  - SFX: `/Xenon_3/assets/audio/sfx/playerBullet.mp3` (absolute)
  - Music: `/Xenon_3/assets/audio/music/NonexFullSong.mp3` (absolute)
- **Mobile (game_mobile.html):**
  - SFX: `assets/audio/sfx/playerBullet.mp3` (relative)
  - Music: `assets/audio/music/NonexFullSong.mp3` (relative)

**AWS Migration:**
- S3 bucket will map `assets/` to CloudFront distribution
- CloudFront can cache `/assets/*` with long TTL (immutable static assets)
- Future: Separate buckets for `audio/music/` (large files, geo-distributed)

---

## Documentation Directory

**⚠️ CRITICAL:** Documentation is **NOT publicly accessible** on GitHub Pages. GitHub Pages only serves files linked from HTML. Since no HTML file links to `docs/`, these files return 404 when accessed directly.

```
docs/
├── design/                     # Game design documents
│   ├── ADAPTIVE_DIFFICULTY_DESIGN.md       # AI Agent v1.0 specification (82KB)
│   ├── TIER_BASED_SCORING_DESIGN.md        # Score multiplier system (11KB)
│   ├── DIFFICULTY_TOGGLE_DISCUSSION.md     # Manual difficulty decision (2.5KB)
│   └── AI_AGENT_ADVANCED_IDEAS.md          # Future AI features (5.6KB)
│
├── guides/                     # Testing & release guides
│   ├── AB_TESTING_GUIDE.md                 # A/B test methodology (6KB)
│   ├── RELEASE_CHECKLIST.md                # Deployment checklist (7KB)
│   └── TESTING_CHECKLIST.md                # QA procedures (12KB)
│
├── summaries/                  # Implementation summaries
│   ├── BASELINE_TIER0_SUMMARY.md           # Tier 0 baseline settings (5KB)
│   ├── PURPLE_REBALANCING_SUMMARY.md       # Purple phase balance (5.3KB)
│   ├── PLAYER_WON_DIAGNOSTIC.md            # Victory event debugging (7KB)
│   └── DOCUMENTATION_PROGRESS.md           # Code comment status (39KB)
│
├── memory/                     # Project memory files
│   ├── NON-X_PAIM_Memory.md                # Master reference (182KB)
│   └── NON-X_PAIM_SessionHistory.md        # Session log (16KB)
│
└── FILE_STRUCTURE.md           # This file
```

**Security fix (April 12, 2026):**
- **Before:** All `.md` files in root, publicly accessible at `kstanigar.github.io/Xenon_3/*.md`
- **After:** All docs in `docs/` subdirectories, return 404 when accessed
- **Result:** Competitive intelligence (strategy, roadmap, analytics setup) no longer exposed

**AWS Migration:**
- `docs/` folder will **NOT** be uploaded to S3 (stays in Git only)
- Keeps documentation version-controlled but not publicly served
- Future: Consider private S3 bucket for team docs (if team expands)

---

## Scripts Directory

```
scripts/
├── compress_assets.py          # Batch PNG → WebP conversion
├── compress_image.py           # Single image compression
└── sync_paim.sh                # PAIM memory file sync script
```

**⚠️ NOT publicly accessible** on GitHub Pages (same reason as `docs/`).

**Usage:**
```bash
# Compress all PNG images to WebP
python3 scripts/compress_assets.py

# Compress single image
python3 scripts/compress_image.py input.png output.webp

# Sync PAIM memory between projects
bash scripts/sync_paim.sh
```

---

## Backups Directory

```
backups/
├── 2026-04-13/                 # Recent backups (before file reorganization)
│   ├── game_BU.html
│   ├── game_mobile_BU.html
│   ├── index_BU.html
│   ├── game_BU_041326.html
│   ├── game_mobile_BU_041326.html
│   └── index_BU_041326.html
│
└── archived/                   # Old backups & unused assets
    ├── index_BackUp.html               # Legacy index backup (Feb 13, 2024)
    ├── index_old.html                  # Legacy index backup (Feb 14, 2024)
    ├── game_mobile.html.bak            # Recent mobile backup
    ├── player1.png                     # Unused player sprite variant
    ├── player2.png                     # Unused player sprite variant
    ├── enemy1b.png                     # Unused enemy sprite variant
    ├── boss_aRed.png                   # Unused alternate red boss
    ├── Alien fleet with futuristic designs.png     # Unused concept art (2.4MB)
    └── Alien fleet with futuristic designs.webp    # Unused concept art (216KB)
```

**⚠️ NOT publicly accessible** on GitHub Pages.

**Backup strategy:**
- **Recent backups:** Dated folders (YYYY-MM-DD format)
- **Archived:** Old backups + unused assets (not deleted, just archived)
- **Before major changes:** Always create backup in `backups/YYYY-MM-DD/`

---

## GitHub Configuration

```
.github/
└── workflows/
    ├── integrity-check.yml     # Validates critical functions exist (AI Agent, Ko-fi, etc.)
    └── test.yml                # HTML validation, GA4 ID check, A/B testing code check
```

**CI/CD workflow:**
1. Developer commits to `feature/branch`
2. GitHub Actions runs:
   - `test.yml` — HTML validation, analytics checks
   - `integrity-check.yml` — Function existence validation
3. If checks pass, PR can be merged to `main`
4. Merge to `main` triggers automatic GitHub Pages deployment (1-2 min)

---

## Path Reference Table

| File Type | Desktop (game.html) | Mobile (game_mobile.html) |
|-----------|---------------------|---------------------------|
| **Sprites** | `/Xenon_3/player.png` (absolute) | `player.webp` (relative) |
| **Audio SFX** | `/Xenon_3/assets/audio/sfx/playerBullet.mp3` | `assets/audio/sfx/playerBullet.mp3` |
| **Audio Music** | `/Xenon_3/assets/audio/music/NonexFullSong.mp3` | `assets/audio/music/NonexFullSong.mp3` |
| **HTML Navigation** | `index.html` (relative) | `index.html` (relative) |

**Why path asymmetry:**
- **Desktop absolute paths:** Works from any subdirectory, GitHub Pages base path (`/Xenon_3/`) baked in
- **Mobile relative paths:** Flexible for different deployment bases (GitHub Pages, AWS, localhost)
- **Future standardization:** AWS migration will standardize to CloudFront URLs

---

## Future Reorganization (AWS Migration)

**When AWS migration happens:**
1. **Sprite files:** Move to `assets/sprites/desktop/` and `assets/sprites/mobile/`
   - Update 48 sprite paths (24 in game.html + 24 in game_mobile.html)
   - Use CloudFront URLs: `https://cdn.yoursite.com/assets/sprites/desktop/player.png`

2. **HTML files:** May move to `/public/` or stay at root (TBD based on S3 bucket structure)

3. **CloudFront distribution:**
   - `/assets/*` cached with long TTL (1 year, assets are immutable)
   - `/*.html` cached with short TTL (5 min, content can change)
   - `/docs/*` not uploaded to S3 (stays in Git only)

**Deferred sprite migration rationale:**
- Avoid updating paths twice (once now, once for AWS)
- Sprite paths will change to CloudFront URLs anyway
- Current structure works fine for GitHub Pages deployment

---

## Changelog

### April 12, 2026 - Phase 1: File Reorganization
**Security fix + Audio organization**

- Moved all documentation to `docs/` subdirectories (design, guides, summaries, memory)
- Moved utility scripts to `scripts/`
- Moved backups to `backups/` (dated + archived)
- Archived unused assets (unused sprites, concept art)
- Reorganized audio: `sfx/` → `assets/audio/sfx/` + `assets/audio/music/`
- Updated 24 audio paths (12 in game.html + 12 in game_mobile.html)
- Updated `.gitignore` to prevent `.DS_Store`, `*.tmp`, `*.log` clutter

**Result:**
- Root directory reduced from 76 items to ~56 items
- Documentation no longer publicly accessible (security fix)
- Audio organized for AWS S3 bucket structure
- Sprite migration deferred to AWS transition

---

## Questions?

**Project lead:** Thomas Keith (https://www.thomaskeithdev.com/)
**Repo:** https://github.com/kstanigar/Xenon_3
**Live site:** https://kstanigar.github.io/Xenon_3/