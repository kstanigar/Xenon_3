# Xenon 3 Repository Structure

**Last Updated:** June 1, 2026

## Overview

Xenon 3 is a space-themed arcade game built with HTML5 Canvas and vanilla JavaScript. The repository contains game files, comprehensive documentation, assets, and deployment configurations.

## Directory Tree

```
Xenon_3/
│
├── .claude/                            # Claude Code configuration and rules
│   ├── hooks/
│   │   └── pre-execution-checklist.md
│   ├── rules/
│   │   └── multi-agent-verification.md
│   └── skills/
│       └── handoff-protocol.md
│
├── .github/                            # GitHub configuration
│   └── workflows/                      # CI/CD workflows
│
├── .git/                               # Git version control
│
├── .gitignore                          # Git ignore rules
│
├── assets/                             # Game assets
│   └── audio/
│       ├── music/
│       │   ├── NonexFullSong.mp3       # Menu/gameplay music
│       │   └── SystemOverload.mp3      # Boss/climax music
│       └── sfx/                        # Sound effects directory
│
├── backups/                            # Backup files
│   ├── 2026-04-13/
│   └── archived/
│
├── docs/                               # Documentation root
│   ├── ARCHIVE_PLAN_2026-06-01.md     # Archive organization plan
│   ├── AWS_RESEARCH_2026.md            # AWS deployment research
│   ├── DEPLOYMENT_PROGRESS.md          # Deployment status tracking
│   ├── DEV_PROD_DEPLOYMENT_PLAN.md    # Dev/prod deployment strategy
│   ├── FILE_STRUCTURE.md               # File structure documentation
│   ├── GIT_COMMIT_WORKFLOW.md          # Git workflow guidelines
│   ├── NEXT_SESSION_PRIORITIES.md      # Next session action items
│   │
│   ├── archive/                        # Archived documentation
│   │   ├── README.md                   # Archive organization guide
│   │   │
│   │   ├── deployment/                 # Archived deployment docs
│   │   │   ├── AUTO_DEPLOYMENT_ANALYSIS.md
│   │   │   ├── AWS_DEPLOYMENT_STATUS.md
│   │   │   ├── DEPLOYMENT_QUICK_REFERENCE.md
│   │   │   ├── LIVE_SITE_STATUS.md
│   │   │   └── WORKFLOW_IMPLEMENTATION_GUIDE.md
│   │   │
│   │   ├── implemented/                # Archived implemented features
│   │   │   └── 2026-04/
│   │   │       ├── BLACK_BACKGROUND_PLAN.md
│   │   │       ├── DOCUMENTATION_PROGRESS.md
│   │   │       └── SUPPORT_DEV_BUTTON_LOCATIONS.md
│   │   │
│   │   ├── planning/                   # Archived planning documents
│   │   │   ├── AI_AGENT_ADVANCED_IDEAS.md
│   │   │   ├── AUTO_DEPLOY_IMPLEMENTATION_PLAN.md
│   │   │   ├── AWS_DEPLOYMENT_PLAN.md
│   │   │   ├── DEPLOYMENT_DOCUMENTATION_INDEX.md
│   │   │   ├── DIFFICULTY_TOGGLE_DISCUSSION.md
│   │   │   └── MUSIC_SELECTOR_PLAN.md
│   │   │
│   │   ├── reference/                  # Reference documents
│   │   │   ├── NON-X_PAIM_Memory.md
│   │   │   └── NON-X_PAIM_SessionHistory.md
│   │   │
│   │   └── sessions/                   # Session handoff and summaries
│   │       ├── HANDOFF_SUMMARY_2026-05-30.md
│   │       ├── HANDOFF_SUMMARY_2026-05-31.md
│   │       └── SESSION_SUMMARY_2026-05-30.md
│   │
│   ├── design/                         # Game design documents
│   │   ├── ADAPTIVE_DIFFICULTY_DESIGN.md      # Difficulty adjustment system
│   │   ├── HERO_SHIP_COLOR_PURCHASE.md        # Hero ship color cosmetics
│   │   └── TIER_BASED_SCORING_DESIGN.md       # Scoring tiers and progression
│   │
│   ├── guides/                         # Implementation guides
│   │   ├── AB_TESTING_GUIDE.md
│   │   └── RELEASE_CHECKLIST.md
│   │
│   ├── summaries/                      # Feature summaries
│   │   ├── BASELINE_TIER0_SUMMARY.md
│   │   └── PURPLE_REBALANCING_SUMMARY.md
│   │
│   └── workflows/                      # Workflow documentation
│       ├── DEV_BRANCH_STRATEGY.md
│       ├── MAIN_BRANCH_PREPARATION.md
│       └── SAFEGUARDS_IMPLEMENTATION_PLAN.md
│
├── scripts/                            # Utility scripts
│   ├── compress_assets.py              # Asset compression tool
│   ├── compress_image.py               # Image compression tool
│   └── sync_paim.sh                    # PAIM sync script
│
├── index.html                          # Landing page
├── game.html                           # Main game (desktop)
├── game_mobile.html                    # Mobile version
├── game_mobile.html.bak                # Mobile backup
│
├── favicon.ico                         # Site favicon
│
├── Game Assets (WebP images)
├── Boss.webp                           # Boss sprite
├── boss_Red.webp                       # Red variant
├── boss_purple.webp                    # Purple variant
├── enemy.webp                          # Generic enemy
├── enemy1_Red.webp                     # Red variant
├── enemy1_purple.webp                  # Purple variant
├── enemy2.webp                         # Enemy type 2
├── enemy2_Red.webp                     # Red variant
├── enemy2_purple.webp                  # Purple variant
├── enemy3.webp                         # Enemy type 3
├── enemy3_Red.webp                     # Red variant
├── enemy3_purple.webp                  # Purple variant
├── enemy4.webp                         # Enemy type 4
├── enemy4_Red.webp                     # Red variant
├── enemy4_purple.webp                  # Purple variant
├── player.webp                         # Player sprite
│
├── Documentation Files
├── README.md                           # Project README
├── repo_map.md                         # This file
├── HANDOFF_SUMMARY.md                  # Current session handoff
├── CURRENT_PRIORITIES.md               # Current priorities and tasks
├── MISSION_CONTROL.md                  # Mission control center
├── DEV_ERRORS_LOG.md                   # Development errors log
├── DEPLOYMENT_AUDIT_FINDINGS.md        # Deployment audit results
├── GITHUB_BRANCH_PROTECTION_GUIDE.md   # GitHub protection settings
│
├── Supporting Files
├── NON-X_AI_Adaptive_Engine_Spec.docx  # AI adaptive engine spec
├── NON-X_Analytics_Setup_Guide.docx    # Analytics setup documentation
├── NONX_Analytics_Event_and_Dashboard_Update.pdf
├── NONX_GA4_Looker_CaseStudy_Pack.pdf
├── Fixing GA4 analytics integration - Claude.htm
│
└── integrity-check.yml                 # Integrity check configuration
```

