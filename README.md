# NON-X - Space Shooter Game

A browser-based top-scrolling space shooter with adaptive AI difficulty and tier-based scoring.

## 🚀 Live Demo
**Play now:** [https://kstanigar.github.io/Xenon_3/](https://kstanigar.github.io/Xenon_3/)

## 📂 Project Structure

```
/Xenon_3/
├── index.html                  # Main menu (platform selector, leaderboard)
├── game.html                   # Desktop game (800×600, 4:3 aspect ratio)
├── game_mobile.html            # Mobile game (480×1040, 19.5:9 aspect ratio)
├── README.md                   # This file
├── favicon.ico                 # Browser icon
│
├── *.png (24 files)            # Desktop sprites (PNG format)
├── *.webp (24 files)           # Mobile sprites (WebP format)
│
├── assets/                     # Production assets
│   └── audio/
│       ├── music/              # Background music (6 tracks, 59MB)
│       └── sfx/                # Sound effects (6 files)
│
├── docs/                       # Documentation (not publicly accessible)
│   ├── design/                 # Game design documents
│   ├── guides/                 # Testing & release checklists
│   ├── summaries/              # Implementation summaries
│   └── memory/                 # Project memory & session history
│
├── scripts/                    # Utility scripts
│   ├── compress_assets.py      # PNG → WebP conversion
│   ├── compress_image.py       # Single image compression
│   └── sync_paim.sh            # PAIM memory sync script
│
├── backups/                    # Historical backups
│   ├── 2026-04-13/            # Recent backups
│   └── archived/               # Old backups & unused assets
│
└── .github/
    └── workflows/
        ├── integrity-check.yml # Function validation CI
        └── test.yml            # HTML/Analytics validation CI
```

## 🎮 Game Features

- **12 Levels** across 3 phases: Green (L1-4), Red (L5-8), Purple (L9-12)
- **3 Boss Encounters** with unique attack patterns
- **AI Agent v1.0:** 7-tier adaptive difficulty system (Tier -3 to +3)
- **Tier-Based Scoring:** Score multipliers (×0.50 to ×1.75) prevent easy-mode exploitation
- **Power-ups:** Health, Shield, Double Laser, Triple Laser, Quad Laser
- **Dual Platform Support:** Optimized for both desktop (keyboard) and mobile (touch)

## 🛠️ Technology Stack

- **Frontend:** Vanilla JavaScript, HTML5 Canvas
- **Analytics:** Google Analytics 4 (GA4)
- **Database:** Firebase Cloud Firestore (leaderboard)
- **Deployment:** GitHub Pages → AWS S3 + CloudFront (planned)
- **CI/CD:** GitHub Actions (integrity checks, HTML validation)

## 📊 Analytics

- **GA4 Property ID:** G-9ECFZ9JBE5
- **Analytics Version:** 4.3 (AI Agent tracking enabled)
- **Custom Events:** player_won, ai_difficulty_adjusted, game_complete, etc.
- **Dashboard:** [non-x_analytics](https://kstanigar.github.io/non-x_analytics/)

## 🚦 Development Workflow

### Git Workflow
```bash
# CRITICAL: Never push directly to main - always use feature branches
git checkout -b feature/your-feature-name
git add <files>
git commit -m "feat: description"
git push -u origin feature/your-feature-name
# Then create PR on GitHub
```

### Testing
```bash
# Run local test server
python3 -m http.server 8000
# Visit: http://localhost:8000/index.html
```

### Asset Compression
```bash
# Compress all PNG images to WebP
python3 scripts/compress_assets.py

# Compress single image
python3 scripts/compress_image.py input.png output.webp
```

## 📈 Deployment

**Current:** GitHub Pages (`main` branch → https://kstanigar.github.io/Xenon_3/)
**Planned:** AWS S3 + CloudFront CDN (production deployment)

Changes go live within 1-2 minutes of pushing to `main`.

## 📄 Documentation

All design documents, guides, and memory files are located in the `docs/` directory:
- **Design:** AI difficulty system, tier-based scoring, difficulty toggle discussion
- **Guides:** A/B testing, release checklist, testing checklist
- **Summaries:** Implementation summaries, baseline settings, rebalancing notes
- **Memory:** Project memory & session history (PAIM reference files)

## 🤝 Contributing

This is a personal project, but feedback and bug reports are welcome!
**Report bugs:** [GitHub Issues](https://github.com/kstanigar/Xenon_3/issues)

## 📜 License

© Raginats 2026 - All rights reserved
**Developer:** [Thomas Keith](https://www.thomaskeithdev.com/)

## 🎵 Credits

**Music:** NonexFullSong.mp3 (+ 5 additional tracks)
**Sound Effects:** Custom sound design for gameplay events