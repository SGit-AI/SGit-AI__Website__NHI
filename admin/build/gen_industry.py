#!/usr/bin/env python3
"""Generates the industry/ provider profile pages from one data structure.

Run from anywhere: python3 admin/build/gen_industry.py
Writes industry/<slug>.html for every provider below. The hub (industry/index.html)
and the SPIFFE concept page (industry/spiffe.html) are authored by hand — this
script only owns the per-provider profiles, so they stay uniform and re-generable.

Profile data is drawn from the two published analyses the site cites (the Aembit
vendor guide and the 2026 NHI tools survey) — attribution is stamped on every page.
"""
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "industry"
SITE_VERSION = (ROOT / "admin/build/version.txt").read_text().strip()
DATE_VERIFIED = "18 August 2026"

GROUPS = {
    "governance": "NHI discovery, posture & governance",
    "workload-iam": "Workload IAM & runtime access",
    "secrets": "Secrets management & detection",
    "machine-id": "Machine identity & certificates",
    "human-iam": "Human IAM platforms extending to agents",
}

PROVIDERS = [
 dict(slug="astrix", name="Astrix Security (Cisco)", group="governance",
  tagline="Discovery and governance of non-human identities, from shadow agents to retirement",
  what="Astrix discovers non-human identities and shadow agents across SaaS and cloud, maps what each can access, flags risky and over-privileged connections, and governs identities from deployment through retirement. Its Agent Control Plane adds short-lived credential provisioning and scoped access for AI agents. Acquired by Cisco.",
  caps=["NHI and shadow-agent discovery across SaaS and cloud", "Privilege analysis and risk flagging", "Lifecycle governance: deployment through retirement", "Agent Control Plane: short-lived credentials, scoped access", "Audit"],
  fits="The discovery-and-posture layer of a mature NHI programme. The cited analysis notes the open question of provisioning-time controls versus runtime enforcement during resource requests.",
  rented="Discovery and governance cover the credentials rented agents hold — finding them, scoping them, retiring them — without being able to attest the agent itself. Governance of the hope, not replacement of it.",
  pricing="Not published; enterprise sales.",
  links=[("Vendor site", "https://astrix.security")]),
 dict(slug="entro", name="Entro Security", group="governance",
  tagline="Secrets-centric NHI security: where every secret lives, who owns it, what it reaches",
  what="Entro takes a secrets-first approach to NHI security: mapping agents to credentials, tracing where secrets live and who owns them, detecting exposure, managing posture, and monitoring behaviour for detection and response.",
  caps=["Agent-to-credential mapping", "Ownership tracking", "Secrets exposure detection", "Posture management", "Behaviour monitoring, detection and response"],
  fits="Discovery-and-posture layer, entered through the secrets. The cited analysis notes it may need pairing with separate workload authentication and preventive access enforcement.",
  rented="Directly relevant to the do-nothing baseline: it finds and tracks the broad credentials rented agents already hold. Visibility over the hope rather than a scoped identity.",
  pricing="Not published; enterprise sales.",
  links=[("Vendor site", "https://entro.security")]),
 dict(slug="oasis", name="Oasis Security", group="governance",
  tagline="One programme for service accounts, machine identities and AI agents",
  what="Oasis runs NHI discovery and lifecycle governance — discovery, posture, rotation, decommissioning — and extends it with agentic access management: intent-aware policy, short-lived session identities, time-bound access, and continuous audit.",
  caps=["NHI discovery and inventory", "Lifecycle governance: posture, rotation, decommissioning", "Intent-aware policy for agents", "Short-lived session identities, time-bound access", "Continuous audit"],
  fits="Spans the discovery-and-posture layer and part of agent access control. The cited analysis notes integration availability and credential-type support vary by application and infrastructure.",
  rented="Short-lived session identities and time-bound access narrow what a rented agent holds where integrations exist; the attestation gap remains structural.",
  pricing="Not published; enterprise sales.",
  links=[("Vendor site", "https://oasis.security")]),
 dict(slug="token-security", name="Token Security", group="governance",
  tagline="Machine-first identity security across hybrid environments",
  what="Token Security approaches identity machine-first: coverage of non-human identities across hybrid environments, with an AI and automation focus in how identities are discovered, contextualised and secured.",
  caps=["Machine-first NHI discovery", "Hybrid environment coverage", "AI/automation-focused identity security"],
  fits="Discovery-and-posture layer, per the 2026 NHI tools survey.",
  rented="As with the category: visibility and governance over the credentials rented agents hold, not attestation of the agent.",
  pricing="Not published; enterprise sales.",
  links=[("Vendor site", "https://token.security")]),
 dict(slug="veza", name="Veza (ServiceNow)", group="governance",
  tagline="The authorization graph: who — human or not — can do what, where",
  what="Veza builds an authorization graph of effective permissions: identity discovery, entitlement analysis, excessive-access identification, ownership, and least-privilege governance, extended with AI agent controls. Acquired by ServiceNow.",
  caps=["Authorization graph of effective permissions", "Identity discovery and entitlement analysis", "Excessive-access identification", "Ownership and least-privilege governance", "AI agent controls"],
  fits="Access intelligence over the whole estate — closest of the category to computing the authorization closure this site's Hope section describes. The cited analysis notes it shows the permission landscape but needs separate systems for workload authentication and live enforcement.",
  rented="Mapping what a rented agent's credential actually reaches is exactly the closure/delta exercise — visibility of the blast radius, not a new identity for the agent.",
  pricing="Not published; enterprise sales.",
  links=[("Vendor site", "https://veza.com")]),
 dict(slug="sailpoint", name="SailPoint", group="governance",
  tagline="Identity governance extended to agents: ownership, certification, lifecycle",
  what="SailPoint's Agent Identity Security applies its identity-governance machinery to agents: discovery, accountable ownership, access-pathway mapping, entitlement certification, and lifecycle governance alongside human and non-human identities.",
  caps=["Agent discovery and inventory", "Accountable ownership", "Access-pathway mapping", "Entitlement reviews and certification", "Lifecycle governance"],
  fits="Governance layer. The cited analysis notes governance establishes approved access; a separate control must apply those decisions when the agent actually connects.",
  rented="Ownership and lifecycle governance are precisely what the CSA survey found missing for agent identities; applies to rented agents' credentials as records, not to the agents as workloads.",
  pricing="Not published; enterprise sales.",
  links=[("Vendor site", "https://www.sailpoint.com")]),
 dict(slug="aembit", name="Aembit", group="workload-iam",
  tagline="Secretless, policy-based access for workloads and agents at runtime",
  what="Aembit does runtime workload IAM: authenticating workloads, evaluating contextual access policies, and delivering credentials just-in-time so applications and agents hold no stored secrets. Includes blended human-agent identity and an MCP Identity Gateway for agent tool calls.",
  caps=["Workload authentication", "Contextual, policy-based access", "Just-in-time credential brokering — no standing secrets", "Blended human-agent identity", "MCP Identity Gateway"],
  fits="The workload-IAM and runtime-control layer — the commercial buy-side of what SPIFFE standardises, assessed on this site as the broker option. The cited analysis (Aembit's own) notes organisations wanting deep discovery or governance may pair it with IGA/NHI tools.",
  rented="The attestation still happens in infrastructure you control; for rented agents the gateway pattern mediates tool calls without attesting the agent itself. Partial — the assessment is on the options page.",
  pricing="Not published; enterprise sales.",
  links=[("Vendor site", "https://aembit.io"), ("Our option assessment", "../options/broker.html")]),
 dict(slug="hashicorp-vault", name="HashiCorp Vault (IBM)", group="secrets",
  tagline="The reference secrets manager: store, issue, rotate, audit — now issuing SPIFFE identities",
  what="Vault centralises secrets: storage, rotation, on-demand dynamic credentials, encryption as a service, and audit of client interactions. It now natively issues SPIFFE-based workload identities for non-human workloads including agents, bridging the secrets layer and the workload-identity layer.",
  caps=["Centralised secrets storage and rotation", "Dynamic, on-demand credentials", "Encryption as a service", "Audit of client interactions", "Native SPIFFE workload identity issuance"],
  fits="The secrets layer. The cited analysis is candid: it manages credentials rather than eliminating them, and does not by itself establish agent identity, preserve user context, or enforce contextual access policy.",
  rented="A rented agent given a Vault token is still holding a bearer credential — narrower and rotatable, which shrinks the hope without removing it.",
  pricing="Open-source edition free; HCP Vault and enterprise tiers priced on the vendor's published pricing page.",
  links=[("Vendor site", "https://www.hashicorp.com/products/vault"), ("SPIFFE for agentic AI (vendor post)", "https://www.hashicorp.com/en/blog/spiffe-securing-the-identity-of-agentic-ai-and-non-human-actors"), ("Our SPIFFE page", "spiffe.html")]),
 dict(slug="cyberark", name="CyberArk (Palo Alto Networks)", group="secrets",
  tagline="Privileged access and machine identity at enterprise scale: Conjur, Venafi, and agent discovery",
  what="CyberArk's portfolio spans privileged access management, Conjur secrets management integrated with its PAM ecosystem, and the Venafi machine-identity line (TLS and code-signing certificate lifecycle automation). The Aembit vendor guide lists the line (as 'Idira') under Palo Alto Networks ownership, with agent discovery and an identity broker for MCP servers.",
  caps=["Privileged account management", "Conjur secrets management", "Venafi: certificate lifecycle automation", "Machine and workload identity", "Agent discovery; identity broker for MCP servers"],
  fits="PAM plus the secrets layer plus machine identity. The cited analysis suits it to agents needing privileged access to infrastructure and sensitive systems; the reach of controls beyond privileged workflows to routine agent access is the open question it names.",
  rented="Privileged-access workflows gate what a rented agent's credential can invoke; the agent itself remains unattested.",
  pricing="Not published; enterprise sales.",
  links=[("Vendor site", "https://www.cyberark.com")]),
 dict(slug="akeyless", name="Akeyless", group="secrets",
  tagline="SaaS-delivered secrets and key management, multi-cloud",
  what="Akeyless delivers secrets management as SaaS: vaultless-architecture secrets, key management, and multi-cloud scaling without self-hosting the secrets infrastructure.",
  caps=["SaaS secrets management", "Key management", "Multi-cloud scaling"],
  fits="The secrets layer, bought rather than run — relevant where the SPIFFE-style build-it path is too expensive.",
  rented="Same shape as the category: narrower, rotatable credentials for rented agents; no attestation.",
  pricing="Published tiers on the vendor's pricing page, including a free tier.",
  links=[("Vendor site", "https://www.akeyless.io")]),
 dict(slug="gitguardian", name="GitGuardian", group="secrets",
  tagline="Finding the credentials that already leaked: code and pipeline secrets detection",
  what="GitGuardian scans code and pipelines for leaked credentials — the detection side of the secrets layer, and directly relevant to the incidents this site cites, where agent-driven CI workflows exposed secrets into logs and public repositories.",
  caps=["Secrets detection in code repositories", "Pipeline scanning", "Leaked-credential discovery and remediation workflows"],
  fits="Detection within the discovery-and-posture layer. Complements rather than replaces every other row of the stack.",
  rented="When a rented agent's broad credential leaks — the failure mode the Black Hat disclosure documents — detection is the compensating control.",
  pricing="Published tiers including a free tier for small teams; business tiers on the vendor's pricing page.",
  links=[("Vendor site", "https://www.gitguardian.com")]),
 dict(slug="keyfactor", name="Keyfactor", group="machine-id",
  tagline="PKI automation: short-lived certificates and crypto-agility at machine scale",
  what="Keyfactor automates PKI: certificate lifecycle at machine scale, short-lived certificates, and crypto-agility. The certificate half of machine identity — the layer a future agent-key registry (see this site's PKI section) would sit beside.",
  caps=["PKI and certificate lifecycle automation", "Short-lived certificates", "Crypto-agility"],
  fits="The machine-identity/certificates layer of the 2026 survey's map, alongside CyberArk's Venafi line.",
  rented="Certificates attest workloads you enrol — the run-your-own population again. The rented-agent key problem is the registry question, not the CA question.",
  pricing="Not published; enterprise sales. Open-source EJBCA community edition exists.",
  links=[("Vendor site", "https://www.keyfactor.com"), ("Our PKI section", "../pki/index.html")]),
 dict(slug="entra", name="Microsoft Entra (Agent ID)", group="human-iam",
  tagline="Agents as first-class identities inside the Microsoft ecosystem",
  what="Microsoft Entra extends its human IAM and workload identity platform to agents: Entra Agent ID gives agents identity blueprints, ownership, sponsorship, authentication and lifecycle governance — the platform-native answer for agents built through Microsoft 365, Azure and Copilot.",
  caps=["Agent identities with blueprints", "Ownership and sponsorship", "Authentication and conditional access", "Lifecycle governance", "Deep Microsoft 365 / Azure / Copilot integration"],
  fits="Human-IAM-extended layer. The cited analysis flags verification needed for non-Microsoft infrastructure and third-party SaaS coverage.",
  rented="The closest thing to per-agent identity for rented agents — when the agent is rented from Microsoft and stays inside the ecosystem. A platform answer, not a portable one: the boundary of the identity is the boundary of the platform.",
  pricing="Bundled with Entra/Microsoft 365 licensing; per-feature tiers on Microsoft's published pricing.",
  links=[("Vendor site", "https://www.microsoft.com/en-us/security/business/microsoft-entra")]),
 dict(slug="okta", name="Okta", group="human-iam",
  tagline="Managing agents through the same identity provider as your workforce",
  what="Okta extends its identity platform to AI agents: discovery, registration, ownership, risk analysis, access policy and lifecycle governance through the same provider and governance framework used for employees and applications, plus the Auth0 line for building agent-facing auth into applications.",
  caps=["Agent discovery and registration", "Ownership and risk analysis", "Access policy through the workforce IdP", "Lifecycle governance", "Auth0: auth for building agentic applications"],
  fits="Human-IAM-extended layer. The cited analysis asks how active workloads behind agents are authenticated and where policy enforces during tool calls.",
  rented="Registering rented agents in the workforce IdP gives them governed OAuth identities toward downstream apps — real progress on lifecycle and audit; the workload behind the token remains unattested.",
  pricing="Published per-user/per-MAU tiers for the workforce and customer identity products on the vendor's pricing pages.",
  links=[("Vendor site", "https://www.okta.com")]),
]

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{name} — industry profile · nhi.sgit.ai</title>
<meta name="description" content="{tagline}. Industry profile from published analyses: capabilities, which layer of the NHI stack it answers, what it means for rented agents, pricing and links.">
<link rel="canonical" href="https://nhi.sgit.ai/industry/{slug}.html">
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
  <a class="nl here" href="index.html">Industry</a>
  <a class="nl" href="../collection/index.html">Collection</a>
  <a class="nl" href="../frameworks/aomm.html">AOMM</a>
  <a class="nl" href="../pki/index.html">PKI</a>
  <a class="nl" href="../documents/index.html">Docs</a>
  <a class="nl" href="../packs/index.html">Packs</a>
  <a class="nl" href="../infographics/index.html">Infographics</a>
  <a class="nl" href="../admin/comms.html">Comms</a>
  <a class="gh" href="https://github.com/SGit-AI/SGit-AI__Website__NHI">★ GitHub</a>
