"""
Build a 6-page A4 marketing teaser PDF for "The Agentic Organisation".

Purpose: entice readers to buy the full book.
Design: book cover on page 1, curated prose + framework visuals on pages 2-5,
        a clean TOC overview, and a final "get the book" page with Amazon QR.

Output: output/teaser/the-agentic-organisation-teaser.pdf

Run from the repo root:
    .venv\\Scripts\\python scripts/build_teaser_pdf.py
or:
    npm run teaser

This script is intentionally one self-contained file (HTML + CSS + Python) so
it is easy to tweak copy, colours, or layout without touching the main book
build pipeline in skills/format-book-agent/.
"""

from __future__ import annotations

# --- Standard library imports ---------------------------------------------------
# We keep dependencies minimal: only weasyprint (already a book build dep) and
# the qrcode package for the Amazon buy-link QR image.
import os
import sys
from pathlib import Path

# --- Windows: make sure WeasyPrint can find Pango/GTK DLLs ---------------------
# On Windows WeasyPrint needs the Pango / GTK shared libraries.  The main book
# build script (skills/format-book-agent/scripts/build_print_pdf.py) uses the
# same trick: add the MSYS2 / GTK3 runtime directories to the DLL search path
# BEFORE importing weasyprint, so ctypes can load libpango, libcairo, etc.
if sys.platform == "win32":
    _default_dll = (
        "C:\\Program Files (x86)\\MSYS2\\mingw64\\bin;"
        "C:\\Program Files\\GTK3-Runtime Win64\\bin"
    )
    _dll_dirs = os.getenv("WEASYPRINT_DLL_DIRECTORIES", _default_dll).split(";")
    for _d in _dll_dirs:
        _d = _d.strip()
        if _d and os.path.isdir(_d) and hasattr(os, "add_dll_directory"):
            # add_dll_directory is the modern, Python 3.8+ way to extend the
            # DLL search path for native libraries loaded via ctypes.
            os.add_dll_directory(_d)
            # Also prepend to PATH so any child processes inherit it.
            os.environ["PATH"] = _d + os.pathsep + os.environ.get("PATH", "")

# --- Third-party imports (after DLL path fix) ----------------------------------
# WeasyPrint is required for every build (HTML -> PDF with @page support).
from weasyprint import HTML, CSS

# qrcode is *optional*: we only need it when the Amazon QR PNG does not yet
# exist on disk. Most builds just reuse the committed PNG in output/teaser/,
# so importing qrcode lazily keeps the teaser buildable on any Python that
# has WeasyPrint -- even if qrcode is not installed there.
try:
    import qrcode as _qrcode_mod  # pylint: disable=unused-import
    _QRCODE_AVAILABLE = True
except ImportError:
    _QRCODE_AVAILABLE = False

# --- Project paths -------------------------------------------------------------
# Resolve once so the rest of the script stays readable and path-independent.
REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = REPO_ROOT / "output" / "teaser"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Final PDF + intermediate assets (QR code) both live under output/teaser/.
PDF_PATH = OUT_DIR / "the-agentic-organisation-teaser.pdf"
QR_PATH = OUT_DIR / "amazon-qr.png"

# Amazon purchase link: the QR code and CTA both point here.
AMAZON_URL = "https://www.amazon.nl/-/en/Stephan-Hartgers-Rus/dp/9083690202"

# Reused image assets (all committed to the repo).
COVER_IMG = (
    REPO_ROOT
    / "output"
    / "20260404 Published version 2"
    / "Covers"
    / "9789083690223-epub-cover.jpg"
)
# Note: the Ch05 framework diagram and the Europe Advantage triad were both
# removed from the teaser on request so the content focuses on prose. Only
# the Four Tiers diagram remains (on page 3).
TIERS_IMG = REPO_ROOT / "book" / "images" / "ch04-four-tiers.png"

# Xomnia logo (negative / white version). The author is CEO of Xomnia; the
# teaser ends with a short block inviting readers to work with Xomnia on
# their AI transformation. The white logo sits on the navy page 6 background.
XOMNIA_LOGO = REPO_ROOT / "input" / "xomnia-negative-white.png"


