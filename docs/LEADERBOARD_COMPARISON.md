# Leaderboard Code Comparison

**Created:** June 14, 2026
**Purpose:** Document differences between working (index.html) and broken (game.html) leaderboards

---

## Quick Summary

| | index.html | game.html |
|---|---|---|
| **Status** | ✅ Working | ❌ Broken (stuck on "Loading...") |
| **Trigger** | Page load + retry | Game over (no retry) |
| **escapeHtml** | ❌ Not used | ✅ Used (line 712) |
| **Retry logic** | ✅ Yes (1200ms) | ❌ No |
| `.catch()` on fetch | ❌ No | ❌ No |
| **# of leaderboard functions** | 4 | 8 |

---

## Root Cause of Bug

**`showLeaderboard()` in game.html has no retry logic and no `.catch()` on the fetch promise.**

When App Check tries to get a reCAPTCHA v3 token on first call, it may hang. `index.html` survives this because it retries after 1200ms. `game.html` has no retry — the promise hangs and the leaderboard stays on "Loading leaderboard..." forever.

---

## Script Block Structure

### index.html
```
<script type="module"> — lines 389–440
  - Firebase config + App Check init
  - window.firebaseGetTopScores() defined here (exposed to global)

<script> — lines 562–1235
  - renderLeaderboard() — lines 755–807
  - toggleLeaderboard() — lines 825–856
  - showFullLeaderboard() — lines 874–967
  - closeLeaderboardModal() — lines 973–978
  - Page init with RETRY LOGIC — lines 1209–1224
```

### game.html
```
<script type="module"> — lines 537–641
  - Firebase config + App Check init
  - window.firebaseSubmitScore() defined here
  - window.firebaseGetTopScores() defined here

<script> — lines 711–8637
  - escapeHtml() defined at line 712 (global scope ✅)
  - submitToLeaderboard() — lines 1342–1400
  - showLeaderboard() — lines 1418–1488
  - showFullLeaderboard() — lines 1506–1575
  - closeLeaderboardModal() — lines 1581–1586
  - playAgainFromModal() — lines 1593–1596
  - leaveGameFromModal() — lines 1599–1606
```

---

## Key Difference: Retry Logic

### index.html — HAS retry (lines 1209–1224)
```javascript
if (typeof window.firebaseGetTopScores === 'function') {
  window.firebaseGetTopScores().then(renderLeaderboard);  // Try immediately
  leaderboardLoaded = true;
} else {
  setTimeout(function () {                                 // Retry after 1200ms
    if (typeof window.firebaseGetTopScores === 'function') {
      window.firebaseGetTopScores().then(renderLeaderboard);
    } else {
      content.innerHTML = "Leaderboard unavailable.";
    }
    leaderboardLoaded = true;
  }, 1200);
}
```

### game.html `showLeaderboard()` — NO retry, NO .catch() (lines 1418–1488)
```javascript
function showLeaderboard() {
  display.innerHTML = "Loading leaderboard...";       // Line 1423

  if (typeof window.firebaseGetTopScores !== 'function') {
    display.innerHTML = "Leaderboard unavailable.";   // Line 1427 — guards undefined
    return;
  }

  window.firebaseGetTopScores().then(function (top10) {  // Line 1432 — NO .catch()
    if (!top10 || top10.length === 0) {
      display.innerHTML = "No scores yet.";
      return;
    }
    // ... render logic
    display.innerHTML = html;                         // Line 1486
  });
  // ❌ No .catch() — if promise hangs or rejects, stays on "Loading..."
  // ❌ No retry — called once at game over with no fallback
}
```

---

## escapeHtml Usage

### index.html — NOT used (XSS still present)
```javascript
// Line 794 — playerName inserted directly, NO escaping
cols[col] += "<span style='color:" + nameColor + ";font-size:12px;'>" + playerName + "</span>";
```
**⚠️ index.html still has XSS vulnerability — escapeHtml was never added here.**

