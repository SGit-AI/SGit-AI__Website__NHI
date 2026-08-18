#!/usr/bin/env python3
"""Generates the packs/ section: dev brief packs, presented like the documents.

Run from anywhere: python3 admin/build/gen_packs.py
Emits packs/index.html (section hub), packs/<pack>/index.html (pack hub with the
file table and a reader for the pack README), and packs/<pack>/<slug>.html per
document (summary, key concepts, key ideas, in-page markdown reader with mermaid
support). Raw sources live verbatim under packs/<pack>/src/ — the source of truth.
Adding a pack or a document = adding a dict here.
"""
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SITE_VERSION = (ROOT / "admin/build/version.txt").read_text().strip()

PACKS = [
 dict(slug="static-publishing",
  name="Static Publishing, `sgit vault serve`, and the Publishing Matrix",
  origin="Authored by an Architect-review agent in the SGit-AI__CLI repo (branch claude/sgit-architect-agent-review-3tl5ti), 17 August 2026. Status: build spec, ready to implement — six decisions await the maintainer; Phases 1 and 3 are unblocked.",
  readme="README.md",
  three_sentences="A vault publishes to a folder: encrypted objects plus a small, declared plaintext surface (loader, cover, manifest, and — only when the vault is deliberately public — the read key). That folder is readable by a browser through the loader and by <code>sgit clone</code> over ordinary GETs, from any HTTP host or a local folder, with no server and no auth. <code>sgit vault serve</code> exists because browsers give local files an opaque origin — the one case everybody tries first, double-clicking <code>index.html</code>, cannot work without it.",
  site_relevance="Two of this pack's measured findings connect straight to claims this site publishes: <b>custody without access requires a manifest</b> (every filename derives from the read key, so a keyless client cannot name a single file — sharpening the <a href='../../pki/registry-rules.html#vaults'>PKI section's custody row</a>), and <b>object ids hash ciphertext with random IVs, so a fork is unlinkable</b> — relevant to the <a href='../../collection/index.html#attribute'>attribution question</a>. The published-folder model is also the substrate the <a href='../../documents/serialised-pr.html'>serialised pull request</a> workflow rides on.",
  docs=[
   dict(slug="dev-brief", file="00__DEV-BRIEF.md",
    title="00 — The executable dev brief",
    role="The brief a developer agent runs from: grounding reads, the five rules, per-phase tasks, definition of done",
    summary="Written to be executed by a developer agent, not just read: the grounding reads in order, the five rules that override convenience, non-negotiable implementation constraints (fixed plaintext allow-list, fail-soft per object, unconditional hash verification, localhost-only serve, writes raise), a definition of done every phase must meet, and an explicit list of what is not the developer's to decide.",
    concepts=[
     ("The five rules", None, "byte-identical ciphertext everywhere; the key never reaches a server; keyless custody; byte-identical loader; plaintext only where the key is published"),
     ("The plaintext allow-list", "architecture.html", "fixed in code, never pattern-derived — otherwise anyone who can write to the vault can move a file into the plaintext surface by naming it"),
     ("Not yours to decide", "decisions-and-evidence.html", "wire formats, key formats, the six open decisions, the loader's JavaScript"),
    ],
    ideas=[
     "Phases are independently shippable: take one, finish it green, open a PR.",
     "If a change weakens one of the five rules, it is wrong even if the tests pass — stop and raise it.",
     "When the spike disagrees with the spec: the spec wins for behaviour, the spike wins for proof it is possible.",
    ]),
   dict(slug="architecture", file="01__architecture.md",
    title="01 — Architecture",
    role="The transport seam, publish-as-projection, the published layout, the manifest contract",
    summary="The whole feature hangs on one seam: every sgit action already accepts an injected api, so the static transport is a sibling class — read-only GET fan-out over any host or folder — with zero changes to any call site, proven by a running spike. Four methods carry the entire read path (including presigned_read_url, which is on the clone path for every blob over ~4 MB — a size-dependent bug waiting for anyone who skips it). Transport resolution is transparent but never silent: sniffed once, sticky, reported in vault info. Publish is a projection of the vault, not a copy, with a fixed plaintext surface recorded by hash in manifest.json.",
    concepts=[
     ("The transport seam", None, "a sibling Vault__API class injected at the CLI boundary — not a mode flag, not a new port"),
     ("Publish as projection", None, "byte-identical ciphertext regardless of destination; the folder is the vault, projected"),
     ("Visible ≠ silent", None, "auto-detection is fine only because the resolved transport is reported and forceable"),
     ("The manifest contract", "decisions-and-evidence.html", "the listing a keyless client needs, and the recorded plaintext surface with sha256 per file"),
    ],
    ideas=[
     "A 404 is an answer (None), not an error — fail-soft per object, never per run.",
     "Local fan-out gets one worker: parallelism on open() is pure overhead.",
     "Two on-host layouts are sniffed on first read, then sticky — the same URL works live and static.",
    ]),
   dict(slug="commands-and-ux", file="02__commands-and-ux.md",
    title="02 — Commands & UX",
    role="The command surface and every CLI / loader mockup — intended user-facing output, word for word",
    summary="Every block is the intended user-facing output, to be matched word for word — several strings are load-bearing because they are the only place a user learns why an irreversible thing is irreversible. The publish baseline is private-and-ciphertext-only; publishing the read key requires --visibility public and a stated-consequence confirmation: anyone with the URL can read every file, now and in every future publish, and copies cannot be recalled.",
    concepts=[
     ("Consequence stated, not implied", None, "the --visibility public confirmation is the disclosure moment, designed as such"),
     ("The safe default", None, "bare visibility: no key published, readers supply their own"),
    ],
    ideas=[
     "Load-bearing strings are part of the spec: change one, explain it in the PR.",
     "The next-steps block after publish teaches the two consumption paths (serve locally, clone from any GET host) at the moment they matter.",
    ]),
   dict(slug="flows", file="03__flows.md",
    title="03 — Flows",
    role="Sequence diagrams: publish → serve → read, the static clone, and the fork round trip",
    summary="The design as sequence diagrams (rendered below): the baseline publish → serve → browser read, where no server does any of the work; the static clone over plain GETs — verified end to end against a real GitHub Pages host; and the fork round trip. The diagrams are the review surface: each one is also a test cell.",
    concepts=[
     ("No server did any of the work", None, "the browser walks refs and trees itself, decrypting client-side — the loader is a static file"),
     ("Layout sniffed once, then sticky", "architecture.html", "the clone flow's first read resolves the on-host layout"),
    ],
    ideas=[
     "The static clone is not aspiration — it is verified against a live Pages host today.",
     "Every diagram maps to a numbered test cell in 04.",
    ]),
   dict(slug="invariants-and-tests", file="04__invariants-and-tests.md",
    title="04 — Invariants & tests",
    role="Five invariants asserted everywhere + fourteen test cells, collapsed from 240 combinations",
    summary="Five dimensions produce 240 combinations, which is not a test plan; separating what must always hold from what genuinely varies collapses it to 5 invariant assertions applied in every cell, plus 14 cells. The invariants are behavioural checks, not code inspection — I2 asserts that no recorded request contained the key, rather than asserting the code doesn't send it. Two cells were re-scoped by measurement, and one (clone with no key at all) is structurally impossible by design.",
    concepts=[
     ("Assert behaviour, not absence of code", None, "prove no request contained the key; don't restate the intent"),
     ("Structurally impossible ≠ untested", "decisions-and-evidence.html", "keyless clone can't name a file; the cell became mirror-with-manifest, with the no-manifest failure as part of the test"),
     ("Runtime-asserted platform facts", None, "cell 10 asserts the CORS header at run time, so a platform change fails the suite instead of quietly breaking the feature"),
    ],
    ideas=[
     "240 combinations → 5 assertions + 14 cells is the test-design move worth stealing.",
     "The fork round trip is the acceptance test.",
    ]),
   dict(slug="implementation-phases", file="05__implementation-phases.md",
    title="05 — Implementation phases",
    role="P1–P7 with file lists, acceptance criteria and risk; start with P1 + P3",
    summary="Seven independently shippable phases, each one PR with green suites and its own acceptance criteria. P1 (static read transport — promote the spike, don't redesign it) and P3 (vault serve) start now: demonstrable value with zero commitment to the publish protocol still being decided. Acceptance criteria are concrete down to the trap: add a >4 MB fixture, because small fixtures will not catch the large-blob path.",
    concepts=[
     ("Promote the spike", None, "the P1 design already exists as running code — productionising it is the task"),
     ("Ship value before protocol", "decisions-and-evidence.html", "P1+P3 first is itself one of the six decisions, with a recommendation"),
    ],
    ideas=[
     "Independently shippable phases keep every PR reviewable and every rollback cheap.",
     "Risk is stated per phase — the two mediums are where the publish protocol touches disk.",
    ]),
   dict(slug="decisions-and-evidence", file="06__decisions-and-evidence.md",
    title="06 — Decisions & evidence",
    role="Six open decisions for the maintainer, and the measured evidence that re-scoped the spec",
    summary="The maintainer's file: six decisions, each with a recommendation, none blocking P1/P3. And the evidence base that changed the spec: GitHub Pages sends access-control-allow-origin: * by default, so key-on-another-origin moved from 'probably unavailable' to 'supported, asserted at run time'; custody without access structurally requires a manifest, because every filename derives from the read key; and object ids are sha256(ciphertext) with random IVs, so two vaults holding the same document share zero object ids — a fork is unlinkable.",
    concepts=[
     ("Measurement over assumption", None, "two source-brief assumptions reversed by a curl and a spike, with reproduction steps"),
     ("The unlinkable fork", "../../collection/index.html#attribute", "ciphertext-hashed ids + random IVs: a private fork of a public template is undetectable — a finding with privacy and attribution edges both ways"),
     ("A visibility default that drifts is a disclosure", None, "decision 5's one-line rationale, worth keeping"),
    ],
    ideas=[
     "Every decision ships with a recommendation, so sign-off is a review, not a design session.",
     "Everything measured is reproducible from named scripts — the same dated, re-runnable discipline this site uses.",
    ]),
  ]),
]