def ensure_qr_code() -> None:
    """Make sure an Amazon QR PNG exists at QR_PATH.

    Behaviour:
    - If the PNG already exists, do nothing. This is the normal path and lets
      the teaser rebuild on any Python that has WeasyPrint, even without the
      qrcode library installed.
    - If the PNG is missing AND qrcode is importable, generate it fresh.
    - If the PNG is missing AND qrcode is not available, raise a clear error
      telling the user exactly how to unblock (one-line pip install).

    Note: if you ever change AMAZON_URL, delete output/teaser/amazon-qr.png so
    it gets regenerated on the next build.
    """
    # Fast path: the PNG is already there, nothing to do.
    if QR_PATH.exists():
        return

    # PNG missing -- we need qrcode to create it.
    if not _QRCODE_AVAILABLE:
        raise SystemExit(
            f"QR code file not found at {QR_PATH}.\n"
            "The 'qrcode' Python package is needed to generate it, but is not\n"
            "installed on this Python interpreter.\n\n"
            "Fix: install it into whichever Python you are running, for example:\n"
            "  python -m pip install 'qrcode[pil]'\n"
            "Or run the build via the project's virtualenv:\n"
            "  .venv\\Scripts\\python scripts\\build_teaser_pdf.py"
        )

    # Generate a crisp QR with high error-correction so it still scans after
    # being printed on textured paper or lightly scuffed. Colour matches the
    # body text (near-black) so it prints cleanly in B&W as well as colour.
    import qrcode  # safe: we just checked _QRCODE_AVAILABLE
    qr = qrcode.QRCode(
        version=None,  # auto-size to fit the URL
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # ~30% redundancy
        box_size=10,
        border=2,
    )
    qr.add_data(AMAZON_URL)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#1A1A1A", back_color="#FFFFFF")
    img.save(QR_PATH)


def file_url(path: Path) -> str:
    """Turn a local filesystem path into a file:// URL WeasyPrint can load.

    WeasyPrint accepts relative paths if you give it a base_url, but using
    absolute file URLs here keeps the HTML portable during debugging.
    """
    return path.resolve().as_uri()


# --- HTML template -------------------------------------------------------------
# The whole teaser is one HTML document with six <section class="page"> blocks.
# Each page forces a page break so WeasyPrint renders exactly 6 pages, no more,
# no less. Copy is curated (not raw chapter text) so readers get the core
# mental model in a few minutes and are motivated to buy the full book.
HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>The Agentic Organisation — A First Look</title>
</head>
<body>

<!-- ========================= PAGE 1: Cover / hook ========================= -->
<section class="page page-cover">
    <div class="cover-top">
        <span class="eyebrow">A FIRST LOOK</span>
    </div>

    <div class="cover-grid">
        <!-- Left: the actual book cover image so readers recognise it instantly -->
        <div class="cover-image-wrap">
            <img src="{cover}" alt="Book cover of The Agentic Organisation" />
        </div>

        <!-- Right: title lock-up and the opening hook quote -->
        <div class="cover-copy">
            <h1 class="cover-title">The Agentic<br>Organisation</h1>
            <p class="cover-subtitle">A complete guide for AI transformations</p>
            <p class="cover-edition">European edition</p>
            <div class="cover-rule"></div>
            <p class="cover-author">Stephan Hartgers-Rus</p>

            <blockquote class="cover-hook">
                &ldquo;The question most boardrooms are asking is the wrong one.&rdquo;
            </blockquote>
        </div>
    </div>

    <!-- Pre-order banner: announces launch date and availability. Sits just
         above the cover footer so it catches the eye without fighting the
         hook quote for attention. -->
    <div class="preorder-banner">
        <strong>Pre-order now</strong>
        <span>Publishing 1 May 2026</span>
        <span>All major bookstores</span>
    </div>

    <div class="cover-footer">
        <span>Agentic Press</span>
        <span>6&#8209;page preview</span>
    </div>
</section>

<!-- ========================= PAGE 2: Why this book ======================== -->
<section class="page page-content">
    <p class="eyebrow">WHY THIS BOOK</p>
    <h2 class="page-title">The right question is harder</h2>

    <div class="two-col">
        <div class="col-main">
            <p class="lead">
                &ldquo;How do we adopt AI?&rdquo; sounds strategic. It leads to pilots,
                proofs of concept, and a lot of activity. It also leads, in the vast
                majority of organisations, to no sustained impact.
            </p>
            <p>
                The harder question belongs in the room where strategy, governance,
                and culture are decided: <em>how do we lead an organisation that can
                absorb and act on AI?</em> This is the largest paradigm shift since
                the industrial revolution. Treating it as another software rollout
                is the single most expensive mistake a leadership team can make.
            </p>
            <p>
                European CEOs are not underprepared because they lack ambition or
                intelligence. They are underprepared because the mental model most
                of them are applying, incremental and project-based, is
                structurally incapable of capturing what this moment demands.
            </p>
            <p>
                This book gives the mental model and the sequence. It is written
                from and for Europe deliberately: the EU AI Act, GDPR-era data
                discipline, and European labour dialogue are a different playing
                field with distinct advantages, not constraints to work around.
            </p>
        </div>

        <!-- Right-hand column: stats that make the urgency concrete. -->
        <aside class="col-side">
            <div class="stat">
                <span class="stat-number">95%</span>
                <span class="stat-label">of enterprise generative AI
                    implementations fail to deliver sustained, measurable
                    impact.<br><small>MIT NANDA, 2025</small></span>
            </div>
            <div class="stat">
                <span class="stat-number">3.6&times;</span>
                <span class="stat-label">three-year total shareholder return at
                    the top 5% of AI leaders vs. their peers.</span>
            </div>
            <div class="stat">
                <span class="stat-number">4 months</span>
                <span class="stat-label">the doubling time of AI task-completion
                    capability since 2024.</span>
            </div>
            <div class="stat">
                <span class="stat-number">2026</span>
                <span class="stat-label">ING signals an &ldquo;agentic enterprise&rdquo;
                    shift to investors at the Morgan Stanley European
                    Financials Conference in London.</span>
            </div>
        </aside>
    </div>
