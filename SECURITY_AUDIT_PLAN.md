# NON-X Security Audit Plan

**Created:** June 13, 2026
**Project:** Xenon 3 (NON-X) — nonx.standingtiger.com
**Stack:** HTML5/JS game, AWS S3 + CloudFront, Firebase Firestore, Google Analytics 4, Ko-fi, FormSubmit.co
**Audit Method:** Haiku agent codebase scan (game.html, game_mobile.html, index.html, configs) + 2026 best practices research
**Files Audited:** game.html (8,682 lines), game_mobile.html (9,562 lines), index.html (1,231 lines), .github/workflows/deploy-aws.yml, integrity-check.yml, scripts/

---

## Quick Reference — Risk Summary

| # | Issue | Severity | Status |
|---|---|---|---|
| 1 | Firestore security rules — unknown state | CRITICAL | ✅ Complete (June 13, 2026) |
| 2 | Firebase API key exposed in all 3 HTML files | HIGH | ✅ Complete (June 13, 2026) |
| 3 | XSS via innerHTML with Firestore player names | HIGH | ✅ Complete (June 14, 2026) |
| 4 | No Content Security Policy (CSP) headers | HIGH | ⬜ Not Started |
| 5 | GA4 privacy / GDPR — no consent mechanism | HIGH | ⬜ Not Started |
| 6 | No CloudFront security headers | HIGH | ✅ Complete (June 14, 2026) |
| 7 | Developer email hardcoded in JS (FormSubmit) | MEDIUM | ⬜ Not Started |
| 8 | URL parameters enable dev/god mode in production | MEDIUM | ⬜ Not Started |
| 9 | localStorage scores submitted directly to leaderboard | MEDIUM | ⬜ Not Started |
| 10 | console.log / console.error / console.warn in production | MEDIUM | ⬜ Not Started |
| 11 | No Subresource Integrity (SRI) on external scripts | MEDIUM | ⬜ Not Started |
| 12 | Developer file paths hardcoded in scripts/sync_paim.sh | MEDIUM | ⬜ Not Started |
| 13 | Ko-fi link uses string interpolation in onclick handler | LOW | ⬜ Not Started |
| 14 | savedHandle from localStorage injected into HTML attribute | LOW | ⬜ Not Started |
| 15 | No HTTPS enforcement verified (relying solely on CloudFront) | LOW | ⬜ Not Started |
| 16 | Firebase App Check not enabled | LOW | ⬜ Not Started |
| 17 | No Firebase budget alerts | LOW | ⬜ Not Started |
| 18 | Developer mode accessible via keyboard shortcuts in production | LOW | ⬜ Not Started |

---

## Tools, Platforms & Third-Party Services Inventory

*Listed regardless of risk — complete picture of all external dependencies.*

| Service | Purpose | Files | Key/ID Exposed | Risk Notes |
|---|---|---|---|---|
| Google Analytics 4 | Game analytics | game.html:118, game_mobile.html:118, index.html:112 | G-9ECFZ9JBE5 | GA4 IDs are public by design; GDPR consent required |
| Firebase / Firestore | Leaderboard read/write | game.html:537-634, game_mobile.html:513-588, index.html:390-430 | apiKey, appId, projectId, measurementId G-3WT4JX5MSG | Safe with proper rules; critical without them |
| Google Tag Manager CDN | Serves GA4 script | game.html:118, game_mobile.html:118, index.html:112 | — | SRI not feasible for gtag.js |
| gstatic.com CDN | Serves Firebase SDK | game.html:538-540, game_mobile.html:514-516, index.html:390-392 | — | No SRI; consider self-hosting |
| Ko-fi | Donations | game.html:6129, game_mobile.html:6832 | ko-fi.com/raginats | Low risk; Ko-fi handle is public |
| FormSubmit.co | Survey & bug reports | game.html:5951, game_mobile.html:6576 | stanigarkeith@gmail.com | Email is publicly visible in JS source |
| GitHub Pages | Analytics dashboard link | game.html:5769, game_mobile.html:6368 | kstanigar.github.io/non-x_analytics/ | Public link; exposes GitHub username |
| thomaskeithdev.com | Developer credit | game.html:5925, 6253, 7015, 7337; game_mobile.html:6547, 6898, 7686, 7884 | — | Informational only |
| AWS S3 | Game file hosting | deploy-aws.yml | Via GitHub secrets (not hardcoded) ✅ | OAC configured correctly |
| AWS CloudFront | CDN / HTTPS delivery | deploy-aws.yml | Via GitHub secrets (not hardcoded) ✅ | Missing security headers |
| GitHub Actions / OIDC | CI/CD deployment | .github/workflows/deploy-aws.yml | IAM role ARNs via secrets ✅ | OIDC federation — best practice |

---

## Hardcoded Keys, IDs & Credentials Found in Code

| Value | Type | Files & Line Numbers | Risk |
|---|---|---|---|
| `AIzaSyDumeBRk__-lcKFJA2WLD7Wi-0y6OuFZlo` | Firebase API Key | game.html:544, game_mobile.html:519, index.html:396 | HIGH — needs domain restriction in GCP Console |
| `nonx---game.firebaseapp.com` | Firebase authDomain | game.html:545, game_mobile.html:520, index.html:396 | Informational |
| `nonx---game` | Firebase projectId | game.html:546, game_mobile.html:521, index.html:396 | Informational |
| `nonx---game.firebasestorage.app` | Firebase storageBucket | game.html:547, game_mobile.html:522, index.html:396 | Informational |
| `404220834268` | Firebase messagingSenderId | game.html:548, game_mobile.html:523, index.html:396 | Informational |
| `1:404220834268:web:6cb71367bf62569ad5df19` | Firebase appId | game.html:549, game_mobile.html:524, index.html:396 | Informational |
| `G-3WT4JX5MSG` | Firebase/GA4 measurementId | game.html:550, game_mobile.html:525, index.html:396 | Informational |
| `G-9ECFZ9JBE5` | GA4 Property ID (primary) | game.html:42,118,123; game_mobile.html:118,123; index.html:32,112 | Low — GA4 IDs are designed to be public |
| `stanigarkeith@gmail.com` | Developer email | game.html:5951, game_mobile.html:6576 | MEDIUM — publicly visible, harvesting risk |
| `leaderboard` | Firestore collection name | game.html:570, game_mobile.html:539 | Low — visible to anyone reading source |
| `/Users/keithstanigar/Documents/Projects/...` | Dev machine paths | scripts/sync_paim.sh:6-7 | MEDIUM — exposes username/directory structure |