NAV = """<nav class="site"><div class="row">
  <a class="brand" href="{p}index.html">nhi<span>.sgit.ai</span></a>
  <span class="stage-pill">mvp draft</span>
  <a class="ver" href="{p}admin/versions.html" title="Site release history">{ver}</a>
  <a class="nl" href="{p}thesis/index.html">Thesis</a>
  <a class="nl" href="{p}hope/index.html">Hope</a>
  <a class="nl" href="{p}method/index.html">Method</a>
  <a class="nl" href="{p}options/index.html">Options</a>
  <a class="nl" href="{p}industry/index.html">Industry</a>
  <a class="nl" href="{p}collection/index.html">Collection</a>
  <a class="nl" href="{p}frameworks/aomm.html">AOMM</a>
  <a class="nl" href="{p}pki/index.html">PKI</a>
  <a class="nl" href="{p}documents/index.html">Docs</a>
  <a class="nl here" href="{packs}">Packs</a>
  <a class="nl" href="{p}infographics/index.html">Infographics</a>
  <a class="nl" href="{p}admin/comms.html">Comms</a>
  <a class="gh" href="https://github.com/SGit-AI/SGit-AI__Website__NHI">★ GitHub</a>
</div></nav>"""

FOOTER = """<footer class="site"><div class="cols">
  <div>
    <div class="brandline">nhi<span>.sgit.ai</span></div>
    <p>Non-human identity, blast radius and agentic security — anchored by the two-populations thesis. All content CC BY 4.0.</p>
    <p class="partnote">⚠ Participant disclosure: published by the sgit project. <a href="{p}about/participant.html" style="display:inline;padding:0">Read the disclosure</a>.</p>
    <p class="verline">site <a href="{p}admin/versions.html">{ver}</a> · <a href="{p}admin/index.html">engineering</a></p>
  </div>
  <div>
    <h4>The research</h4>
    <a href="{p}thesis/index.html">The thesis</a>
    <a href="{p}method/index.html">Method</a>
    <a href="{p}options/index.html">Options</a>
    <a href="{p}industry/index.html">Industry</a>
  </div>
  <div>
    <h4>The collection</h4>
    <a href="{p}collection/index.html">By question</a>
    <a href="{p}documents/index.html">Documents</a>
    <a href="{packs}">Packs</a>
    <a href="{p}pki/index.html">PKI</a>
  </div>
  <div>
    <h4>Site</h4>
    <a href="{p}admin/comms.html">Comms</a>
    <a href="{p}admin/versions.html">Versions</a>
    <a href="{p}llms.txt">llms.txt</a>
    <a href="https://sgit.ai">sgit.ai</a>
  </div>
</div></footer>"""