</section>

<!-- ========================= PAGE 3: The core idea ======================== -->
<section class="page page-content">
    <p class="eyebrow">THE CORE IDEA</p>
    <h2 class="page-title">What is the Agentic Organisation?</h2>

    <!-- Definition copied verbatim from the book (Chapter 1) so the teaser
         and the book stay perfectly consistent. -->
    <div class="definition">
        <p class="def-label">Definition &middot; The Agentic Organisation</p>
        <p>
            The Agentic Organisation is a company redesigned so that humans
            and AI agents work together as a unified system.
        </p>
    </div>

    <p>
        Getting there is not a technology project. It is a leadership project
        with a clear sequence: understand the shift, own the leadership
        requirement, learn what the destination looks like, then build it in
        stages with the right foundations and the right measures.
    </p>
    <p>
        The work compounds (or fails to) across four tiers. An
        agentic <em>employee</em> is more productive than a non-agentic one.
        An agentic <em>team</em> produces outcomes neither humans nor AI alone
        could. An agentic <em>department</em> rewires its operating model.
        An agentic <em>organisation</em> redesigns strategy, structure, and
        governance around that model. Each tier requires different things
        from leadership; skip one and the next will not hold.
    </p>

    <figure class="tiers-figure">
        <img src="{tiers}" alt="Four tiers: individual, team, department, organisation" />
        <figcaption>
            Transformation compounds across four tiers. Leaders who only act at
            the individual or team level capture a fraction of the value.
        </figcaption>
    </figure>
</section>

<!-- ========================= PAGE 4: One tier brought to life ============ -->
<!-- Page 4 uses the same page-content class as pages 2 and 3 so the font
     sizes and overall "look" match exactly. Instead of explaining the whole
     framework (which would duplicate the book), it zooms in on ONE tier --
     Tier 3, the department level -- and brings it to life with a concrete
     European proof point. The page closes on a cliffhanger that points at
     Tier 4 without resolving it, echoing the back-matter pitch. Every
     statistic and quote here is drawn verbatim from Chapter 4 so the teaser
     stays perfectly consistent with the book. -->
<section class="page page-content">
    <p class="eyebrow">A CLOSER LOOK</p>
    <h2 class="page-title">Most AI programmes are<br>not transformations.</h2>

    <p class="lead">
        They are productivity theatre. Real transformation demands that
        capability compound: from individual to team, from team to
        department, from department to the whole organisation. The graveyard
        is specific: for every <strong>33 proofs of concept</strong> that
        enter production pipelines, only <strong>four</strong> emerge.
    </p>

    <p>
        The leap that kills the most initiatives is the one from team to
        department: from Tier 2 to Tier 3, where a function is meant
        to start running on agentic workflows. Most departments do the
        opposite: they add AI on top of existing processes, existing org
        charts, existing decision-making structures, and ask it to make
        things faster. That produces a faster version of the same thing.
        It does not produce transformation.
    </p>

    <p>
        Done properly, a departmental redesign looks different. Consider a
        finance function at Tier 3. Agent 1 extracts invoice data. Agent 2
        pulls the relevant contract. Agent 3 flags discrepancies. Agent 4
        drafts the resolution email. A human intervenes only at the decision
        point. A team of two to five people supervises an &ldquo;agent
        factory&rdquo; of 50 to 100 specialised agents running an entire
        process. Cycle times fall by up to <strong>80%</strong>. Audit trails
        improve.
    </p>

    <p>
        That is not a thought experiment. At Airbus, <strong>10,000
        engineers</strong> trained on AI coding tools achieved a
        <strong>40%</strong> improvement in simulation cycle times. Across
        European organisations more broadly, 56% increased profits or reduced
        costs through AI, with an average financial impact of over six
        million euros per firm.
    </p>

    <!-- Mid-page transition into the cliffhanger. Italic + accent bar mark
         the shift from "here's the example" to "here's what you still
         don't know". -->
    <p class="cliff-lead">
        And yet even the best departmental redesign stalls short of the prize.
    </p>

    <p>
        Tier 4, cross-functional agentic workflows, where AI becomes
        the connective tissue between departments rather than a tool within
        them, is where real compounding happens. A demand surge in
        one region triggers, within seconds, reallocated advertising spend,
        adjusted pricing, rerouted stock, and refreshed creative across the
        whole organisation.
    </p>

    <p class="cliff-close">
        What unlocks that is not a better model. Not a bigger budget. Not a
        smarter data team. It is something most boards have never governed
        for &mdash; and it is why the rest of this book exists.
    </p>
