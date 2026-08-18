#!/usr/bin/env python3
"""Assembles the Altitude Robotics static site.

Every page shares one header/footer so navigation can never drift.
Run:  python3 build.py     ->  writes .html files next to this script.
"""
import os, re, sys

OUT = os.path.dirname(os.path.abspath(__file__))

BRAND = "Altitude Robotics"
EMAIL = "hello@altituderobotics.sg"
PHONE = "+65 6000 0000"
PHONE_WA = "6560000000"
ADDR1 = "71 Ayer Rajah Crescent"
ADDR2 = "Singapore 139951"

MARK = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" '
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" width="100%" height="100%">'
        '<path d="M12 9.5a2.5 2.5 0 100 5 2.5 2.5 0 000-5zM6 6 9 9M18 6l-3 3M6 18l3-3M18 18l-3-3'
        'M4 5.5a1.5 1.5 0 113 0 1.5 1.5 0 01-3 0zM17 5.5a1.5 1.5 0 113 0 1.5 1.5 0 01-3 0z'
        'M4 18.5a1.5 1.5 0 113 0 1.5 1.5 0 01-3 0zM17 18.5a1.5 1.5 0 113 0 1.5 1.5 0 01-3 0z"/></svg>')

ARR = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
       'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>')
TICK = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6L9 17l-5-5"/></svg>')
DOT = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
       'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="7"/></svg>')

HERO_POSTER = "https://images.unsplash.com/photo-1473968512647-3e447244af8f?w=1800&amp;q=68&amp;auto=format&amp;fit=crop"

SECTORS = [
    ("sectors-mcst.html", "mcst", "MCST &amp; managing agents",
     "Condominium and strata councils working to an AGM calendar and a sinking fund."),
    ("sectors-reit.html", "reit", "REITs &amp; asset managers",
     "Portfolio owners who need repeatable numbers, ESG data and no incidents."),
    ("sectors-fm.html", "fm", "FM &amp; cleaning contractors",
     "Keep the contract. Subcontract the height. White-label aerial capacity."),
    ("sectors-developer.html", "dev", "Developers &amp; main contractors",
     "Handover cleans and defect-liability recleans that fit inside the programme."),
]


def nav_links(active):
    drop = "".join(
        '<a href="%s" data-nav-key="%s">%s<span>%s</span></a>' % (h, k, t, s)
        for h, k, t, s in SECTORS)
    return """
      <ul class="nav-links">
        <li><a href="services.html" data-nav-key="services">Services</a></li>
        <li data-dropdown>
          <button class="dbtn" aria-expanded="false" aria-haspopup="true">Sectors
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>
          </button>
          <div class="drop">%s</div>
        </li>
        <li><a href="compliance.html" data-nav-key="compliance">Compliance</a></li>
        <li><a href="projects.html" data-nav-key="projects">Projects</a></li>
        <li><a href="about.html" data-nav-key="about">About</a></li>
      </ul>""" % drop


def mobile_menu():
    drop = "".join('<a href="%s" data-nav-key="%s">%s</a>' % (h, k, t) for h, k, t, s in SECTORS)
    return """
  <nav class="mobile-menu" aria-label="Mobile">
    <a href="index.html" data-nav-key="home">Home</a>
    <a href="services.html" data-nav-key="services">Services</a>
    <div class="grp">Sectors</div>
    %s
    <div class="grp">Company</div>
    <a href="compliance.html" data-nav-key="compliance">Compliance &amp; safety</a>
    <a href="projects.html" data-nav-key="projects">Projects</a>
    <a href="about.html" data-nav-key="about">About</a>
    <a href="careers.html" data-nav-key="careers">Careers</a>
    <a class="btn btn-primary" href="contact.html">Request a site survey %s</a>
  </nav>""" % (drop, ARR)


def shell(fname, nav, title, desc, body, crumb=None):
    social = ('<div class="socials">'
              '<a href="#" aria-label="LinkedIn"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M7 10v7M7 7v.01M11 17v-4a2 2 0 014 0v4M11 17v-7"/></svg></a>'
              '<a href="#" aria-label="Instagram"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="4"/><circle cx="12" cy="12" r="4"/><circle cx="17.2" cy="6.8" r="1"/></svg></a>'
              '<a href="#" aria-label="YouTube"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2.5" y="5" width="19" height="14" rx="4"/><path d="M10.5 9.2l5 2.8-5 2.8z"/></svg></a>'
              '</div>')

    sector_links = "".join('<a href="%s">%s</a>' % (h, t) for h, k, t, s in SECTORS)

    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta name="theme-color" content="#06080B">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700;800&amp;family=Inter:wght@400;500;600&amp;family=JetBrains+Mono:wght@400;500&amp;display=swap" rel="stylesheet">
<script>document.documentElement.classList.add('js');</script>
<link rel="stylesheet" href="assets/site.css">
<script src="assets/site.js" defer></script>
</head>
<body data-nav="{nav}">
<a class="skip" href="#main">Skip to content</a>

<div class="opsbar"><div class="wrap">
  <span><span class="dot"></span>Operating in Singapore &mdash; all flights under CAAS permit</span>
  <span><b id="sgt">&mdash;&mdash;</b></span>
</div></div>

<header><div class="wrap nav">
  <a href="index.html" class="logo" data-nav-key="home"><span class="mark">{mark}</span>{brand}</a>
  {navlinks}
  <div class="nav-cta">
    <a class="btn btn-primary btn-sm" href="contact.html">Request a site survey {arr}</a>
    <button class="burger" aria-label="Open menu" aria-expanded="false"><span></span><span></span><span></span></button>
  </div>
</div></header>
{mobile}

<main id="main">
{body}
</main>

<footer><div class="wrap">
  <div class="fgrid">
    <div class="fcol fbrand">
      <a href="index.html" class="logo"><span class="mark">{mark}</span>{brand}</a>
      <p>Drone facade, glass and solar cleaning for Singapore's high-rise stock. Nobody works at height, and every flight is permitted, documented and handed over with evidence.</p>
      {social}
    </div>
    <div class="fcol"><h2>Services</h2>
      <a href="services.html#facade">Facade &amp; glass</a>
      <a href="services.html#solar">Solar array cleaning</a>
      <a href="services.html#treatment">Surface treatment</a>
      <a href="services.html#capture">Condition capture</a>
    </div>
    <div class="fcol"><h2>Sectors</h2>{sectors}</div>
    <div class="fcol"><h2>Company</h2>
      <a href="compliance.html">Compliance &amp; safety</a>
      <a href="projects.html">Projects</a>
      <a href="about.html">About</a>
      <a href="careers.html">Careers</a>
      <a href="contact.html">Contact</a>
    </div>
    <div class="fcol"><h2>Contact</h2>
      <p>{addr1}<br>{addr2}</p>
      <p><a href="mailto:{email}">{email}</a></p>
      <p><a href="tel:{phone_raw}">{phone}</a></p>
      <p><a href="https://wa.me/{wa}">WhatsApp</a></p>
    </div>
  </div>
  <div class="fbottom">
    <span>&copy; <span data-year>2026</span> {brand} Pte. Ltd.</span>
    <span>Credential status is published on the <a href="compliance.html" style="color:var(--ink-2)">compliance page</a></span>
  </div>
</div></footer>
</body>
</html>
""".format(title=title, desc=desc, nav=nav, mark=MARK, brand=BRAND, arr=ARR,
           navlinks=nav_links(nav), mobile=mobile_menu(), body=body, social=social,
           sectors=sector_links, addr1=ADDR1, addr2=ADDR2, email=EMAIL,
           phone=PHONE, phone_raw=PHONE.replace(" ", ""), wa=PHONE_WA)


# ---------------------------------------------------------------- components
def sec_head(idx, label, h2, lead="", solo=False):
    if solo:
        return ('<div class="sec-head solo reveal"><span class="eyebrow">%s</span>'
                '<h2 style="margin:16px 0 14px">%s</h2>%s</div>'
                % (label, h2, '<p class="lead">%s</p>' % lead if lead else ""))
    return ('<div class="sec-head reveal">'
            '<div class="idx"><b>%s</b>%s</div>'
            '<div><h2>%s</h2>%s</div></div>'
            % (idx, label, h2, '<p class="lead">%s</p>' % lead if lead else ""))


def vslot(label, caption, mode="loop", ratio="", pending=None, poster="", src=""):
    cls = "vslot" + ((" " + ratio) if ratio else "")
    return ('<figure class="%s reveal" data-src="%s" data-poster="%s" data-mode="%s" '
            'data-label="%s" data-caption="%s"%s></figure>'
            % (cls, src, poster, mode, label, caption,
               ' data-pending="%s"' % pending if pending else ""))


CREDENTIALS = [
    ("CAAS-OP", "UA Operator Permit", "Civil Aviation Authority of Singapore",
     "Certifies Altitude as a competent operator. Required for every non-recreational flight, whatever the airframe weighs.",
     "Permit no."),
    ("CAAS-UAPL", "Unmanned Aircraft Pilot Licence", "Civil Aviation Authority of Singapore",
     "Every pilot who flies on your site holds a current UAPL. Commercial facade work cannot legally be flown without one.",
     "Pilots licensed"),
    ("CAAS-AP1", "Class 1 Activity Permit", "Civil Aviation Authority of Singapore",
     "Site-specific authorisation for commercial flight, for work above 60&nbsp;m, and for sites within 5&nbsp;km of an aerodrome. We apply per building.",
     "Per-site basis"),
    ("CAAS-REG", "Airframe registration &amp; B-RID", "Civil Aviation Authority of Singapore",
     "Every airframe over 250&nbsp;g is registered with CAAS and broadcasts Remote ID, so your security team can identify what is in the air.",
     "Airframes"),
    ("NEA-CBL", "Cleaning Business Licence", "National Environment Agency",
     "The legal permission to provide cleaning services at all. Engaging an unlicensed cleaner is an offence for the buyer as well as the contractor.",
     "Licence class"),
    ("WSHC-BS", "bizSAFE", "Workplace Safety and Health Council",
     "An audited risk-management system. Level 3 is the practical floor for commercial and government tenders; Star requires ISO 45001.",
     "Level"),
    ("ISO-QEHS", "ISO 9001 / 14001 / 45001", "SAC-accredited certification body",
     "Quality, environmental, and occupational health and safety management systems &mdash; the set MNC and GLC vendor frameworks ask for.",
     "Certificates"),
    ("INS-TPL", "Liability &amp; WICA cover", "Insurer &mdash; policy on request",
     "Third-party public liability for aerial operations, plus Work Injury Compensation for every crew member on your site.",
     "Sum insured"),
]


def cred_card(c, aria_hidden=False):
    code, title, body, desc, reflabel = c
    return ('<article class="cred" data-status="pending"%s>'
            '<div class="cred-top"><span class="cred-code">%s</span>'
            '<span class="status">In progress</span></div>'
            '<h3>%s</h3><div class="body">%s</div><p>%s</p>'
            '<div class="ref"><span>%s</span><b>&mdash;&mdash;</b></div>'
            '</article>' % (' aria-hidden="true"' if aria_hidden else "", code, title, body, desc, reflabel))


CRED_NOTE = """
<!-- ===================================================================
     CREDENTIAL STATUS  — READ THIS BEFORE YOU PUBLISH
     Every card below is set to data-status="pending"  (amber, "In progress").
     For each credential you actually hold, change TWO things on that card:
        1.  data-status="pending"      ->  data-status="held"
        2.  <span class="status">In progress</span>  ->  <span class="status">Held</span>
        3.  replace the &mdash;&mdash; in the .ref line with the real number
     Do not switch a card to "held" before the certificate is in your hand:
     everything on this page is a representation you will be held to in a tender.
     =================================================================== -->
"""


def cta(title, text, primary=("contact.html", "Request a site survey"), secondary=("compliance.html", "See our compliance pack")):
    return """
<section class="ctaband"><div class="wrap"><div class="inner reveal">
  <div><h2>%s</h2><p>%s</p></div>
  <div class="acts">
    <a class="btn btn-primary" href="%s">%s %s</a>
    <a class="btn btn-ghost" href="%s">%s</a>
  </div>
