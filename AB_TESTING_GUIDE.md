# A/B Testing Guide - NON-X

## Active A/B Tests

### Test 1: Music Default (ON vs OFF)

**Hypothesis:** Players with music ON by default will have higher engagement and completion rates.

**Test Groups:**
- **Group A:** Music ON by default (50% of users)
- **Group B:** Music OFF by default (50% of users)

**Implementation:**
- Random assignment on first visit
- Stored in `localStorage.nonx_ab_music_group` (value: 'A' or 'B')
- Default music preference set based on group
- User can still manually toggle music (respects user choice)

---

## Tracking Metrics

### Primary Metrics (by Group)
1. **Completion Rate**
   - % who beat final boss
   - Compare Group A vs Group B

2. **Average Session Duration**
   - Time from start to game over/victory
   - Longer = better engagement

3. **Level Reached**
   - Average level reached before quitting
   - Shows drop-off point by group

4. **Boss Defeat Rate**
   - % who defeat Boss 1, 2, 3
   - By group

### Secondary Metrics
5. **Instagram Handle Submission Rate**
   - % who submit to leaderboard
   - By group

6. **Return Player Rate**
   - % who play more than once
   - By group

7. **Music Toggle Rate**
   - % who manually change music setting
   - Shows how many override the default

---

## Data Collection

### With Google Analytics

Add to game files when tracking events:

```javascript
// On game start
gtag('event', 'game_start', {
  'ab_music_group': userABGroup,  // 'A' or 'B'
  'platform': 'mobile',
  'music_on': localStorage.getItem('nonex_music') !== 'off'
});

// On level complete
gtag('event', 'level_complete', {
  'ab_music_group': userABGroup,
  'level': level,
  'score': score
});

// On boss defeated
gtag('event', 'boss_defeated', {
  'ab_music_group': userABGroup,
  'boss_number': currentBoss,
  'score': score
});

// On game complete (victory)
gtag('event', 'game_complete', {
  'ab_music_group': userABGroup,
  'final_score': score,
  'music_on': localStorage.getItem('nonex_music') !== 'off'
});

// On game over
gtag('event', 'game_over', {
  'ab_music_group': userABGroup,
  'level_reached': level,
  'score': score
});

// On leaderboard submit
gtag('event', 'leaderboard_submit', {
  'ab_music_group': userABGroup,
  'score': score,
  'instagram_provided': !!sanitized
});

// On music toggle (in-game)
gtag('event', 'music_toggle', {
  'ab_music_group': userABGroup,
  'new_state': bgMusic.paused ? 'off' : 'on'
});
```

### With Custom Analytics Endpoint

Send this data with each event:

```javascript
{
  event: 'game_start',
  ab_group: userABGroup,
  music_on: localStorage.getItem('nonex_music') !== 'off',
  platform: 'mobile',
  timestamp: Date.now(),
  session: sessionStorage.getItem('nonex_session')
}
```

---

## Analysis Plan

### Week 1: Collect Data
- Monitor that groups are roughly 50/50 split
- Verify tracking is working
- No changes

### Week 2-3: Analyze
Run these queries in Google Analytics or your database:

**Completion Rate by Group:**
```
Group A: [X%] completed game
Group B: [Y%] completed game
Winner: [A or B]
```

**Average Session Duration:**
```
Group A: [X] minutes average
Group B: [Y] minutes average
Winner: [A or B]
```

**Level Reached:**
```
Group A: Average level [X]
Group B: Average level [Y]
Winner: [A or B]
```

### Statistical Significance
- Need at least 100 players per group for valid results
- Use chi-square test for completion rate
- Use t-test for session duration

**Online Calculator:**
https://www.optimizely.com/sample-size-calculator/

---

## Decision Framework

### If Group A (Music ON) Wins
- **Action:** Keep music ON by default
- **Rationale:** Music enhances engagement
- **Remove test:** Set all new users to music ON

### If Group B (Music OFF) Wins
- **Action:** Keep music OFF by default
- **Rationale:** Players prefer to control audio
- **Remove test:** Set all new users to music OFF

### If No Significant Difference
- **Action:** Default to OFF (respects user control)
- **Rationale:** Better UX to let users opt-in
- **Remove test:** Set all new users to music OFF

---

## Current Test Status

**Test Started:** [Add date when deployed]
**Sample Size:** Check localStorage.nonx_ab_music_group distribution
**Expected Duration:** 2-3 weeks (or until 200+ players per group)

---

## Viewing Test Assignment

### In Browser Console:
```javascript
// Check your test group
localStorage.getItem('nonx_ab_music_group')
// Returns: 'A' or 'B'

// Check music preference
localStorage.getItem('nonex_music')
// Returns: 'on' or 'off'
```

### Analytics Dashboard:
- Create custom dimension for `ab_music_group`
- Filter all reports by this dimension
- Compare metrics side-by-side

---

## Future A/B Tests

### Potential Tests:
1. **Difficulty Curve**
   - Group A: Current difficulty
   - Group B: -20% enemy health
   - Metric: Completion rate

2. **Power-up Frequency**
   - Group A: Current spawn rate
   - Group B: +30% spawn rate
   - Metric: Average score

3. **Boss Difficulty**
   - Group A: Current health
   - Group B: -25% health
   - Metric: Boss defeat rate

4. **UI/UX**
   - Group A: Current layout
   - Group B: Different button placement
   - Metric: Click-through rate

---

## Best Practices

1. **One test at a time** - Don't run multiple A/B tests simultaneously
2. **Document everything** - Keep this file updated
3. **Wait for significance** - Don't make decisions on small sample sizes
4. **User consistency** - Same user always sees same variant
5. **Track everything** - More data = better decisions

---

## Questions?

- What is my test group? Check `localStorage.nonx_ab_music_group`
- How to force a group? `localStorage.setItem('nonx_ab_music_group', 'A')`
- How to reset test? `localStorage.removeItem('nonx_ab_music_group')`
- Where's the data? Google Analytics or custom endpoint

**Note:** Users assigned via main menu toggle are NOT in the test (they made an explicit choice).
