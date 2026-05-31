# Documentation Archive

**Purpose:** Historical reference for completed features, deferred plans, and superseded documentation.

## Structure

### `implemented/` - Completed Features
Features fully implemented and tested. Archived by completion date.

**2026-04:**
- BLACK_BACKGROUND_PLAN.md - Victory/game over screen backgrounds
- SUPPORT_DEV_BUTTON_LOCATIONS.md - Ko-fi and Player Intel button redesigns
- DOCUMENTATION_PROGRESS.md - Code documentation sessions (Sessions 1-3)

### `planning/` - Deferred Plans
Feature plans not yet implemented or deferred to future versions.

- MUSIC_SELECTOR_PLAN.md - Player music selection (post-AWS migration)
- DIFFICULTY_TOGGLE_DISCUSSION.md - Manual difficulty toggle (deferred)
- AI_AGENT_ADVANCED_IDEAS.md - Future AI system enhancements (v2.0+)

### `testing/` - Testing Documentation
Completed testing phases and diagnostic procedures.

- TESTING_CHECKLIST.md - Adaptive difficulty Stage 1 testing
- PLAYER_WON_DIAGNOSTIC.md - GA4 player_won event troubleshooting

### `reference/` - AI Memory & Session History
Historical AI agent memory and session logs.

- NON-X_PAIM_Memory.md - Master project memory (superseded by implementation)
- NON-X_PAIM_SessionHistory.md - AI session summaries through April 2026

## Restoring Archived Docs

To restore a document to active status:
```bash
mv docs/archive/[category]/[filename].md docs/[destination]/
```

## Archive Date
Initial archive: May 30, 2026