</section>

<!-- ========================= PAGE 5: Inside the book ======================= -->
<section class="page page-content">
    <p class="eyebrow">INSIDE THE BOOK</p>
    <h2 class="page-title">Sixteen chapters. One leadership playbook.</h2>

    <div class="toc-grid">
        <!-- Left: full TOC grouped by Part. We prefix chapter numbers in the
             text instead of using <ol start="N"> because some PDF renderers
             (including WeasyPrint) reset the counter per list, which would
             wrongly number Part II as "1. What the Agentic Organisation"
             instead of "3. What the Agentic Organisation". -->
        <div class="toc-col">
            <div class="toc-part">
                <h3>Part I &middot; Building Momentum</h3>
                <ul class="toc-list">
                    <li><span class="toc-num">1</span> The Largest Shift Since the Industrial Revolution</li>
                    <li><span class="toc-num">2</span> When Sponsorship Is Not Enough</li>
                </ul>
            </div>
            <div class="toc-part">
                <h3>Part II &middot; The Model</h3>
                <ul class="toc-list">
                    <li><span class="toc-num">3</span> What the Agentic Organisation Looks Like</li>
                    <li><span class="toc-num">4</span> When Local Wins Don&rsquo;t Add Up</li>
                    <li><span class="toc-num">5</span> Every Transformation Needs a Map</li>
                    <li><span class="toc-num">6</span> The Vision Layer</li>
                    <li><span class="toc-num">7</span> The Product Layer</li>
                    <li><span class="toc-num">8</span> The Operational Layer</li>
                    <li><span class="toc-num">9</span> The Foundational Layer</li>
                    <li><span class="toc-num">10</span> The AI Decision Lens</li>
                </ul>
            </div>
            <div class="toc-part">
                <h3>Part III &middot; The European Advantage</h3>
                <ul class="toc-list">
                    <li><span class="toc-num">11</span> Europe&rsquo;s Distinctive Edge</li>
                    <li><span class="toc-num">12</span> The Decisions That Mattered</li>
                </ul>
            </div>
            <div class="toc-part">
                <h3>Part IV &middot; The CEO&rsquo;s Playbook</h3>
                <ul class="toc-list">
                    <li><span class="toc-num">13</span> Building Your Agentic Organisation</li>
                    <li><span class="toc-num">14</span> Readiness</li>
                    <li><span class="toc-num">15</span> Measuring What Matters</li>
                    <li><span class="toc-num">16</span> A Leadership Decision</li>
                </ul>
            </div>
        </div>

        <!-- Right: single teaser box spotlighting the case-study chapter. -->
        <aside class="toc-side">
            <div class="side-card">
                <h4>Nine decisions.<br>Six European companies.<br>One playbook.</h4>
                <p class="cases">
                    BBVA &middot; ING &middot; Siemens<br>
                    Allianz &middot; Klarna &middot; Schneider Electric
                </p>
                <p>
                    Chapter 12 distils nine transferable lessons from leaders
                    who decided under pressure.
                </p>
            </div>
        </aside>
    </div>
</section>