</div></div></section>""" % (title, text, primary[0], primary[1], ARR, secondary[0], secondary[1])


def phero(crumbs, label, h1, lead, pills=None):
    cr = '<div class="crumb"><a href="index.html">Home</a>'
    for text, href in crumbs:
        cr += '<i>/</i>' + (('<a href="%s">%s</a>' % (href, text)) if href else ('<span>%s</span>' % text))
    cr += '</div>'
    p = ""
    if pills:
        p = '<div class="phero-meta">' + "".join('<span class="pill">%s</span>' % x for x in pills) + '</div>'
    return ('<section class="phero"><div class="wrap">%s'
            '<div style="margin-top:26px"><span class="eyebrow">%s</span>'
            '<h1>%s</h1><p class="lead">%s</p>%s</div></div></section>' % (cr, label, h1, lead, p))


def acc(items):
    out = '<div class="acc reveal">'
    for q, a in items:
        out += '<details><summary>%s</summary><div class="ans">%s</div></details>' % (q, a)
    return out + '</div>'


def checks(items, warn=False):
    out = '<ul class="checks%s">' % (" warn" if warn else "")
    for it in items:
        out += '<li>%s<span>%s</span></li>' % (TICK, it)
    return out + '</ul>'


# ================================================================= PAGES
PAGES = {}

# ---------------------------------------------------------------- HOME
PAGES["index.html"] = dict(nav="home",
    title="Drone facade &amp; solar cleaning in Singapore &mdash; " + BRAND,
    desc="Altitude Robotics cleans high-rise facades, glass and solar arrays by drone in Singapore. No personnel at height, every flight under CAAS permit, evidence handed over with the job.",
    body="""
<section class="hero">
  <!-- HERO VIDEO: put your file in /media, then set data-src on the line below.
       Keep data-poster filled — the poster image is what loads first and is what
       Google measures. Recommended: <=4 MB desktop MP4, H.264, 1920x1080, muted loop. -->
  <div class="hero-media" data-src="" data-poster="POSTER">
    <img src="POSTER" alt="Cleaning drone working against a high-rise facade" fetchpriority="high" decoding="async">
  </div>
  <div class="wrap hero-inner">
    <span class="eyebrow">Drone facade &amp; solar cleaning &middot; Singapore</span>
    <h1>Cleaning at height, with <em>nobody at height.</em></h1>
    <p class="lead">We wash facades, glass and rooftop solar from the air &mdash; no gondola booking, no rope teams over your entrance, no scaffold. Your crews stay on the ground, your tenants stay in the building, and you get the paperwork a Singapore building owner is actually asked for.</p>
    <div class="hero-cta">
      <a class="btn btn-primary" href="contact.html">Request a site survey ARROW</a>
      <a class="btn btn-ghost" href="compliance.html">Compliance &amp; safety pack</a>
    </div>
    <div class="hero-readout reveal">
      <div><div class="n">0</div><div class="l">Personnel at height</div></div>
      <div><div class="n">100<u>&nbsp;%</u></div><div class="l">Flights under CAAS permit</div></div>
      <div><div class="n">48<u>&nbsp;h</u></div><div class="l">Quotation turnaround</div></div>
      <div><div class="n">2&ndash;4<u>&nbsp;wk</u></div><div class="l">CAAS permit lead time</div></div>
    </div>
  </div>
</section>

<section class="sec tight flush alt">
  <div class="wrap" style="margin-bottom:22px">
    <h2 class="lbl">Cleared to fly &middot; licensed to clean &mdash; live credential status</h2>
  </div>
  RAIL
  <div class="wrap" style="margin-top:20px">
    <a class="lbl lbl-a" href="compliance.html">Full compliance pack &amp; certificate numbers &rarr;</a>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    SECHEAD_CAP
    <div class="g4">
      <article class="card reveal"><div class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 21h18M5 21V5a1 1 0 011-1h7a1 1 0 011 1v16M14 21V9a1 1 0 011-1h3a1 1 0 011 1v12M8 8h2M8 12h2M8 16h2"/></svg></div>
        <h3>Facade &amp; glass</h3><p>Full-elevation washing with pure water fed from a ground base station. Spot-free on glass, no residue on cladding, no marks on the paving below.</p>
        <div class="kv"><span>Substrates</span><b>Glass / ACP / tile / render</b></div></article>
      <article class="card reveal"><div class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M5 5l2 2M17 17l2 2M5 19l2-2M17 7l2-2"/></svg></div>
        <h3>Solar array cleaning</h3><p>Soiling costs you yield every month it is left. Cell-safe, deionised water only &mdash; no detergent film to attract the next layer of dust.</p>
        <div class="kv"><span>Method</span><b>RO+DI, no abrasion</b></div></article>
      <article class="card reveal"><div class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3s6 6.4 6 10.5a6 6 0 11-12 0C6 9.4 12 3 12 3z"/></svg></div>
        <h3>Surface treatment</h3><p>Anti-mould and anti-algae application on the north and shaded elevations where Singapore's humidity does its worst, applied on the same mobilisation as the wash.</p>
        <div class="kv"><span>Timing</span><b>Same mobilisation</b></div></article>
      <article class="card reveal"><div class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/><path d="M12 13v-3M16 8l-3 3"/></svg></div>
        <h3>Condition capture</h3><p>The drone is already at the facade, so it films it. You get elevation-by-elevation imagery and a defect log alongside the clean &mdash; useful when your BCA cycle comes round.</p>
        <div class="kv"><span>Output</span><b>Imagery + defect log</b></div></article>
    </div>
  </div>
</section>

<section class="sec alt">
  <div class="wrap">
    SECHEAD_CMP
    <div class="tblwrap reveal">
      <table class="tbl">
        <caption>Access methods compared &mdash; typical high-rise commercial or strata elevation</caption>
        <thead><tr><th scope="col">&nbsp;</th><th scope="col">Drone</th><th scope="col">Rope access</th><th scope="col">Gondola / BMU</th><th scope="col">Scaffold</th></tr></thead>
        <tbody>
          <tr><th scope="row">Personnel at height</th><td class="yes">None</td><td>Yes</td><td>Yes</td><td>Yes</td></tr>
          <tr><th scope="row">Setup before first clean</th><td class="yes">Hours</td><td>About a day</td><td>Days &mdash; booking and rigging</td><td>One to two weeks</td></tr>
          <tr><th scope="row">Ground-level disruption</th><td class="yes">Exclusion zone only, moved with the crew</td><td>Drop zones and closed walkways</td><td>Drop zones, parking loss</td><td>Entrance and landscape encroachment</td></tr>
          <tr><th scope="row">Complex geometry</th><td class="yes">Overhangs, setbacks, lightwells, atria</td><td>Good</td><td>Limited by track and davit reach</td><td>Limited</td></tr>
          <tr><th scope="row">Deep reveals and recesses</th><td class="no">Limited &mdash; we bring rope access for these</td><td>Good</td><td>Good</td><td>Good</td></tr>
          <tr><th scope="row">Water and chemical volume</th><td class="yes">Controlled flow, pure water</td><td>Standard</td><td>Standard</td><td>Standard</td></tr>
          <tr><th scope="row">Authority lead time</th><td>CAAS permit, 2&ndash;4 weeks</td><td>Work-at-height permit</td><td>WAH permit + BMU certification</td><td>Scaffold inspection + WAH permit</td></tr>
        </tbody>
      </table>
    </div>
    <div class="note reveal" style="margin-top:22px">
      <div class="lbl">Where drones are the wrong tool</div>
      Deep reveals, heavily recessed windows, interior-facing light wells with no line of sight, and heavy organic build-up that needs mechanical contact still want a rope team. We say so at survey rather than at handover, and we price the hybrid.
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    SECHEAD_HOW
    <div style="margin-bottom:44px">FILM</div>
    <div class="g3">
      <article class="card stepcard reveal"><div class="num"><i>01 &mdash; SURVEY</i></div>
        <h3>Survey and permit</h3><p>We walk the site, record substrates and soiling, fix the water and power points, map the exclusion zones, and file the CAAS activity permit. Allow two to four weeks for the permit &mdash; start six to eight weeks before any deadline you are working to.</p></article>
      <article class="card stepcard reveal"><div class="num"><i>02 &mdash; FLY</i></div>
        <h3>Notify, then fly</h3><p>Residents and tenants get written notice before we arrive. The base station goes in at ground level, the crew stays on the ground, and the elevations are flown on a planned grid with a spotter on comms throughout.</p></article>
      <article class="card stepcard reveal"><div class="num"><i>03 &mdash; HAND OVER</i></div>
        <h3>Hand over the evidence</h3><p>Before-and-after capture per elevation, the flight log, the defect log, and the signed completion record &mdash; the pack your council, your auditor or your client asks for later.</p></article>
    </div>
  </div>
</section>

<section class="sec alt">
  <div class="wrap">
    SECHEAD_SEC
    <div class="g4">SECTORCARDS</div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    SECHEAD_EV
    <div class="split" style="margin-bottom:44px">
      <div>
        <h3 style="font-size:1.5rem;margin-bottom:14px">We publish the numbers, not adjectives.</h3>
        <p class="lead" style="font-size:1rem;margin-bottom:22px">Every completed job is written up to the same fixed schema, so you can put two of our projects side by side &mdash; or put ours next to another contractor's and see what is missing from theirs.</p>
        CHECKS_EV
        <a class="btn btn-ghost" style="margin-top:26px" href="projects.html">See the case study schema ARROW</a>
      </div>
      <div>BASLIDER</div>
    </div>
    <div class="g3">
      <a class="card reveal" href="case-study.html"><div class="lbl lbl-a">Case 001</div><h3 style="margin:12px 0 8px">Awaiting first published project</h3><p>The template is built and the schema is fixed. The first completed job publishes here with every field filled in.</p><div class="kv"><span>Status</span><b>Template ready</b></div></a>
      <a class="card reveal" href="case-study.html"><div class="lbl lbl-a">Case 002</div><h3 style="margin:12px 0 8px">Awaiting publication</h3><p>Reserved for the first solar array job &mdash; yield before and after, panel count, litres used.</p><div class="kv"><span>Status</span><b>Template ready</b></div></a>
      <a class="card reveal" href="case-study.html"><div class="lbl lbl-a">Case 003</div><h3 style="margin:12px 0 8px">Awaiting publication</h3><p>Reserved for a strata job written up for a council audience, with the resident-notice pack attached.</p><div class="kv"><span>Status</span><b>Template ready</b></div></a>
    </div>
  </div>
</section>

<section class="sec alt">
  <div class="wrap">
    SECHEAD_FEED
    <div class="g3">FEEDS</div>
  </div>
</section>
CTA
""")

# ---------------------------------------------------------------- SERVICES
PAGES["services.html"] = dict(nav="services",
    title="Services &mdash; facade, glass, solar and condition capture &mdash; " + BRAND,
    desc="Drone facade and glass washing, solar array cleaning, surface treatment and facade condition capture in Singapore. Methods, substrates, limits and abort thresholds.",
    body=phero([("Services", None)], "What we do",
               "Four services, one mobilisation, one crew on the ground.",
               "We bring a ground base station, a pure-water plant and a licensed flight crew. Everything below runs off the same setup, which is why combining them costs less than booking them separately.",
               ["Facade &amp; glass", "Solar arrays", "Surface treatment", "Condition capture"]) + """
