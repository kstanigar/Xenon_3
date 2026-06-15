# Finding 5 — GA4 Consent Mode v2 Implementation Plan

**Created:** June 14, 2026
**Finding:** 5 — GA4 privacy / GDPR — no consent mechanism
**Severity:** HIGH
**Branch:** `feat/ga4-consent-banner`
**Files:** `game.html`, `game_mobile.html`, `index.html`
**Status:** ⏳ Ready to implement

---

## What This Does

Adds a cookie consent banner to all 3 entry-point pages. GA4 analytics are denied by
default until the user clicks Accept. Required for GDPR compliance.

- **First visit:** Banner appears at bottom of screen. User clicks Accept or Decline.
- **Returning visit:** Banner hidden. Consent state restored from localStorage.
- **Key:** `nonx_consent` in localStorage — value is `'granted'` or `'denied'`

---

## Banner Appearance

Fixed bar at the bottom of every page:
- Dark navy background (`#1a1a2e`) with cyan top border (`#00FFFF`)
- Left: "This game uses analytics cookies to track gameplay. Privacy Policy"
- Right: **Decline** (gray outline) + **Accept** (cyan filled)
- `z-index: 99999` — always on top

Appears on all 3 pages because each is a standalone entry point (direct link, bookmark, share).

---

## Task List

### Task 1 — Add consent `default` block BEFORE the gtag script

Deny all analytics by default before GA4 loads. Insert immediately before the
`<script async src="...gtag/js...">` line in each file.

**Code to insert:**
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

| File | Insert BEFORE line | Anchor text |
|---|---|---|
| `game.html` | 118 | `<script async src="https://www.googletagmanager.com/gtag/js?id=G-9ECFZ9JBE5">` |
| `game_mobile.html` | 118 | `<script async src="https://www.googletagmanager.com/gtag/js?id=G-9ECFZ9JBE5">` |
| `index.html` | 112 | `<script async src="https://www.googletagmanager.com/gtag/js?id=G-9ECFZ9JBE5">` |

---

### Task 2 — Add banner HTML as first element inside `<body>`

**Code to insert:**
```html
<div id="consentBanner" style="position:fixed;bottom:0;left:0;right:0;background:#1a1a2e;color:#ccc;padding:14px 20px;z-index:99999;font-size:13px;display:flex;align-items:center;justify-content:space-between;gap:16px;font-family:monospace;border-top:1px solid #00FFFF;">
  <span>This game uses analytics cookies to track gameplay. <a href="/privacy.html" style="color:#00FFFF;">Privacy Policy</a></span>
  <div style="display:flex;gap:8px;flex-shrink:0;">
    <button id="declineConsent" style="padding:6px 16px;background:transparent;color:#888;border:1px solid #444;border-radius:4px;cursor:pointer;font-family:monospace;">Decline</button>
    <button id="acceptConsent" style="padding:6px 16px;background:#00FFFF;color:#000;border:none;border-radius:4px;cursor:pointer;font-weight:bold;font-family:monospace;">Accept</button>
  </div>
</div>
```

| File | Insert AFTER line | Anchor text |
|---|---|---|
| `game.html` | 644 | `<body>` |
| `game_mobile.html` | 600 | `<body>` |
| `index.html` | 443 | `<body>` |

---

### Task 3 — Add consent handler JS to main script block

Handles: restoring consent on return visits, Accept button, Decline button.
Insert after the `escapeHtml` function closing brace in each file.

**Code to insert:**
```javascript
(function() {
  var banner = document.getElementById('consentBanner');
  if (!banner) return;
  if (localStorage.getItem('nonx_consent') === 'granted') {
    banner.style.display = 'none';
    gtag('consent', 'update', { 'analytics_storage': 'granted' });
    return;
  }
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

| File | Insert AFTER line | Anchor text |
|---|---|---|
| `game.html` | 710 | closing `}` of `escapeHtml` function |
| `game_mobile.html` | 666 | closing `}` of `escapeHtml` function |
| `index.html` | 567 | closing `}` of `escapeHtml` function |

---

## Verify After Implementation

- [ ] Open game in incognito → banner appears at bottom
- [ ] No GA4 `collect` requests in Network tab before clicking Accept
- [ ] Click Accept → GA4 requests appear in Network tab
- [ ] Reload page → banner does NOT reappear
- [ ] Clear localStorage → banner reappears

---

## Notes

- `privacy.html` link in banner points to `/privacy.html` — this page does not exist yet.
  Finding 5 in SECURITY_AUDIT_PLAN.md notes a Privacy Policy page is needed (3B).
  The link will 404 until that page is created — acceptable for now.
- All 3 files are standalone entry points, so the banner must appear on all 3.
- localStorage key `nonx_consent` added to localStorage inventory in SECURITY_AUDIT_PLAN.md.

---

**Total changes:** 9 edits across 3 files (3 per file × 3 files)