---

## External URL Inventory

| URL | Found In | Purpose |
|---|---|---|
| `https://www.googletagmanager.com/gtag/js?id=G-9ECFZ9JBE5` | All 3 HTML files | GA4 analytics script |
| `https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js` | All 3 HTML files | Firebase App SDK |
| `https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js` | All 3 HTML files | Firebase Firestore SDK |
| `https://ko-fi.com/raginats` | game.html:6129, game_mobile.html:6832 | Ko-fi donation button |
| `https://formsubmit.co/ajax/stanigarkeith@gmail.com` | game.html:5951, game_mobile.html:6576 | Survey/bug report submission |
| `https://kstanigar.github.io/non-x_analytics/` | game.html:5769, game_mobile.html:6368 | NON-X analytics dashboard |
| `https://www.thomaskeithdev.com/` | game.html:5925,6253,7015,7337; game_mobile.html:6547,6898,7686,7884 | Developer credit |
| `https://nonx.standingtiger.com` | deploy-aws.yml:34 | Production URL |
| `https://dev.nonx.standingtiger.com` | deploy-aws.yml:40 | Dev URL |

---

## localStorage Key Inventory

| Key | Files | What's Stored | Tamperable? |
|---|---|---|---|
| `nonx_player_id` | Both | UUID generated on first visit | Yes — affects player tracking only |
| `nonx_ab_music_group` | Both | A/B test assignment (A or B) | Yes — minor analytics skew |
| `nonex_music` | Both | Music on/off preference | Yes — benign |
| `nonex_movement` | game_mobile.html | Touch control preference | Yes — benign |
| `nonx_ai_mode` | Both | AI difficulty mode toggle | Yes — affects gameplay |
| `nonx_has_visited` | Both | First visit flag | Yes — benign |
| `nonx_visit_count` | Both | Session count for survey trigger | Yes — affects survey timing |
| `nonx_ig_handle` | Both | Player display name (sanitized) | Yes — see Finding 14 |
| `nonx_submitted_score` | Both | Last score submitted to Firebase | Yes — see Finding 9 |
| `nonx_ai_tier` | Both | Difficulty tier (-3 to +3) | Yes — could manipulate difficulty |
| `nonx_ai_cycles` | Both | Completed cycle count | Yes — affects difficulty scaling |
| `nonx_ai_speed_locked` | Both | Speed ratchet lock state | Yes — could reduce difficulty |
| `nonx_dev_mode` | Both | Dev mode persistence | Yes — enables dev features |
| `nonx_game_count` | Both | Games played (survey trigger) | Yes — affects survey timing |
| `nonx_survey_done` | Both | Survey completion flag | Yes — suppresses survey |
| `xenonHighScores` | Both | JSON array of local top scores | Yes — see Finding 9 |

---

## AWS Infrastructure Security Status

| Item | Status | Notes |
|---|---|---|
| S3 Block Public Access (prod) | ✅ Enabled | All 4 settings — June 3, 2026 |
| S3 Block Public Access (dev) | ✅ Enabled | All 4 settings |
| CloudFront OAC (prod) | ✅ nonx-prod-oac | June 3, 2026 |
| CloudFront OAC (dev) | ✅ Configured | May 31, 2026 |
| S3 Versioning (prod) | ✅ Enabled | June 3, 2026 |
| HTTPS enforcement | ⚠️ Unverified | Verify Viewer Protocol Policy — see Finding 15 |
| CloudFront security headers | ❌ Missing | Finding 6 |
| Content Security Policy | ❌ Missing | Finding 4 |
| CloudFront access logging | ⚠️ Unknown | Verify in CloudFront console |
| Minimum TLS version | ⚠️ Unknown | Should be TLSv1.2_2021 minimum |
| AWS WAF | ❌ Not configured | Optional but recommended |
| AWS Shield Standard | ✅ Default | Free, always on |
| GitHub Actions OIDC | ✅ Configured | Best practice — no hardcoded keys |
| GitHub repository secrets | ✅ Correct | All AWS credentials via secrets |

---

## Prioritized Phase Plan

### Phase 1 — Critical (Do Before Any Public Traffic) ~25 min
- [x] 1A — Verify and deploy Firestore security rules (Finding 1) — June 13, 2026
- [x] 1B — Rules confirmed published in Firebase Console
- [ ] 1C — Set Firebase budget alerts (Finding 17) — N/A: on Spark plan, monitor quotas instead

### Phase 2 — High Priority (This Week) ~85 min
- [x] 2A — Restrict Firebase API key to production domains (Finding 2) — June 13, 2026
- [ ] 2B — Enable Firebase App Check with reCAPTCHA v3 (Finding 16)
- [ ] 2C — Refactor leaderboard rendering to use textContent (Finding 3)
- [ ] 2D — Create & attach CloudFront Security Headers policy (Finding 6)
- [ ] 2E — Create & attach CloudFront CSP header in Report-Only mode (Finding 4)
- [ ] 2F — Gate dev/god URL params and keyboard shortcuts to non-production (Findings 8, 18)

### Phase 3 — Medium Priority (This Sprint) ~110 min
- [ ] 3A — Implement GA4 Consent Mode v2 + consent banner (Finding 5)
- [ ] 3B — Add Privacy Policy page
- [ ] 3C — Replace FormSubmit email with hashed endpoint (Finding 7)
- [ ] 3D — Audit & refactor score submission to use in-memory variable (Finding 9)
- [ ] 3E — Replace console.* calls with hostname-gated logger (Finding 10)
- [ ] 3F — Fix savedHandle HTML attribute encoding (Finding 14)
- [ ] 3G — Refactor Ko-fi onclick to addEventListener (Finding 13)

