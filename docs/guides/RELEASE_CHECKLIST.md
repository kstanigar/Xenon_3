# NON-X Release Checklist

## 🔒 SECURITY / PEN TESTING

### Pre-Release Security Checks ✅

- [x] **XSS Protection**: No user input directly rendered via innerHTML
- [x] **Email Validation**: Regex validation + sanitization added
- [x] **No External Dependencies**: All code is self-contained
- [x] **HTTPS Only**: Ensure GitHub Pages uses HTTPS (automatic)
- [x] **localStorage Safety**: Only storing game data, no sensitive info
- [ ] **Test on Multiple Browsers**: Chrome, Firefox, Safari, Edge
- [ ] **Test on Multiple Devices**: iOS, Android, Desktop

### Recommended Security Headers (GitHub Pages)
Add to your repo as `.github/workflows/security-headers.yml` if using custom domain:
```yaml
Content-Security-Policy: default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN
```

### Manual Testing Checklist
- [ ] Try entering malicious email: `<script>alert('xss')</script>@test.com`
- [ ] Test localStorage quota (try playing 100+ games)
- [ ] Test with browser extensions (ad blockers, script blockers)
- [ ] Test offline behavior
- [ ] Test on slow network (throttle to 3G)

---

## 📊 ANALYTICS SETUP

### Option 1: Google Analytics (Recommended for beginners)

**Setup Steps:**
1. Create Google Analytics account: https://analytics.google.com
2. Create new property for "NON-X"
3. Get your Measurement ID (format: G-XXXXXXXXXX)
4. Add to `index.html`, `game.html`, and `game_mobile.html`:

```html
<!-- Google tag (gtag.js) - Add BEFORE closing </head> -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

**Track Custom Events:**
Add to game files:
```javascript
// When player starts game
gtag('event', 'game_start', {
  'platform': 'mobile' // or 'desktop'
});

// When player completes a level
gtag('event', 'level_complete', {
  'level': level,
  'score': score
});

// When player defeats boss
gtag('event', 'boss_defeated', {
  'boss_number': currentBoss,
  'score': score
});

// When player reaches victory
gtag('event', 'game_complete', {
  'final_score': score,
  'time_played': sessionTime
});

// When player dies
gtag('event', 'game_over', {
  'level_reached': level,
  'score': score
});
```

---

### Option 2: Custom Analytics Endpoint

The code already has analytics infrastructure! Just need to configure it.

**In `index.html` - Update analytics endpoint:**
```javascript
// Line ~450 in index.html
var ANALYTICS_ENDPOINT = 'https://your-api.com/analytics'; // Add your endpoint
```

**Backend Setup (Node.js Example):**
```javascript
// server.js
const express = require('express');
const app = express();
app.use(express.json());

app.post('/analytics', (req, res) => {
  const { event, data, session } = req.body;
  
  // Store in database (MongoDB, PostgreSQL, etc.)
  console.log('Event:', event, 'Data:', data, 'Session:', session);
  
  // Or send to analytics service (Mixpanel, Amplitude, etc.)
  
  res.json({ success: true });
});

app.listen(3000);
```

---

### Key Metrics to Track

**Engagement Metrics:**
- Game starts (total plays)
- Platform split (mobile vs desktop)
- Average session duration
- Completion rate (% who beat final boss)
- Drop-off points (which level players quit)

**Performance Metrics:**
- Page load time
- Time to first interaction
- Average FPS (if implemented)

**Progression Metrics:**
- Level reached distribution
- Boss defeat rates (Boss 1, 2, 3)
- High score distribution
- Power-up collection rates

**Conversion Metrics:**
- Email subscription rate
- Return player rate

---

## 🚀 DEPLOYMENT CHECKLIST

### Pre-Deploy
- [ ] Remove debug key (V for victory) or document it
- [ ] Test all sound effects work across browsers
- [ ] Verify all images load correctly
- [ ] Test responsive design on various screen sizes
- [ ] Check spelling/grammar in all text
- [ ] Verify Modmotif link works
- [ ] Test email submission flow

### GitHub Pages Deploy
```bash
# Ensure main branch is ready
git status
git add .
git commit -m "Production release v1.0"
git push origin main

# Verify at: https://<username>.github.io/Xenon_3/
```

### Post-Deploy
- [ ] Test live site on mobile device
- [ ] Test live site on desktop
- [ ] Verify analytics tracking works
- [ ] Check console for any errors
- [ ] Test email collection
- [ ] Share with beta testers

---

## 📱 PRIVACY & COMPLIANCE

### What Data You Collect
- High scores (localStorage only)
- Email addresses (localStorage only, user consented)
- Session data (if analytics enabled)

### Privacy Policy (Required for GDPR)
Create `privacy.html`:
- What data you collect
- How it's used
- How it's stored
- User rights (access, deletion)
- Contact info

### Add Privacy Link
In `index.html` and game files, add:
```html
<a href="privacy.html" style="position: fixed; bottom: 10px; right: 10px;">Privacy Policy</a>
```

---

## 🎯 LAUNCH STRATEGY

1. **Soft Launch** (Week 1)
   - Share with friends/family
   - Gather feedback
   - Monitor analytics

2. **Beta Release** (Week 2)
   - Post on game dev forums (Reddit: r/WebGames, r/gamedev)
   - Fix critical bugs

3. **Public Launch**
   - Social media announcement
   - Submit to game directories (itch.io, Kongregate, Newgrounds)
   - Reach out to gaming YouTubers/streamers

---

## 📈 POST-LAUNCH MONITORING

### Week 1 Checklist
- [ ] Monitor analytics daily
- [ ] Check for bug reports
- [ ] Respond to user feedback
- [ ] Track email submissions

### Week 2-4 Checklist
- [ ] Analyze player behavior (where do they drop off?)
- [ ] Plan updates based on data
- [ ] A/B test improvements

---

## 🔧 OPTIMIZATION TIPS

### Performance
- All sprites already optimized ✅
- Sound files compressed ✅
- Consider adding service worker for offline play
- Consider adding lazy loading for assets

### SEO (If you want organic traffic)
Add to `<head>`:
```html
<meta name="description" content="NON-X - An intense top-scrolling space shooter. Battle through 12 levels across 3 phases. Free to play!">
<meta property="og:title" content="NON-X - Space Shooter Game">
<meta property="og:description" content="Battle through 12 levels of intense space combat!">
<meta property="og:image" content="https://your-site.com/preview.png">
<meta name="twitter:card" content="summary_large_image">
```

---

## ✅ READY TO LAUNCH?

Your game is production-ready when:
- [x] All features working
- [ ] Tested on 3+ devices
- [ ] Analytics configured
- [ ] Privacy policy created
- [ ] No critical bugs
- [ ] Load time < 3 seconds
- [ ] Email collection works
- [ ] Music/SFX work across browsers

**Current Status: 90% Ready!**

Just need to:
1. Configure analytics
2. Test on devices
3. Add privacy policy (if collecting emails)
4. Deploy!

Good luck with your launch! 🚀
