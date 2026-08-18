#!/usr/bin/env python3
"""Generates the documents/ reader pages — one per captured markdown document.

Run from anywhere: python3 admin/build/gen_documents.py
Each page carries the common apparatus (metadata, summary, key concepts, key
ideas, infographic slot) and then renders the raw markdown in-page via
assets/mdreader.js. The raw file under briefs/ stays the source of truth —
the page is presentation, which is the raw-plus-curated discipline the
shared-drives brief argues for. Adding a document = adding a dict here.
"""
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "documents"
SITE_VERSION = (ROOT / "admin/build/version.txt").read_text().strip()

DOCS = [
 dict(slug="nhi-site-brief",
  title="nhi.sgit.ai: The Question Splits Into Two Populations",
  md="v0.33.59__strategy-brief__nhi-site-two-populations-industry-answers-only-agents-you-run.md",
  version="v0.33.59", date="16 August 2026", dtype="Strategy brief",
  summary="The brief that scoped this site. The question “how do I give an identity to my agents?” splits into agents you run and agents you rent; the industry's mature answer (attested, short-lived identities from an open standard) serves only the first population, while every agent practitioners actually name belongs to the second — where the honest current practice is to hand over a broad credential and hope. The brief turns that asymmetry into the site's thesis, scopes the research as one concrete scenario per option rather than a vendor list, and sets the participant discipline: method before findings, everything dated, our own gaps published.",
  concepts=[
   ("The two populations", "../thesis/index.html", "agents you run vs. agents you rent — different answers, only one served"),
   ("Hand over a credential and hope", "../hope/index.html", "the honest description of current practice, taken seriously as a named posture"),
   ("The reproducible-test discipline", "../method/index.html", "one scenario, same columns, privileges granted as the differentiating column, dated"),
   ("The participant problem", "../about/participant.html", "who writes this, method before findings, where our approach loses"),
  ],
  ideas=[
   "A collection without a position is an archive — the thesis belongs on the front page.",
   "Vendor lists are worthless and date in weeks; scenarios are comparable, checkable and re-runnable.",
   "Five concerns get bundled as “identity” (authentication, authorisation, secret storage, audit, lifecycle) and the research should scope to three.",
   "The measure of success: somebody with four agents and four vaults can read the site and know what to do next — including when the answer is that nothing available does what they want.",
  ],
  pages="Became this site: the thesis, method, options, collection, and comms structure all follow this brief's build order."),
 dict(slug="shared-drives",
  title="Shared Drives For Agents: Everything Available Runs On Your Identity",
  md="v0.33.59__research-brief__shared-drives-for-agents-identity-segregation-no-per-agent-keys.md",
  version="v0.33.59", date="16 August 2026", dtype="Research brief",
  summary="A survey of ways to give two agent sessions a shared file area — and three findings that matter more than the option list. Every available option runs on your identity, so a rogue session reaches everything every other session can reach and nothing can be attributed to an agent; the only real granularity is segregation (a dedicated drive per agent), not scoping; and nothing surveyed supports per-agent public and private keys. Three requirement rows come back empty across the entire market, which is the finding rather than an omission — and the first concrete, evidenced instance of the site's thesis.",
  concepts=[
   ("Granularity by segregation", "../hope/index.html#segregation", "when possession of access is binary, granularity comes from the shape of what you store"),
   ("Everything acts as you", "../research/shared-drives.html#identity", "connector authorisation is per identity; every session is indistinguishable from you"),
   ("Attribution from content, not platform", "../hope/index.html#segregation", "own paths and signed writes — a design decision, not a feature to wait for"),
   ("Curation destroys provenance", "../research/shared-drives.html#memory", "memory platforms resolve conflicting facts on write, which erases who said what, when"),
  ],
  ideas=[
   "The ecosystem's dominant advice is the opposite of the question: isolate parallel sessions, don't share.",
   "The scope paradox: the safe scope can't read your existing files; the useful scope reads everything and can't be narrowed.",
   "No option offers micropayments or per-call billing, so per-agent economics are not currently purchasable.",
   "The empty rows are standing refutation targets — anybody who fills one improves the research.",
  ],
  pages="Presented as a research page at ../research/shared-drives.html; its findings propagate through the thesis, Hope, method and options pages."),
 dict(slug="pki-registry",
  title="pki.sgit.ai: The Public Key Registry Has A Documented Failure To Learn From",
  md="v0.33.59__strategy-brief__pki-sgit-keyserver-failure-append-only-ownership-rule.md",
  version="v0.33.59", date="16 August 2026", dtype="Strategy brief",
  summary="Scopes pki.sgit.ai — a site and a registry of agent keys — from one historical lesson: the global keyserver network was destroyed in 2019 by a certificate-flooding attack its own maintainer called unsalvageable, and the cause was a stated design goal (never delete), not a bug. The brief turns the three abused properties into registry rules, resolves the tension with the corpus's own append-only pattern precisely (append-only is safe when the writer owns what it writes), makes revocation a signed append rather than a deletion, and separates identity from mandate as independently revocable signed statements. Private registry before public: testable versus commitment.",
  concepts=[
   ("The 2019 keyserver failure", "../pki/keyserver-failure.html", "~150,000 garbage signatures on one key; unrepairable by design"),
   ("The ownership rule", "../pki/keyserver-failure.html#append-only", "append-only is a guarantee when writers own their records, an attack surface when anyone appends to another's"),
   ("The four registry rules", "../pki/registry-rules.html", "owner-only writes, revocation as signed append, size bounds, every entry signed"),
   ("Identity vs. mandate", "../pki/registry-rules.html#mandate", "who the key belongs to vs. what the agent may do — separately revocable"),
  ],
  ideas=[
   "Third-party attestations are what made the old system valuable and what made it attackable — the central design choice, to be made deliberately.",
   "Vaults supply distribution, safe mirroring and versioning; the ownership rule, size bound and signature checking are the registry logic still to build.",
   "Fractal trust structures require declared roots, or the graph is unevaluable.",
   "Lead with the failure page — the most linkable thing the site will have, and proof the design knew the history.",
  ],
  pages="Became the PKI section: the hub, the keyserver-failure page, and the registry-rules page."),
]

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title} · documents · nhi.sgit.ai</title>
<meta name="description" content="Original document, readable in-page: summary, key concepts and key ideas, then the full markdown. {dtype}, {version}, {date}. CC BY 4.0.">
<link rel="canonical" href="https://nhi.sgit.ai/documents/{slug}.html">
<link rel="stylesheet" href="../assets/site.css">
</head>
<body>

