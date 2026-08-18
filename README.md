# nhi.sgit.ai — non-human identity, blast radius and agentic security

The site's thesis: the question "how do I give an identity to my agents?" splits into
**agents you run** and **agents you rent** — and the industry only answers the first.
For rented agents (hosted coding assistants, chat interfaces, API-run agents) there is
no way to issue a scoped, short-lived, attested identity today; the honest current
practice is to hand over a broad credential and hope.

Live site: https://nhi.sgit.ai (GitHub Pages, deployed from `dev`).

## Structure

- `index.html` — front page: the thesis leads
- `thesis/` — the two-populations argument, with citations
- `hope/` — hope-driven development: concepts and the workflows that replace hope
- `method/` — the research method: one scenario, same columns, published before findings
- `options/` — dated option assessments (SPIFFE, commercial broker, do-nothing baseline)
- `collection/` — the published corpus, organised by question
- `frameworks/aomm.html` — the Agentic Outbound Maturity Model, promoted to a page
- `infographics/` — the request list for the published LinkedIn infographics
- `about/participant.html` — the participant disclosure, and where our approach loses
- `admin/` — engineering: comms (tasks & requests), versions, build tooling
- `assets/site.css` — shared stylesheet (sgit.ai design language)

## Release process

1. Bump `admin/build/version.txt` (vX.Y.Z, exactly once per release) and add a row to
   `admin/versions.html`; update `admin/comms.html`.
2. `node admin/build/validate.js`
3. `git commit -am "site vX.Y.Z: ..." && git push origin dev`

Every push to `dev` runs `.github/workflows/deploy-pages.yml`: validate → auto-tag
(`vX.Y.Z`, verified against version.txt and the commit subject, next-minor enforced) →
deploy to GitHub Pages. Same pipeline as
[SGit-AI__Website](https://github.com/SGit-AI/SGit-AI__Website).

All content CC BY 4.0 unless noted. Code under the repository licence.