### Phase 4 — Low Priority / Polish ~65 min
- [ ] 4A — Replace hardcoded paths in scripts/sync_paim.sh (Finding 12)
- [ ] 4B — Add SRI to Ko-fi script and DOMPurify (Finding 11)
- [ ] 4C — Verify CloudFront HTTPS enforcement (Finding 15)
- [ ] 4D — Verify CloudFront TLS policy = TLSv1.2_2021
- [ ] 4E — Verify CloudFront access logging enabled
- [ ] 4F — Switch CSP from Report-Only to enforcement mode (after Phase 2E verified)

---

---

# Step-by-Step Instructions Per Finding

---

## Finding 1 — Verify & Deploy Firestore Security Rules
**Severity: CRITICAL**
**Estimated Time:** 15 minutes
**Files:** Firebase Console only (no code changes)

### Steps
1. Open Firebase Console: https://console.firebase.google.com/
2. Select the NON-X project from the project list
3. In the left sidebar click **Firestore Database**
4. Click the **Rules** tab at the top of the Firestore panel
5. Read the current rules — if they contain `allow read, write: if true` the database is wide open and this is urgent
6. Replace the entire contents of the rules editor with the code below
7. Before publishing, click **Rules Simulator** (button near top of editor)
8. Run these 5 test cases in the simulator:
   - **Test 1:** GET `/leaderboard/anyDoc` as unauthenticated → should **ALLOW**
   - **Test 2:** CREATE `/leaderboard/newDoc` with `{score: 5000, name: "Player1", timestamp: <now>}` → should **ALLOW**
   - **Test 3:** CREATE with `{score: 9999999, name: "Player1", timestamp: <now>}` → should **DENY** (score > 999999)
   - **Test 4:** UPDATE where new score <= existing score → should **DENY**
   - **Test 5:** DELETE any document → should **DENY**
9. Once all 5 tests pass, click **Publish**

### Verify
- [ ] Rules tab shows "Published" status
- [ ] Leaderboard loads correctly in the game (no Firestore auth errors)
- [ ] Open browser DevTools Console on the game and attempt: `firebase.firestore().collection('leaderboard').add({score: 9999999, name: 'hack', timestamp: new Date()})` → should fail with permission-denied

### Code
```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /leaderboard/{docId} {
      // Anyone can read leaderboard
      allow read: if true;

      // Create: all fields required, score and name validated, timestamp must be server time
      allow create: if
        request.resource.data.keys().hasAll(['score', 'name', 'timestamp']) &&
        request.resource.data.score is int &&
        request.resource.data.score >= 0 &&
        request.resource.data.score <= 999999 &&
        request.resource.data.name is string &&
        request.resource.data.name.size() >= 1 &&
        request.resource.data.name.size() <= 30 &&
        request.resource.data.timestamp == request.time;

      // Update: only allow if new score is strictly higher
      allow update: if
        request.resource.data.score is int &&
        request.resource.data.score > resource.data.score &&
        request.resource.data.score <= 999999;

      // Nobody deletes leaderboard entries from client
      allow delete: if false;
    }

    // Deny everything else
    match /{document=**} {
      allow read, write: if false;
    }
  }
}
```

---

## Finding 2 — Restrict Firebase API Key in Google Cloud Console
**Severity: HIGH**
**Estimated Time:** 10 minutes
**Files:** Google Cloud Console only (no code changes)

### Steps
1. Open Google Cloud Console: https://console.cloud.google.com/
2. Confirm the correct project (`nonx---game`) is selected in the top project dropdown
3. In the left sidebar go to **APIs & Services** → **Credentials**
4. Under the **API keys** section find the Firebase web key (labeled "Browser key" or "Android key" — look for the one matching `AIzaSyDumeBRk__-lcKFJA2WLD7Wi-0y6OuFZlo`)
5. Click the key name to open its edit page
6. Under **Application restrictions** select **HTTP referrers (web sites)**
7. Click **Add an item** and add each of these (one per line):
   ```
   https://nonx.standingtiger.com/*
   https://dev.nonx.standingtiger.com/*
   ```
8. Under **API restrictions** select **Restrict key**
9. In the dropdown check only:
   - Cloud Firestore API
   - Firebase Installations API
   - Identity Toolkit API (required for Firebase SDK initialization)
10. Click **Save**
11. Wait 1–2 minutes for restrictions to propagate

### Verify
- [ ] Navigate to https://nonx.standingtiger.com — leaderboard loads without errors
- [ ] Navigate to https://dev.nonx.standingtiger.com — leaderboard loads without errors
- [ ] In Google Cloud Console → Credentials, confirm the key shows "HTTP referrers" restriction with 2 entries
- [ ] Optional: attempt to call Firestore from a different origin (e.g., localhost not in the allowed list) — should receive 403

### Notes
- No code changes needed in the game files
- The Firebase config in your HTML files does not need to change — the restriction is enforced server-side by Google

---

## Finding 3 — Fix XSS via innerHTML (Leaderboard Player Names)
**Severity: HIGH**
**Estimated Time:** 20 minutes
**Files:** game.html (lines 1452–1474, 1530–1561), game_mobile.html (lines 1395–1417, 1474–1504)

### Steps
1. Open `game.html` in your editor
2. Search for the leaderboard rendering function — find where `playerName` is concatenated into an HTML string then assigned to `innerHTML`
3. Locate the two main instances:
   - **Compact leaderboard** (game.html ~1452–1474): builds `cols[col] += ...playerName...` then `display.innerHTML = html`
   - **Modal leaderboard** (game.html ~1530–1561): same pattern into `content.innerHTML = html`
4. Refactor using the before/after pattern in the Code section below
5. Repeat for the same two functions in `game_mobile.html` (~1395–1417 and ~1474–1504)
6. Test: leaderboard should still display correctly with scores and names

### Verify
- [ ] Leaderboard displays correctly with real player names and scores
- [ ] In browser DevTools → Elements inspector, confirm player name text is inside a text node (not raw HTML)
- [ ] Test with a specially crafted name: go to Firebase Console → Firestore → leaderboard collection → add a test document with `name: "<img src=x onerror=alert(1)>"` — the leaderboard should display the literal text `<img src=x onerror=alert(1)>`, not execute the script

### Code

