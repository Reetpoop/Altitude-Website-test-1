# Altitude Robotics — website

Dark technical static site, 12 pages. No build tools required to run it:
open `index.html` and it works. Deploy by dragging the folder into Vercel.

```
index.html               home
services.html            the four services, methods, limits, abort thresholds
sectors-mcst.html        MCSTs & managing agents
sectors-reit.html        REITs & asset managers
sectors-fm.html          FM & cleaning contractors (white-label / subcontract)
sectors-developer.html   developers & main contractors
compliance.html          credentials, document pack, PDPA policy, objections FAQ
projects.html            the case study schema + project index
case-study.html          the per-project template (copy this per job)
about.html  careers.html  contact.html
assets/site.css          ALL styling, every page
assets/site.js           ALL behaviour, every page
media/                   put your videos and photos here (see media/README.txt)
build.py                 optional — regenerates the HTML from one shared shell
```

---

## 1. Before you publish — the credential flags

Every credential card on the homepage rail and the compliance carousel is
currently set to **In progress** (amber). For each one you actually hold,
edit `build.py` → the `CREDENTIALS` list, or edit the HTML directly and change
**three things** on that card:

```html
<article class="cred" data-status="pending">      ->  data-status="held"
<span class="status">In progress</span>           ->  <span class="status">Held</span>
<div class="ref"><span>Permit no.</span><b>——</b> ->  put the real number in <b>
```

Held turns the card teal. **Do not flip a card until the certificate is in your
hand** — everything on that page is a representation you will be held to in a
tender.

## 2. Dropping in videos

Every video slot in the site is the same component and is already wired.
Find the `<figure class="vslot" ...>` you want and fill in `data-src`:

```html
<figure class="vslot"
        data-src="media/facade-wash.mp4"          <- desktop file
        data-src-mobile="media/facade-wash-m.mp4" <- optional smaller file
        data-poster="media/facade-wash.jpg"       <- always set this
        data-mode="loop"                          <- loop | film
        data-label="Feed 01"
        data-caption="Facade wash — 32 storeys"></figure>
```

* **`loop`** — silent ambient b-roll. Autoplays muted when it scrolls into
  view, pauses when it scrolls away, never downloads until needed.
* **`film`** — long form with sound. Shows the poster plus a play button;
  the video only loads when someone clicks.

Leave `data-src` empty and the slot shows the "Awaiting feed" placeholder.
Change the placeholder wording with `data-pending="..."`.

**The hero video** works the same way — `<div class="hero-media" data-src="">`
near the top of `index.html`. Keep the `<img>` poster inside it: that image is
what loads first and what Google measures. The video only loads after the page
has painted.

Encoding guidance is in `media/README.txt`. The short version: H.264 MP4,
≤4 MB desktop, ≤2 MB mobile, `-movflags +faststart`, no audio on loops.

## 3. Before / after sliders

```html
<div class="ba-pane ba-before"><img src="media/before.jpg" alt=""></div>
<div class="ba-pane ba-after"><img src="media/after.jpg" alt=""></div>
```
Delete the two `<span class="ph">` placeholder lines when you add images.
Shoot both from a tripod in the same position at the same time of day.

## 4. Publishing a case study

1. Copy `case-study.html` to `case-001-buildingname.html`.
2. Fill in every `<dd>` and delete its `class="empty"`.
3. Point the video slots and the before/after images at your files.
4. Link it from `projects.html` (replace one of the three reserved cards).

Do not delete a row because the number is unflattering. A fixed schema is only
worth something if it stays fixed.

## 5. Making the contact form send

1. Create a free form at https://formspree.io and copy the form ID.
2. In `contact.html`, change:
   ```html
   <form class="panel" id="quoteForm" data-validate data-demo data-ok="#formOk">
   ```
   to:
   ```html
   <form class="panel" id="quoteForm" data-validate action="https://formspree.io/f/YOUR_ID" method="POST">
   ```
   Removing `data-demo` is what switches it from the local thank-you message to
   a real submission. Validation keeps working either way.

## 6. Editing colours, type and text

* **Colours and type** — `assets/site.css`, the `:root { }` block at the top.
  `--accent` is the teal. `--r` is the corner radius (2px, deliberately square).
* **Text** — edit the `.html` files directly.
* **Anything that repeats on every page** (nav, footer, phone, address) lives in
  the shared shell inside `build.py`. Change it there and run `python3 build.py`
  to regenerate all 12 pages. If you would rather not use Python, just
  find-and-replace across the `.html` files instead — both work.

Repeated strings: `Altitude Robotics`, `hello@altituderobotics.sg`,
`+65 6000 0000`, `71 Ayer Rajah Crescent`.

## 7. Things deliberately left out

* **No testimonials and no client logos.** The previous version had invented
  ones. Publishing fabricated references to Singapore MCST councils and REIT
  asset managers is a real risk, and those buyers check. The structure is there
  — fill it when you have a named, contactable reference.
* **No performance claims that are not yours yet** (percentage cost savings,
  litres saved, working heights). The hero readout uses operational commitments
  you control instead. Add real numbers once you have measured them on a job.
* **The compliance download pack is a placeholder.** When the ZIP exists, swap
  the "Pack in preparation" span in `compliance.html` for a real download link.

## 8. Deploy

Double-click `index.html` to preview locally. To go live: vercel.com → Add New
→ Project → drag this folder in → Deploy. `index.html` becomes the home page.