READER_SCRIPTS = """<script src="https://cdn.jsdelivr.net/npm/marked@12/marked.min.js"></script>
<script src="{p}assets/mdreader.js"></script>"""

DOC_PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title} · {pack_name_plain} · packs · nhi.sgit.ai</title>
<meta name="description" content="{role}. Part of the {pack_name_plain} dev pack — summary, key concepts and the full document, readable in-page.">
<link rel="canonical" href="https://nhi.sgit.ai/packs/{pack}/{slug}.html">
<link rel="stylesheet" href="../../assets/site.css">
</head>
<body>

{nav}

<main class="doc">
<div class="crumb"><a href="../../index.html">nhi.sgit.ai</a> / <a href="../index.html">packs</a> / <a href="index.html">{pack}</a> / {slug}</div>
<h1>{title}</h1>

<div class="docmeta">
  <span class="k">Pack</span><span class="v"><a href="index.html">{pack_name}</a></span>
  <span class="k">Role</span><span class="v">{role}</span>
  <span class="k">Date</span><span class="v">17 August 2026 · pack v0</span>
  <span class="k">Origin</span><span class="v">Architect-review agent, SGit-AI__CLI repo</span>
  <span class="k">Source</span><span class="v"><a href="src/{file}">raw markdown</a> · <a href="https://github.com/SGit-AI/SGit-AI__CLI/blob/claude/sgit-architect-agent-review-3tl5ti/team/explorer/dev/impl-plans/08/17/static-publishing/{file}">original on GitHub</a></span>
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