**Before (Vulnerable):**
```javascript
// Builds HTML string with playerName from Firestore, then dumps into innerHTML
var html = '';
entries.forEach(function(entry, i) {
  var playerName = entry.name || 'Anonymous';
  html += "<div class='lb-row'>";
  html += "<span class='lb-rank'>" + (i + 1) + "</span>";
  html += "<span class='lb-name' style='color:" + nameColor + ";'>" + playerName + "</span>";
  html += "<span class='lb-score'>" + entry.score + "</span>";
  html += "</div>";
});
display.innerHTML = html;  // XSS risk if playerName contains HTML
```

**After (Safe — DOM construction):**
```javascript
// Builds DOM nodes directly — textContent never executes HTML
var container = document.createDocumentFragment();
entries.forEach(function(entry, i) {
  var playerName = entry.name || 'Anonymous';

  var row = document.createElement('div');
  row.className = 'lb-row';

  var rankSpan = document.createElement('span');
  rankSpan.className = 'lb-rank';
  rankSpan.textContent = (i + 1);

  var nameSpan = document.createElement('span');
  nameSpan.className = 'lb-name';
  nameSpan.style.color = nameColor;
  nameSpan.textContent = playerName;  // Safe — never executes HTML

  var scoreSpan = document.createElement('span');
  scoreSpan.className = 'lb-score';
  scoreSpan.textContent = entry.score;

  row.appendChild(rankSpan);
  row.appendChild(nameSpan);
  row.appendChild(scoreSpan);
  container.appendChild(row);
});

display.textContent = '';  // Clear existing content safely
display.appendChild(container);
```

---

## Finding 4 — Deploy Content Security Policy via CloudFront
**Severity: HIGH**
**Estimated Time:** 15 minutes
**Files:** AWS CloudFront Console only