</div></nav>

<main class="doc">
<div class="crumb"><a href="../index.html">nhi.sgit.ai</a> / <a href="index.html">industry</a> / {slug}</div>
<h1>{name}</h1>
<p class="lead">{tagline}. Group: <a href="index.html#{group}">{group_name}</a>.</p>

<div class="evbox ev-warn"><span class="evtag">Profile status</span>
<p>Compiled from published analyses — principally the <a href="https://aembit.io/blog/10-identity-security-vendors-for-ai-agents-strengths-tradeoffs-and-how-they-fit/">Aembit vendor guide</a> and the <a href="https://guptadeepak.com/top-non-human-identity-nhi-management-tools-2026/">2026 NHI tools survey</a> — and the vendor's own materials. <b>Date verified: {date}.</b> Not a hands-on assessment; capabilities and pricing move monthly and corrections are welcome via <a href="../admin/comms.html">comms</a>.</p></div>

<h2 id="what">What it does</h2>
<p>{what}</p>

<h2 id="caps">Key capabilities</h2>
<ul>
{caps}
</ul>

<h2 id="fits">Which part of the question it answers</h2>
<p>{fits}</p>

<h2 id="rented">And for rented agents?</h2>
<p>{rented}</p>

<h2 id="pricing">Pricing</h2>
<p>{pricing}</p>