<nav class="site"><div class="row">
  <a class="brand" href="../index.html">nhi<span>.sgit.ai</span></a>
  <span class="stage-pill">mvp draft</span>
  <a class="ver" href="../admin/versions.html" title="Site release history">{ver}</a>
  <a class="nl" href="../thesis/index.html">Thesis</a>
  <a class="nl" href="../hope/index.html">Hope</a>
  <a class="nl" href="../method/index.html">Method</a>
  <a class="nl" href="../options/index.html">Options</a>
  <a class="nl" href="../industry/index.html">Industry</a>
  <a class="nl" href="../collection/index.html">Collection</a>
  <a class="nl" href="../frameworks/aomm.html">AOMM</a>
  <a class="nl" href="../pki/index.html">PKI</a>
  <a class="nl here" href="index.html">Docs</a>
  <a class="nl" href="../infographics/index.html">Infographics</a>
  <a class="nl" href="../admin/comms.html">Comms</a>
  <a class="gh" href="https://github.com/SGit-AI/SGit-AI__Website__NHI">★ GitHub</a>
</div></nav>

<main class="doc">
<div class="crumb"><a href="../index.html">nhi.sgit.ai</a> / <a href="index.html">documents</a> / {slug}</div>
<h1>{title}</h1>

<div class="docmeta">
  <span class="k">Type</span><span class="v">{dtype}</span>
  <span class="k">Version</span><span class="v">{version}</span>
  <span class="k">Date</span><span class="v">{date}</span>
  <span class="k">Author</span><span class="v">Dinis Cruz (project lead) and collaborators</span>
  <span class="k">Licence</span><span class="v">CC BY 4.0</span>
  <span class="k">Source</span><span class="v"><a href="../briefs/{md}">raw markdown</a> · <a href="https://github.com/SGit-AI/SGit-AI__Website__NHI/blob/dev/briefs/{md}">view on GitHub</a></span>