<h2 id="read">Read the document</h2>
<div class="mdread-label">📄 Pack document · {file} · rendered from the <a href="src/{file}">raw markdown</a> (the source of truth)</div>
<div class="mdread" id="mdread" data-src="src/{file}"><noscript><p class="dim">In-page rendering needs JavaScript — <a href="src/{file}">open the raw markdown</a>.</p></noscript></div>

<div class="pagenav">
  <a href="{prev}">{prev_label}</a>
  <a href="{next}">{next_label}</a>
</div>
</main>

{footer}

{scripts}
</body>
</html>
"""

PACK_HUB = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{pack_name_plain} — dev pack · nhi.sgit.ai</title>
<meta name="description" content="A build-spec pack, readable in-page: the executable dev brief, architecture, commands & UX, flows, invariants & tests, phases, and decisions & evidence.">
<link rel="canonical" href="https://nhi.sgit.ai/packs/{pack}/index.html">
<link rel="stylesheet" href="../../assets/site.css">
</head>
<body>

{nav}

<main class="doc">
<div class="crumb"><a href="../../index.html">nhi.sgit.ai</a> / <a href="../index.html">packs</a> / {pack}</div>
<h1>{pack_name}</h1>
<p class="lead">{three}</p>

<div class="note"><b>Origin.</b> {origin} Raw sources are captured verbatim under <code>src/</code> (linked from each document page); each document below has a reader page with the same apparatus as the site's <a href="../../documents/index.html">documents</a>.</div>

<h2 id="files">The documents</h2>
<div class="tablewrap"><table>
  <thead><tr><th>Document</th><th>Role</th></tr></thead>
  <tbody>
{rows}
  </tbody>
</table></div>

<h2 id="relevance">Why it is on this site</h2>
<p>{relevance}</p>

<h2 id="readme">The pack README</h2>
<div class="mdread-label">📄 Pack overview · {readme} · rendered from the <a href="src/{readme}">raw markdown</a> (the source of truth)</div>
<div class="mdread" id="mdread" data-src="src/{readme}"><noscript><p class="dim">In-page rendering needs JavaScript — <a href="src/{readme}">open the raw markdown</a>.</p></noscript></div>

<div class="pagenav">
  <a href="../index.html">← All packs</a>
  <a href="{first}.html">First document →</a>
</div>
</main>

{footer}

{scripts}
</body>
</html>
"""

SECTION_HUB = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Dev packs — build specs, readable here · nhi.sgit.ai</title>
<meta name="description" content="Implementation-plan packs authored by dev agents, captured verbatim and presented for reading: each pack has a hub and a reader page per document, with summaries, key concepts and rendered diagrams.">
<link rel="canonical" href="https://nhi.sgit.ai/packs/index.html">
<link rel="stylesheet" href="../assets/site.css">
</head>
<body>

{nav}

<main class="doc">
<div class="crumb"><a href="../index.html">nhi.sgit.ai</a> / packs</div>
<h1>Dev packs</h1>
<p class="lead">Implementation-plan packs authored by dev agents — captured verbatim, and presented the same way as the site's <a href="../documents/index.html">documents</a>: a hub per pack, and a reader page per document with a summary, key concepts, key ideas and the full markdown (diagrams rendered). These will eventually move to their own site; the treatment established here moves with them.</p>