<!-- ========================= PAGE 6: Get the book ========================= -->
<section class="page page-close">
    <p class="eyebrow light">GET THE BOOK</p>
    <h2 class="close-headline">
        Three years from now,<br>two kinds of organisations will exist.
    </h2>
    <p class="close-sub">
        One will have built the Agentic Organisation. The other will still
        be piloting. This book is for leaders who have already decided which
        one they want to be.
    </p>

    <div class="close-grid">
        <!-- Left: book details (ISBNs, formats) -->
        <div class="close-details">
            <h3>The Agentic Organisation</h3>
            <p class="details-sub">
                A complete guide for AI transformations &mdash; European edition
            </p>
            <p class="details-author">by Stephan Hartgers-Rus</p>
            <ul class="isbn-list">
                <li><span>Hardback</span> 978&#8209;90&#8209;836902&#8209;0&#8209;9</li>
                <li><span>Paperback</span> 978&#8209;90&#8209;836902&#8209;1&#8209;6</li>
                <li><span>EPUB</span> 978&#8209;90&#8209;836902&#8209;2&#8209;3</li>
            </ul>
            <p class="author-bio">
                <strong>Stephan Hartgers-Rus</strong> is CEO of Xomnia and a former
                McKinsey strategy consultant with 25+ years helping organisations
                turn technology into value. He holds degrees in Econometrics and
                Computer Science and lives in The Hague.
            </p>

            <!-- Xomnia soft-promotion block. The author bio above already
                 names Xomnia, so this block explains what Xomnia does and
                 invites the reader to hire them. Copy mirrors Xomnia.com
                 (tagline "We make AI work." and the three service pillars:
                 strategy, data platforms, data & AI products). Kept compact
                 so it enhances rather than overshadows the book pitch. -->
            <div class="xomnia-block">
                <p class="xomnia-label">Work with Xomnia</p>
                <img src="{xomnia}" class="xomnia-logo" alt="Xomnia logo" />
                <p class="xomnia-tagline">We make AI work.</p>
                <p class="xomnia-copy">
                    The Amsterdam-based data and AI consultancy the author
                    leads. We partner with organisations across Europe to 
                    turn AI strategy into measurable, agentic impact.
                </p>
                <p class="xomnia-services">
                    Data &amp; AI strategy &middot; Cloud data platforms &middot; Agentic products
                </p>
                <p class="xomnia-url">xomnia.com</p>
            </div>
        </div>

        <!-- Right: the big CTA + QR code linking straight to Amazon. -->
        <div class="close-cta">
            <div class="qr-wrap">
                <img src="{qr}" alt="QR code to buy the book on Amazon" />
            </div>
            <p class="cta-line">Scan to buy on Amazon</p>
            <p class="cta-url">amazon.nl/dp/9083690202</p>
        </div>
    </div>

    <!-- Pre-order banner (dark variant): same copy as page 1 so the message
         is consistent across the opening and closing pages. -->
    <div class="preorder-banner dark">
        <strong>Pre-order now</strong>
        <span>Publishing 1 May 2026</span>
        <span>All major bookstores</span>
    </div>

    <div class="close-footer">
        Agentic Press &middot; 2026
    </div>
</section>

</body>
</html>
"""


# --- CSS -----------------------------------------------------------------------
# Big chunk of CSS that defines A4 page geometry, colour palette, typography,
# and per-page layouts. Kept in one place so it is easy to tweak.
CSS_STYLES = """
/* ---- Web fonts: Source Serif Pro (body) + Inter (display). Falls back to
       system serif / sans if offline so the build never breaks. -------- */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Source+Serif+Pro:ital,wght@0,400;0,600;0,700;1,400&display=swap');

/* ---- A4 page geometry. No default margins: each page draws its own
       padding so backgrounds can be full-bleed. ------------------------- */
@page {
    size: A4;
    margin: 0;
}

/* ---- Colour palette, mirrors the cover (warm orange + dark navy + cream). */
:root {
    --accent: #D8761B;        /* cover orange/gold */
    --accent-dark: #B55F13;   /* hover/deeper gold for lines */
    --ink: #1A1A1A;           /* body text */
    --ink-soft: #4A4A4A;      /* secondary text */
    --navy: #0F1B2D;          /* headings, deep accent */
    --cream: #FAF6EE;         /* subtle warm background */
    --rule: #E5DFD1;          /* divider lines */
}

html, body {
    margin: 0;
    padding: 0;
    font-family: 'Source Serif Pro', Georgia, 'Times New Roman', serif;
    font-size: 10.5pt;
    line-height: 1.55;
    color: var(--ink);
    background: white;
}

/* Every section = one physical page. force-break makes sure we hit exactly 6. */
.page {
    width: 210mm;
    height: 297mm;
    padding: 18mm 18mm 16mm 18mm;
    box-sizing: border-box;
    page-break-after: always;
    position: relative;
    overflow: hidden;
}
.page:last-of-type { page-break-after: auto; }

/* ---- Shared typography bits ---------------------------------------------- */
.eyebrow {
    font-family: 'Inter', Helvetica, Arial, sans-serif;
    font-size: 8.5pt;
    font-weight: 600;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--accent);
}
.eyebrow.light { color: var(--accent); }

.page-title {
    font-family: 'Source Serif Pro', Georgia, serif;
    font-weight: 700;
    font-size: 28pt;
    line-height: 1.15;
    color: var(--navy);
    margin: 6mm 0 6mm 0;
    max-width: 140mm;
}

.lead {
    font-size: 13pt;
    line-height: 1.5;
    color: var(--navy);
    margin-top: 0;
}

p { margin: 0 0 3.2mm 0; }