</div>

<h2 id="summary">Summary</h2>
<p>{summary}</p>

<h2 id="concepts">Key concepts</h2>
<ul>
{concepts}
</ul>

<h2 id="ideas">Key ideas</h2>
<ul>
{ideas}
</ul>

<h2 id="on-site">On this site</h2>
<p>{pages}</p>

<h2 id="infographic">Infographic</h2>
<div class="warnbox"><b>Slot reserved.</b> The matching LinkedIn infographic has not yet been linked — the request list is on the <a href="../infographics/index.html">infographics page</a> (N1 on <a href="../admin/comms.html">comms</a>). Once identified it will appear here, pointing back to this document.</div>

<h2 id="read">Read the document</h2>
<div class="mdread-label">📄 Original document · {version} · {date} · rendered from the <a href="../briefs/{md}">raw markdown</a> (the source of truth)</div>
<div class="mdread" id="mdread" data-src="../briefs/{md}"><noscript><p class="dim">In-page rendering needs JavaScript — <a href="../briefs/{md}">open the raw markdown</a>.</p></noscript></div>

<div class="pagenav">
  <a href="index.html">← All documents</a>
  <a href="../briefs/{md}">Raw markdown →</a>
</div>
</main>

<footer class="site"><div class="cols">
  <div>
    <div class="brandline">nhi<span>.sgit.ai</span></div>
    <p>Non-human identity, blast radius and agentic security — anchored by the two-populations thesis. All content CC BY 4.0.</p>
    <p class="partnote">⚠ Participant disclosure: published by the sgit project. <a href="../about/participant.html" style="display:inline;padding:0">Read the disclosure</a>.</p>
    <p class="verline">site <a href="../admin/versions.html">{ver}</a> · <a href="../admin/index.html">engineering</a></p>
  </div>
  <div>
    <h4>The research</h4>
    <a href="../thesis/index.html">The thesis</a>
    <a href="../method/index.html">Method</a>
    <a href="../options/index.html">Options</a>
    <a href="../industry/index.html">Industry</a>
  </div>
  <div>
    <h4>The collection</h4>
    <a href="../collection/index.html">By question</a>
    <a href="../frameworks/aomm.html">The AOMM</a>
    <a href="../hope/index.html">Hope</a>
    <a href="index.html">Documents</a>
  </div>
  <div>
    <h4>Site</h4>
    <a href="../admin/comms.html">Comms</a>
    <a href="../admin/versions.html">Versions</a>
    <a href="../llms.txt">llms.txt</a>
    <a href="https://sgit.ai">sgit.ai</a>
  </div>
</div></footer>

<script src="https://cdn.jsdelivr.net/npm/marked@12/marked.min.js"></script>
<script src="../assets/mdreader.js"></script>
</body>
</html>
"""

def concepts_li(items):
    return "\n".join(
        f'  <li><a href="{u}"><b>{html.escape(t)}</b></a> — {d}</li>' for t, u, d in items)

def ideas_li(items):
    return "\n".join(f"  <li>{i}</li>" for i in items)

OUT.mkdir(exist_ok=True)
for d in DOCS:
    md_file = ROOT / "briefs" / d["md"]
    assert md_file.exists(), f"missing source markdown: {md_file}"
    page = PAGE.format(ver=SITE_VERSION, slug=d["slug"], title=html.escape(d["title"]),
        md=d["md"], version=d["version"], date=d["date"], dtype=d["dtype"],
        summary=d["summary"], concepts=concepts_li(d["concepts"]),
        ideas=ideas_li(d["ideas"]), pages=d["pages"])
    (OUT / f"{d['slug']}.html").write_text(page)
    print(f"wrote documents/{d['slug']}.html")
print(f"{len(DOCS)} document pages at {SITE_VERSION}")
