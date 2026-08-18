# nhi.sgit.ai — the question splits into two populations, and the industry only answers one

> "How do I give an identity to my agents?" splits into **agents you run** and **agents
> you rent** — and everything the industry sells assumes the first, while every agent
> people actually name is the second. For those, the honest current answer is: hand over
> a broad credential, and hope.

*Source: <https://nhi.sgit.ai/index.html> · site v0.1.10 · markdown twin of the front page.*

---

## Two populations, one question

| | Agents you run | Agents you rent |
|---|---|---|
| Where it executes | Your infrastructure | Somebody else's |
| Can you attest the workload? | Yes — that is the mechanism | **No** |
| Can you install an identity agent? | Yes | **No** |
| What you control | Everything | **The credential you hand over** |
| Industry answer | Mature, and expensive | **None** |

For the first population, an open standard (SPIFFE) issues short-lived cryptographic
identities based on workload attestation — described by practitioners as a multi-year
engineering project needing a dedicated team. For the second, the equivalent capability
is an open feature request. [The full argument, with citations](thesis/index.html).

## Hope is not a control

When you hand an agent a broad credential you are making two hopes: that it will not
misuse what it holds, and that it will not find the rest of what that credential
actually reaches. Neither hope changes your accountability.
[The Hope section — concepts and workflows](hope/index.html).

## The research

Not a vendor list. One scenario (four agents, four vaults, one repository, nobody able
to use another's access), the same columns per option, privileges granted as the
differentiating column, a verification date on everything.

- [The method, published before the findings](method/index.html)
- [SPIFFE / SPIRE — the open standard](options/spiffe.html)
- [A commercial workload-identity broker](options/broker.html)
- [Do nothing — broad credential + hope](options/do-nothing.html)

## The collection

- [Organised by question](collection/index.html)
- [The Agentic Outbound Maturity Model](frameworks/aomm.html)
- [Infographics](infographics/index.html)

## Who is writing this

This site is published by the sgit project; vaults are a candidate answer to part of the
question studied here. [The participant disclosure, including where our own approach
loses](about/participant.html).

## Site

- [Comms: tasks & requests](admin/comms.html)
- [Release history](admin/versions.html)
- [llms.txt](llms.txt)