### Steps
1. Open AWS CloudFront Console: https://console.aws.amazon.com/cloudfront/v3/home
2. In the left sidebar click **Policies** → **Response headers**
3. Click **Create response headers policy**
4. Name it: `nonx-csp-policy`
5. Scroll to **Custom headers** section → click **Add header**
6. Add this header in **Report-Only mode first** (safer — won't break anything):
   - Header name: `Content-Security-Policy-Report-Only`
   - Value: (use the CSP value in the Code section below)
   - Override: Yes
7. Click **Create policy**
8. Navigate to **Distributions** → select your distribution → **Behaviors** tab
9. Select the default behavior (`*`) → click **Edit**
10. Under **Response headers policy** select `nonx-csp-policy`
11. Click **Save changes** — wait 3–5 minutes for propagation
12. Repeat steps 8–11 for the dev distribution

### Verify
- [ ] Open https://nonx.standingtiger.com in Chrome → DevTools → Network tab → click index.html → Response Headers → confirm `content-security-policy-report-only` is present
- [ ] Check DevTools Console for any CSP violation warnings — these indicate what needs to be added to the policy before switching to enforcement mode
- [ ] The game should function completely normally (Report-Only never blocks anything)
- [ ] After verifying zero violations: update the header name to `Content-Security-Policy` (enforcement mode) — see Phase 4 task 4F

### Code

**CSP header value (paste this as the header value in CloudFront):**
```
default-src 'none'; script-src 'self' https://www.googletagmanager.com https://www.gstatic.com https://cdn.jsdelivr.net 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; media-src 'self' blob:; connect-src 'self' https://*.googleapis.com https://firestore.googleapis.com https://securetoken.googleapis.com https://*.firebaseio.com https://www.google-analytics.com https://analytics.google.com https://region1.google-analytics.com https://ko-fi.com https://cdn.ko-fi.com https://formsubmit.co; frame-src https://ko-fi.com; font-src 'self'; object-src 'none'; base-uri 'none'; form-action 'self' https://formsubmit.co; frame-ancestors 'none'; upgrade-insecure-requests;
```

**Note on combining with Finding 6:** CloudFront allows only **one** Response Headers Policy per cache behavior. Create **one policy** that contains both the CSP header (Finding 4) AND all security headers (Finding 6) — do not create two separate policies.

---

## Finding 5 — GA4 Consent Mode v2 + Consent Banner
**Severity: HIGH**
**Estimated Time:** 20 minutes
**Files:** game.html, game_mobile.html, index.html

### Steps
1. Open `game.html`
2. Find the GA4 script block (lines 117–127):
   ```html
   <script async src="https://www.googletagmanager.com/gtag/js?id=G-9ECFZ9JBE5"></script>
   ```
3. **Immediately before** that `<script async>` line, add the consent default block (Code section — Block A)
4. In the `<body>` tag, add the consent banner HTML (Code section — Block B) as the very first element inside `<body>`
5. In your main `<script>` block, add the consent banner handler (Code section — Block C)
6. Repeat steps 2–5 for `game_mobile.html` and `index.html`

### Verify
- [ ] Open the game in an incognito window → DevTools → Network tab
- [ ] Filter by `collect` or `google-analytics` — before clicking Accept, confirm **no GA4 collect requests are sent**
- [ ] Click the Accept button → confirm GA4 collect requests **now appear** in Network tab
- [ ] Reload the page (without clearing localStorage) → banner should **not** re-appear (consent persisted)
- [ ] Clear localStorage and reload → banner should appear again

### Code

**Block A — Add BEFORE the `<script async src="...gtag/js">` line:**
```html
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  gtag('consent', 'default', {
    'analytics_storage': 'denied',
    'ad_storage': 'denied',
    'ad_user_data': 'denied',
    'ad_personalization': 'denied'
  });
</script>
```

**Block B — First element inside `<body>`:**
```html
<div id="consentBanner" style="position:fixed;bottom:0;left:0;right:0;background:#1a1a2e;color:#ccc;padding:14px 20px;z-index:99999;font-size:13px;display:flex;align-items:center;justify-content:space-between;gap:16px;font-family:monospace;border-top:1px solid #00FFFF;">
  <span>This game uses analytics cookies to track gameplay. <a href="/privacy.html" style="color:#00FFFF;">Privacy Policy</a></span>
  <div style="display:flex;gap:8px;flex-shrink:0;">
    <button id="declineConsent" style="padding:6px 16px;background:transparent;color:#888;border:1px solid #444;border-radius:4px;cursor:pointer;font-family:monospace;">Decline</button>
    <button id="acceptConsent" style="padding:6px 16px;background:#00FFFF;color:#000;border:none;border-radius:4px;cursor:pointer;font-weight:bold;font-family:monospace;">Accept</button>
  </div>
</div>
```

**Block C — Consent handler (add in your main script block):**
```javascript
(function() {
  var banner = document.getElementById('consentBanner');
  if (!banner) return;

  // Already consented — hide banner and grant
  if (localStorage.getItem('nonx_consent') === 'granted') {
    banner.style.display = 'none';
    gtag('consent', 'update', { 'analytics_storage': 'granted' });
    return;
  }
  // Already declined — hide banner and keep denied
  if (localStorage.getItem('nonx_consent') === 'denied') {
    banner.style.display = 'none';
    return;
  }

  document.getElementById('acceptConsent').addEventListener('click', function() {
    localStorage.setItem('nonx_consent', 'granted');
    gtag('consent', 'update', {
      'analytics_storage': 'granted',
      'ad_storage': 'granted',
      'ad_user_data': 'granted',
      'ad_personalization': 'granted'
    });
    banner.style.display = 'none';
  });

  document.getElementById('declineConsent').addEventListener('click', function() {
    localStorage.setItem('nonx_consent', 'denied');
    banner.style.display = 'none';
  });
})();
```

---

## Finding 6 — CloudFront Security Headers
**Severity: HIGH**
**Estimated Time:** 15 minutes
**Files:** AWS CloudFront Console only

### Steps

**Important:** Combine this with Finding 4 into a single Response Headers Policy (CloudFront only allows one policy per cache behavior).

1. Open AWS CloudFront Console: https://console.aws.amazon.com/cloudfront/v3/home
2. Go to **Policies** → **Response headers**
3. Click **Create response headers policy**
4. Name it: `nonx-security-headers`
5. In the **Security headers** section, enable and configure:
   - **Strict-Transport-Security:** Enable → `max-age=63072000; includeSubDomains; preload`
   - **X-Content-Type-Options:** Enable → `nosniff`
   - **X-Frame-Options:** Enable → `DENY`
   - **Referrer-Policy:** Enable → `strict-origin-when-cross-origin`
   - **X-XSS-Protection:** Enable → `1; mode=block` (legacy browsers)
6. In **Custom headers** section → **Add header** for Permissions-Policy:
   - Header name: `Permissions-Policy`
   - Value: `camera=(), microphone=(), geolocation=(), payment=()`
7. In the same **Custom headers** section → **Add header** for the CSP from Finding 4:
   - Header name: `Content-Security-Policy-Report-Only`
   - Value: (paste CSP value from Finding 4)
8. Click **Create policy**
9. Go to **Distributions** → select distribution → **Behaviors** → default behavior → **Edit**
10. Under **Response headers policy** select `nonx-security-headers`
11. **Save changes** — wait 3–5 minutes
12. Repeat for dev distribution

### Verify
- [ ] Open https://nonx.standingtiger.com → DevTools → Network → select index.html → Response Headers
- [ ] Confirm all of these headers are present:
  - `strict-transport-security`
  - `x-content-type-options: nosniff`
  - `x-frame-options: DENY`
  - `referrer-policy: strict-origin-when-cross-origin`
  - `permissions-policy`
  - `content-security-policy-report-only`
- [ ] Run Mozilla Observatory scan: https://observatory.mozilla.org → enter `nonx.standingtiger.com` → grade should improve significantly

---

## Finding 7 — Replace FormSubmit Email with Hashed Endpoint
**Severity: MEDIUM**
**Estimated Time:** 10 minutes
**Files:** game.html (line 5951), game_mobile.html (line 6576)

### Steps
1. Go to https://formsubmit.co/
2. In the main form, enter `stanigarkeith@gmail.com` and submit once — this activates the email and generates a hash
3. Check your email inbox — FormSubmit sends a confirmation/activation email
4. After activation, your hashed endpoint will be in the format:
   `https://formsubmit.co/ajax/[32-character-hash]`
   (FormSubmit shows this on their site after activation, or it is included in the confirmation email)
5. Open `game.html` and go to line 5951:
   ```javascript
   var FORMSUBMIT_URL = 'https://formsubmit.co/ajax/stanigarkeith@gmail.com';
   ```
6. Replace with:
   ```javascript
   var FORMSUBMIT_URL = 'https://formsubmit.co/ajax/[YOUR-HASH-HERE]';
   ```
7. Open `game_mobile.html` and make the same change at line 6576
8. Test by submitting a survey or bug report in the game — you should still receive the email

### Verify
- [ ] View page source on the live game — confirm no email address appears in the source
- [ ] Submit a test bug report or survey through the game
- [ ] Confirm you receive the form submission at `stanigarkeith@gmail.com`

---

## Finding 8 — Gate Dev/God URL Parameters to Non-Production
**Severity: MEDIUM**
**Estimated Time:** 10 minutes
**Files:** game.html (lines 1830–1845), game_mobile.html (equivalent lines)

### Steps
1. Open `game.html` and find the URL parameter parsing block around line 1830
2. Wrap the entire URL param block with the environment check shown in the Code section
3. Save and test on dev: `https://dev.nonx.standingtiger.com/game.html?dev=true&god=true` → dev/god mode should activate
4. Test on production: `https://nonx.standingtiger.com/game.html?dev=true&god=true` → params should be silently ignored
5. Repeat for `game_mobile.html`

### Verify
- [ ] Dev URL with params → dev/god mode activates
- [ ] Production URL with same params → no effect, no console errors
- [ ] Level selection param (`?level=5`) works on dev, silently ignored on production

### Code
```javascript
var isDevEnvironment = (
  window.location.hostname === 'localhost' ||
  window.location.hostname.startsWith('127.') ||
  window.location.hostname === 'dev.nonx.standingtiger.com'
);

if (isDevEnvironment) {
  var urlParams = new URLSearchParams(window.location.search);
  var startLevel = parseInt(urlParams.get('level'), 10);
  if (startLevel >= 1 && startLevel <= 12) { /* set level */ }
  if (urlParams.get('god') === 'true') { godMode = true; }
  if (urlParams.get('dev') === 'true') {
    devMode = true;
    localStorage.setItem('nonx_dev_mode', 'true');
  }
}
```

---

## Finding 9 — Confirm Score Comes from Memory, Not localStorage
**Severity: MEDIUM**
**Estimated Time:** 25 minutes
**Files:** game.html, game_mobile.html

### Steps
1. Open `game.html` and search for where score is incremented during gameplay (search for `score +=` or `score =`)
2. Verify the authoritative score variable is a local JS variable (e.g., `var score = 0`) in the game loop scope — **not** read from localStorage
3. Search for where the score is submitted to Firebase (`firebaseSubmitScore` call) — confirm it uses the in-memory `score` variable, not `localStorage.getItem('nonx_submitted_score')`
4. If score IS read from localStorage at submission time, refactor using the ScoreManager pattern below
5. The `nonx_submitted_score` localStorage key should only be written AFTER successful submission (as a record of what was submitted), never read back for a new submission

### Verify
- [ ] Open DevTools Console on the game → type `score` → should return `undefined` or ReferenceError (not accessible globally if scoped properly)
- [ ] Play through a game and verify the final submitted score matches what was earned in gameplay
- [ ] Check that `localStorage.getItem('nonx_submitted_score')` is never used as the value passed to `firebaseSubmitScore()`

### Code (ScoreManager IIFE — use only if score needs refactoring)
```javascript
var ScoreManager = (function() {
  var _score = 0;
  return {
    addPoints: function(pts) { _score += Math.max(0, pts); return _score; },
    getScore: function() { return _score; },
    reset: function() { _score = 0; }
  };
})();

// Usage: ScoreManager.addPoints(100); ScoreManager.getScore();
// At submission: firebaseSubmitScore({ score: ScoreManager.getScore(), ... });
```

---

## Finding 10 — Replace console.* with Production-Safe Logger
**Severity: MEDIUM**
**Estimated Time:** 15 minutes
**Files:** game.html (6 instances), game_mobile.html (7 instances), index.html (1 instance)

### Steps
1. Open `game.html`
2. Add the `logger` object near the top of your main `<script>` block (Code section below)
3. Use Find & Replace (Cmd+H in VS Code):
   - Find `console.error(` → Replace `logger.error(`
   - Find `console.warn(` → Replace `logger.warn(`
4. Repeat for `game_mobile.html` and `index.html`
5. Test on dev: confirm error/warn messages still appear in DevTools Console
6. Test on production: confirm DevTools Console is clean (no game messages)

### Instance List to Replace
**game.html:** lines 611, 631, 3267, 3277, 3718, 7635
**game_mobile.html:** lines 575, 587, 3559, 3567, 3930, 7121, 8448
**index.html:** line 430

### Verify
- [ ] Open dev.nonx.standingtiger.com → DevTools Console → error messages appear as expected
- [ ] Open nonx.standingtiger.com → DevTools Console → **no game-related messages appear**
- [ ] Game functions correctly on both environments

### Code
```javascript
// Add near top of main <script> block in each file
var logger = (function() {
  var isProd = window.location.hostname === 'nonx.standingtiger.com';
  return {
    error: function() { if (!isProd) console.error.apply(console, arguments); },
    warn:  function() { if (!isProd) console.warn.apply(console, arguments);  },
    log:   function() { if (!isProd) console.log.apply(console, arguments);   }
  };
})();
```

---

## Finding 11 — Subresource Integrity (SRI) for External Scripts
**Severity: MEDIUM**
**Estimated Time:** 20 minutes
**Files:** game.html, game_mobile.html, index.html

### Steps

**DOMPurify (add if refactoring Finding 3):**
1. Open Terminal and run to generate the SRI hash:
   ```bash
   curl -s https://cdn.jsdelivr.net/npm/dompurify@3.1.6/dist/purify.min.js | openssl dgst -sha384 -binary | openssl base64 -A
   ```
2. Copy the output hash
3. Add to HTML `<head>` before your main script:
   ```html
   <script src="https://cdn.jsdelivr.net/npm/dompurify@3.1.6/dist/purify.min.js"
           integrity="sha384-PASTE_HASH_HERE"
           crossorigin="anonymous"></script>
   ```

**Ko-fi (if a formal widget script is ever added):**
1. Get the exact Ko-fi CDN script URL from your embed code
2. Run: `curl -s [KO_FI_SCRIPT_URL] | openssl dgst -sha384 -binary | openssl base64 -A`
3. Add `integrity="sha384-HASH" crossorigin="anonymous"` to the `<script>` tag

**Firebase & GA4:** SRI is **not feasible** — Google updates these files server-side without changing URLs. Mitigate via CSP (Finding 4) which restricts which domains can load scripts.

### Verify
- [ ] Load game in browser → DevTools → Console → no SRI mismatch errors
- [ ] DevTools → Network → select the DOMPurify script → confirm `integrity` attribute is present in Initiator or Elements inspector

---

## Finding 12 — Fix Hardcoded Paths in sync_paim.sh
**Severity: MEDIUM**
**Estimated Time:** 10 minutes
**Files:** scripts/sync_paim.sh

### Steps
1. Open `scripts/sync_paim.sh`
2. Replace hardcoded paths on lines 6–7 with environment variable pattern (Code section below)
3. Open `.gitignore` in the project root and add `.env` if not already there
4. Create a `.env` file in project root (this file should **never** be committed):
   ```bash
   XENON_PATH="/Users/ks2026/Documents/Projects/2026/Xenon_3"
   ANALYTICS_PATH="/Users/ks2026/Documents/Projects/2026/non-x_analytics"
   ```
5. Test the script: `source .env && ./scripts/sync_paim.sh`

### Verify
- [ ] `git status` does not show `.env` as a tracked or modified file
- [ ] `grep -r "keithstanigar" scripts/` returns no results
- [ ] Script runs correctly when env vars are set

### Code

**Before:**
```bash
XENON="/Users/keithstanigar/Documents/Projects/Xenon_3/NON-X_PAIM_Memory.md"
ANALYTICS="/Users/keithstanigar/Documents/Projects/non-x_analytics/docs/NON-X_PAIM_Memory.md"
```

**After:**
```bash
# Paths via environment variables — set in .env (never commit .env)
XENON_PATH="${XENON_PATH:-/Users/ks2026/Documents/Projects/2026/Xenon_3}"
ANALYTICS_PATH="${ANALYTICS_PATH:-/Users/ks2026/Documents/Projects/2026/non-x_analytics}"
XENON="${XENON_PATH}/NON-X_PAIM_Memory.md"
ANALYTICS="${ANALYTICS_PATH}/docs/NON-X_PAIM_Memory.md"
```

**.gitignore entry to add:**
```
.env
.env.local
```

---

## Finding 13 — Refactor Ko-fi onclick to addEventListener
**Severity: LOW**
**Estimated Time:** 15 minutes
**Files:** game.html (line 6129), game_mobile.html (line 6832)

### Steps
1. Open `game.html` and find the Ko-fi link builder around line 6129
2. Refactor using the pattern in the Code section — remove inline `onclick` string, return a DOM element instead of an HTML string, attach the gtag event via `addEventListener`
3. Update all call sites to use `appendChild` instead of `innerHTML +=`
4. Repeat for `game_mobile.html` line 6832

### Verify
- [ ] Ko-fi button appears correctly in the game
- [ ] Clicking it opens `https://ko-fi.com/raginats` in a new tab
- [ ] DevTools → Network → confirm a GA4 `kofi_click` event fires after clicking

### Code

**Before:**
```javascript
function buildKofiButtonHTML(source) {
  return "<a href='https://ko-fi.com/raginats' target='_blank' " +
    "onclick=\"if(typeof gtag !== 'undefined') gtag('event', 'kofi_click', {location: '" + source + "'});\">" +
    "Support ⚡</a>";
}
container.innerHTML += buildKofiButtonHTML('game_over');
```

**After:**
```javascript
function buildKofiButton(source) {
  var link = document.createElement('a');
  link.href = 'https://ko-fi.com/raginats';
  link.target = '_blank';
  link.rel = 'noopener noreferrer';
  link.textContent = 'Support ⚡';
  link.addEventListener('click', function() {
    if (typeof gtag !== 'undefined') {
      gtag('event', 'kofi_click', { location: source });
    }
  });
  return link;
}
container.appendChild(buildKofiButton('game_over'));
```

---

## Finding 14 — HTML-encode savedHandle Before Attribute Injection
**Severity: LOW**
**Estimated Time:** 10 minutes
**Files:** game.html (lines 1903, 6181), game_mobile.html (equivalent lines)

### Steps
1. Open `game.html` and add the `escapeAttr()` function near the top of your main script block
2. Find all instances where `savedHandle` is used inside an HTML attribute string (search for `value='" + savedHandle`)
3. Wrap each occurrence: `value='" + escapeAttr(savedHandle) + "'`
4. Repeat for `game_mobile.html`

### Verify
- [ ] Submit a name with special characters: `Test's "Quote" <tag>`
- [ ] Reload the page — the input field should correctly pre-fill with that name
- [ ] View page source — the value attribute should show HTML-encoded characters (`&#x27;`, `&quot;`, etc.) not raw `'` or `"`

### Code
```javascript
function escapeAttr(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g,  '&amp;')
    .replace(/</g,  '&lt;')
    .replace(/>/g,  '&gt;')
    .replace(/"/g,  '&quot;')
    .replace(/'/g,  '&#x27;');
}

// Usage:
// Before: "value='" + savedHandle + "'"
// After:  "value='" + escapeAttr(savedHandle) + "'"
```

---

## Finding 15 — Verify CloudFront HTTPS Enforcement
**Severity: LOW**
**Estimated Time:** 10 minutes
**Files:** AWS CloudFront Console only

### Steps
1. Open AWS CloudFront Console: https://console.aws.amazon.com/cloudfront/v3/home
2. Select your production distribution (ED9CRAIN93YRS)
3. Click the **Behaviors** tab
4. Select the default behavior (`*`) → click **Edit**
5. Find **Viewer protocol policy** — confirm it is set to **Redirect HTTP to HTTPS**
   - If it shows anything else, change it to "Redirect HTTP to HTTPS"
6. Scroll down → **Save changes**
7. Repeat for dev distribution (E1Q496KLUYVM0Z)
8. While in the distribution settings, check **Security policy** under **Settings** tab → confirm it is `TLSv1.2_2021` or higher

### Verify
- [ ] In a browser, navigate to `http://nonx.standingtiger.com` (plain HTTP)
- [ ] Browser should automatically redirect to `https://nonx.standingtiger.com`
- [ ] DevTools → Network tab → first request should show status 301/302 with Location: https://...

---

## Finding 16 — Enable Firebase App Check
**Severity: LOW**
**Estimated Time:** 30 minutes
**Files:** Firebase Console + game.html, game_mobile.html, index.html

### Steps
1. Open Firebase Console: https://console.firebase.google.com/
2. Select the NON-X project
3. In the left sidebar go to **Build** → **App Check**
4. Click **Get started** if first time
5. Click on your registered web app (or **Register app** if not registered)
6. Under **reCAPTCHA v3**, click **Manage** → this opens Google reCAPTCHA Admin Console
7. Register your site: https://www.google.com/recaptcha/admin/create
   - Label: `NON-X Game`
   - reCAPTCHA type: **v3**
   - Domains: `nonx.standingtiger.com`, `dev.nonx.standingtiger.com`
   - Click **Submit** → copy the **Site Key**
8. Back in Firebase App Check — paste the reCAPTCHA v3 Site Key → click **Save**
9. Add the initializeAppCheck code to your HTML files (Code section below) — add it in the Firebase module script, immediately after `initializeApp(firebaseConfig)`
10. Set enforcement mode: In Firebase Console → App Check → your app → click **Enforce** (or start with **Monitor** for 1–2 days first to verify no legitimate traffic is blocked)
11. For dev testing, get a debug token:
    - Firebase Console → App Check → your app → **Debug tokens** → **Add debug token**
    - Copy the token
    - In browser DevTools on dev.nonx.standingtiger.com, run: `localStorage.setItem('FIREBASE_APPCHECK_DEBUG_TOKEN', 'YOUR_DEBUG_TOKEN')`

### Verify
- [ ] Reload the game — no App Check errors in DevTools Console
- [ ] Leaderboard loads and score submission works
- [ ] Firebase Console → App Check → Metrics → confirm requests showing "verified" status

### Code
```javascript
// Add to your Firebase module script, after initializeApp(firebaseConfig)
import { initializeAppCheck, ReCaptchaV3Provider } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app-check.js";

const appCheck = initializeAppCheck(app, {
  provider: new ReCaptchaV3Provider('YOUR_RECAPTCHA_V3_SITE_KEY'),
  isTokenAutoRefreshEnabled: true
});
```

---

## Finding 17 — Set Firebase Budget Alerts
**Severity: LOW**
**Estimated Time:** 15 minutes
**Files:** Firebase Console / Google Cloud Console only

### Steps

**First — determine your Firebase plan:**
1. Firebase Console → gear icon (Project Settings) → **Usage and billing** tab
2. Note if you're on **Spark** (free) or **Blaze** (pay-as-you-go)

**If on Spark (Free) plan:**
- No billing alerts available (there is no bill on Spark)
- Instead, monitor daily quotas:
  - Firebase Console → Project Settings → **Usage and billing**
  - Daily limits: 20K Firestore reads, 20K writes, 50K deletes, 1GB bandwidth
  - These reset at midnight Pacific time
- Consider upgrading to Blaze if you want budget alerts — Blaze is pay-as-you-go and free tier usage still costs $0

**If on Blaze (Pay-as-you-go) plan:**
1. Open Google Cloud Console: https://console.cloud.google.com/
2. Confirm your NON-X project is selected
3. Left sidebar → **Billing** → **Budgets & alerts**
4. Click **Create budget**
5. Name: `NON-X Firebase Alert`
6. Scope: select your project
7. Set budget amount: `$5` → under Threshold rules:
   - 50% of $5 → alert at $2.50 (early warning)
   - 100% of $5 → alert at $5.00
8. Click **Finish** → then create two more budgets:
   - `NON-X Firebase Warning` → $20
   - `NON-X Firebase Critical` → $50
9. Add email notification: use your email address as a notification channel

### Verify
- [ ] Google Cloud Console → Billing → Budgets & alerts shows 3 budgets listed
- [ ] Each budget shows your email address as a notification recipient
- [ ] Firebase Console → Usage and billing confirms plan tier

---

## Finding 18 — Gate Dev Keyboard Shortcuts to Non-Production
**Severity: LOW**
**Estimated Time:** 10 minutes
**Files:** game.html, game_mobile.html

### Steps
1. Open `game.html` and search for `keydown` event listener or `e.shiftKey`
2. Find the block handling Shift+D (dev mode) and Shift+A (AI mode toggle if present)
3. Wrap the entire `addEventListener('keydown', ...)` registration in the `isDevEnvironment` check (Code section below)
4. Repeat for `game_mobile.html`

### Verify
- [ ] On dev.nonx.standingtiger.com: Shift+D toggles dev mode (confirm in DevTools Console)
- [ ] On nonx.standingtiger.com: Shift+D has no effect (no console output, no mode change)
- [ ] Game plays normally on production with no side-effects

### Code
```javascript
var isDevEnvironment = (
  window.location.hostname === 'localhost' ||
  window.location.hostname.startsWith('127.') ||
  window.location.hostname === 'dev.nonx.standingtiger.com'
);

if (isDevEnvironment) {
  document.addEventListener('keydown', function(e) {
    if (e.shiftKey && e.key === 'D') {
      devMode = !devMode;
      localStorage.setItem('nonx_dev_mode', devMode ? 'true' : 'false');
      logger.log('Dev mode:', devMode);
    }
    if (e.shiftKey && e.key === 'A') {
      // AI mode toggle or other dev shortcut
      logger.log('Dev shortcut triggered');
    }
  });
}
```

---

## 2026 Research Sources

| Topic | Source |
|---|---|
| CSP | https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP |
| Firestore Security Rules | https://firebase.google.com/docs/firestore/security/get-started |
| Firebase App Check | https://firebase.google.com/docs/app-check |
| Firebase Security Checklist | https://firebase.google.com/support/guides/security-checklist |
| Firebase API Key Best Practices | https://firebase.google.com/docs/projects/api-keys |
| GA4 Consent Mode v2 | https://developers.google.com/tag-platform/security/guides/consent |
| GA4 Cookies Reference | https://developers.google.com/analytics/devguides/collection/ga4/cookies-user-id |
| GDPR + Analytics | https://edpb.europa.eu/our-work-tools/our-documents/guidelines |
| XSS Prevention (DOM) | https://cheatsheetseries.owasp.org/cheatsheets/DOM_based_XSS_Prevention_Cheat_Sheet.html |
| DOMPurify | https://github.com/cure53/DOMPurify |
| Trusted Types API | https://developer.mozilla.org/en-US/docs/Web/API/Trusted_Types_API |
| localStorage Security | https://cheatsheetseries.owasp.org/cheatsheets/HTML5_Security_Cheat_Sheet.html |
| CloudFront Response Headers | https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/creating-response-headers-policies.html |
| CloudFront Managed Policies | https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/using-managed-response-headers-policies.html |
| AWS S3 Security Best Practices | https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html |
| Subresource Integrity | https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity |
| SRI Hash Generator | https://srihash.org/ |
| OWASP Game Security Framework | https://owasp.org/www-project-game-security-framework/ |
| OWASP Logging Cheat Sheet | https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html |
| Ko-fi Privacy Policy | https://ko-fi.com/Privacy |
| Mozilla Observatory (test headers) | https://observatory.mozilla.org |
| HSTS Preload List | https://hstspreload.org |

---

**Document Status:** Active
**Last Updated:** June 13, 2026
**Related Docs:** CURRENT_PRIORITIES.md, DEV_ERRORS_LOG.md, HANDOFF_SUMMARY.md