<section class="sec flush" id="facade">
  <div class="wrap">
    SECHEAD_F
    <div class="split wide">
      <div>
        <p class="lead" style="margin-bottom:24px">Full-elevation washing using reverse-osmosis and deionised water fed from ground level. Pure water dries without spotting, so there is no detergent film left to catch the next month of dust.</p>
        CHECKS_F
      </div>
      <div>VSLOT_F</div>
    </div>
    <div class="tblwrap reveal" style="margin-top:40px">
      <table class="tbl">
        <caption>Method by substrate</caption>
        <thead><tr><th scope="col">Substrate</th><th scope="col">Method</th><th scope="col">Notes</th></tr></thead>
        <tbody>
          <tr><th scope="row">Glass and glazed curtain wall</th><td>Pure-water rinse, low pressure</td><td>Spot-free finish; we log the TDS reading at the nozzle on every job</td></tr>
          <tr><th scope="row">Aluminium composite panel</th><td>Soft wash, controlled flow</td><td>Angle managed to avoid driving water behind the panel joint</td></tr>
          <tr><th scope="row">Ceramic tile and mosaic</th><td>Soft wash, detergent where staining requires</td><td>Loose or drummy tile is flagged, not washed &mdash; it goes in the defect log</td></tr>
          <tr><th scope="row">Painted render and concrete</th><td>Soft wash, anti-algae option</td><td>Pressure limited by substrate condition and paint age</td></tr>
          <tr><th scope="row">Natural stone</th><td>Pure water, no detergent by default</td><td>Test patch agreed with you before the full elevation</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>

<section class="sec alt" id="solar">
  <div class="wrap">
    SECHEAD_S
    <div class="split wide">
      <div>
        <p class="lead" style="margin-bottom:24px">Rooftop and podium arrays cleaned without walking the array. No panel loading, no micro-cracking from foot traffic, no detergent residue to bake on.</p>
        CHECKS_S
      </div>
      <div>VSLOT_S</div>
    </div>
  </div>
</section>

<section class="sec" id="treatment">
  <div class="wrap">
    SECHEAD_T
    <div class="split wide">
      <div>
        <p class="lead" style="margin-bottom:24px">Singapore's humidity and shaded elevations grow biological soiling back fast. Treatment applied on the same mobilisation as the wash buys you a longer interval before the next one.</p>
        CHECKS_T
      </div>
      <div>VSLOT_T</div>
    </div>
  </div>
</section>

<section class="sec alt" id="capture">
  <div class="wrap">
    SECHEAD_C
    <div class="split wide">
      <div>
        <p class="lead" style="margin-bottom:24px">The aircraft is already flying your facade at close range. Capturing it costs almost nothing extra and gives you a dated visual record of condition, elevation by elevation.</p>
        CHECKS_C
        <div class="note reveal" style="margin-top:26px">
          <div class="lbl">This is not a statutory facade inspection</div>
          A BCA Periodic Facade Inspection is a separate exercise with its own methodology and must be endorsed by a registered Professional Engineer. What we hand over is condition evidence and a defect log &mdash; useful input to that process, and useful on its own for tracking deterioration between cycles. If you need the statutory inspection, we will say so and point you to it.
        </div>
      </div>
      <div>VSLOT_C</div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    SECHEAD_W
    <div class="split">
      <div>
        <p class="lead" style="margin-bottom:22px">Water is made on site. A reverse-osmosis and deionisation stage strips the dissolved solids out of the mains supply, which is what makes a rinse dry clear instead of leaving a mineral ghost on the glass.</p>
        <div class="spec reveal">
          <div class="row"><dt>Water treatment</dt><dd>Reverse osmosis + deionisation</dd></div>
          <div class="row"><dt>Target purity at nozzle</dt><dd>Logged per job, shown on the completion record</dd></div>
          <div class="row"><dt>Hot-water option</dt><dd>Available for degreasing on kitchen-exhaust and street-level elevations</dd></div>
          <div class="row"><dt>Supply</dt><dd>Ground base station; rooftop feed where riser access is available</dd></div>
          <div class="row"><dt>Detergent</dt><dd>None by default. Where staining requires it, we tell you which product and why</dd></div>
        </div>
      </div>
      <div>VSLOT_W</div>
    </div>
  </div>
</section>

<section class="sec alt">
  <div class="wrap">
    SECHEAD_L
    <div class="split">
      <div>
        <div class="tblwrap reveal">
          <table class="tbl">
            <caption>Stop-work thresholds</caption>
            <thead><tr><th scope="col">Condition</th><th scope="col">Action</th></tr></thead>
            <tbody>
              <tr><th scope="row">Wind above the airframe limit</th><td>Flight suspended. Limit is stated in the site-specific method statement and is airframe dependent.</td></tr>
              <tr><th scope="row">Rain or lightning risk</th><td>Grounded. Lightning within the vicinity stops work regardless of local conditions.</td></tr>
              <tr><th scope="row">Loss of visual line of sight</th><td>Return to launch. The spotter calls it, not the pilot.</td></tr>
              <tr><th scope="row">Person or vehicle enters the exclusion zone</th><td>Flow off, aircraft holds or lands. Zone re-secured before resuming.</td></tr>
              <tr><th scope="row">Permit conditions cannot be met</th><td>No flight. There is no informal version of this.</td></tr>
            </tbody>
          </table>
        </div>
      </div>
      <div>
        <h3 style="font-size:1.35rem;margin-bottom:14px">What we will not do</h3>
        CHECKS_L
      </div>
    </div>
  </div>
</section>
CTA
""")

# ---------------------------------------------------------------- COMPLIANCE
PAGES["compliance.html"] = dict(nav="compliance",
    title="Compliance, safety and privacy &mdash; " + BRAND,
    desc="CAAS permits, NEA cleaning licence, bizSAFE, ISO and insurance status for Altitude Robotics, plus our PDPA resident-privacy policy and downloadable compliance pack.",
    body=phero([("Compliance", None)], "Compliance &amp; safety",
               "Everything your procurement team is going to ask for, on one page.",
               "Singapore buyers de-risk before they compare. Rather than make you email us for it, the licences, the insurance position, the privacy policy and the method statements live here &mdash; with an honest status against each one.",
               ["CAAS", "NEA", "bizSAFE", "ISO", "PDPA", "Insurance"]) + """
<section class="sec flush">
  <div class="wrap">
    SECHEAD_CR
    <div class="note warn reveal" style="margin-bottom:30px">
      <div class="lbl">How to read the status flags</div>
      <b>Held</b> means the certificate is issued and in our hands, and the reference number is printed on the card. <b>In progress</b> means the application is filed or the audit is booked, and we will not imply otherwise to win work. If a credential you require is still in progress, ask us for the date &mdash; we would rather lose a tender than misrepresent one of these.
    </div>
    CAROUSEL
  </div>
</section>

<section class="sec alt">
  <div class="wrap">
    SECHEAD_PK
    <div class="split">
      <div>
        <p class="lead" style="margin-bottom:24px">Managing agents and FM procurement teams have to attach contractor documents to their own submissions. Ours will download as one file, with no form in front of it.</p>
        <div class="spec reveal">
          <div class="row"><dt>Risk assessment</dt><dd class="empty">In preparation</dd></div>
          <div class="row"><dt>Safe work procedure</dt><dd class="empty">In preparation</dd></div>
          <div class="row"><dt>Generic method statement</dt><dd class="empty">In preparation</dd></div>
          <div class="row"><dt>Insurance certificate</dt><dd class="empty">In preparation</dd></div>
          <div class="row"><dt>Licence and permit copies</dt><dd class="empty">In preparation</dd></div>
          <div class="row"><dt>Sample completion report</dt><dd class="empty">In preparation</dd></div>
          <div class="row"><dt>Resident notice template</dt><dd class="empty">In preparation</dd></div>
        </div>
        <div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:24px">
          <!-- When the ZIP is ready: change the <span> below to
               <a class="btn btn-primary" href="downloads/altitude-compliance-pack.zip" download>Download the pack</a> -->
          <span class="btn btn-ghost" aria-disabled="true">Pack in preparation</span>
          <a class="btn btn-primary" href="mailto:EMAIL?subject=Compliance%20pack%20request">Email me the documents ARROW</a>
        </div>
      </div>
      <div>
        <h3 style="font-size:1.35rem;margin-bottom:16px">Site-specific documents</h3>
        <p style="color:var(--ink-2);margin-bottom:22px">The generic pack gets you through prequalification. Before we fly your building we also issue, at no charge:</p>
        CHECKS_PK
      </div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    SECHEAD_PD
    <div class="split wide">
      <div>
        <p class="lead" style="margin-bottom:22px">A camera flying past a bedroom window collects personal data, and under the PDPA that is our problem to manage &mdash; and yours, if your contractor has not thought about it. This is the policy we operate to, and you are welcome to attach it to your own resident communications.</p>
        CHECKS_PD
      </div>
      <div>
        <div class="note reveal">
          <div class="lbl">Resident notice template</div>
          <p style="margin-bottom:14px">We write the circular for you: purpose, dates, working window, what the camera does and does not record, who to call. Your managing agent puts it on letterhead and posts it at the lift lobbies.</p>
          <p><b>Nobody else in this market hands you that document.</b> It is the single most annoying part of a facade job for a managing agent, and it takes us twenty minutes.</p>
        </div>
        <div class="spec reveal" style="margin-top:20px">
          <div class="row"><dt>Notice period</dt><dd>Written notice before works, posted at lift lobbies and issued to the MA for circulation</dd></div>
          <div class="row"><dt>Working window</dt><dd>Daytime only, agreed with you; out-of-hours available for commercial elevations</dd></div>
          <div class="row"><dt>Camera use</dt><dd>Facade condition only. Angles set to the building, never into the room</dd></div>
          <div class="row"><dt>Footage handling</dt><dd>Not redistributed, not reproduced, retained only for the agreed period</dd></div>
          <div class="row"><dt>Resident guidance</dt><dd>Windows and blinds closed during the pass over your elevation</dd></div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="sec alt">
  <div class="wrap">
    SECHEAD_FQ
    ACC
  </div>
</section>
CTA
""")

# ---------------------------------------------------------------- PROJECTS
PAGES["projects.html"] = dict(nav="projects",
    title="Projects and the numbers behind them &mdash; " + BRAND,
    desc="Every Altitude Robotics job is written up to a fixed schema: area cleaned, access method replaced, crew, days, water used, incidents. Compare us like for like.",
    body=phero([("Projects", None)], "Evidence",
               "Every job, written up the same way.",
               "Most contractors publish a photo and an adjective. We publish a fixed set of fields for every completed project, in the same order, so you can compare two of our jobs to each other &mdash; or hold another contractor's write-up next to ours and notice what is missing.",
               ["Fixed schema", "Named references", "Before / after"]) + """
<section class="sec flush">
  <div class="wrap">
    SECHEAD_SCH
    <div class="split wide">
      <div>
        <div class="spec reveal">
          <div class="row"><dt>Building type</dt><dd>Strata residential, commercial office, industrial, institutional</dd></div>
          <div class="row"><dt>Height and storeys</dt><dd>Metres to the highest cleaned point, and storey count</dd></div>
          <div class="row"><dt>Facade substrate</dt><dd>Every material on the elevations we touched</dd></div>
          <div class="row"><dt>Area cleaned</dt><dd>Square metres, measured, not estimated</dd></div>
          <div class="row"><dt>Access method replaced</dt><dd>Gondola, BMU, rope access, MEWP or scaffold</dd></div>
          <div class="row"><dt>Crew size</dt><dd>Pilots, spotters, ground crew</dd></div>
          <div class="row"><dt>Shifts and calendar days</dt><dd>Both, because they are rarely the same number</dd></div>
          <div class="row"><dt>Water used</dt><dd>Litres, against the baseline for the method we replaced</dd></div>
          <div class="row"><dt>Detergent used</dt><dd>Product and volume, or none</dd></div>
          <div class="row"><dt>Incidents and near-misses</dt><dd>Reported whether or not there were any. A blank field is not the same as a zero</dd></div>
          <div class="row"><dt>Exclusion zone footprint</dt><dd>Area closed at ground level, and for how long</dd></div>
          <div class="row"><dt>Tenant or resident complaints</dt><dd>Count, and what they were about</dd></div>
          <div class="row"><dt>Defects found</dt><dd>What the condition capture picked up that nobody had logged</dd></div>
          <div class="row"><dt>Before and after</dt><dd>Same position, same time of day, same light</dd></div>
          <div class="row"><dt>Client reference</dt><dd>Named person, named role, contactable on request</dd></div>
        </div>
      </div>
      <div>
        <div class="note reveal" style="margin-bottom:20px">
          <div class="lbl">Why the awkward fields are in there</div>
          Incidents, complaints and exclusion-zone footprint are the three things a managing agent gets shouted at about, and the three things contractors leave out of a case study. Publishing them is the point.
        </div>
        BASLIDER
      </div>
    </div>
  </div>
