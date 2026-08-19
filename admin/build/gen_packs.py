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
  origin="Authored by an Architect-review agent in the SGit-AI__CLI repo (branch claude/sgit-architect-agent-review-3tl5ti), 17 August 2026; revised nine times through 19 August under maintainer review — three added documents (publish output, API docs, asset origin), the no-target and no-ciphertext-copy publish decisions, an executed end-to-end tabletop exercise, and a change-control log recording every revision with its trigger. Status: build spec, ready to implement — Phases 1 and 3 are unblocked.",
  date="17–19 August 2026 · pack v0",
  origin_short="Architect-review agent, SGit-AI__CLI repo",
  gh_base="https://github.com/SGit-AI/SGit-AI__CLI/blob/claude/sgit-architect-agent-review-3tl5ti/team/explorer/dev/impl-plans/08/17/static-publishing/",
  commit="a1d5ce6", captured="19 August 2026",
  commit_url="https://github.com/SGit-AI/SGit-AI__CLI/commit/a1d5ce6ce5e681ab37aa6875a9ac76629d3b1e98",
  row_date="17–19 Aug 2026 · build spec",
  one_line="Publish a vault to any static host or folder; browse and clone it with no server and no auth. 12 documents plus a change-control log, including an executed tabletop exercise.",
  meta_desc="A build-spec pack, readable in-page: the executable dev brief, architecture, commands &amp; UX, flows, invariants &amp; tests, phases, the publish output, published API docs, the asset-origin question, decisions &amp; evidence, an executed end-to-end tabletop exercise, and the pack's change-control log.",
  readme="README.md",
  three_sentences="A vault publishes to a folder: encrypted objects plus a small, declared plaintext surface (loader, cover, manifest, and — only when the vault is deliberately public — the read key). That folder is readable by a browser through the loader and by <code>sgit clone</code> over ordinary GETs, from any HTTP host or a local folder, with no server and no auth. <code>sgit vault serve</code> exists because browsers give local files an opaque origin — the one case everybody tries first, double-clicking <code>index.html</code>, cannot work without it.",
  site_relevance="Two of this pack's measured findings connect straight to claims this site publishes: <b>custody without access requires a manifest</b> (every filename derives from the read key, so a keyless client cannot name a single file — sharpening the <a href='../../pki/registry-rules.html#vaults'>PKI section's custody row</a>), and <b>object ids hash ciphertext with random IVs, so a fork is unlinkable</b> — relevant to the <a href='../../collection/index.html#attribute'>attribution question</a>. The published-folder model is also the substrate the <a href='../../documents/serialised-pr.html'>serialised pull request</a> workflow rides on.",
  docs=[
   dict(slug="dev-brief", file="00__DEV-BRIEF.md",
    title="00 — The executable dev brief",
    role="The brief a developer agent runs from: grounding reads, the six rules, per-phase tasks, definition of done",
    summary="Written to be executed by a developer agent, not just read: the grounding reads in order, the six rules that override convenience, non-negotiable implementation constraints (fixed plaintext allow-list, fail-soft per object, unconditional hash verification, localhost-only serve, writes raise), a definition of done every phase must meet, and an explicit list of what is not the developer's to decide. The 18–19 Aug revision added the sixth rule — publishing never changes the vault — and phase P4b for the published API docs.",
    concepts=[
     ("The six rules", None, "byte-identical ciphertext everywhere; the key never reaches a server; keyless custody; byte-identical loader; plaintext only where the key is published; publishing never changes the vault"),
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
    summary="The whole feature hangs on one seam: every sgit action already accepts an injected api, so the static transport is a sibling class — read-only GET fan-out over any host or folder — with zero changes to any call site, proven by a running spike. Four methods carry the entire read path (including presigned_read_url, which is on the clone path for every blob over ~4 MB — a size-dependent bug waiting for anyone who skips it). Transport resolution is transparent but never silent: sniffed once, sticky, reported in vault info. As of r9, publish emits the plaintext surface only — the ciphertext store is never copied; the served root is composed at deployment, either co-located (serve the repo itself, zero copies) or assembled by a keyless copy of bare/ into place.",
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
    summary="Every block is the intended user-facing output, to be matched word for word — several strings are load-bearing because they are the only place a user learns why an irreversible thing is irreversible. The publish baseline is private-and-ciphertext-only; publishing the read key requires --visibility public and a stated-consequence confirmation: anyone with the URL can read every file, now and in every future publish, and copies cannot be recalled. The 19 Aug revision removes the target argument — publish always writes .sg_vault/publish/ and deployment is a separate act — and adds the API-docs flags with the CDN default.",
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
    role="Six invariants asserted everywhere + fourteen test cells, collapsed from 240 combinations",
    summary="Five dimensions produce 240 combinations, which is not a test plan; separating what must always hold from what genuinely varies collapses it to 6 invariant assertions applied in every cell, plus 14 cells — I6 (publishing never changes the vault: publish, push, assert the object count unchanged) was added in the 18 Aug revision to catch the amplification loop. The invariants are behavioural checks, not code inspection — I2 asserts that no recorded request contained the key, rather than asserting the code doesn't send it. Two cells were re-scoped by measurement, and one (clone with no key at all) is structurally impossible by design.",
    concepts=[
     ("Assert behaviour, not absence of code", None, "prove no request contained the key; don't restate the intent"),
     ("Structurally impossible ≠ untested", "decisions-and-evidence.html", "keyless clone can't name a file; the cell became mirror-with-manifest, with the no-manifest failure as part of the test"),
     ("Runtime-asserted platform facts", None, "cell 10 asserts the CORS header at run time, so a platform change fails the suite instead of quietly breaking the feature"),
    ],
    ideas=[
     "240 combinations → 6 assertions + 14 cells is the test-design move worth stealing.",
     "The fork round trip is the acceptance test.",
    ]),
   dict(slug="implementation-phases", file="05__implementation-phases.md",
    title="05 — Implementation phases",
    role="P1–P7 (plus P4b, published API docs) with file lists, acceptance criteria and risk; start with P1 + P3",
    summary="Independently shippable phases, each one PR with green suites and its own acceptance criteria. P1 (static read transport — promote the spike, don't redesign it) and P3 (vault serve) start now: demonstrable value with zero commitment to the publish protocol still being decided; the revision adds P4b, the published API docs, gated on P2. Acceptance criteria are concrete down to the trap: add a >4 MB fixture, because small fixtures will not catch the large-blob path.",
    concepts=[
     ("Promote the spike", None, "the P1 design already exists as running code — productionising it is the task"),
     ("Ship value before protocol", "decisions-and-evidence.html", "P1+P3 first is itself one of the twelve decisions, with a recommendation"),
    ],
    ideas=[
     "Independently shippable phases keep every PR reviewable and every rollback cheap.",
     "Risk is stated per phase — the two mediums are where the publish protocol touches disk.",
    ]),
   dict(slug="decisions-and-evidence", file="06__decisions-and-evidence.md",
    title="06 — Decisions & evidence",
    role="Twelve open decisions for the maintainer, and the measured evidence that re-scoped the spec",
    summary="The maintainer's file: twelve decisions (up from six across the 18–19 Aug revisions — decision 11 making plaintext expansion a future sgit vault expand command, decision 12 making publish emit the surface only, with no ciphertext copy), each with a recommendation, none blocking P1/P3. And the evidence base that changed the spec: GitHub Pages sends access-control-allow-origin: * by default, so key-on-another-origin moved from 'probably unavailable' to 'supported, asserted at run time'; custody without access structurally requires a manifest, because every filename derives from the read key; object ids are sha256(ciphertext) with random IVs, so two vaults holding the same document share zero object ids — a fork is unlinkable; and Swagger UI measures 2.7× the vault it documents, which reversed decision 7 to a CDN-with-SRI default.",
    concepts=[
     ("Measurement over assumption", None, "source-brief assumptions — and two of the pack's own — reversed by a curl and a spike, with reproduction steps"),
     ("The unlinkable fork", "../../collection/index.html#attribute", "ciphertext-hashed ids + random IVs: a private fork of a public template is undetectable — a finding with privacy and attribution edges both ways"),
     ("A visibility default that drifts is a disclosure", None, "decision 5's one-line rationale, worth keeping"),
    ],
    ideas=[
     "Every decision ships with a recommendation, so sign-off is a review, not a design session.",
     "Everything measured is reproducible from named scripts — the same dated, re-runnable discipline this site uses.",
    ]),
   dict(slug="publish-target", file="07__publish-target.md",
    title="07 — The publish output",
    role="Revised 19 Aug (twice): publish takes no target and copies no ciphertext — it emits the plaintext surface only; the served root is composed at deployment",
    summary="The first version of this file was a rule policing where an output directory may live — the maintainer removed the question instead: sgit publish takes no target, writes .sg_vault/publish/ and nothing else on disk, and deployment is a separate act. Then r9 removed the last copy too: the output is the plaintext surface only — loader, cover, manifest, key file, optional API docs — and never contains ciphertext. The manifest enumerates the store (ids, sizes, sha256), so publishing is O(KB) regardless of vault size (measured: 5 files, ~5 KB, for a 22-object store), and re-publishing never churns a gigabyte store. The served root is composed at deployment — co-located (the one-repo pattern: serve the repo, zero copies) or assembled by a keyless copy of bare/ into place — and sgit vault serve composes virtually by routing. Invariant I1 becomes true by construction: what is served is the store. The two index.html files stay apart: the loader is generated plaintext, always sgit's template; the vault's own index.html is encrypted content — the decrypted page wins at expanded deployment.",
    concepts=[
     ("Remove the question rather than police it", None, "no target argument means no containment rule, no refusal messages, no escape hatch — and the amplification loop is impossible by construction, not by rule"),
     ("The surface, not the store", None, "publish emits O(KB) of plaintext; the ciphertext is never duplicated on disk or in git — composition happens at deployment, by keyless copy or by serving the repo itself"),
     ("The two index.html files", "tabletop-github-pages.html", "the loader (generated, plaintext, byte-identical everywhere) versus the vault's own page (ordinary encrypted content) — conflating them was the earlier framing's one real error"),
    ],
    ideas=[
     ".sg_vault/publish/ contains no vault content at all, which is why it is safe to commit to a public repository even for a private vault.",
     "The secondary vault.html loader copy was dropped: it guarded a partial-expansion mode that does not exist.",
     "manifest.json records which file ended up at the served root and its hash, so the choice is auditable from the artefact rather than from console history.",
    ]),
   dict(slug="api-docs", file="08__api-docs.md",
    title="08 — Published API docs",
    role="Added 18 Aug from the maintainer's proposal: openapi.json generated from the manifest, and Swagger UI as CDN-pinned or bundled",
    summary="Swagger for the published folder is two artefacts with very different costs. The spec (api/openapi.json, a few KB) is generated from manifest.json by the tool that just wrote the folder, so it cannot drift, describes only what the folder actually serves, and uses a relative server URL so it works on any host. The UI is 1.53 MB — measured at 2.7× the entire published vault it documents — so it is opt-in, with CDN-plus-SRI as the default and bundling for offline or no-third-party policies. The non-obvious security interaction: the docs page is same-origin with the loader, which may store keys, so the CDN mode requires the exact-version pin, integrity hashes, crossorigin, no-referrer, and a CSP whose connect-src 'self' means even a script that somehow ran could not exfiltrate a key.",
    concepts=[
     ("Generated from the manifest, so it cannot drift", None, "the publisher's spec describes this deployment; the API team's spec describes the live service — complementary, and the conformance loop closes from both ends"),
     ("SRI is the mitigation, not CDN avoidance", None, "a pinned hash means substituted bytes do not execute; a floating version tag is not acceptable in any mode"),
     ("A demonstration, not documentation", "../../thesis/index.html", "a Swagger UI whose every operation returns opaque bytes, with no auth scheme at all, makes the zero-knowledge claim visible — the ciphertext panel's argument for a different reader"),
    ],
    ideas=[
     "The root fix belongs in the loader: keep keys in memory, never in localStorage, and the same-origin objection collapses for every script anyone ever adds.",
     "A published vault becomes self-describing to an agent — a machine-readable contract with no out-of-band explanation.",
     "The 230 KB standalone preset is simply not emitted: a fixed-spec page never uses it.",
    ]),
   dict(slug="asset-origin", file="09__asset-origin.md",
    title="09 — A first-party asset origin",
    role="Added 19 Aug from the maintainer's static.sgit.ai proposal: yes to the asset site, no to Pages, and never on the reader's critical path",
    summary="The maintainer proposed publishing pinned JS and brand assets to a static.sgit.ai site. The pack's answer draws one line: yes to the asset origin — but on S3/CloudFront, not GitHub Pages (Pages stamps max-age=600 on everything, unfit for immutable assets), and only as the publish-time source for bundled assets, never as a read-time origin. Today a published vault makes zero requests to SGit-AI infrastructure — structural, not policy; putting first-party JS on the reader's critical path would make static.sgit.ai a beacon receiving a request from every reader of every vault, joining readership to the operator's logs. At publish time the same mirror is safe and strictly better than a public CDN fetch, because the SRI hash decides and a substituted byte fails closed.",
    concepts=[
     ("Prefer the third party who cannot correlate", None, "a CDN learns 'somebody loaded swagger-ui'; a first-party origin joins that to our domains, accounts and hub — a zero-knowledge product cannot operate the beacon every reader pings"),
     ("Publish-time source, not read-time origin", None, "the fetch happens once on the publisher's machine, hash-verified — every reader-side concern disappears"),
     ("A permanent public commitment", "../../pki/registry-rules.html", "URLs baked into folders on hosts you do not control can never change: append-only, never rewritten, indefinitely — the registry-rules discipline applied to an asset bucket"),
    ],
    ideas=[
     "The line is drawn by whether the consuming page may hold vault key material — sgit.ai and hub.sgit.ai yes, any published vault folder no.",
     "'It's just a logo' is exactly how a first-party origin ends up on every reader's critical path.",
     "Publish the SRI hash next to every asset, so consumers verify the mirror against upstream instead of trusting it.",
    ]),
   dict(slug="changelog", file="CHANGELOG.md",
    title="Change control — the pack's own release history",
    role="r0–r9, newest first: every spec-editing commit adds an entry — what changed, the trigger, and which decisions moved",
    summary="The pack has reversed load-bearing decisions more than once — healthy, the log says, but only if the reversals are legible in one place. Nine revisions in three days, each entry naming its trigger (almost always a one-line maintainer question: 'why do you need the vault.html file?', 'publish ./site should not be allowed'), what changed, and which numbered decisions moved. r8 is the log acting on itself: the R1 contradiction fixed by making plaintext expansion a future sgit vault expand command (decision 11), manifest entries gaining a per-object sha256 because the tabletop's keyless mirror could content-verify only 12 of 18 objects, and the visibility-downgrade warning added because a fresh CI clone resolves to bare. r9 removes publish's last copy: the output is the plaintext surface only — O(KB) for any vault — and the served root is composed at deployment (decision 12). Updating this file is now part of a developer agent's definition of done.",
    concepts=[
     ("Change control for a spec", None, "every commit that edits a spec file adds an entry — what changed, why (the trigger), which decisions moved; a reader returning after a gap reads this file first"),
     ("Reversals made legible", "decisions-and-evidence.html", "decision 7 reversed (CDN default), decision 9 settled (no target), decision 2 re-settled (loader separation) — each traceable to a maintainer question and a measurement"),
     ("Findings become spec", "tabletop-github-pages.html", "R-numbers from the 19 Aug review and F-numbers from the executed tabletop are fixed in r8 or assigned owners — not just recorded"),
    ],
    ideas=[
     "Eight revisions in three days, almost every trigger a one-line maintainer question — the pack is a conversation with an audit trail.",
     "The same discipline as this site's own versions page: dated entries, newest first, reversals stated plainly.",
     "The keyless mirror's 12-of-18 verification gap became a manifest sha256 requirement — measurement turning into contract.",
    ]),
   dict(slug="tabletop-github-pages", file="10__tabletop__github-pages-one-repo.md",
    title="10 — Tabletop: one repo carrying the key, the files, and the vault",
    role="An executed end-to-end tabletop exercise: the maintainer's scenario run for real with the shipped CLI, producing four live findings",
    explainer=("What is happening in this document — and why it is unusual", [
     "A <b>tabletop exercise</b> is a security-practice staple: before you build or deploy something, you walk the scenario end to end with every party at the table — here an author, a host (GitHub), a reader, an archivist who refuses keys, and a CI runner — and find out where the plan breaks while it is still cheap to fix. Normally a tabletop is a conversation: people around a whiteboard saying &ldquo;the author would now push, and we assume the push succeeds&rdquo;.",
     "This one is different, and it is worth pausing on. It was run by the development agent (an LLM) <b>inside the real codebase, and it is executed, not imagined</b>. Every <code>sgit</code> command in the document actually ran — <code>init</code>, <code>commit</code>, <code>push</code>, <code>derive-keys</code>, key classification, the read-only static clone, decryption, verification — against a real local server, with the agent playing all five roles and pasting the genuine output. Only two things are simulated, and the document marks them every time they appear: the <code>sgit publish</code> command (not built yet — its stand-in uses the product's real cryptography classes) and GitHub's hosting (a local git repo plus a plain HTTP server).",
     "This is not a common use of LLMs. Agents are mostly asked to write code or write prose; here the agent used the codebase as a <b>laboratory</b> — it designed the experiment, executed it, measured what happened (git blob dedup counts, cache lifetimes, object tallies), and reported findings that reading the specification could not have produced. Four live findings (F1–F4) came out of the run, one of which reversed an assumption the pack itself held: a repo that commits the vault store is <em>already</em> statically clonable with shipped code, no publish step involved. The CI drill even fails first — a fresh checkout holds no key material — and the recovery (a full republish from the committed public read key alone, zero secrets) was demonstrated rather than asserted.",
     "What makes the result trustworthy is the discipline around it: every simulated element is labelled at each appearance, every claim is tied to real output, and the lab scripts are committed so the whole exercise re-runs. The design was tested before it was built — the same dated, re-runnable, evidence-over-assumption practice the rest of this site argues for, applied by an agent to its own team's specification.",
    ]),
    summary="The maintainer posed the scenario — one GitHub repo, served by Pages, carrying all three at once: the public read key, the decrypted files, and the encrypted vault store with its history — and the agent ran it rather than reasoning about it. Results, all from real runs: publish → push is a no-op, so the amplification loop is impossible by construction (invariant I6 checked with the shipped CLI); the reader's clone over plain GETs comes back identical to the author's tree in both deployment modes; keyless custody verified every content-addressed object with zero key material; and the ordered commit list needed only the read key, so sgit publish never needs the vault key. The final table records what every party ends up holding — and that the one deliberate act that made the host able to read was publishing the key. The document is kept as a historical record: a note marks that r9 later removed publish's ciphertext copy (making the run's git-dedup measurement moot), and that mode B — cloning straight off the repo's own .sg_vault/, verified here with zero projection involved — is exactly the shape the r9 spec generalises.",
    concepts=[
     ("Executed, not imagined", None, "every command block is real shipped-CLI output; the two simulated stand-ins (publish, GitHub hosting) are marked at every appearance and use the real crypto inside"),
     ("F4: the repo is already a static vault", None, "the committed bare store cloned with no publish step involved — what publish adds is the browser, custody and key discovery, not clonability"),
     ("The zero-secret CI republish", None, "a fresh checkout fails first (no key material — correct), then republishes from the committed public-read-key filename alone; a private vault's CI needs the read key as a secret and an explicit --visibility"),
    ],
    ideas=[
     "Two systems ignore each other's private half mechanically: .git is in sgit's always-ignored set, .sg_vault/local/ is in .gitignore — and the tabletop caught the one leak (F1: the root .gitignore is itself vault content).",
     "The exercise changed the spec it tested: mode B's zero-projection clone became r9's design — publish emits the surface only, and the store is composed in at deployment.",
     "A refused push still rewrote mutable ref bytes (F2) — spurious git dirty states, filed as a code issue: the kind of bug only an executed exercise surfaces.",
     "Pages' max-age=600 means a reader can see the old head ref for up to ten minutes after a redeploy; immutable objects are unaffected.",
    ]),
  ]),
 dict(slug="hub-sgit-ai",
  name="hub.sgit.ai: The Fractal Forge",
  origin="Authored by the Explorer/Architect agent in the SGit-AI__CLI repo (branch claude/sgit-architect-agent-review-3tl5ti), 18 August 2026, responding to the 15-document hub briefing pack (v0.33.56–v0.33.59) plus three maintainer-raised dimensions: community-run hubs, the fractal hub-of-hubs, and commercialisation. Status: design pack — two audit findings change the plan materially, and one (the sub-vault decision) should be resolved before hub architecture is written.",
  date="18 August 2026 · pack v0",
  origin_short="Explorer/Architect agent, SGit-AI__CLI repo",
  gh_base="https://github.com/SGit-AI/SGit-AI__CLI/blob/claude/sgit-architect-agent-review-3tl5ti/team/explorer/architect/contracts/08/18/hub-sgit-ai/",
  commit="fbebe0c", captured="18 August 2026",
  commit_url="https://github.com/SGit-AI/SGit-AI__CLI/commit/fbebe0ce25f63638ec6af12ecf666c07f4445e8a",
  row_date="18 Aug 2026 · design pack",
  one_line="A forge whose application layer is the browser; a hub is itself a vault, so the network is fractal by composition. 9 documents.",
  meta_desc="A design pack, readable in-page: the dev brief, the fractal model, the capability audit and its two findings, architecture &amp; flows, permissions as key topology, commercialisation, mockups, and the roadmap.",
  readme="README.md",
  three_sentences="A <b>forge whose application layer is the browser</b>: the client holds the key, the server stores ciphertext and reads nothing. A hub is <b>itself a vault</b> — a cover, a catalogue and a loader — which means a hub can list other hubs and the network is <b>fractal by composition</b> rather than by new protocol; anyone can run one, because &ldquo;run a hub&rdquo; means &ldquo;publish a folder&rdquo;. The pack opens with two findings about the shipped CLI: the sub-vault primitive every brief builds permissions on <b>does not exist</b>, and a third access tier — the structure key, which decrypts a vault's shape but not its content — is <b>shipped, tested and unused</b>.",
  site_relevance="This pack is the site's arguments in the builder's seat. Finding 1 — every brief assumed a sub-vault primitive that no code implements — is the <a href='../../hope/index.html'>hope gap</a> caught by an audit before it shipped: enumerate what exists before you architect on it. The four key positions (vault, read, structure, none) are <a href='../../documents/ambient-authority.html'>capability attenuation</a> in practice — each weaker key derives one-way from the stronger. The CI section is this site's over-privileged-agent problem verbatim: a runner must read to build, and the only model-consistent answer is a scoped key — least authority for a non-human identity, with the honest open question of who assembles the scope. And &ldquo;revocation is not retroactive&rdquo; is the operational face of the <a href='../../pki/registry-rules.html'>registry rules</a>' supersede-not-delete: rotation protects the future and returns nothing already taken.",
  docs=[
   dict(slug="dev-brief", file="00__DEV-BRIEF.md",
    title="00 — The executable dev brief",
    role="The brief the hub-builder runs from: Step 0 before architecture, the six rules, the step table, what is not theirs to decide",
    summary="Written to be executed: the grounding reads in order, then the instruction the specification itself insists on — two things land before any hub architecture is written: the web-side capability audit, and the sub-vault decision. Six rules override convenience: the server reads nothing, ever (the catastrophic-failure principle as a design test); features follow the key, not the tier; classify keys by declaration and refuse a vault key in any read surface; never imply a capability that does not exist; sparse by default; and a hub is a vault — if hubs seem to need a server-side feature to talk to each other, stop. Eight steps from the audits to structure-key views, a definition of done per step, and an explicit list of what is not the builder's to decide.",
    concepts=[
     ("Step 0 before architecture", "capability-audit.html", "a design written without the inventory is wrong in one of two expensive directions: rebuilding what exists, or assuming what does not"),
     ("The catastrophic-failure design test", None, "if a total compromise of the hub would disclose content that was not already public, the feature fails — out, not deferred"),
     ("Features follow the key, not the tier", None, "anything a user holds a key to gets the full experience; only discovery across keyless vaults needs a reading index"),
    ],
    ideas=[
     "When a brief contradicts the code, the code wins — two of the briefing pack's open questions were already settled by measurement.",
     "The sub-vault decision is raised, never resolved in code: recommend, do not implement unilaterally.",
     "The moment a hub is necessary rather than convenient, the fractal stops being real.",
    ]),
   dict(slug="the-model-and-the-fractal", file="01__the-model-and-the-fractal.md",
    title="01 — The model, and the fractal",
    role="The settled forge model, and the 18 Aug addition: a hub is a vault, so the network is fractal by composition",
    summary="The model is settled: a forge whose application layer runs in the browser — the client decrypts, the server is object storage plus a small interface and reads nothing; the reference class is a self-hostable forge, with the claim that the server can be storage rather than an application. The fractal is the new part, and its virtue is that it is not a new mechanism: the catalogue lives in a vault and publishing is a folder copy, so a hub is just a vault containing a cover, a catalogue and a loader — and nothing stops a catalogue entry pointing at another hub. Navigating the network is client-side graph navigation; federation needs no federation protocol. A hub can be a useful index of things it cannot read: private vaults are listed, described and requestable — and still opaque.",
    concepts=[
     ("A hub is a vault", "architecture-and-flows.html", "cover + catalogue + loader; every edge in the network is the same operation the client already performs — open a vault"),
     ("The fractal as adoption strategy", None, "a community cannot adopt a platform it must be granted access to; it can adopt a format — a hub costs a bucket and a publish, and forks are unlinkable"),
     ("Trust does not compose", None, "hub A listing hub B is not an endorsement; provenance (who listed this, when, what they verified) is a catalogue field, not an emergent property"),
    ],
    ideas=[
     "The fractal needs exactly three things: a catalogue schema with kind: vault | hub, a cover schema, and a loop guard — no consensus, no registry, no server-side crawl.",
     "The shape of the estate is disclosed regardless: a hub is a public statement that these vaults exist — the stated exception travels with the claim.",
     "Stale pointers are the failure mode: an intermediary cannot forge content, but it can serve last week's — surface the head's age.",
    ]),
   dict(slug="capability-audit", file="02__capability-audit.md",
    title="02 — Capability audit",
    role="The CLI-side inventory (done — facts), the two findings, and the web-side audit template that gates architecture",
    summary="The specification says the first deliverable is an inventory, not architecture; this file does the CLI half — which nobody had done, and which produced the pack's two findings. Present and merely surfaced by a forge: read-key-only open, tree navigation, single-object fetch, history, diff, branch/merge, sparse fetch, and the per-path index shipped as the cache layer. Present but unused: the structure key, a third access tier that decrypts metadata — paths, tree shape, history, sizes — but no blob content, with one consumer and full tests. Absent: the sub-vault/link-file primitive every brief builds granularity on, blame, bisect, and cross-vault search without a key (impossible by construction). The web-side template follows, with two rows added so absences are recorded on both sides rather than assumed present on the other.",
    concepts=[
     ("Finding 1: the missing primitive", "permissions-topology.html", "no sub-vault or link file exists anywhere in the CLI — the permissions-as-topology model in every brief currently has nothing to stand on"),
     ("Finding 2: the structure key", None, "browse the shape without reading the files — shipped, tested, one consumer; a permissions tier and a commercial tier at the same time, looking for a product"),
     ("Surfacing vs adding vs absent", None, "the classification every forge feature must carry, so the plan never silently assumes a capability into existence"),
    ],
    ideas=[
     "A partial capability is more dangerous to a plan than an absent one, because it gets assumed complete.",
     "Four usable key positions exist, all shipped, none requiring server policy — the briefing pack works with only two of them.",
     "Report gaps as plainly as presences: the audit's value is the absences it puts on the record.",
    ]),
   dict(slug="architecture-and-flows", file="03__architecture-and-flows.md",
    title="03 — Architecture & flows",
    role="The ciphertext boundary, the single-file data path, the fractal walk, and the five user flows",
    summary="Drawn so it is obvious from the diagram alone that the server cannot read: the browser holds the key and does everything a forge does — derive ids, decrypt, walk trees, diff, render, merge — while only ciphertext and client-computed names cross the boundary. The server's entire read surface is one GET of a name it cannot interpret; it cannot distinguish a public vault from a private one because the bytes are identical. The single-file data path is the whole system in miniature (rendered below as a sequence diagram), with two shipped optimisations — the per-path index turning path resolution into one request, and sparse fetch making the honest performance claim true. Then the fractal walk (visited set, depth bound) and the five user flows, including the key-supply ladder and the vault-key refusal.",
    concepts=[
     ("The ciphertext boundary", None, "one GET of a client-computed name is the whole read surface; every response is opaque bytes — the hub cannot tell a file from a folder"),
     ("The key-supply ladder", "mockups.html", "fragment → stored (opt-in) → key service → paste as a chosen fallback, never the default; strip the fragment once read, never store without asking"),
     ("Scales with what you look at", None, "sparse by default plus the per-path index — the claim is only honest if the interface actually behaves that way"),
    ],
    ideas=[
     "Proposing a change needs no credential on the target vault at all — the inverse of the CI problem, and the reason it is the easy case.",
     "More of the substrate is shipped than the briefing pack assumes: the hub is assembly, not construction.",
     "Branch and merge already exist client-side; the write is the only step that needs the write key.",
    ]),
   dict(slug="permissions-topology", file="04__permissions-topology.md",
    title="04 — Permissions as key topology",
    role="Possession is access: the four key positions, worked topologies, the missing-primitive options, and CI by scope",
    summary="The part most likely to be got wrong, because it inverts a forge assumption: permissions here are not a policy a server enforces — possession of a key is access, there is no referee, and a cryptographic boundary has no bypass. It must be designed in advance, and revocation is not retroactive. Four positions exist today (vault key, read key, structure key, no key = custody), each derived one-way so the weaker discloses nothing about the stronger. Worked topologies for an open-source project, a mostly-private company estate, and a contractor — all expressible now as separate vaults plus key tiers. Then the missing primitive's three options: A, separate vaults plus a link convention (recommended — the fractal edge applied inside a vault, no format change); B, nested sub-vaults with derived keys (a real protocol project); C, per-path content keys (breaks CAS dedup — not recommended). CI is the genuine hole: a runner must read, and the model-consistent answer is a scoped vault, whose open question is who assembles it.",
    concepts=[
     ("The four key positions", "capability-audit.html", "vault, read, structure, none — a ladder of one-way derivations; handing out the weaker key reveals nothing about the stronger"),
     ("Option A: separate vaults + a link convention", None, "the same mechanism the fractal already needs, applied inside a vault; small, honest, and buildable today — B should not gate the hub"),
     ("Revocation is not retroactive", None, "rotating a key protects future commits and returns nothing already taken; a git-hosted publication cannot revoke read access at all (measured)"),
    ],
    ideas=[
     "A shape you can see is easier to audit than a table of rules nobody has read — the honest counterweight to granularity costing structure.",
     "The hub as a useful index of things it cannot read is the shape most organisations actually have.",
     "Publish the two hard limits; do not let users discover them.",
    ]),
   dict(slug="commercialisation", file="05__commercialisation.md",
    title="05 — Commercialisation",
    role="What you can charge for when you cannot read: the inversion, four honest revenue lines, what must never be monetised",
    summary="GitHub's original product was private repositories — a policy the host maintains and charges for, possible because the server can read. On a blind host privacy is the default and costs nothing, so it cannot be the product: a positioning gift, but it forces the revenue onto what a blind host genuinely provides. Four lines: durability and availability (with the warning that ciphertext neither compresses nor deduplicates, so the economics are not a code host's — unmodelled since 14 Aug); namespace and identity (who may publish to acme/ — the one identity question, a write-path product, exactly what registries charge for); discovery and curation across published-key vaults (the only reading feature that exists); and scoped CI, the one key-holding service, defensible only when scoped and said out loud. The fractal changes the market from &ldquo;who hosts your repos&rdquo; to &ldquo;whose hub do you appear in&rdquo;; escrow of the write key is an enterprise product whose selling point is the operator's inability to read.",
    concepts=[
     ("Privacy cannot be the product", None, "the bytes for a public and a private vault are identical — there is no private tier to sell because there is no public tier to downgrade from"),
     ("The one identity question", None, "reading needs no identity; who may publish to this namespace is the write-path question, and the answerable one"),
     ("Escrow before publishing", "roadmap-and-open.html", "a vault whose write key is lost is frozen — readable forever, never updatable; escrow is a precondition, not good practice"),
    ],
    ideas=[
     "&ldquo;We cannot sell you privacy, because you already have it&rdquo; — and the four things sold instead, with the host still unable to read a byte.",
     "The estate's shape is disclosed to the operator unavoidably; selling it is a choice that would poison the pitch.",
     "No lock-in by design means retention is earned every year — the artefact is a folder anyone can copy.",
    ]),
   dict(slug="mockups", file="06__mockups.md",
    title="06 — Interface mockups",
    role="The one screen that matters (the live ciphertext panel), the hub index's four row states, key handling, fork = rekey",
    summary="A familiar thing on unfamiliar foundations: forge conventions are followed everywhere, and the novelty budget is spent on exactly two things — the ciphertext panel and the tier indicators. The panel is the screen the specification says must be designed in, not bolted on: while a visitor reads a file, it lists the actual requests the page made — names, sizes, opaque bytes — which makes it an argument rather than a marketing claim. The hub index renders four row states (readable, listed-only, structure-visible, and hub — the fractal edge), with mirror offered on every row including the ones you cannot read. The private-vault open flow carries the vault-key refusal word for word, and the fork screen states the measured properties: a rekey turns over 100% of object ids, and forks share zero identifiers.",
    concepts=[
     ("The live ciphertext panel", None, "lists the requests this page actually made, all opaque — far more persuasive than any page explaining zero knowledge"),
     ("Four row states", None, "readable, listed-only, structure-visible, hub — the affordances differ by what you hold, and the tier you are in is always visible"),
     ("Custody without access is a capability", None, "mirror appears on rows you cannot read — holding and verifying ciphertext needs no trust and no key"),
    ],
    ideas=[
     "The structure-key screen is buildable today, and no conventional forge can express it.",
     "Never imply a capability that does not exist: no revoke button, no search box that silently searches only what you hold.",
     "Show the head's age — freshness is the reader's problem, so the interface must surface it.",
    ]),
   dict(slug="roadmap-and-open", file="07__roadmap-and-open.md",
    title="07 — Roadmap & open questions",
    role="Build order 0–10, the four absences stated plainly, blocking / important / answered questions, what each team owes",
    summary="The build order runs from the two audits (step 0, blocking) through the public read-only forge view, the private-vault view (the step that makes it a forge rather than a gallery), the ciphertext panel, hub-as-vault, fractal navigation, and structure-key views, to issues, change proposals, discovery and scoped CI. Four absences are stated rather than deferred — cross-vault search without keys, CI, server-enforced granular permissions, content-triggered notifications — each with its reason. Open questions are split into blocking (the sub-vault decision, the web audit, storage economics), important (catalogue schema, discoverability, abuse handling on unreadable content, operational commitments), and answered since the briefing pack was written — including the measurement that content-addressed ids do not survive a rekey, so a private fork of a public template leaks nothing and no protocol change is needed.",
    concepts=[
     ("The four absences", None, "naming them is what makes the pack credible — the same discipline as this site's where-our-approach-loses page"),
     ("Answered by measurement", "../../collection/index.html#attribute", "two vaults holding the same document share zero object ids; a rekey turns over 100% — settling an open protocol question, and making template-diffing by identifier impossible"),
     ("Do not call components &ldquo;plugins&rdquo;", "../../documents/ambient-authority.html", "that word already means a capability grant in this product, and the runtime ships a deny-by-default permission model on that basis"),
    ],
    ideas=[
     "Publishing a vault is publishing a repository: once the key is out, clones cannot be recalled — the difference is that the host still cannot read it.",
     "Step 5, fractal navigation, is the one that turns a product into an ecosystem.",
     "Abuse handling on unreadable content needs a stated policy before launch: the unit of action is the vault, not the file.",
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
  <span class="k">Date</span><span class="v">{date}</span>
  <span class="k">Origin</span><span class="v">{origin_short}</span>
  <span class="k">Source</span><span class="v"><a href="src/{file}">raw markdown</a> · <a href="{gh_base}{file}">original on GitHub</a></span>
  <span class="k">Captured</span><span class="v">{captured}, at commit <a href="{commit_url}"><code>{commit}</code></a> — the raw file under <code>src/</code> is byte-identical to that commit</span>
</div>
{explainer}
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
<meta name="description" content="{meta_desc}">
<link rel="canonical" href="https://nhi.sgit.ai/packs/{pack}/index.html">
<link rel="stylesheet" href="../../assets/site.css">
</head>
<body>

{nav}

<main class="doc">
<div class="crumb"><a href="../../index.html">nhi.sgit.ai</a> / <a href="../index.html">packs</a> / {pack}</div>
<h1>{pack_name}</h1>
<p class="lead">{three}</p>

<div class="note"><b>Origin.</b> {origin} Captured {captured} at commit <a href="{commit_url}"><code>{commit}</code></a>: the raw sources under <code>src/</code> are byte-identical to that commit's tree — verify with a diff against it. Each document below has a reader page with the same apparatus as the site's <a href="../../documents/index.html">documents</a>.</div>

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

def explainer_html(d):
    ex = d.get("explainer")
    if not ex:
        return ""
    title, paras = ex
    body = "\n".join(f"<p>{p}</p>" for p in paras)
    return f'\n<h2 id="explainer">{title}</h2>\n<div class="note">\n{body}\n</div>\n'

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
            date=pack["date"], origin_short=pack["origin_short"], gh_base=pack["gh_base"],
            commit=pack["commit"], commit_url=pack["commit_url"], captured=pack["captured"],
            explainer=explainer_html(d),
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
        commit=pack["commit"], commit_url=pack["commit_url"], captured=pack["captured"],
        meta_desc=pack["meta_desc"],
        readme=pack["readme"], rows="\n".join(rows), first=docs[0]["slug"])
    (pdir / "index.html").write_text(hub)
    print(f"wrote packs/{pack['slug']}/index.html")
    section_rows.append(f'    <tr><td><a href="{pack["slug"]}/index.html"><b>{html.escape(plain)}</b></a></td><td>{pack["row_date"]}</td><td>{pack["one_line"]}</td></tr>')

sec = SECTION_HUB.format(nav=nav_for(1, SITE_VERSION), footer=footer_for(1, SITE_VERSION),
                         rows="\n".join(section_rows))
(ROOT / "packs" / "index.html").write_text(sec)
print("wrote packs/index.html")
print(f"packs section at {SITE_VERSION}")
