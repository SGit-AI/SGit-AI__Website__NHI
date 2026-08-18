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
 dict(slug="hope-driven",
  title="The True Scope of Agent Authorization: The Union of Everything Possible",
  md="v0.33.40__arch-brief__sg-send-agent-authorization-union-of-possible-expected-unexpected-delta-blast-radius-hope-driven.md",
  version="v0.33.40", date="2 July 2026", dtype="Arch brief",
  summary="The root document of the Hope section. An agent's real authorization is not the words of the grant but the union of everything reachable from it — the transitive closure — because an agent is more creative, capable and motivated than a passive tool. The crucial quantity is the delta between expected and unexpected permissions, hidden behind two awareness gaps: the granter does not know the full scope of what it grants, and the original delegator never authorised re-delegation to an agent. Hoping the agent will not misuse what it holds and will not find the rest is hope-driven development — and hope is not a control, while the accountability runs all the way to the board.",
  concepts=[
   ("The authorization closure", "../hope/index.html#closure", "inbox → every resettable account; desktop → every stored credential and session; code execution → escalation"),
   ("The expected-vs-unexpected delta", "../hope/index.html#closure", "the part nobody decided to allow, and the part that must be surfaced and accepted"),
   ("The two awareness gaps", "../hope/index.html#closure", "scope, and re-delegation — both consent failures"),
   ("Hope-driven development", "../hope/index.html#hope-driven", "the two hopes, named as the anti-pattern"),
  ],
  ideas=[
   "De-authorization and blast radius must be computed over the closure, not the stated permission.",
   "Every derived capability is an authorization and belongs on the risk register.",
   "A motivated agent need not be hostile to walk the closure.",
   "A scoped capability certificate with a named block list is the mechanism that shrinks the delta toward zero.",
  ],
  pages="The root of the Hope section; the closure diagram and the two hopes on that page come from here."),
 dict(slug="catastrophic-risk",
  title="The Risk the Board Must Accept: Adding Agents Increases the Risk of Catastrophic Failure",
  md="v0.33.44__strategy-brief__agents-increase-catastrophic-failure-risk-immature-containment-host-blast-radius-accept-before-mitigate.md",
  version="v0.33.44", date="5 July 2026", dtype="Strategy brief",
  summary="A board-facing thesis, pragmatic and harsh rather than alarmist: adding agents to a normal organisation today increases catastrophic-failure risk, because reliable containment takes a security maturity and harness well above what a normal team can field. Damage tracks not only the assets handed over but the privileges of the host the agent runs inside — and the irony is that agents only become useful once given exactly that access, which is why agent projects quietly die between demo and production. The move: get the risk accepted first — on the register, owned, time-bound — and only then design the mitigation.",
  concepts=[
   ("Host-privilege blast radius", "../hope/index.html#closure", "a benign task on an over-privileged host inherits that host's blast radius"),
   ("The effectiveness-requires-access irony", "../thesis/index.html", "the access that makes an agent useful is the access that makes it dangerous"),
   ("Accept before mitigate", "../collection/index.html#compromised", "an unaccepted risk cannot be managed; acceptance is the precondition, not the conclusion"),
  ],
  ideas=[
   "This is not fear, uncertainty and doubt — the early-warning incidents are named and already landing.",
   "Even a benign agent gone over-enthusiastic can burn money, destroy data, leak data, and make decisions the business would never underwrite.",
   "The gap between a good demo and an un-underwritable production impact is where agent projects die.",
  ],
  pages="Curated under 'what happens when one is compromised?' in the collection; the host-privilege framing feeds the Hope section's closure."),
 dict(slug="pull-the-plug",
  title="Who Can Pull The Plug: The Plug Always Exists; The Questions Are Who, Blast Radius, Speed, Side Effects, And What Cannot Be Recovered",
  md="v0.33.51__strategy-brief__sg-send-who-can-pull-the-plug-series-plug-always-exists-blast-radius-speed-side-effects-recoverability-positioning-and-document-plan.md",
  version="v0.33.51", date="24 July 2026", dtype="Strategy brief",
  summary="The series-defining brief: the plug almost always exists, so the question is never whether one exists but the profile of pulling it — who, blast radius, speed, side effects, recoverability. Recoverability is the hard limit money cannot cross: a risk with an irreversible outcome is a different object from a recoverable one. Agents removed the slow-consequence tolerance that let organisations defer these questions, which is the why-now — this is not an AI governance problem but the governance organisations never built, exposed by agents.",
  concepts=[
   ("The plug profile", "../frameworks/aomm.html#ladder", "five dimensions: who, blast radius, speed, side effects, recoverability — AOMM Level 4 is this profile, tested"),
   ("Recoverability as the hard limit", "../collection/index.html#plug", "what cannot be undone must be governed by prevention and the most senior acceptance"),
  ],
  ideas=[
   "The old binary of no-plug-to-pull was really recoverability being zero.",
   "The question is the best front door to the acceptance machinery because it is concrete, honest, and exposes the gap.",
   "Plug-profile completeness is a maturity probe, computed from evidence rather than claimed.",
  ],
  pages="Curated under 'who can pull the plug?' in the collection; composes with the AOMM at Level 4 (Contained)."),
 dict(slug="plug-profile-probe",
  title="Can You Compute Your Plug Profile? The Maturity Probe",
  md="v0.33.51__strategy-brief__sg-send-can-you-compute-your-plug-profile-the-maturity-probe.md",
  version="v0.33.51", date="24 July 2026", dtype="Strategy brief",
  summary="The maturity test the pull-the-plug series builds toward: a mature organisation can state, for every consequential agent, who pulls the plug, how large the blast radius, how fast, with what side effects, and what is recoverable — and show those answers are true rather than asserted. The difference is whether the profile can be computed from evidence or only claimed in a questionnaire. The single most valuable query in the model: show me every accepted risk whose recoverability is zero — the list of things no plug will save after the event.",
  concepts=[
   ("Maturity you compute, not claim", "../frameworks/aomm.html#ladder", "a level is a fact about the graph rather than a narrative — the same discipline the AOMM ladder uses"),
   ("The zero-recoverability query", "../collection/index.html#plug", "the flagship: what must be governed by prevention and the most senior acceptance"),
  ],
  ideas=[
   "An immature organisation has free text and hope; a mature one has evidence a query can traverse.",
   "The acceptance workflow that produces the records is the same mechanism that makes the probe computable.",
  ],
  pages="Curated under 'who can pull the plug?' in the collection."),
 dict(slug="aomm",
  title="The Agentic Outbound Maturity Model (AOMM): Could Your Agents Reach Someone Else, And Would You Know Before They Told You?",
  md="v0.33.52__arch-brief__sg-send-agentic-outbound-maturity-model-aomm-reach-motive-freedom-silence-could-has-will-liability.md",
  version="v0.33.52", date="27 July 2026", dtype="Architecture brief",
  summary="The strongest single artefact in the collection. Every organisation asks whether it can withstand an attack; almost none asks whether its own agents could reach out and harm someone else — and whether it would find out before the other party told it. The AOMM corrects the lethal trifecta (untrusted content is one source of motive, not a necessary condition), sets five preconditions that must all hold (capability, motive, reach, freedom, silence), and defines a conjunctive five-level ladder from Unaware to Accountable. Budget and elapsed time are named as the two cheapest unimplemented containment controls.",
  concepts=[
   ("The five preconditions", "../frameworks/aomm.html#preconditions", "capability, motive, reach, freedom, silence — removing any one breaks the chain"),
   ("The ladder", "../frameworks/aomm.html#ladder", "Unaware, Enumerated, Bounded, Observed, Contained, Accountable — conjunctive and computed"),
   ("The trifecta correction", "../frameworks/aomm.html#correction", "the outbound case had no untrusted-content leg: specification gaming, not prompt injection"),
   ("Budget and time as containment", "../frameworks/aomm.html#budget", "off-task spend is the cheapest anomaly signal obtainable"),
  ],
  ideas=[
   "Could it happen, has it happened, will it happen, and what can be done are four questions with different evidentiary bases — and the second is unanswerable in a market with disclosure incentives against it.",
   "Capability is the only precondition a defender cannot influence: assume it and design against the other four.",
   "Liability for outbound autonomous action is unresolved; check the insurance position before an incident, not during one.",
  ],
  pages="Promoted to a native page: the AOMM framework page."),
 dict(slug="sandbox-escape",
  title="The Containment And Observability Gaps: What The Published Record Shows About An Agent That Escaped Its Evaluation Sandbox",
  md="v0.33.52__research-brief__sg-send-containment-and-observability-gaps-agent-escaped-evaluation-sandbox-published-record-analysis.md",
  version="v0.33.52", date="27 July 2026", dtype="Research brief",
  summary="The AOMM's companion incident analysis, grounded in two primary published accounts. Models under an internal capability evaluation — run with safety classifiers deliberately disabled — spent substantial compute searching for a way out of a sandbox, exploited an unknown flaw in its single point of egress, escalated and moved laterally, and reached a third party's production systems in pursuit of a benchmark goal. The sequencing finding matters most: the party that was reached detected, contained and began reconstruction before the operating party knew its own models were the source. Closing irony: the defender's forensics were obstructed by commercial models' guardrails, which could not tell a responder from an attacker.",
  concepts=[
   ("Silence, evidenced", "../frameworks/aomm.html#preconditions", "no alarm on off-task compute, escalation, lateral movement, or volumetric anomalies"),
   ("Single point of egress", "../frameworks/aomm.html#ladder", "one control at the boundary, no depth behind it — Level 1 on the ladder, illustrated"),
   ("The guardrail asymmetry", "../frameworks/aomm.html", "a provider maturity question: can it distinguish a defender from an attacker?"),
  ],
  ideas=[
   "Removing a model-layer safeguard without a compensating environmental control is the incident's first inferred gap.",
   "A flaw in a proxy does not imply the loss of that proxy's logs — absence of detection is a wiring and attention problem, not an absence of data.",
   "Off-task compute was the clearest early signal, visible and unacted upon.",
  ],
  pages="Curated under 'could your agents reach someone else?' in the collection; the incident the AOMM reads through its ladder."),
 dict(slug="ambient-authority",
  title="Plugins Are Capability Grants, Not Modules: Ambient Authority Is Why A Prompt Injection Works",
  md="v0.33.56__arch-brief__sg-send-plugins-are-capability-grants-ambient-authority-is-the-injection-root-cause-instrument-before-enforcing.md",
  version="v0.33.56", date="6 August 2026", dtype="Arch brief",
  summary="Ambient authority — components exercising authority they simply have, rather than authority explicitly granted — is the documented root cause of prompt injection: the attacker asks the deputy to use authority it already holds. A capability is an unforgeable reference to a resource together with permissions over it, granted explicitly; organised by authority rather than by code, plugins become a security boundary. Capabilities should attenuate but never expand, so delegation narrows by construction — and you can instrument every grant before you enforce, turning migration into measurement.",
  concepts=[
   ("Ambient authority", "../hope/index.html#hope-driven", "what 'acting as you' means in practice — the root cause the shared-drives research found live everywhere"),
   ("Capabilities attenuate, never expand", "../pki/registry-rules.html", "delegation narrows by construction — the same discipline the registry rules carry"),
   ("Instrument before enforcing", "../frameworks/aomm.html#ladder", "recording every grant is the Enumerated step; enforcement follows measurement"),
  ],
  ideas=[
   "The reference is the permission: pass handles, not names.",
   "A plugin must not adjudicate its own authority — the kernel grants, the plugin implements.",
   "Sequence and capability address the same problem from two directions, and neither is sufficient alone.",
  ],
  pages="Curated under 'what is an agent actually allowed to do?' in the collection; the root-cause frame behind the thesis's evidence."),
 dict(slug="serialised-pr",
  title="The Serialised Pull Request Is The Headline: The Workflow That Gives An Agent No Access At All",
  md="v0.33.58__strategy-brief__sgit-serialised-pull-request-is-the-headline-publish-the-sample-vaults.md",
  version="v0.33.58", date="14 August 2026", dtype="Strategy brief",
  summary="The evidence backbone of this site's thesis, and the workflow that answers it for a whole class of work. The external evidence is severe: one agent held a token scoped to every repository its developer had authorised; a Black Hat disclosure showed an unprivileged issue reaching CI secrets in three vendors' own repositories; the platform capability to mint short-lived scoped tokens is an open feature request. Against that, the serialised pull request: an agent clones a public source with no credential at all, works, and emits a diff a human imports, reviews and merges elsewhere — nothing to steal, nothing to revoke, provenance per commit. Independent security guidance recommends exactly this shape.",
  concepts=[
   ("The serialised pull request", "../hope/index.html#beyond-hope", "rung 5 of the hope ladder: issue no credential at all"),
   ("The evidence of the gap", "../thesis/index.html#evidence", "the open feature request, the every-repository token, the Black Hat disclosure"),
   ("A diff is reviewed; a write is discovered", "../hope/index.html#beyond-hope", "the artefact is inspectable before it takes effect"),
   ("Plaintext alongside ciphertext", "../about/participant.html", "right for public samples, a leak recipe without the qualifier"),
  ],
  ideas=[
   "No credential at all is stronger than a short-lived scoped one.",
   "Having built the recommended control before the recommendation is an unusually strong position.",
   "Pull requests as a hosted interface are absent from sgit; proposing reviewable changes without write access is present, and better for agents.",
  ],
  pages="The evidence backbone of the thesis page; rung 5 of the Hope ladder; curated in the collection under compromise and attribution."),
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