<h2 id="links">Links</h2>
<ul>
{links}
</ul>

<div class="pagenav">
  <a href="index.html">← Industry map</a>
  <a href="../method/index.html">Our method →</a>
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
    <a href="index.html">Industry</a>
  </div>
  <div>
    <h4>The collection</h4>
    <a href="../collection/index.html">By question</a>
    <a href="../frameworks/aomm.html">The AOMM</a>
    <a href="../hope/index.html">Hope</a>
    <a href="../pki/index.html">PKI</a>
  </div>
  <div>
    <h4>Site</h4>
    <a href="../admin/comms.html">Comms</a>
    <a href="../admin/versions.html">Versions</a>
    <a href="../llms.txt">llms.txt</a>
    <a href="https://sgit.ai">sgit.ai</a>
  </div>
</div></footer>

</body>
</html>
"""

def li(items):
    return "\n".join(f"  <li>{i}</li>" for i in items)

def links_li(links):
    return "\n".join(f'  <li><a href="{u}">{html.escape(t)}</a></li>' for t, u in links)

OUT.mkdir(exist_ok=True)
for p in PROVIDERS:
    page = PAGE.format(
        name=html.escape(p["name"]), tagline=p["tagline"], slug=p["slug"],
        group=p["group"], group_name=GROUPS[p["group"]], ver=SITE_VERSION,
        date=DATE_VERIFIED, what=p["what"], caps=li(p["caps"]), fits=p["fits"],
        rented=p["rented"], pricing=p["pricing"], links=links_li(p["links"]))
    (OUT / f"{p['slug']}.html").write_text(page)
    print(f"wrote industry/{p['slug']}.html")
print(f"{len(PROVIDERS)} provider profiles at {SITE_VERSION}")