<div class="tablewrap"><table>
  <thead><tr><th>Pack</th><th>Date · status</th><th>In one line</th></tr></thead>
  <tbody>
{rows}
  </tbody>
</table></div>

<div class="note"><b>Adding a pack.</b> Point the working session at a repo path or paste the files; the sources land under <code>packs/&lt;name&gt;/src/</code> verbatim and the pages are one entry in <code>admin/build/gen_packs.py</code>.</div>

<div class="pagenav">
  <a href="../documents/index.html">← The documents</a>
  <a href="static-publishing/index.html">First pack →</a>
</div>
</main>

{footer}
</body>
</html>
"""

def nav_for(depth, ver):
    p = "../" * depth
    packs = ("index.html" if depth == 1 else "../index.html")
    return NAV.format(p=p, ver=ver, packs=packs)

def footer_for(depth, ver):
    p = "../" * depth
    packs = ("index.html" if depth == 1 else "../index.html")
    return FOOTER.format(p=p, ver=ver, packs=packs)

def concepts_li(items):
    out = []
    for t, u, d in items:
        if u:
            out.append(f'  <li><a href="{u}"><b>{html.escape(t)}</b></a> — {d}</li>')
        else:
            out.append(f'  <li><b>{html.escape(t)}</b> — {d}</li>')
    return "\n".join(out)

def ideas_li(items):
    return "\n".join(f"  <li>{i}</li>" for i in items)

section_rows = []
for pack in PACKS:
    pdir = ROOT / "packs" / pack["slug"]
    assert (pdir / "src").is_dir(), f"missing sources: {pdir}/src"
    plain = pack["name"].replace("`", "")
    nav2, foot2 = nav_for(2, SITE_VERSION), footer_for(2, SITE_VERSION)
    docs = pack["docs"]
    rows = []
    for i, d in enumerate(docs):
        assert (pdir / "src" / d["file"]).exists(), f"missing {d['file']}"
        prev = (docs[i-1]["slug"] + ".html") if i > 0 else "index.html"
        prev_label = ("← " + docs[i-1]["title"]) if i > 0 else "← Pack hub"
        nxt = (docs[i+1]["slug"] + ".html") if i+1 < len(docs) else "index.html"
        next_label = (docs[i+1]["title"] + " →") if i+1 < len(docs) else "Back to the pack hub →"
        page = DOC_PAGE.format(nav=nav2, footer=foot2,
            scripts=READER_SCRIPTS.format(p="../../"),
            title=html.escape(d["title"]), pack=pack["slug"], slug=d["slug"],
            pack_name=html.escape(pack["name"]), pack_name_plain=html.escape(plain),
            role=d["role"], file=d["file"], summary=d["summary"],
            concepts=concepts_li(d["concepts"]), ideas=ideas_li(d["ideas"]),
            prev=prev, prev_label=html.escape(prev_label),
            next=nxt, next_label=html.escape(next_label))
        (pdir / f"{d['slug']}.html").write_text(page)
        print(f"wrote packs/{pack['slug']}/{d['slug']}.html")
        rows.append(f'    <tr><td><a href="{d["slug"]}.html"><b>{html.escape(d["title"])}</b></a></td><td>{d["role"]}</td></tr>')
    hub = PACK_HUB.format(nav=nav2, footer=foot2,
        scripts=READER_SCRIPTS.format(p="../../"),
        pack=pack["slug"], pack_name=html.escape(pack["name"]),
        pack_name_plain=html.escape(plain), three=pack["three_sentences"],
        origin=pack["origin"], relevance=pack["site_relevance"],
        readme=pack["readme"], rows="\n".join(rows), first=docs[0]["slug"])
    (pdir / "index.html").write_text(hub)
    print(f"wrote packs/{pack['slug']}/index.html")
    section_rows.append(f'    <tr><td><a href="{pack["slug"]}/index.html"><b>{html.escape(plain)}</b></a></td><td>17 Aug 2026 · build spec</td><td>Publish a vault to any static host or folder; browse and clone it with no server and no auth. 8 documents.</td></tr>')

sec = SECTION_HUB.format(nav=nav_for(1, SITE_VERSION), footer=footer_for(1, SITE_VERSION),
                         rows="\n".join(section_rows))
(ROOT / "packs" / "index.html").write_text(sec)
print("wrote packs/index.html")
print(f"packs section at {SITE_VERSION}")