/* ============================= PAGE 1: COVER ============================= */
.page-cover {
    background: linear-gradient(180deg, #FAF6EE 0%, #F3ECDC 100%);
    padding: 14mm 16mm 12mm 16mm;
    display: flex;
    flex-direction: column;
}
.cover-top { margin-bottom: 4mm; }
.cover-grid {
    display: grid;
    grid-template-columns: 72mm 1fr;
    gap: 10mm;
    align-items: center;
    flex: 1;
}
.cover-image-wrap img {
    width: 100%;
    height: auto;
    /* Subtle shadow so the cover "lifts" off the cream background. */
    box-shadow: 0 6px 24px rgba(15, 27, 45, 0.22),
                0 2px 6px rgba(15, 27, 45, 0.12);
    border-radius: 1px;
}
.cover-copy { padding-left: 4mm; }
.cover-title {
    font-family: 'Source Serif Pro', Georgia, serif;
    font-weight: 700;
    font-size: 38pt;
    line-height: 1.02;
    color: var(--navy);
    margin: 0 0 4mm 0;
    letter-spacing: -0.01em;
}
.cover-subtitle {
    font-family: 'Inter', sans-serif;
    font-size: 13pt;
    color: var(--ink);
    margin: 0;
    font-weight: 500;
}
.cover-edition {
    font-family: 'Inter', sans-serif;
    font-size: 10.5pt;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--accent);
    margin: 3mm 0 4mm 0;
    font-weight: 600;
}
.cover-rule {
    width: 18mm;
    height: 2px;
    background: var(--accent);
    margin: 4mm 0;
}
.cover-author {
    font-family: 'Inter', sans-serif;
    font-size: 11pt;
    color: var(--navy);
    margin: 0 0 8mm 0;
    font-weight: 500;
}
.cover-hook {
    font-family: 'Source Serif Pro', Georgia, serif;
    font-style: italic;
    font-size: 16pt;
    line-height: 1.35;
    color: var(--navy);
    border-left: 2.5px solid var(--accent);
    padding: 0 0 0 6mm;
    margin: 2mm 0 0 0;
    max-width: 95mm;
}
.cover-footer {
    display: flex;
    justify-content: space-between;
    font-family: 'Inter', sans-serif;
    font-size: 8.5pt;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--ink-soft);
    margin-top: 4mm;
}

/* --- Pre-order banner --------------------------------------------------
   A horizontal strip used on pages 1 and 6 to announce the launch date
   and availability. Thin orange rules top and bottom give it visual
   weight without shouting. The dark variant (page 6) keeps the same
   orange rules but lets the navy page colour show through. */
.preorder-banner {
    display: flex;
    justify-content: center;
    align-items: baseline;
    gap: 6mm;
    padding: 3mm 4mm;
    margin-top: 5mm;
    font-family: 'Inter', sans-serif;
    font-size: 9pt;
    font-weight: 500;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--navy);
    border-top: 1.5px solid var(--accent);
    border-bottom: 1.5px solid var(--accent);
    text-align: center;
}
.preorder-banner strong {
    color: var(--accent);
    font-weight: 700;
    letter-spacing: 0.18em;
}
/* Dark variant used on the navy page 6: white text, same orange rules. */
.preorder-banner.dark {
    color: #FFFFFF;
    border-top-color: var(--accent);
    border-bottom-color: var(--accent);
}

/* ============================= PAGE 2/3/5 CONTENT ========================= */
.page-content { background: white; }

.two-col {
    display: grid;
    grid-template-columns: 1fr 58mm;
    gap: 10mm;
    margin-top: 2mm;
}
.col-main p { margin-bottom: 3.5mm; }

.col-side {
    background: var(--cream);
    border-left: 2.5px solid var(--accent);
    padding: 7mm 7mm 6mm 7mm;
}
.stat { margin-bottom: 6mm; }
.stat:last-child { margin-bottom: 0; }
.stat-number {
    display: block;
    font-family: 'Source Serif Pro', Georgia, serif;
    font-weight: 700;
    font-size: 26pt;
    line-height: 1;
    color: var(--navy);
    margin-bottom: 1mm;
}
.stat-label {
    display: block;
    font-family: 'Inter', sans-serif;
    font-size: 9pt;
    line-height: 1.4;
    color: var(--ink-soft);
}
.stat-label small { color: var(--ink-soft); font-size: 8pt; }

/* --- Definition callout (page 3) ---------------------------------------- */
.definition {
    background: var(--cream);
    border-left: 3px solid var(--accent);
    padding: 6mm 7mm;
    margin: 4mm 0 6mm 0;
}
.def-label {
    font-family: 'Inter', sans-serif;
    font-weight: 700;
    font-size: 8.5pt;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--accent);
    margin: 0 0 2mm 0;
}
.definition p:last-child { margin-bottom: 0; font-size: 11.5pt; line-height: 1.5; }

