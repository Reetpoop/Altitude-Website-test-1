/* ============================================================
   ALTITUDE ROBOTICS — SITE SCRIPT
   Loaded with `defer` on every page. Everything is optional:
   each block checks that its elements exist before running.
   ============================================================ */
(function () {
  'use strict';

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------------------------------------------------------
     1. ACTIVE NAV  — driven by <body data-nav="services">
     --------------------------------------------------------- */
  (function () {
    var key = document.body.getAttribute('data-nav');
    if (!key) return;
    document.querySelectorAll('[data-nav-key]').forEach(function (el) {
      if (el.getAttribute('data-nav-key') === key) {
        el.classList.add('active');
        if (el.tagName === 'A') el.setAttribute('aria-current', 'page');
        // if the active link lives inside a dropdown, light up its parent too
        var drop = el.closest('.drop');
        if (drop) {
          var btn = drop.parentElement.querySelector('.dbtn');
          if (btn) btn.classList.add('active');
        }
      }
    });
  })();

  /* ---------------------------------------------------------
     2. OPS BAR CLOCK (Singapore time)
     --------------------------------------------------------- */
  (function () {
    var el = document.getElementById('sgt');
    if (!el) return;
    function tick() {
      var t = new Date().toLocaleTimeString('en-GB', {
        timeZone: 'Asia/Singapore', hour: '2-digit', minute: '2-digit'
      });
      el.textContent = t + ' SGT';
    }
    tick();
    setInterval(tick, 30000);
  })();

  /* ---------------------------------------------------------
     3. MOBILE MENU
     --------------------------------------------------------- */
  (function () {
    var burger = document.querySelector('.burger');
    var menu = document.querySelector('.mobile-menu');
    if (!burger || !menu) return;
    function setOpen(open) {
      burger.classList.toggle('open', open);
      menu.classList.toggle('open', open);
      burger.setAttribute('aria-expanded', String(open));
      document.body.style.overflow = open ? 'hidden' : '';
    }
    burger.addEventListener('click', function () {
      setOpen(!menu.classList.contains('open'));
    });
    menu.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () { setOpen(false); });
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && menu.classList.contains('open')) {
        setOpen(false); burger.focus();
      }
    });
  })();

  /* ---------------------------------------------------------
     4. DESKTOP DROPDOWN (Sectors)
     --------------------------------------------------------- */
  (function () {
    var wraps = document.querySelectorAll('[data-dropdown]');
    if (!wraps.length) return;
    wraps.forEach(function (wrap) {
      var btn = wrap.querySelector('.dbtn');
      var panel = wrap.querySelector('.drop');
      if (!btn || !panel) return;
      var timer = null;
      function open(v) {
        panel.classList.toggle('open', v);
        btn.setAttribute('aria-expanded', String(v));
      }
      btn.addEventListener('click', function (e) {
        e.stopPropagation();
        open(!panel.classList.contains('open'));
      });
      wrap.addEventListener('mouseenter', function () {
        clearTimeout(timer); open(true);
      });
      wrap.addEventListener('mouseleave', function () {
        timer = setTimeout(function () { open(false); }, 140);
      });
      wrap.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') { open(false); btn.focus(); }
      });
      document.addEventListener('click', function (e) {
        if (!wrap.contains(e.target)) open(false);
      });
      panel.addEventListener('focusout', function () {
        setTimeout(function () {
          if (!wrap.contains(document.activeElement)) open(false);
        }, 0);
      });
    });
  })();

  /* ---------------------------------------------------------
     5. SCROLL REVEAL
     --------------------------------------------------------- */
  (function () {
    var els = document.querySelectorAll('.reveal');
    if (!els.length) return;
    if (reduced || !('IntersectionObserver' in window)) {
      els.forEach(function (el) { el.classList.add('in'); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    els.forEach(function (el) { io.observe(el); });
  })();

  /* ---------------------------------------------------------
     6. COUNT-UP NUMBERS  — <span data-count="60">0</span>
     --------------------------------------------------------- */
  (function () {
    var els = document.querySelectorAll('[data-count]');
    if (!els.length) return;
    els.forEach(function (el) {
      var target = parseFloat(el.getAttribute('data-count'));
      if (isNaN(target)) return;
      if (reduced || !('IntersectionObserver' in window)) {
        el.textContent = target.toLocaleString(); return;
      }
      var started = false;
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (!en.isIntersecting || started) return;
          started = true; io.disconnect();
          var dur = 1400, t0 = performance.now();
          (function step(now) {
            var p = Math.min((now - t0) / dur, 1);
            var v = (1 - Math.pow(1 - p, 3)) * target;
            el.textContent = (target % 1 ? v.toFixed(1) : Math.floor(v)).toLocaleString();
            if (p < 1) requestAnimationFrame(step);
            else el.textContent = target.toLocaleString();
          })(t0);
        });
      }, { threshold: 0.5 });
      io.observe(el);
    });
  })();

  /* ---------------------------------------------------------
     7. VIDEO SLOTS
     ---------------------------------------------------------
     <figure class="vslot"
             data-src="media/facade-wash.mp4"        <- desktop file
             data-src-mobile="media/facade-wash-m.mp4"  (optional)
             data-poster="media/facade-wash.jpg"     (strongly recommended)
             data-mode="loop"    loop | film
             data-label="FEED 01"
             data-caption="Facade wash — 32 storeys">

     Leave data-src EMPTY and the slot renders the "awaiting feed"
     placeholder. Fill it in and the player builds itself.
     - loop : muted, autoplaying, looping ambient clip (b-roll)
     - film : poster + play button, sound on, native controls
     --------------------------------------------------------- */
  (function () {
    var slots = document.querySelectorAll('.vslot');
    if (!slots.length) return;

    var isMobile = window.matchMedia('(max-width: 700px)').matches;

    function pick(slot) {
      var m = (slot.getAttribute('data-src-mobile') || '').trim();
      var d = (slot.getAttribute('data-src') || '').trim();
      return (isMobile && m) ? m : d;
    }

    function caption(slot) {
      var label = slot.getAttribute('data-label') || '';
      var cap = slot.getAttribute('data-caption') || '';
      if (!label && !cap) return '';
      return '<figcaption><b>' + esc(label) + '</b><span>' + esc(cap) + '</span></figcaption>';
    }

    function esc(s) {
      return String(s).replace(/[&<>"']/g, function (c) {
        return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
      });
    }

    function pending(slot) {
      var note = slot.getAttribute('data-pending') || 'Footage in production — drop the file into /media and set data-src';
      slot.innerHTML =
        '<div class="vs-pending">' +
          '<div>' +
            '<div class="t">Awaiting feed</div>' +
            '<div class="s">' + esc(note) + '</div>' +
            '<div class="bar"></div>' +
          '</div>' +
        '</div>' +
        '<div class="brk"></div>' + caption(slot);
    }

    function posterImg(slot) {
      var p = (slot.getAttribute('data-poster') || '').trim();
      return p ? '<img class="poster" src="' + esc(p) + '" alt="' +
        esc(slot.getAttribute('data-caption') || 'Video still') + '" loading="lazy" decoding="async">' : '';
    }

    slots.forEach(function (slot) {
      var src = pick(slot);
      var mode = slot.getAttribute('data-mode') || 'loop';

      if (!src) { pending(slot); return; }

      /* ---- FILM: poster is the LCP element; video builds on click ---- */
      if (mode === 'film') {
        slot.innerHTML = posterImg(slot) +
          '<button class="vs-play" type="button" aria-label="Play video">' +
            '<i><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg></i>' +
          '</button>' +
          '<div class="brk"></div>' + caption(slot);
        slot.querySelector('.vs-play').addEventListener('click', function () {
          var v = document.createElement('video');
          v.src = src; v.controls = true; v.playsInline = true; v.autoplay = true;
          v.setAttribute('preload', 'metadata');
          var p = slot.getAttribute('data-poster');
          if (p) v.poster = p;
          slot.innerHTML = '';
          slot.appendChild(v);
          v.play().catch(function () { /* user can press play on the native control */ });
        });
        return;
      }

      /* ---- LOOP: ambient b-roll, muted, activated when scrolled into view ---- */
      slot.innerHTML = posterImg(slot) + '<div class="brk"></div>' + caption(slot);

      if (reduced) return; // poster only — respects reduced-motion

      var v = document.createElement('video');
      v.muted = true; v.loop = true; v.playsInline = true; v.defaultMuted = true;
      v.setAttribute('muted', ''); v.setAttribute('playsinline', '');
      v.setAttribute('webkit-playsinline', ''); v.setAttribute('preload', 'none');
      v.setAttribute('aria-hidden', 'true'); v.tabIndex = -1;
      var poster = slot.getAttribute('data-poster');
      if (poster) v.poster = poster;
      slot.insertBefore(v, slot.firstChild);

      var loaded = false;
      if (!('IntersectionObserver' in window)) { v.src = src; v.play().catch(function () {}); return; }
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) {
            if (!loaded) { loaded = true; v.src = src; }
            v.play().catch(function () {});
          } else if (loaded) {
            v.pause();
          }
        });
      }, { threshold: 0.2 });
      io.observe(slot);
    });
  })();

  /* ---------------------------------------------------------
     8. HERO BACKGROUND VIDEO (same rules, different markup)
     <div class="hero-media" data-src="" data-poster="...">
     --------------------------------------------------------- */
  (function () {
    var host = document.querySelector('.hero-media[data-src]');
    if (!host) return;
    var src = (host.getAttribute('data-src') || '').trim();
    if (!src || reduced) return;               // poster <img> stays as the LCP element
    var v = document.createElement('video');
    v.muted = true; v.loop = true; v.playsInline = true; v.defaultMuted = true;
    v.setAttribute('muted', ''); v.setAttribute('playsinline', '');
    v.setAttribute('webkit-playsinline', ''); v.setAttribute('preload', 'none');
    v.setAttribute('aria-hidden', 'true'); v.tabIndex = -1;
    var poster = host.getAttribute('data-poster');
    if (poster) v.poster = poster;
    v.style.position = 'absolute'; v.style.inset = '0';
    host.insertBefore(v, host.firstChild);
    // load after first paint so the poster wins the LCP race
    window.addEventListener('load', function () {
      setTimeout(function () { v.src = src; v.play().catch(function () {}); }, 250);
    });
  })();

  /* ---------------------------------------------------------
     9. CAROUSEL (compliance credentials)
     --------------------------------------------------------- */
  (function () {
    var cars = document.querySelectorAll('.carousel');
    if (!cars.length) return;
    cars.forEach(function (car) {
      var track = car.querySelector('.car-track');
      var prev = car.querySelector('[data-car="prev"]');
      var next = car.querySelector('[data-car="next"]');
      if (!track) return;
      function step() {
        var first = track.firstElementChild;
        if (!first) return 320;
        var gap = parseFloat(getComputedStyle(track).columnGap || getComputedStyle(track).gap || 14) || 14;
        return first.getBoundingClientRect().width + gap;
      }
      function sync() {
        if (!prev || !next) return;
        var max = track.scrollWidth - track.clientWidth - 2;
        prev.disabled = track.scrollLeft <= 2;
        next.disabled = track.scrollLeft >= max;
      }
      if (prev) prev.addEventListener('click', function () { track.scrollBy({ left: -step(), behavior: reduced ? 'auto' : 'smooth' }); });
      if (next) next.addEventListener('click', function () { track.scrollBy({ left: step(), behavior: reduced ? 'auto' : 'smooth' }); });
      track.addEventListener('scroll', sync, { passive: true });
      window.addEventListener('resize', sync);
      sync();
    });
  })();

  /* ---------------------------------------------------------
     10. BEFORE / AFTER SLIDER
     --------------------------------------------------------- */
  (function () {
    var bas = document.querySelectorAll('.ba');
    if (!bas.length) return;
    bas.forEach(function (ba) {
      var range = ba.querySelector('input[type=range]');
      var after = ba.querySelector('.ba-after');
      var handle = ba.querySelector('.ba-handle');
      if (!range || !after) return;
      function draw() {
        var v = range.value;
        after.style.clipPath = 'inset(0 0 0 ' + v + '%)';
        if (handle) handle.style.left = v + '%';
      }
      range.addEventListener('input', draw);
      draw();
    });
  })();

  /* ---------------------------------------------------------
     11. FORM VALIDATION
     Fields marked `data-required` are checked. Type "email"
     also gets a format check. Wire to a real endpoint by giving
     the <form> an action= and removing data-demo (see README).
     --------------------------------------------------------- */
  (function () {
    var forms = document.querySelectorAll('form[data-validate]');
    if (!forms.length) return;
    forms.forEach(function (form) {
      form.setAttribute('novalidate', '');
      form.addEventListener('submit', function (e) {
        var ok = true;
        form.querySelectorAll('.field[data-required]').forEach(function (field) {
          var input = field.querySelector('input, select, textarea');
          if (!input) return;
          var v = (input.value || '').trim();
          var bad = !v;
          if (!bad && input.type === 'email' && !/^[^@\s]+@[^@\s]+\.[^@\s]{2,}$/.test(v)) bad = true;
          field.classList.toggle('invalid', bad);
          if (bad && ok) input.focus();
          if (bad) ok = false;
        });
        if (!ok) { e.preventDefault(); return; }

        // Demo mode: no endpoint wired yet, so show the confirmation locally.
        if (form.hasAttribute('data-demo')) {
          e.preventDefault();
          var okBox = document.querySelector(form.getAttribute('data-ok') || '.form-ok');
          form.style.display = 'none';
          if (okBox) { okBox.classList.add('show'); okBox.setAttribute('tabindex', '-1'); okBox.focus(); }
        }
      });
      form.querySelectorAll('.field[data-required] input, .field[data-required] select, .field[data-required] textarea')
        .forEach(function (input) {
          input.addEventListener('input', function () {
            input.closest('.field').classList.remove('invalid');
          });
        });
    });
  })();

  /* ---------------------------------------------------------
     12. CURRENT YEAR
     --------------------------------------------------------- */
  document.querySelectorAll('[data-year]').forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });
})();