</section>

<section class="sec alt">
  <div class="wrap">
    SECHEAD_IDX
    <div class="g3">
      <a class="card reveal" href="case-study.html"><div class="lbl lbl-a">Case 001</div><h3 style="margin:12px 0 8px">First facade project</h3><p>Reserved. Publishes with every schema field completed and a named reference.</p><div class="kv"><span>Status</span><b>Awaiting completion</b></div></a>
      <a class="card reveal" href="case-study.html"><div class="lbl lbl-a">Case 002</div><h3 style="margin:12px 0 8px">First solar array</h3><p>Reserved. Yield before and after, panel count, litres, and the cleaning interval we recommend from it.</p><div class="kv"><span>Status</span><b>Awaiting completion</b></div></a>
      <a class="card reveal" href="case-study.html"><div class="lbl lbl-a">Case 003</div><h3 style="margin:12px 0 8px">First strata project</h3><p>Reserved. Written for a council audience, with the resident notice and complaint log attached.</p><div class="kv"><span>Status</span><b>Awaiting completion</b></div></a>
    </div>
    <div class="note reveal" style="margin-top:26px">
      <div class="lbl">No invented references</div>
      There are no case studies on this page yet and no testimonials anywhere on this site, because we have not earned them yet. When the first job completes it goes up with the client named and reachable. If you want to be the first, the survey is free and we will price it as a first project.
    </div>
  </div>
</section>
CTA
""")

# ---------------------------------------------------------------- CASE STUDY TEMPLATE
PAGES["case-study.html"] = dict(nav="projects",
    title="Case study template &mdash; " + BRAND,
    desc="The fixed reporting schema Altitude Robotics publishes for every completed drone facade cleaning project in Singapore.",
    body=phero([("Projects", "projects.html"), ("Case template", None)], "Case 000 &middot; template",
               "Case study template &mdash; not yet a project.",
               "This is the page every completed job gets. It is live so you can see exactly what we will publish about your building before you engage us, and so we cannot quietly drop a field that turns out to be unflattering.",
               ["Template", "Fields locked", "Awaiting first project"]) + """
<section class="sec flush">
  <div class="wrap">
    <div class="note warn reveal" style="margin-bottom:36px">
      <div class="lbl">Editing this page</div>
      Copy this file to <code style="font-family:var(--f-mono);color:var(--ink)">case-001-buildingname.html</code>, fill in the <code style="font-family:var(--f-mono);color:var(--ink)">&lt;dd&gt;</code> values, remove the <code style="font-family:var(--f-mono);color:var(--ink)">class="empty"</code> attributes, point the video slots at your files, then link it from projects.html. Do not delete a row because the number is unflattering &mdash; that is the whole point of a fixed schema.
    </div>
    <div class="split wide">
      <div>
        SECHEAD_R
        <div class="spec reveal">
          <div class="row"><dt>Building type</dt><dd class="empty">&mdash;&mdash;</dd></div>
          <div class="row"><dt>Height / storeys</dt><dd class="empty">&mdash;&mdash;</dd></div>
          <div class="row"><dt>Facade substrate</dt><dd class="empty">&mdash;&mdash;</dd></div>
          <div class="row"><dt>Area cleaned (m&sup2;)</dt><dd class="empty">&mdash;&mdash;</dd></div>
          <div class="row"><dt>Access method replaced</dt><dd class="empty">&mdash;&mdash;</dd></div>
          <div class="row"><dt>Crew size</dt><dd class="empty">&mdash;&mdash;</dd></div>
          <div class="row"><dt>Shifts / calendar days</dt><dd class="empty">&mdash;&mdash;</dd></div>
          <div class="row"><dt>Water used (L) vs baseline</dt><dd class="empty">&mdash;&mdash;</dd></div>
          <div class="row"><dt>Detergent used</dt><dd class="empty">&mdash;&mdash;</dd></div>
          <div class="row"><dt>Incidents / near-misses</dt><dd class="empty">&mdash;&mdash;</dd></div>
          <div class="row"><dt>Exclusion zone footprint</dt><dd class="empty">&mdash;&mdash;</dd></div>
          <div class="row"><dt>Complaints logged</dt><dd class="empty">&mdash;&mdash;</dd></div>
          <div class="row"><dt>Defects found</dt><dd class="empty">&mdash;&mdash;</dd></div>
          <div class="row"><dt>Permit reference</dt><dd class="empty">&mdash;&mdash;</dd></div>
          <div class="row"><dt>Client reference</dt><dd class="empty">&mdash;&mdash;</dd></div>
        </div>
      </div>
      <div>
        <div class="lbl" style="margin-bottom:14px">Before / after &mdash; same position, same light</div>
        BASLIDER
        <div style="margin-top:20px">VSLOT_1</div>
      </div>
    </div>
  </div>
</section>

<section class="sec alt">
  <div class="wrap">
    SECHEAD_M
    <div class="g2">VSLOT_2</div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="split">
      <div>
        SECHEAD_D
        <div class="note reveal">
          <div class="lbl">Defect found during the clean</div>
          <p>Reserved for the thing the wash turned up that nobody had logged &mdash; a cracked sealant run, a drummy tile, a corroded bracket. Describe it, show it, say what we recommended and what the client did about it.</p>
          <p style="margin-top:12px"><b>This is the section asset managers forward internally.</b> A clean is a cost line. A defect caught before it falls is a different conversation.</p>
        </div>
      </div>
      <div>
        SECHEAD_Q
        <div class="card reveal">
          <p style="font-size:1.06rem;color:var(--ink-3);font-style:italic">Client quotation goes here, attributed to a named person and role, published with their written permission and contactable on request.</p>
          <div class="kv"><span>Reference</span><b>&mdash;&mdash;</b></div>
        </div>
      </div>
    </div>
  </div>
</section>
CTA
""")

# ---------------------------------------------------------------- ABOUT
PAGES["about.html"] = dict(nav="about",
    title="About &mdash; " + BRAND,
    desc="Altitude Robotics is a Singapore drone facade and solar cleaning company built around ground-based crews, permitted flight and documented handover.",
    body=phero([("About", None)], "Who we are",
               "A cleaning contractor that happens to fly.",
               "Facade cleaning in Singapore has been done the same way for forty years: put a person on a rope or in a cradle and hope. The technology to stop doing that exists now. The harder part is being the kind of contractor a managing agent or an asset manager is willing to sign, and that is what we have built the company around.",
               ["Singapore", "Founded 2025", "SMU BIG"]) + """
<section class="sec flush">
  <div class="wrap">
    SECHEAD_A
    <div class="g3">
      <article class="card reveal"><h3>Ground-based by design</h3><p>Every service we sell is one where the crew stays on the ground. We are not a rope access company with a drone in the van. If a job genuinely needs a rope team, we bring one and we tell you which parts of the building it is for.</p></article>
      <article class="card reveal"><h3>Paperwork is the product</h3><p>The wash is the easy part. What makes a contractor keepable in Singapore is the permit filed on time, the resident notice that went out, the risk assessment that matched the site, and the completion record that survives an audit two years later.</p></article>
      <article class="card reveal"><h3>The facade is data</h3><p>An aircraft at close range with a camera is a survey platform that happens to be holding a hose. Every wash produces a dated visual record of your elevations, which is worth something on its own.</p></article>
    </div>
  </div>
</section>

<section class="sec alt">
  <div class="wrap">
    SECHEAD_B
    <div class="split">
      <div>
        <p class="lead" style="margin-bottom:22px">We are a young company and we are not going to pretend otherwise. Here is what that means in practice, so you can decide whether it is a problem for your building.</p>
        CHECKS_B
      </div>
      <div>
        <div class="note reveal">
          <div class="lbl">What you should ask any drone cleaning contractor</div>
          <p>Which CAAS permits do you hold, and can I see the numbers? Who is your insurer and what is the sum insured? Who writes the resident notice? What happens if a window leaks? What parts of my building can you not reach?</p>
          <p style="margin-top:12px">Ask us the same questions. If a contractor gets vague on any of the five, that is your answer.</p>
        </div>
        <div class="stats reveal" style="margin-top:20px">
          <div><div class="n">SG</div><div class="l">Base of operations</div></div>
          <div><div class="n">0</div><div class="l">Personnel at height, ever</div></div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    SECHEAD_C2
    <div class="g3">
      <article class="card reveal"><div class="lbl lbl-a">Flight operations</div><h3 style="margin:12px 0 8px">Licensed pilots and spotters</h3><p>UAPL-holding pilots, a dedicated spotter on every flight, and a documented abort procedure that the spotter &mdash; not the pilot &mdash; is empowered to call.</p></article>
      <article class="card reveal"><div class="lbl lbl-a">Ground operations</div><h3 style="margin:12px 0 8px">Water plant and exclusion zones</h3><p>The base station crew runs the RO+DI plant, the hose management and the exclusion zone, and holds the line with anyone who tries to walk through it.</p></article>
      <article class="card reveal"><div class="lbl lbl-a">Compliance</div><h3 style="margin:12px 0 8px">Permits and documentation</h3><p>Permit applications, site-specific risk assessments, resident notices and completion records. Filed early, because CAAS lead times do not care about your deadline.</p></article>
    </div>
    <div style="margin-top:36px"><a class="btn btn-ghost" href="careers.html">We are hiring pilots and ground crew ARROW</a></div>
  </div>
</section>
CTA
""")

# ---------------------------------------------------------------- CAREERS
PAGES["careers.html"] = dict(nav="careers",
    title="Careers &mdash; " + BRAND,
    desc="Join Altitude Robotics: drone pilots, ground crew and operations roles in Singapore's drone facade cleaning industry.",
    body=phero([("Careers", None)], "Careers",
               "Build the crew that never leaves the ground.",
               "We are hiring the first operating crews. If you fly, or you want to be trained to, and you would rather run a technical operation than dangle off a building, this is the job.",
               ["Singapore", "Full-time", "Training provided"]) + """
<section class="sec flush">
  <div class="wrap">
    SECHEAD_J
    <div style="display:flex;flex-direction:column;gap:14px">
      <a class="job reveal" href="contact.html"><div><h3>Drone pilot &mdash; facade operations</h3><div class="meta"><span>Singapore</span><span>Full-time</span><span>UAPL required or in training</span></div></div><span class="arrow">ARROW_S</span></a>
      <a class="job reveal" href="contact.html"><div><h3>Ground crew &mdash; water plant and exclusion zone</h3><div class="meta"><span>Singapore</span><span>Full-time</span><span>No flight experience needed</span></div></div><span class="arrow">ARROW_S</span></a>
      <a class="job reveal" href="contact.html"><div><h3>Operations and compliance coordinator</h3><div class="meta"><span>Singapore</span><span>Full-time</span><span>Permits, RA/SWP, scheduling</span></div></div><span class="arrow">ARROW_S</span></a>
      <a class="job reveal" href="contact.html"><div><h3>Business development &mdash; property and FM</h3><div class="meta"><span>Singapore</span><span>Full-time</span><span>MCST / FM network valued</span></div></div><span class="arrow">ARROW_S</span></a>
    </div>
    <div class="note reveal" style="margin-top:30px">
      <div class="lbl">No matching role?</div>
      Send us what you do and what you want to be doing in two years. We are small enough that a good person changes the plan.
    </div>
  </div>
</section>

<section class="sec alt">
  <div class="wrap">
    SECHEAD_W2
    <div class="g3">
      <article class="card reveal"><h3>Training paid for</h3><p>UAPL training and the associated CAAS requirements are covered for ground crew who want to move into the pilot seat.</p></article>
      <article class="card reveal"><h3>Nobody works at height</h3><p>The entire premise of the company. Whatever the job title, you are on the ground with your feet on concrete.</p></article>
      <article class="card reveal"><h3>Early enough to matter</h3><p>The procedures you write in the first year become how the company operates. That is either exciting or terrifying, depending on who you are.</p></article>
    </div>
  </div>