.tiers-figure {
    margin: 6mm 0 0 0;
    text-align: center;
}
.tiers-figure img {
    max-width: 140mm;
    width: 100%;
    height: auto;
}
.tiers-figure figcaption {
    font-family: 'Inter', sans-serif;
    font-size: 9pt;
    color: var(--ink-soft);
    margin-top: 3mm;
    max-width: 140mm;
    margin-left: auto;
    margin-right: auto;
}

/* --- Page 4 cliffhanger styles -----------------------------------------
   .cliff-lead: italic transition line with a thin accent bar on the left,
                marks the pivot from "example" to "what you still don't know".
   .cliff-close: closing paragraph, slightly larger and in navy so the reader
                 finishes the page on an emphatic (not decorative) note. */
.cliff-lead {
    font-family: 'Source Serif Pro', Georgia, serif;
    font-style: italic;
    font-size: 12pt;
    line-height: 1.5;
    color: var(--navy);
    border-left: 2.5px solid var(--accent);
    padding: 1mm 0 1mm 6mm;
    margin: 5mm 0 4mm 0;
    max-width: 150mm;
}
.cliff-close {
    font-size: 11.5pt;
    line-height: 1.55;
    color: var(--navy);
    font-weight: 600;
    margin-top: 3mm;
}

/* ============================= PAGE 5: TOC =============================== */
.toc-grid {
    display: grid;
    grid-template-columns: 1fr 66mm;
    gap: 8mm;
    margin-top: 2mm;
}
.toc-part { margin-bottom: 5mm; }
.toc-part h3 {
    font-family: 'Inter', sans-serif;
    font-size: 10pt;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--accent);
    margin: 0 0 2mm 0;
    padding-bottom: 1.5mm;
    border-bottom: 1px solid var(--rule);
}
/* Custom TOC list: no automatic numbering (see HTML comment). We draw the
   chapter number in a fixed-width coloured span so the titles line up cleanly
   regardless of whether the number is 1 digit or 2 digits. */
.toc-part ul.toc-list {
    list-style: none;
    margin: 0;
    padding: 0;
}
.toc-part ul.toc-list li {
    font-family: 'Source Serif Pro', Georgia, serif;
    font-size: 10.5pt;
    line-height: 1.4;
    color: var(--navy);
    margin-bottom: 1.2mm;
    display: flex;
    align-items: baseline;
}
.toc-num {
    display: inline-block;
    width: 7mm;
    flex: 0 0 7mm;
    color: var(--accent);
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    font-size: 10pt;
    text-align: right;
    padding-right: 3mm;
}

.toc-side { display: flex; flex-direction: column; gap: 5mm; }
.side-card {
    background: var(--cream);
    border-left: 2.5px solid var(--accent);
    padding: 5mm 5mm;
}
.side-card h4 {
    font-family: 'Source Serif Pro', Georgia, serif;
    font-weight: 700;
    font-size: 13pt;
    line-height: 1.2;
    color: var(--navy);
    margin: 0 0 3mm 0;
}
.side-card p {
    font-size: 9.5pt;
    line-height: 1.45;
    margin: 0 0 2mm 0;
    color: var(--ink);
}
.side-card .cases {
    font-family: 'Inter', sans-serif;
    font-size: 9pt;
    color: var(--ink-soft);
    letter-spacing: 0.02em;
    margin-bottom: 3mm;
}
/* ============================= PAGE 6: CLOSE / CTA ======================== */
/* Tightened padding and headline so the close-grid has enough room for
   both the book details + author bio block AND the Xomnia soft-promo
   block below it, without overflowing the pre-order banner. */
.page-close {
    background: var(--navy);
    color: #FFFFFF;
    padding: 14mm 18mm 12mm 18mm;
    display: flex;
    flex-direction: column;
}
.page-close .eyebrow { color: var(--accent); }
.close-headline {
    font-family: 'Source Serif Pro', Georgia, serif;
    font-weight: 700;
    font-size: 24pt;
    line-height: 1.18;
    color: #FFFFFF;
    margin: 2mm 0 4mm 0;
    max-width: 155mm;
}
.close-sub {
    font-size: 11pt;
    line-height: 1.5;
    color: #E8E2D3;
    max-width: 155mm;
    margin-bottom: 6mm;
}

