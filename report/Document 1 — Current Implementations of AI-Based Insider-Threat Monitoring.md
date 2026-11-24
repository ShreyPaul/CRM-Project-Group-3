Three vendors market tools that analyse employee communications to flag potential insiders. Descriptions below follow the vendors' own materials; comments are ours.

## Proofpoint — Insider Threat Management
Explicitly uses **sentiment analysis** on workplace communications so security teams can understand the motive and emotional state behind anomalous actions, helping identify disgruntled employees who may pose a malicious threat (Proofpoint, n.d.).

**Our comment:** Directly matches our traitor scenario. However, MITRE reports that language and sentiment analysis has not shown strong proactive detection and produces many irrelevant alerts (MITRE Insider Threat Research & Solutions, n.d.). Privacy practices: **[blank — not in source]**.

## Securonix — "Insider Threat Psycholinguistics"
Analyses language and communication patterns across the enterprise; identifies deviations in **linguistic tone** that correlate with behavioural shifts indicative of sabotage or espionage (Securonix, n.d.).

**Our comment:** Relevant to our administrator-sabotage scenario (S3). Our source notes record that details on *when exactly* messages/emails are monitored are not available — a gap that matters for our privacy concern.

## Living Security — Human Risk Management (HRM)
Uses predictive analytics and psycholinguistic monitoring to detect shifts in word choice and tone that precede insider incidents; argues that a **psychological baseline** per user is critical to prevent threats before data exfiltration occurs (Living Security, n.d.).

**Our comment:** Our source notes record that the material analyses user messages/email to determine threat, with **no mention of privacy** — so it does not address the issue at the centre of our project.

## Cross-vendor assessment (our comments)
- All three rely on sentiment/psycholinguistic signals; MITRE's caveat above applies to all of them.
- Rare attacks plus imperfect detectors mean most alerts can be false (base-rate fallacy; see Document 2 and Axelsson, 2000).
- Our source notes do not document Regime-C-style privacy or anonymisation checks for any of these products.

## Research datasets used for ML-based detection
Dataset descriptions in our source use numbered entries from an unnamed survey; full bibliographic details are **[blank — not in source]**.

| Dataset | Key facts | Our comment |
|---|---|---|
| Enron email | ~500,000 emails, 150 employees, 2000–2002; email content and social-network interactions | Real-world data, but **no ground-truth labels** for malicious activity |
| CERT (CMU SEI) | Synthetic; traitor and masquerader instances; five log files (logon/logoff, email, web, removable media, thumb drives); `psychometric.csv` with Big Five traits. r4.2 "dense"; r6.2 "sparse" (5 insiders of 3,995 users, Jan 2010–Jun 2011, ~40,000 activities/employee); includes disgruntled-employee theft, admin sabotage, unauthorised access | Labelled and behaviourally rich, but simulated; r6.2's rarity of insiders mirrors the base-rate problem |
| TWOS (Wolf of SUTD) | SUTD competition, March 2017; six sources (keystrokes, screen, cursor, emails, logins, network traffic); personality assessments; 24 users over 5 days; 12 masquerader instances (90 min each), 5 traitor instances (120 min each) | Multi-modal plus psychology, but very small and short |

## References
Axelsson, S. (2000). The base-rate fallacy and the difficulty of intrusion detection. *ACM Transactions on Information and System Security, 3*(3), 186–205. https://doi.org/10.1145/357830.357849

Living Security. (n.d.). *Predict insider threats AI* [Blog post]. https://www.livingsecurity.com/blog/predict-insider-threats-ai

MITRE Insider Threat Research & Solutions. (n.d.). *Guiding principles*. https://insiderthreat.mitre.org/guiding-principles/

Proofpoint. (n.d.). *Insider threat management* [Solution brief]. https://www.proofpoint.com/sites/default/files/solution-briefs/pfpt-en-sb-insider-threat-management.pdf

Securonix. (n.d.). *Insider threat psycholinguistics* [Blog post]. https://www.securonix.com/blog/insider-threat-psycholinguistics/

---