</section>
CTA
""")

# ---------------------------------------------------------------- CONTACT
PAGES["contact.html"] = dict(nav="contact",
    title="Request a site survey &mdash; " + BRAND,
    desc="Tell us the building and we will come back with a flight plan, a price and a date. Free site survey across Singapore.",
    body=phero([("Contact", None)], "Get started",
               "Tell us the building. We will tell you what it takes.",
               "The survey is free and there is no obligation. Give us the address and rough height and we will come back with the access approach, what we can and cannot reach, the permit timeline, and a price.",
               ["Free survey", "Quotation in 48 h", "Island-wide"]) + """
<section class="sec flush">
  <div class="wrap">
    <div class="split wide">
      <div>
        <form class="panel" id="quoteForm" data-validate data-demo data-ok="#formOk">
          <div class="lbl" style="margin-bottom:22px">Site survey request</div>
          <div class="frow">
            <div class="field" data-required><label for="f-name">Your name <span class="req">*</span></label><input id="f-name" name="name" type="text" autocomplete="name"><div class="err">Required</div></div>
            <div class="field" data-required><label for="f-email">Email <span class="req">*</span></label><input id="f-email" name="email" type="email" autocomplete="email"><div class="err">Enter a valid email</div></div>
          </div>
          <div class="frow">
            <div class="field"><label for="f-org">Organisation</label><input id="f-org" name="organisation" type="text" autocomplete="organization"></div>
            <div class="field" data-required><label for="f-role">You are <span class="req">*</span></label>
              <select id="f-role" name="role">
                <option value="">Select&hellip;</option>
                <option>MCST council member</option>
                <option>Managing agent</option>
                <option>REIT / asset manager</option>
                <option>Facility manager</option>
                <option>Cleaning contractor</option>
                <option>Developer / main contractor</option>
                <option>Building owner</option>
                <option>Other</option>
              </select><div class="err">Required</div></div>
          </div>
          <div class="field" data-required><label for="f-building">Building name and address <span class="req">*</span></label><input id="f-building" name="building" type="text"><div class="err">Required</div></div>
          <div class="frow">
            <div class="field"><label for="f-storeys">Storeys / height</label><input id="f-storeys" name="storeys" type="text" placeholder="e.g. 24 storeys, approx 78 m"></div>
            <div class="field"><label for="f-facade">Facade type</label>
              <select id="f-facade" name="facade">
                <option value="">Select&hellip;</option>
                <option>Glass curtain wall</option>
                <option>Aluminium composite panel</option>
                <option>Ceramic tile</option>
                <option>Painted render / concrete</option>
                <option>Mixed</option>
                <option>Not sure</option>
              </select></div>
          </div>
          <div class="frow">
            <div class="field"><label for="f-service">Service needed</label>
              <select id="f-service" name="service">
                <option value="">Select&hellip;</option>
                <option>Facade &amp; glass cleaning</option>
                <option>Solar array cleaning</option>
                <option>Surface treatment</option>
                <option>Condition capture</option>
                <option>Combination</option>
              </select></div>
            <div class="field"><label for="f-when">Timeline</label>
              <select id="f-when" name="timeline">
                <option value="">Select&hellip;</option>
                <option>Within a month</option>
                <option>One to three months</option>
                <option>Next budget cycle</option>
                <option>Just pricing for now</option>
              </select><div class="hint">CAAS permits take 2&ndash;4 weeks, so tell us early if you have a deadline.</div></div>
          </div>
          <div class="field"><label for="f-notes">Anything else</label><textarea id="f-notes" name="notes" placeholder="Known problem elevations, restricted hours, previous contractor, deadlines you are working to&hellip;"></textarea></div>
          <button class="btn btn-primary" type="submit" style="width:100%">Send survey request ARROW</button>
          <p class="hint" style="margin-top:14px">We reply within one business day and quote within 48 hours of the survey.</p>
        </form>
        <div class="form-ok panel" id="formOk">
          <div class="ck">TICK</div>
          <h2>Request received</h2>
          <p>We will come back within one business day to arrange the survey.</p>
        </div>
      </div>
      <div>
        <div class="lbl" style="margin-bottom:20px">Direct lines</div>
        <div class="crow"><div class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg></div><div><div class="lbl">Email</div><div class="val"><a href="mailto:EMAIL">EMAIL</a></div></div></div>
        <div class="crow"><div class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 4h4l2 5-3 2a12 12 0 005 5l2-3 5 2v4a1 1 0 01-1 1A16 16 0 014 5a1 1 0 011-1z"/></svg></div><div><div class="lbl">Phone</div><div class="val"><a href="tel:PHONERAW">PHONE</a></div></div></div>
        <div class="crow"><div class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 11.5a8.4 8.4 0 01-12.3 7.5L3 21l2-5.6A8.4 8.4 0 1121 11.5z"/></svg></div><div><div class="lbl">WhatsApp &mdash; fastest</div><div class="val"><a href="https://wa.me/WA">Message us</a></div></div></div>
        <div class="crow"><div class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 21s7-5.6 7-11a7 7 0 10-14 0c0 5.4 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/></svg></div><div><div class="lbl">Office</div><div class="val">ADDR1<br>ADDR2</div></div></div>
        <div class="note reveal" style="margin-top:30px">
          <div class="lbl">What happens next</div>
          <p style="margin-bottom:10px"><b>1.</b> We reply within a business day and book the survey.</p>
          <p style="margin-bottom:10px"><b>2.</b> We walk the site, record substrates and access constraints, and identify what we cannot reach.</p>
          <p style="margin-bottom:10px"><b>3.</b> You get a scope, a price, a permit timeline and a method statement within 48 hours.</p>
          <p><b>4.</b> If drones are the wrong answer for your building, we say so at step two.</p>
        </div>
      </div>
    </div>
  </div>
</section>
""")


# ---------------------------------------------------------------- SECTOR PAGES
def sector_page(nav, label, h1, lead, pills, accountable, fit_intro, fit_checks,
                deliverables, docs, timeline, faqs, closing):
    rows = "".join('<tr><th scope="row">%s</th><td>%s</td></tr>' % (a, b) for a, b in deliverables)
    acards = "".join(
        '<article class="card reveal"><div class="lbl lbl-a">%s</div><h3 style="margin:12px 0 8px">%s</h3><p>%s</p></article>'
        % (k, t, d) for k, t, d in accountable)
    tsteps = "".join(
        '<article class="card stepcard reveal"><div class="num"><i>%s</i></div><h3>%s</h3><p>%s</p></article>'
        % (n, t, d) for n, t, d in timeline)
    return phero([("Sectors", None), (re.sub("<[^>]+>", "", label), None)], "Built for " + label,
                 h1, lead, pills) + """
<section class="sec flush">
  <div class="wrap">
    %s
    <div class="g3">%s</div>
  </div>
</section>

<section class="sec alt">
  <div class="wrap">
    %s
    <div class="split">
      <div><p class="lead" style="margin-bottom:24px">%s</p>%s</div>
      <div>
        <div class="tblwrap reveal">
          <table class="tbl"><caption>What you get, every job</caption>
            <tbody>%s</tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    %s
    <div class="split">
      <div>%s</div>
      <div><div class="note reveal">%s</div></div>
    </div>
  </div>
</section>

<section class="sec alt">
  <div class="wrap">
    %s
    <div class="g3">%s</div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    %s
    %s
  </div>