.close-grid {
    display: grid;
    grid-template-columns: 1fr 72mm;
    gap: 10mm;
    flex: 1;
}
.close-details h3 {
    font-family: 'Source Serif Pro', Georgia, serif;
    font-size: 18pt;
    color: #FFFFFF;
    margin: 0 0 1.5mm 0;
}
.details-sub {
    font-family: 'Inter', sans-serif;
    font-size: 10.5pt;
    color: var(--accent);
    margin: 0 0 3mm 0;
    font-weight: 500;
}
.details-author {
    font-family: 'Inter', sans-serif;
    font-size: 10pt;
    color: #C9C2B2;
    margin: 0 0 6mm 0;
}
.isbn-list {
    list-style: none;
    padding: 0;
    margin: 0 0 7mm 0;
    border-top: 1px solid rgba(255,255,255,0.15);
}
.isbn-list li {
    font-family: 'Inter', sans-serif;
    font-size: 9.5pt;
    color: #E8E2D3;
    padding: 2mm 0;
    border-bottom: 1px solid rgba(255,255,255,0.15);
    display: flex;
    justify-content: space-between;
}
.isbn-list li span {
    color: var(--accent);
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    font-size: 8.5pt;
}
.author-bio {
    font-size: 9.5pt;
    line-height: 1.55;
    color: #D4CDBD;
    margin: 0;
    font-style: italic;
}

/* --- Xomnia block (page 6, left column, below author bio) ---------------
   Separated from the author bio by a thin orange rule so it reads as a
   distinct "and here's how to hire us" section. White logo on navy sits
   beautifully; body text uses the same muted cream as the author bio so
   the two blocks feel visually related. */
.xomnia-block {
    margin-top: 5mm;
    padding-top: 4mm;
    border-top: 1.5px solid rgba(216, 118, 27, 0.55);
}
.xomnia-label {
    font-family: 'Inter', sans-serif;
    font-size: 8.5pt;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--accent);
    margin: 0 0 2.5mm 0;
}
.xomnia-logo {
    height: 6mm;
    width: auto;
    display: block;
    margin: 0 0 3mm 0;
}
.xomnia-tagline {
    font-family: 'Source Serif Pro', Georgia, serif;
    font-size: 13pt;
    font-weight: 700;
    color: #FFFFFF;
    margin: 0 0 2.5mm 0;
    letter-spacing: -0.005em;
}
.xomnia-copy {
    font-size: 9pt;
    line-height: 1.45;
    color: #D4CDBD;
    margin: 0 0 2.5mm 0;
}
.xomnia-services {
    font-family: 'Inter', sans-serif;
    font-size: 8pt;
    font-weight: 500;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--accent);
    margin: 0 0 2mm 0;
}
.xomnia-url {
    font-family: 'Inter', sans-serif;
    font-size: 10pt;
    font-weight: 600;
    color: #FFFFFF;
    margin: 0;
    letter-spacing: 0.02em;
}

.close-cta {
    background: #FFFFFF;
    color: var(--navy);
    border-radius: 3px;
    padding: 8mm 6mm 7mm 6mm;
    text-align: center;
    align-self: flex-start;
}
.qr-wrap {
    background: #FFFFFF;
    padding: 0;
    display: flex;
    justify-content: center;
}
.qr-wrap img {
    width: 48mm;
    height: 48mm;
    display: block;
}
.cta-line {
    font-family: 'Inter', sans-serif;
    font-weight: 700;
    font-size: 12pt;
    color: var(--navy);
    margin: 5mm 0 1mm 0;
    letter-spacing: 0.02em;
}
.cta-url {
    font-family: 'Inter', sans-serif;
    font-size: 9pt;
    color: var(--accent-dark);
    margin: 0;
    word-break: break-all;
}

.close-footer {
    font-family: 'Inter', sans-serif;
    font-size: 8.5pt;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #9E9686;
    text-align: center;
    margin-top: 6mm;
}
"""


def main() -> None:
    """Generate the QR code, render the HTML, and write the final PDF."""
    # 1) Make sure the Amazon QR image exists. We reuse the committed PNG in
    #    output/teaser/ if present (so the build works without the qrcode lib)
    #    and only regenerate when it is missing.
    ensure_qr_code()

    # 2) Fill in the HTML template with absolute file:// URLs to all the image
    #    assets. WeasyPrint will follow those URLs when rendering the page.
    html_str = HTML_TEMPLATE.format(
        cover=file_url(COVER_IMG),
        tiers=file_url(TIERS_IMG),
        qr=file_url(QR_PATH),
        xomnia=file_url(XOMNIA_LOGO),
    )

    # 3) Render HTML + CSS to a single PDF. base_url=REPO_ROOT lets any
    #    relative paths in the HTML resolve against the repo root as well.
    HTML(string=html_str, base_url=str(REPO_ROOT)).write_pdf(
        target=str(PDF_PATH),
        stylesheets=[CSS(string=CSS_STYLES)],
    )

    # 4) Friendly confirmation for the terminal.
    size_kb = PDF_PATH.stat().st_size / 1024
    print(f"Teaser PDF written: {PDF_PATH} ({size_kb:,.0f} KB)")


if __name__ == "__main__":
    main()