### game.html — Used correctly (lines 1466, 1544)
```javascript
// Line 1466 — top 10 leaderboard
cols[col] += "<span style='color:" + nameColor + ";font-size:11px;'>" + escapeHtml(playerName) + "</span>";

// Line 1544 — top 25 modal
cols[col] += "<span style='color:" + nameColor + ";font-size:11px;'>" + escapeHtml(playerName) + "</span>";
```

---

## All Leaderboard Lines of Code

### index.html

| Lines | Description |
|---|---|
| 389–440 | Firebase module block (App Check + firebaseGetTopScores) |
| 429–439 | `window.firebaseGetTopScores()` definition |
| 562 | Regular `<script>` block start |
| 755–807 | `renderLeaderboard()` — renders top 10 |
| 775–776 | playerName extraction |
| 792–795 | HTML row construction (NO escapeHtml — XSS present) |
| 806 | `content.innerHTML = html` |
| 825–856 | `toggleLeaderboard()` |
| 840 | Fetch call #1 |
| 847 | Fetch call #2 (retry) |
| 874–967 | `showFullLeaderboard()` — top 25 modal |
| 885 | Modal fetch call |
| 973–978 | `closeLeaderboardModal()` |
| 1209–1224 | Page load init with retry logic |
| 1211 | Fetch call #3 (page load immediate) |
| 1217 | Fetch call #4 (page load retry) |

### game.html

| Lines | Description |
|---|---|
| 537–641 | Firebase module block |
| 576–620 | `window.firebaseSubmitScore()` definition |
| 630–640 | `window.firebaseGetTopScores()` definition |
| 711 | Regular `<script>` block start |
| 712–716 | `escapeHtml()` definition (global scope) |
| 1342–1400 | `submitToLeaderboard()` — score submission UI handler |
| 1380 | Firebase submit call |
| 1418–1488 | `showLeaderboard()` — top 10 render |
| 1423 | "Loading leaderboard..." set |
| 1426–1429 | Guard: `window.firebaseGetTopScores` undefined check |
| 1432 | `window.firebaseGetTopScores().then(...)` — NO .catch() |
| 1447–1448 | playerName extraction |
| 1466 | `escapeHtml(playerName)` — top 10 |
| 1486 | `display.innerHTML = html` |
| 1506–1575 | `showFullLeaderboard()` — top 25 modal |
| 1521 | `window.firebaseGetTopScores(25).then(...)` — NO .catch() |
| 1533–1534 | playerName extraction |
| 1544 | `escapeHtml(playerName)` — top 25 |
| 1573 | `content.innerHTML = html` |
| 1581–1586 | `closeLeaderboardModal()` |
| 1593–1596 | `playAgainFromModal()` |
| 1599–1606 | `leaveGameFromModal()` |
| 5942, 6267, 7031, 7353 | `showLeaderboard()` called on game over / victory screens |

---

## Required Fixes

### Fix 1 — game.html: Add `.catch()` + timeout to showLeaderboard() (line 1432)
```javascript
// CURRENT (broken):
window.firebaseGetTopScores().then(function (top10) { ... });

// FIXED:
var leaderboardTimeout = setTimeout(function() {
  display.innerHTML = "<div style='color:#aaa;font-size:13px;margin-top:10px;'>Leaderboard unavailable.</div>";
}, 5000);

window.firebaseGetTopScores().then(function (top10) {
  clearTimeout(leaderboardTimeout);
  // ... existing render logic
}).catch(function() {
  clearTimeout(leaderboardTimeout);
  display.innerHTML = "<div style='color:#aaa;font-size:13px;margin-top:10px;'>Leaderboard unavailable.</div>";
});
```

### Fix 2 — Same pattern for showFullLeaderboard() (line 1521)

### Fix 3 — index.html + game_mobile.html: Add escapeHtml (XSS still present in index.html)
- index.html line 794: `playerName` → `escapeHtml(playerName)` (need to add escapeHtml function too)
- game_mobile.html: verify same fix applied

---

**Last Updated:** June 14, 2026