</section>
""" % (sec_head("01", "Your exposure", "What you are accountable for."),
       acards,
       sec_head("02", "How we fit", "Where we slot into how you already work."),
       fit_intro, checks(fit_checks), rows,
       sec_head("03", "Documentation", "The paperwork you get, without asking."),
       checks(docs), closing,
       sec_head("04", "Sequence", "How a job runs, start to finish."), tsteps,
       sec_head("05", "Questions", "The ones you were going to ask anyway."), acc(faqs))


PAGES["sectors-mcst.html"] = dict(nav="mcst",
    title="For MCSTs and managing agents &mdash; " + BRAND,
    desc="Drone facade cleaning for Singapore condominiums: AGM-ready pricing, resident notice templates, PDPA compliance and a documented handover for your council.",
    body=sector_page(
        "mcst", "MCSTs &amp; managing agents",
        "Your council has to approve it. We write it so they can.",
        "A facade clean is not a technical decision for an MCST, it is a governance one. Somebody has to explain the spend at a general meeting, answer the owner who thinks a drone will film her bedroom, and produce the paperwork if something goes wrong two years later. We build the job around those three problems.",
        ["Strata", "BMSMA", "Sinking fund", "AGM cycle"],
        accountable=[
            ("Money", "Spending owners' money in public",
             "Every dollar comes out of the management or sinking fund and gets read out at a general meeting. Capital expenditure above S$200,000 needs a 75% special resolution by share value, so the size of the package changes what approval you need."),
            ("Residents", "Two hundred owners with opinions",
             "Somebody will object to a camera near their window, somebody else will complain about water on their car, and both will email you, not us. Getting ahead of that in writing is most of the job."),
            ("Liability", "Common property is your responsibility",
             "The facade is common property under the BMSMA. If an unlicensed contractor works on it, or an uninsured one damages it, the exposure sits with the MCST and, uncomfortably, with the council members who approved it."),
        ],
        fit_intro="Managing agents run several estates and do not have time to educate a new contractor about strata process. We arrive already knowing what your council will ask, and we produce the documents in the form your AGM pack needs them.",
        fit_checks=[
            "<b>Quotes scoped to the approval you need.</b> We will structure the package around your thresholds and tell you plainly which approval route it triggers, rather than handing you a number and letting you find out.",
            "<b>An AGM one-pager, written for owners.</b> Plain-language scope, cost, timeline, safety position and the answer to &ldquo;why not just use the usual rope guys&rdquo; &mdash; on one side of A4 you can put straight into the pack.",
            "<b>The resident notice, drafted for you.</b> Purpose, dates, working window, camera policy, who to call. You put it on letterhead. This is the part managing agents tell us they hate most.",
            "<b>We attend the council meeting if it helps.</b> Somebody technical in the room answering owners directly usually shortens the whole process by a cycle.",
            "<b>Complaints come to us with a log.</b> Every complaint recorded, responded to and reported back to you at completion, not quietly absorbed.",
        ],
        deliverables=[
            ("Licence and insurance copies", "Provided at quotation, before you shortlist"),
            ("Site-specific risk assessment", "Issued before mobilisation, matched to your estate"),
            ("Resident notice, draft", "Ready for your letterhead and lift-lobby boards"),
            ("Working window", "Daytime, agreed with you and stated in the notice"),
            ("Exclusion zone plan", "Marked on your site plan, with the car park impact shown"),
            ("Before and after per elevation", "Same position, same light, dated"),
            ("Defect log", "What the wash found on your facade that nobody had logged"),
            ("Complaint log", "Every resident contact, and what we did about it"),
            ("Completion record", "Signed, for your files and the next council"),
        ],
        docs=[
            "<b>Before you shortlist:</b> licence copies, insurance certificate with the sum insured, and the generic method statement.",
            "<b>Before the AGM:</b> the one-page owner summary and the cost breakdown by elevation or block.",
            "<b>Before mobilisation:</b> site-specific risk assessment, safe work procedure, the CAAS permit reference, and the resident notice ready to post.",
            "<b>At completion:</b> before-and-after set, defect log, complaint log, flight log and signed completion record.",
        ],
        timeline=[
            ("01 &mdash; ENQUIRY", "Survey, free", "We walk the estate with your MA, record substrates and access, and identify anything drones cannot reach. You get scope and price within 48 hours."),
            ("02 &mdash; APPROVAL", "Council or AGM", "You get the one-pager and the cost breakdown. We will attend the meeting if owners want to ask questions directly."),
            ("03 &mdash; PERMIT", "CAAS filing", "Two to four weeks. Start six to eight weeks before any date you are committed to."),
            ("04 &mdash; NOTICE", "Residents informed", "Notices go up at the lift lobbies and circulars go out, ahead of the works, with the working window stated."),
            ("05 &mdash; WORKS", "Crew on the ground", "Base station at ground level, exclusion zone managed, elevations flown to plan. Your security team knows what is in the air."),
            ("06 &mdash; HANDOVER", "Evidence pack", "Before and after, defect log, complaint log, completion record. Filed so the next council can find it."),
        ],
        faqs=[
            ("A resident says the drone will film into her flat. What do I tell her?",
             "<p>That the concern is legitimate and the policy exists for exactly that reason. Cameras point at the building, not into it. Footage is used for facade condition and cleaning verification, is not redistributed or reproduced, and is retained only for the agreed period. Residents are asked to close windows and blinds during the pass over their elevation, which is the same guidance HDB uses on its own facade drone work.</p><p>We give you all of this in writing before the notice goes out, so you are not improvising an answer at the AGM.</p>"),
            ("What if the drone damages a window or a car?",
             "<p>Third-party public liability cover applies, and the sum insured is on the compliance page rather than buried in a policy we make you request. The exclusion zone plan is agreed with you in advance precisely so that cars are not underneath us, and we will ask you to reserve or cone specific lots on specific days.</p>"),
            ("Is this cheaper than the gondola contractor we use now?",
             "<p>Sometimes, and it depends on your building. The saving comes from setup and disruption rather than the wash itself: no cradle booking, no rigging days, no closed walkways, and an exclusion zone that moves with the crew instead of sitting on your entrance for a fortnight. On a building with a working BMU and simple elevations, the gap narrows.</p><p>We will tell you at survey if the honest answer for your estate is that it is a wash. We would rather do that than win one job and lose the managing agent.</p>"),
            ("Our building is 30 storeys. Can you even reach the top?",
             "<p>The default ceiling for uncontrolled flight is 60 metres above mean sea level, which most Singapore high-rises exceed. Working above it needs a Class 1 activity permit with a safety case showing the aircraft stays within the building's own airspace. That is normal work for us, but it is the reason the permit takes two to four weeks and the reason you should not engage anyone a fortnight before a deadline.</p>"),
            ("Do we still need our regular cleaning contractor?",
             "<p>Almost certainly yes. We do facades, glass, solar and hard-to-reach exteriors. Common area cleaning, bin centres, pool decks and daily janitorial work are a different licence and a different business. We are additive to your cleaning contract, not a replacement for it.</p>"),
        ],
        closing="<div class=\"lbl\">One thing to check on every quote you receive</div><p style=\"margin-bottom:12px\">Ask each drone contractor for their NEA Cleaning Business Licence number and check it against NEA's public list.</p><p>Engaging an unlicensed cleaning business is an offence for the buyer, not only the contractor &mdash; a fine of up to S$10,000, and S$1,000 a day if it continues. That exposure lands on the MCST. It takes two minutes to check and it is the cheapest risk control available to a council.</p>"))

PAGES["sectors-reit.html"] = dict(nav="reit",
    title="For REITs and asset managers &mdash; " + BRAND,
    desc="Portfolio facade cleaning by drone: repeatable per-asset numbers, ESG-ready data, zero work-at-height exposure, and condition capture on the same flight.",
    body=sector_page(
        "reit", "REITs &amp; asset managers",
        "One method, every asset, numbers you can put in a report.",
        "You are not buying a clean building, you are buying a line item that has to be defensible: comparable across assets, low on incident risk, and reportable when the sustainability team comes asking. A contractor who cannot give you the same fields for every property is a contractor you will have to chase every quarter.",
        ["Portfolio", "ESG reporting", "Opex", "Tenant experience"],
        accountable=[
            ("Risk", "Work-at-height sits on your asset",
             "Facade access is among the highest-risk activity that happens on a commercial property. Every rope drop and every cradle movement is exposure that appears in your incident statistics, your insurance conversations and, if it goes wrong, your annual report."),
            ("Reporting", "Numbers that have to reconcile",
             "Water volume, chemical use, incident count and contractor hours all have somewhere to go in your reporting. Getting them from a contractor who has never been asked before means a quarterly chase and an estimate you cannot stand behind."),
            ("Tenants", "Disruption is a leasing problem",
             "Closed walkways, cradles outside meeting rooms and cordoned drop-off areas are the sort of thing tenants remember at renewal. The cost of a facade programme is not only what you pay the contractor."),
        ],
        fit_intro="We work to the same schema on every asset, so the second building costs you less management attention than the first. Portfolio work is scheduled as a programme, not as a sequence of unrelated quotations.",
        fit_checks=[
            "<b>Identical reporting fields on every asset.</b> Area, litres, crew, days, incidents, complaints, defects. The same fields in the same order, whether it is a suburban office or a CBD tower.",
            "<b>Machine-readable output.</b> The completion data comes as a spreadsheet as well as a PDF, so your team is not retyping numbers into a reporting template.",
            "<b>Condition capture on the same flight.</b> Every wash produces a dated visual record of the elevations. Over a few cycles you have deterioration tracking nobody had to commission separately.",
            "<b>Programme pricing across assets.</b> One mobilisation planning exercise across several properties, rather than pricing each one as a cold start.",
            "<b>Work-at-height exposure removed, not transferred.</b> There is no subcontracted rope team quietly doing the parts we did not mention. Where rope access is genuinely required, it is named in the scope and priced in the open.",
        ],
        deliverables=[
            ("Per-asset data export", "Spreadsheet plus PDF, same fields every time"),
            ("Water and chemical volumes", "Measured on site, not estimated afterwards"),
            ("Incident and near-miss record", "Reported whether or not there were any"),
            ("Personnel-at-height hours", "Zero for drone scope; stated separately if rope access is used"),
            ("Facade condition imagery", "Elevation by elevation, dated, retained for comparison"),
            ("Defect log", "Ranked, with what we recommend and how urgent it is"),
            ("Exclusion zone and disruption record", "Ground area affected and duration"),
            ("Permit references", "Per site, per date"),
        ],
        docs=[
            "<b>At prequalification:</b> licences, insurance, ISO position, bizSAFE level and our safety statistics &mdash; with honest status flags rather than implied claims.",
            "<b>Per asset before works:</b> site-specific risk assessment, method statement and the permit reference.",
            "<b>Per asset at completion:</b> the full data export, imagery set, defect log and completion record.",
            "<b>Annually:</b> a consolidated portfolio summary you can hand to whoever writes your sustainability reporting.",
        ],
        timeline=[
            ("01 &mdash; PORTFOLIO REVIEW", "Assets triaged", "We look at the whole list and sort it by what drones do well, what needs a hybrid approach, and what is honestly better left to your incumbent."),
            ("02 &mdash; PILOT ASSET", "One building, fully documented", "Start with a single property and the complete data set. That is the artefact you take to your investment committee."),
            ("03 &mdash; PROGRAMME", "Scheduled across assets", "Mobilisations planned as a sequence, priced as a programme, scheduled around your tenant calendars."),
            ("04 &mdash; REPORTING", "Consolidated annually", "Portfolio-level roll-up of volumes, incidents, condition changes and defects found."),
        ],
        faqs=[
            ("Can you give us data in our reporting format?",
             "<p>Yes. The underlying fields are fixed, and mapping them into your template is a small piece of work we would rather do once at the start than argue about every quarter. Tell us the format at prequalification.</p>"),
            ("How does this affect our work-at-height statistics?",
             "<p>Drone scope contributes zero personnel-hours at height. Where a building genuinely needs rope access for recessed areas, those hours exist and we report them separately rather than folding them into a headline claim. A contractor who tells you their number is zero on every building is not describing a real building.</p>"),
            ("What is the realistic cost picture across a portfolio?",
             "<p>It varies more by geometry than by size. Simple towers with a working BMU are where traditional access is most competitive. Complex podiums, setbacks, atria and buildings with no cradle track are where the difference is largest, because the alternative involves rigging that costs more than the cleaning does.</p><p>The honest way to find out is to price two contrasting assets rather than accept a portfolio-wide percentage from anyone.</p>"),
            ("Do you subcontract?",
             "<p>Flight operations are ours. Where a scope genuinely needs rope access we name the partner in the proposal, with their licences attached, rather than presenting their work as ours.</p>"),
        ],
        closing="<div class=\"lbl\">The asset-level argument</div><p style=\"margin-bottom:12px\">Singapore's climate is unusually hard on facades: sustained high UV, around 80% humidity, heavy monsoon rain and constant thermal cycling from air conditioning. Materials that would last decades in a temperate climate deteriorate materially faster here.</p><p>Which means the interesting output of a facade clean is not the clean. It is the dated, elevation-by-elevation record of what your building looked like this year compared with last year &mdash; and we generate it as a by-product of work you were going to pay for anyway.</p>"))

PAGES["sectors-fm.html"] = dict(nav="fm",
    title="For FM and cleaning contractors &mdash; " + BRAND,
    desc="White-label drone facade cleaning capacity for Singapore facility management and cleaning contractors. Keep the client, subcontract the height.",
    body=sector_page(
        "fm", "FM &amp; cleaning contractors",
        "Keep the contract. Subcontract the height.",
        "Your client is asking about drones. Building the capability yourself means airframes, pilots, permits and an insurance conversation you did not budget for &mdash; and it means being the operator of record when something goes wrong. Bringing it in as a subcontracted line keeps the relationship where it is and puts the aviation risk with the people who are licensed for it.",
        ["Subcontract", "White-label", "Day rates", "No client contact"],
        accountable=[
            ("The relationship", "The client is yours and stays yours",
             "You have spent years on that account. The last thing you need is a specialist subcontractor introducing themselves to your client and quoting direct six months later."),
            ("The scope", "You are being asked for something new",
             "Drone facade cleaning is turning up in tender documents and AGM agendas. Answering &ldquo;we do not do that&rdquo; often enough eventually costs you the whole contract, not just the facade line."),
            ("The risk", "Aviation is a different liability class",
             "Operating unmanned aircraft commercially means operator permits, licensed pilots, per-site activity permits and specific insurance. That is a capability build, not a purchase, and it sits on your licence if you take it on."),
        ],
        fit_intro="We are set up to work behind you. Our crews turn up in whatever presentation you specify, report to your site supervisor, and never contact your client without you in the room.",
        fit_checks=[
            "<b>Non-solicitation, in writing.</b> Your clients are off limits for the term and after it. We will sign it before we quote, not after you ask.",
            "<b>Unbranded or co-branded on site.</b> Your uniform, your signage, your site induction. We are a resource on your job, not a competitor doing a demo.",
            "<b>Day rates and per-m&sup2; rates.</b> Pricing you can mark up and put straight into your own tender without reverse-engineering a bundled quotation.",
            "<b>Documents in your format.</b> Risk assessments and method statements written into your templates, so your WSH officer is not reconciling two systems.",
            "<b>We slot into your PPM schedule.</b> Cyclical facade work planned against your existing maintenance calendar, not dropped on top of it.",
        ],
        deliverables=[
            ("Rate card", "Day rate and per-m&sup2;, with mobilisation stated separately"),
            ("Subcontractor pack", "Licences, insurance, bizSAFE, ISO position, safety record"),
            ("Non-solicitation undertaking", "Signed before we quote on your account"),
            ("RA and SWP", "Written into your document templates"),
            ("Permit handling", "We file with CAAS; you never touch an aviation form"),
            ("Site presentation", "Unbranded or co-branded, your call"),
            ("Reporting", "Handed to you, in your format, for you to pass on as yours"),
            ("Capacity commitment", "Agreed crew availability windows, stated in the agreement"),
        ],
        docs=[
            "<b>At onboarding:</b> full subcontractor prequalification pack, insurance certificates and signed non-solicitation.",
            "<b>Per job:</b> site-specific risk assessment and method statement in your templates, plus the permit reference.",
            "<b>At completion:</b> reporting pack in your format, unbranded, for you to issue to your client under your own cover.",
        ],
        timeline=[
            ("01 &mdash; ONBOARD", "Prequalification once", "You run us through your vendor process once. After that we are an available resource, not a fresh procurement exercise per job."),
            ("02 &mdash; PRICE", "Rate card, not quotations", "You price your own client from our rate card. No waiting on us to turn a quotation around while your tender clock runs."),
            ("03 &mdash; DELIVER", "Under your banner", "Our crew, your site presentation, your supervisor. Permits and aviation compliance stay with us."),
            ("04 &mdash; REPORT", "In your format", "You receive the pack unbranded and issue it to your client as your own deliverable."),
        ],
        faqs=[
            ("What stops you approaching our client directly?",
             "<p>A signed non-solicitation undertaking covering the account for the term and a defined period after it, executed before we quote. We will also decline inbound enquiries from a building we know is yours and tell you it came in &mdash; that is more valuable to us than one job.</p>"),
            ("Can we white-label completely?",
             "<p>Yes. Unbranded crew presentation and reporting delivered without our name on it are both standard options. Some contractors prefer co-branding because the technology is a selling point for them; that is your commercial decision, not ours.</p>"),
            ("Who holds the aviation liability?",
             "<p>We do. The operator permit, the pilot licences, the per-site activity permit and the aviation liability cover are ours, and the flight is our operation. Your exposure is the same as engaging any other specialist subcontractor.</p>"),
            ("What lead time do you need?",
             "<p>Crew scheduling is usually days. The binding constraint is the CAAS activity permit, which runs two to four weeks per site. If you are bidding work with a fixed start date, involve us at bid stage rather than at award, and we will file early.</p>"),
        ],
        closing="<div class=\"lbl\">The window is not open forever</div><p style=\"margin-bottom:12px\">Every serious FM and cleaning group in Singapore is currently working out whether to buy this capability, build it, or partner for it. A large staffing and FM group has already tied up exclusive regional distribution for an autonomous facade cleaning platform.</p><p>Partnering is the cheapest way to have an answer for your clients while that plays out &mdash; and it costs you nothing to have the rate card sitting in your bid library before you need it.</p>"))

PAGES["sectors-developer.html"] = dict(nav="dev",
    title="For developers and main contractors &mdash; " + BRAND,
    desc="Handover cleaning and defect-liability recleans by drone for Singapore developers and main contractors. Fits the programme, removes work at height from the WSH plan.",
    body=sector_page(
        "dev", "Developers &amp; main contractors",
        "Handover cleans that do not hold up the programme.",
        "At the end of a project the facade needs to be spotless, the scaffold is coming down, the cradle may not be commissioned yet, and every remaining trade is fighting for the same access. A cleaning method that needs no ties, no rigging and no cradle track removes one of the dependencies from your critical path.",
        ["Handover", "TOP", "DLP recleans", "WSH plan"],
        accountable=[
            ("Programme", "The facade clean is on the critical path",
             "It cannot start until the trades above are done, and it cannot finish after handover. Anything that needs a week of rigging in that window is a scheduling problem before it is a cleaning problem."),
            ("Safety", "Work at height is in your WSH plan",
             "Every rope drop and cradle movement in the final weeks is another entry in your risk register, at exactly the point when the site is most congested and the schedule pressure is highest."),
            ("Defects", "The liability period keeps going",
             "Recleans and facade touch-ups during the defects liability period happen in an occupied building, where scaffolding and closed walkways are no longer acceptable to the people living or working there."),
        ],
        fit_intro="We mobilise off a ground base station in a few hours and need no structural attachment to the building. That makes us schedulable late, movable at short notice, and workable in the same window as other trades with an exclusion zone that moves with us.",
        fit_checks=[
            "<b>No ties, no rigging, no cradle dependency.</b> We do not need the BMU commissioned and we do not need scaffold left standing for our benefit.",
            "<b>Mobilisation in hours, not days.</b> Which means we can absorb a programme slip instead of adding to one.",
            "<b>Site-specific RA and SWP into your WSH file.</b> In your templates, submitted before we come through the gate, with zero personnel-at-height hours in the drone scope.",
            "<b>Sequenced around other trades.</b> Exclusion zones move with the crew, so we are not holding a whole elevation for a fortnight.",
            "<b>DLP recleans in an occupied building.</b> The same method works after handover, when scaffolding is no longer an option.",
        ],
        deliverables=[
            ("Site-specific RA and SWP", "In your templates, ahead of mobilisation"),
            ("Permit-to-work compliance", "We work to your site permit system"),
            ("Toolbox and induction", "Our crew inducts to your site like any other trade"),
            ("Exclusion zone plan", "Sequenced against your other trades"),
            ("Handover condition capture", "Dated imagery of every elevation at practical completion"),
            ("Defect log", "What the wash exposed, before the client's consultant finds it"),
            ("Completion record", "For your handover documentation"),
            ("DLP call-off", "Agreed rates for recleans during the liability period"),
        ],
        docs=[
            "<b>At tender:</b> licences, insurance, safety record and an outline method statement you can attach to your submission.",
            "<b>Before mobilisation:</b> site-specific risk assessment and safe work procedure in your format, plus the CAAS permit reference.",
            "<b>At handover:</b> condition imagery per elevation, defect log and signed completion record for the O&amp;M file.",
        ],
        timeline=[
            ("01 &mdash; PRE-TENDER", "Method into your bid", "Bring us in at bid stage and the outline method statement and rates go into your submission. Permit lead time gets planned rather than discovered."),
            ("02 &mdash; PROGRAMME", "Slotted, not squeezed", "We agree the window against your trade sequence and file the CAAS permit against it, allowing two to four weeks."),
            ("03 &mdash; HANDOVER CLEAN", "Elevation by elevation", "Ground base station, moving exclusion zone, no attachment to the structure, no interference with the cradle commissioning."),
            ("04 &mdash; DLP", "Call-off recleans", "Agreed rates for the liability period, in an occupied building, without scaffolding."),
        ],
        faqs=[
            ("Can you work while other trades are still on the facade?",
             "<p>Not on the same elevation at the same time &mdash; nothing can. But because our exclusion zone is small and moves with the crew, we can work an elevation while other trades hold a different one, which is rarely possible with a cradle or a scaffold run.</p>"),
            ("What about construction residue, cement splash and adhesive?",
             "<p>Some of it comes off with a controlled wash and some of it does not. Cementitious splatter and cured adhesive often need mechanical contact, which means a rope team on those specific panels. We identify it at survey and price it openly rather than discovering it on handover week.</p>"),
            ("Do you need the BMU commissioned?",
             "<p>No. We are entirely independent of the building's access system, which is often the point &mdash; the cradle is frequently the last thing to be signed off, and it tends to be signed off after the facade needed to be clean.</p>"),
            ("How late can we bring you in?",
             "<p>Crew scheduling is days. The CAAS activity permit is two to four weeks and is not compressible by paying more. That single constraint is the reason to talk to us at bid stage rather than at the point the client's handover inspection is booked.</p>"),
        ],
        closing="<div class=\"lbl\">One thing worth planning early</div><p style=\"margin-bottom:12px\">The permit is the only part of this that cannot be accelerated with money or effort. Two to four weeks, per site, filed against a defined location, date and altitude.</p><p>Bring it into the programme at bid stage and it costs you nothing. Discover it three weeks before handover and it is the reason the facade is not clean on the day the client walks the building.</p>"))


# ================================================================= COMPONENTS
ARROW_SM = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" width="18" height="18" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>')

RAIL_HTML = ('<div class="rail" role="region" aria-label="Credential status">' + CRED_NOTE +
             '<div class="rail-track">' +
             "".join(cred_card(c) for c in CREDENTIALS) +
             "".join(cred_card(c, aria_hidden=True) for c in CREDENTIALS) +
             '</div></div>')

CAROUSEL_HTML = ('<div class="carousel reveal">' + CRED_NOTE +
                 '<div class="car-nav">'
                 '<button class="car-btn" data-car="prev" aria-label="Previous credentials">'
                 '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 6l-6 6 6 6"/></svg></button>'
                 '<button class="car-btn" data-car="next" aria-label="Next credentials">'
                 '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg></button>'
                 '</div>'
                 '<div class="car-track" tabindex="0" role="group" aria-label="Credentials, scrollable">' +
                 "".join(cred_card(c) for c in CREDENTIALS) +
                 '</div></div>')


def ba_slider(before="Before", after="After"):
    return ('<div class="ba reveal">'
            '<div class="ba-pane ba-before"><span class="ph">Before &mdash; image pending</span></div>'
            '<div class="ba-pane ba-after"><span class="ph">After &mdash; image pending</span></div>'
            '<span class="ba-tag l">%s</span><span class="ba-tag r">%s</span>'
            '<span class="ba-handle"></span>'
            '<input type="range" min="0" max="100" value="50" aria-label="Reveal the after image">'
            '</div>'
            '<!-- BEFORE/AFTER IMAGES: add <img src="media/before.jpg" alt=""> inside .ba-before'
            ' and <img src="media/after.jpg" alt=""> inside .ba-after, then delete the two <span class="ph"> lines. -->'
            % (before, after))


SECTOR_CARDS = "".join(
    '<a class="card reveal" href="%s"><div class="lbl lbl-a">Sector</div>'
    '<h3 style="margin:12px 0 8px">%s</h3><p>%s</p>'
    '<div class="kv"><span>Read the brief</span><b>&rarr;</b></div></a>' % (h, t, s)
    for h, k, t, s in SECTORS)


# ================================================================= TOKENS
TOKENS = {
    "ARROW": ARR,
    "ARROW_S": ARROW_SM,
    "TICK": TICK,
    "POSTER": HERO_POSTER,
    "EMAIL": EMAIL,
    "PHONE": PHONE,
    "PHONERAW": PHONE.replace(" ", ""),
    "WA": PHONE_WA,
    "ADDR1": ADDR1,
    "ADDR2": ADDR2,
    "RAIL": RAIL_HTML,
    "CAROUSEL": CAROUSEL_HTML,
    "SECTORCARDS": SECTOR_CARDS,
    "BASLIDER": ba_slider(),

    # ---- home
    "SECHEAD_CAP": sec_head("01", "Capability", "Four services, one crew, nobody off the ground.",
                            "Everything runs off the same ground base station, which is why booking them together costs less than booking them apart."),
    "SECHEAD_CMP": sec_head("02", "The comparison", "How this actually differs from a cradle.",
                            "The saving is in setup and disruption more than in the wash itself. Here is the honest version, including where we are the wrong answer."),
    "SECHEAD_HOW": sec_head("03", "Method", "Survey, permit, fly, hand over the evidence.",
                            "The flying is the short part. What makes a job go well in Singapore is what happens in the four weeks before it."),
    "SECHEAD_SEC": sec_head("04", "Who we work for", "Four buyers, four different problems.",
                            "A council chair, an asset manager, an FM director and a project manager are buying completely different things. Pick yours."),
    "SECHEAD_EV": sec_head("05", "Evidence", "Numbers, not adjectives."),
    "SECHEAD_FEED": sec_head("06", "Field footage", "Watch the method, not a rendering.",
                             "These slots go live as the first jobs complete. Nothing here is stock footage or a simulation, which is why they are empty rather than filled with somebody else's building."),
    "CHECKS_EV": checks([
        "<b>Area, crew, days and litres</b> for every job, measured rather than estimated.",
        "<b>Incidents and complaints published</b> whether or not there were any. A blank field is not the same as a zero.",
        "<b>Before and after from the same position</b>, same time of day, same light &mdash; not a bright day against a grey one.",
        "<b>A named, contactable reference</b> on every project, published with their permission.",
    ]),
    "FILM": vslot("Film 01", "Survey to handover &mdash; the full method", mode="film", ratio="wide",
                  pending="Process film in production. Drop the MP4 into /media and set data-src on this slot."),
    "FEEDS": (
        vslot("Feed 01", "Before / after &mdash; locked-off comparison",
              pending="Locked-off before and after pass. Same tripod position, same time of day.") +
        vslot("Feed 02", "Water plant &mdash; RO+DI and TDS reading",
              pending="Base station walkthrough with the TDS meter reading on camera.") +
        vslot("Feed 03", "Safety &mdash; exclusion zone and abort procedure",
              pending="Exclusion zone setup, spotter comms and the abort call, filmed for WSH officers.")),

    # ---- services
    "SECHEAD_F": sec_head("01", "Facade &amp; glass", "Pure water, controlled flow, no residue."),
    "SECHEAD_S": sec_head("02", "Solar arrays", "Yield you are losing to dust."),
    "SECHEAD_T": sec_head("03", "Surface treatment", "Buy back the interval between cleans."),
    "SECHEAD_C": sec_head("04", "Condition capture", "The facade record you get for free."),
    "SECHEAD_W": sec_head("05", "Water system", "The part that decides whether the glass streaks."),
    "SECHEAD_L": sec_head("06", "Limits", "When we stop, and what we decline."),
    "CHECKS_F": checks([
        "<b>Reverse-osmosis and deionised water</b> made on site, so the rinse dries clear without a squeegee.",
        "<b>Flow and angle managed per substrate</b> &mdash; the setting for sealed glazing is not the setting for a tiled facade.",
        "<b>Exclusion zone moves with the crew</b> rather than closing your entrance for the duration.",
        "<b>Overspray controlled by sequencing</b>, with vehicle areas cleared elevation by elevation instead of all at once.",
        "<b>Hot water available</b> where street-level or kitchen-exhaust elevations need degreasing.",
    ]),
    "CHECKS_S": checks([
        "<b>Nobody walks the array.</b> No point loading, no micro-cracking, no cracked backsheets from foot traffic.",
        "<b>Deionised water only.</b> Detergent leaves a film that attracts the next layer of soiling faster than no clean at all.",
        "<b>Output measured either side</b> where your inverter data allows it, so the interval is set by evidence rather than habit.",
        "<b>Rooftop, podium and carport arrays</b>, including the ones no safe walkway was ever designed for.",
    ]),
    "CHECKS_T": checks([
        "<b>Anti-mould and anti-algae</b> on shaded and north-facing elevations where regrowth is fastest.",
        "<b>Applied on the same mobilisation</b> as the wash, so you pay one setup instead of two.",
        "<b>Product named in the quotation</b>, with the safety data sheet attached before we apply anything.",
        "<b>Test patch first</b> on any substrate we have not treated at your building before.",
    ]),
    "CHECKS_C": checks([
        "<b>Elevation-by-elevation imagery</b>, dated and retained so next year's set can be compared with this one.",
        "<b>Defect log</b> covering what we saw: sealant failure, drummy or cracked tile, corrosion staining, render cracking.",
        "<b>Flagged, not washed.</b> Anything that looks loose gets recorded and left alone rather than blasted off your building.",
        "<b>Handed over as data</b>, not only as a PDF, so it is usable by whoever does your next condition assessment.",
    ]),
    "CHECKS_L": checks([
        "<b>We do not fly without a permit.</b> There is no informal version of a CAAS activity permit and nobody should offer you one.",
        "<b>We do not wash loose or damaged substrate.</b> If a tile is drummy it goes in the defect log and we work around it.",
        "<b>We do not claim to reach everything.</b> Deep reveals, enclosed light wells and heavy mechanical soiling need a rope team, and we say so at survey.",
        "<b>We do not fly outside the agreed window</b> to catch up a schedule, and we do not fly in marginal weather to avoid a return visit.",
    ]),
    "VSLOT_F": vslot("Feed 04", "Facade wash &mdash; elevation pass",
                     pending="Facade wash b-roll. Locked-off and tracking shots of a full elevation pass."),
    "VSLOT_S": vslot("Feed 05", "Solar array &mdash; rooftop pass",
                     pending="Rooftop array cleaning pass, shot from ground and roof level."),
    "VSLOT_T": vslot("Feed 06", "Treatment application",
                     pending="Anti-algae application on a shaded elevation."),
    "VSLOT_C": vslot("Feed 07", "Condition capture &mdash; defect close-up",
                     pending="Close-range facade capture, with a defect find shown at full resolution."),
    "VSLOT_W": vslot("Feed 08", "Base station &mdash; RO+DI plant", ratio="portrait",
                     pending="Water plant walkthrough with the TDS meter reading shown on camera."),

    # ---- compliance
    "SECHEAD_CR": sec_head("01", "Credentials", "Every licence, with an honest status against it.",
                           "Scroll the set. Each card names the issuing body, what the credential actually permits, and whether we hold it today."),
    "SECHEAD_PK": sec_head("02", "Document pack", "Downloadable, and not behind a form.",
                           "You should not have to give a specialist contractor your contact details to find out whether they are insured."),
    "SECHEAD_PD": sec_head("03", "Privacy", "A camera near a bedroom window is a PDPA problem.",
                           "Under the PDPA, imagery that captures identifiable people is personal data &mdash; and facade cameras capture interiors whether or not that is the intention."),
    "SECHEAD_FQ": sec_head("04", "Objections", "The awkward questions, answered."),
    "CHECKS_PK": checks([
        "<b>Site-specific risk assessment</b> written for your building, not a generic template with your name pasted in.",
        "<b>Safe work procedure and method statement</b> covering the substrates and access constraints we found at survey.",
        "<b>Exclusion zone plan</b> marked on your own site plan, with vehicle and pedestrian impact shown.",
        "<b>CAAS permit reference</b> for your site, dates and altitude, before we mobilise.",
        "<b>Resident or tenant notice</b> drafted for your letterhead.",
    ]),
    "CHECKS_PD": checks([
        "<b>Written notice before works</b>, posted at lift lobbies and issued to your managing agent for circulation, stating purpose, dates and working window.",
        "<b>Cameras face the building.</b> Angles are set to the facade, and the flight path holds the aircraft off the glass rather than against it.",
        "<b>Footage is used for facade condition and cleaning verification only.</b> Not redistributed, not reproduced, not used in marketing without your written consent.",
        "<b>Defined retention period</b>, agreed with you before we fly, after which the imagery is deleted.",
        "<b>Residents asked to close windows and blinds</b> during the pass over their elevation &mdash; the same precaution used on HDB's own facade drone work.",
        "<b>A named contact for objections</b> on the notice, so a resident can call somebody rather than corner your MA at the letterboxes.",
    ]),
    "ACC": acc([
        ("Do we need to apply for anything?",
         "<p>No. The CAAS activity permit is our application, filed against your site, dates and altitude. What we need from you is access to the ground positions, confirmation of the working window, and your help getting the resident notice circulated.</p><p>Allow two to four weeks for the permit. If you have a hard deadline, engage six to eight weeks out.</p>"),
        ("How high can you actually work?",
         "<p>The default ceiling for flight without an activity permit is 60 metres above mean sea level, which most Singapore high-rises exceed. Working above it requires a Class 1 activity permit supported by a safety case showing the aircraft stays within the building's own airspace rather than straying into open sky.</p><p>Sites within 5 kilometres of Changi, Seletar or a military airbase need clearance regardless of height, and some locations will not get it. We check the airspace at survey and tell you before you plan around us.</p>"),
        ("What happens if water gets into a unit?",
         "<p>Flow is controlled and directed downward rather than driven into panel joints, and we ask that windows are closed during the pass. If ingress happens anyway, it is covered by our public liability policy, and the completion record documents which elevation was worked on which day so the claim is not a guessing exercise.</p><p>Ask any contractor for the sum insured, not just confirmation that insurance exists.</p>"),
        ("What about noise and working hours?",
         "<p>A cleaning drone is audible and there is no point pretending otherwise. Works run in an agreed daytime window and the notice tells residents which days affect their elevation. Commercial buildings can often take an out-of-hours window instead, which removes the problem entirely.</p>"),
        ("What can drones not clean?",
         "<p>Deep reveals and recessed windows the aircraft cannot get a working angle on. Enclosed light wells with no safe line of sight. Heavy organic or cementitious build-up that needs mechanical contact. Anything already loose &mdash; that gets logged, not washed.</p><p>These get identified at survey and priced as rope access alongside the drone scope, in the open, in the same quotation.</p>"),
        ("How do we verify your licences?",
         "<p>NEA publishes a list of licensed cleaning businesses, and you can check any contractor against it, including us. CAAS credentials we will provide as certificate copies on request. bizSAFE status is on the WSH Council register.</p><p>This is worth doing for every quote you receive, not only ours: engaging an unlicensed cleaning business is an offence for the buyer, with a fine of up to S$10,000.</p>"),
    ]),

    # ---- projects / case study
    "SECHEAD_SCH": sec_head("01", "The schema", "Fifteen fields, published every time.",
                            "Locked before we won any work, so we cannot quietly drop the ones that turn out to be unflattering."),
    "SECHEAD_IDX": sec_head("02", "Project index", "Completed work."),
    "SECHEAD_R": sec_head("01", "Record", "Project data."),
    "SECHEAD_M": sec_head("02", "Footage", "What the job looked like."),
    "SECHEAD_D": sec_head("03", "Defect find", "What the wash turned up.", solo=True),
    "SECHEAD_Q": sec_head("04", "Reference", "In the client's words.", solo=True),
    "VSLOT_1": vslot("Feed A", "Elevation pass", pending="Job footage goes here."),
    "VSLOT_2": (vslot("Feed B", "Ground operations", pending="Base station and exclusion zone.") +
                vslot("Feed C", "Handover walkthrough", mode="film", pending="Client walkthrough at completion.")),

    # ---- about / careers
    "SECHEAD_A": sec_head("01", "Position", "Three things we organised the company around."),
    "SECHEAD_B": sec_head("02", "Straight answers", "What being early means for you."),
    "SECHEAD_C2": sec_head("03", "The crew", "Who turns up at your building."),
    "CHECKS_B": checks([
        "<b>We have fewer completed projects than the incumbents.</b> That is a real thing to weigh, and it is why the survey is free and the first-project pricing is what it is.",
        "<b>Our credential status is published, card by card.</b> Held means held. In progress means in progress. You will not find out at contract stage that a certificate was aspirational.",
        "<b>We will tell you when we are the wrong answer.</b> Buildings with a working BMU and simple elevations are often better served by what you already have, and saying so costs us less than a bad first job.",
        "<b>The documentation is ahead of the fleet.</b> Method statements, risk assessments, privacy policy and reporting schema were built before the first customer, because that is the part contractors usually bolt on afterwards.",
    ]),
    "SECHEAD_J": sec_head("01", "Open roles", "Four roles, all Singapore-based."),
    "SECHEAD_W2": sec_head("02", "Why here", "What you get out of it."),
}

CTA_DEFAULT = cta("Send us a building and we will tell you what it takes.",
                  "The survey is free. You get the access approach, what we can and cannot reach, the permit timeline and a price &mdash; within 48 hours of the walk.")


# ================================================================= WRITE
def render(body):
    out = body
    for key in sorted(TOKENS, key=len, reverse=True):
        out = re.sub(r'\b' + re.escape(key) + r'\b', lambda m, v=TOKENS[key]: v, out)
    out = re.sub(r'\bCTA\b', lambda m: CTA_DEFAULT, out)
    return out


CTA_ALT = cta("Send us a building and we will tell you what it takes.",
              "The survey is free. You get the access approach, what we can and cannot reach, the permit timeline and a price &mdash; within 48 hours of the walk.",
              secondary=("projects.html", "See how we report a job"))


def main():
    written = []
    for fname, page in PAGES.items():
        body = render(page["body"])
        if fname == "compliance.html":
            body = body.replace(CTA_DEFAULT, CTA_ALT)
        html = shell(fname, page["nav"], page["title"], page["desc"], body)
        with open(os.path.join(OUT, fname), "w", encoding="utf-8") as fh:
            fh.write(html)
        written.append((fname, len(html)))
    for f, n in sorted(written):
        print("  %-26s %6d bytes" % (f, n))
    print("\n%d pages written to %s" % (len(written), OUT))


if __name__ == "__main__":
    main()