## Key Files

### Game Files
- **game.html** (385 KB): Main desktop game implementation
- **game_mobile.html**: Responsive mobile version
- **index.html**: Landing page and entry point

### Audio Assets
- **NonexFullSong.mp3** (4.4 MB): Menu and gameplay background music
- **SystemOverload.mp3** (3.2 MB): Boss battle and climax music

### Documentation Structure
- **Root level (.md files)**: Current priorities, handoffs, mission control
- **docs/**: Active documentation and guides
- **docs/archive/**: Organized historical documentation by category:
  - **deployment/**: Deployment-related archived docs
  - **implemented/**: Completed feature documentation
  - **planning/**: Past planning documents
  - **reference/**: Reference materials (memory, session history)
  - **sessions/**: Handoff summaries and session notes
  - **design/**, **guides/**, **summaries/**, **workflows/**: Active design and workflow docs

### Game Assets
- **Sprites**: Boss, enemies (4 types with variants), player in WebP format
- **Color Variants**: Red and Purple theme variations for all enemies and boss

## Recent Changes (June 1, 2026)

1. **Music Files**: Consolidated from 6 files to 2 active files
   - Removed: Various background track variations
   - Kept: NonexFullSong.mp3, SystemOverload.mp3

2. **Documentation Archive**: Reorganized 11+ files into structured archive
   - Deployment docs moved to `docs/archive/deployment/`
   - Planning docs moved to `docs/archive/planning/`
   - Testing docs moved to `docs/archive/testing/`
   - Session summaries moved to `docs/archive/sessions/`
   - Implemented features moved to `docs/archive/implemented/2026-04/`

3. **New Root Documentation**:
   - HANDOFF_SUMMARY.md: Current session handoff
   - CURRENT_PRIORITIES.md: Active priorities
   - MISSION_CONTROL.md: Mission control center

4. **New Design Doc**:
   - docs/design/HERO_SHIP_COLOR_PURCHASE.md: Color cosmetics feature

## Repository Statistics

- **Total Directories**: 14 main directories + archives
- **Documentation Files**: 40+ markdown files
- **Game Code Files**: 3 (index.html, game.html, game_mobile.html)
- **Asset Files**: 15 WebP images + 2 MP3 files
- **Script Files**: 3 utility scripts

## Git Information

- **Main Branch**: main
- **Feature Branches**: Available for feature development
- **Recent Commits**:
  - 464b92a: Documentation and Handoff Summary
  - 2e4c241: Merge PR #104 (Music Selector Plan)
  - 9bd8437: Add music selector feature plan and audio assets
  - 3a12199: Merge PR #103 (Keep Lights On Button)
  - 668322b: Implement 'Keep the Lights On' button redesign

## Configuration Files

- **.gitignore**: Git exclusion rules
- **integrity-check.yml**: Deployment integrity checks
- **.claude/**: Claude Code configuration including multi-agent rules, handoff protocol
- **.github/workflows/**: GitHub Actions CI/CD workflows