---
title: "Personal data, PIPL and getting data out of China"
description: "The three laws, the lawful bases, and the three routes for moving personal data abroad — with the thresholds that decide which route applies."
category: "Compliance"
layer: 5
answer: "PIPL requires a lawful basis, a Chinese-language notice, separate consent for sensitive data, and a mechanism for any export: a CAC security assessment, a filed standard contract, or certification. Small-scale exports are exempt under the 2024 relaxation, but the thresholds are per-year and easy to cross. Sensitive data and important data change the analysis completely."
updated: 2026-11-23
read: 10
---

China's data rules are three laws that stack:

- **Cybersecurity Law (CSL, 2017)** — network operators, security obligations, the foundation.
- **Data Security Law (DSL, 2021)** — data classification, important data, state authority over data.
- **Personal Information Protection Law (PIPL, 2021)** — the GDPR-shaped personal data statute, with Chinese characteristics.

For a foreign-founded company the practical questions are: what may I collect, what must I tell people, and how do I move data across the border.

## Lawful basis and notice

PIPL requires one of several bases: consent, necessity to perform a contract with the individual, legal obligation, public interest, public health or emergency, and a few others. In practice, most consumer products rely on consent, and consent has to be informed, voluntary and specific.

The notice must be in Chinese, clear, and cover:

- The identity of the processor and contact details.
- What is collected, for what purpose, and how it is used.
- Retention periods.
- How individuals exercise rights.
- Who it is shared with, including overseas recipients.
- The export mechanism, where data leaves China.

**Sensitive personal information** — biometrics, religious belief, specific identity, medical health, financial accounts, whereabouts, minors under 14 — needs separate consent and a necessity justification. Minors under 14 require guardian consent and a dedicated processing rule.

Individuals have rights to access, copy, correct, delete, restrict, port and object, and to an explanation of the processing rules. You need a working process, not just a policy page.

## The three export routes

| Route | Who it applies to | What it involves |
|---|---|---|
| CAC security assessment | Important data, data processed by a CIIO, or personal data above the volume thresholds | Application to the provincial CAC, security self-assessment, contracts, review |
| Standard contract | Personal data below the assessment thresholds, not important data | Sign the CAC template with the overseas recipient, file it with the provincial CAC, complete a personal information protection impact assessment |
| Certification | Voluntary route via an accredited institution | Certification of the processing and the overseas recipient |

The assessment thresholds matter. Under the March 2024 relaxation, a security assessment is triggered when an operator exports personal data of more than **one million individuals** in a calendar year (cumulatively), or sensitive personal data of more than **10,000 individuals**, or important data of any amount. Below that, the standard contract route is available, and small exports are exempt entirely:

- Non-sensitive personal data of fewer than 100,000 individuals in a year: no assessment, no filing.
- Sensitive personal data of fewer than 10,000 individuals in a year: no assessment — but the other PIPL obligations still apply.

These thresholds are per calendar year and cumulative, not per transfer. A company that starts small can cross them quietly in month nine.

:::warn
"Important data" is not defined by volume. It is defined by catalogue and by impact on national security and public interest — and the catalogues are still being issued sector by sector. If your data could plausibly be important (maps, transport, health, population, critical infrastructure), assume the assessment route until a lawyer tells you otherwise.
:::

## Localisation

- **Critical information infrastructure operators** must store personal data and important data domestically, and go through the assessment to export.
- **Important data** must be stored domestically in general.
- For everyone else, localisation is not mandatory, but the export mechanism is.

## What to build

1. **A data map** — what you collect, where it is stored, who sees it, where it goes.
2. **A Chinese privacy notice** and consent flows, including separate consent for sensitive data and minors.
3. **Vendor contracts** with processors, including overseas group companies.
4. **A retention schedule** and deletion process.
5. **An incident response plan** — PIPL requires notification to individuals and the authority where harm is likely.
6. **A named person accountable** for data protection. PIPL requires a dedicated officer for processors above the CAC's volume threshold, currently set at one million individuals' personal data.

## Where foreign companies trip

- **HR data.** Employee data goes to the global HR system by default. That is an export, and consent from employees is a weak basis when the employer is the requester.
- **Support and CRM.** A global ticketing tool means every Chinese customer's message leaves the country.
- **Analytics and cookies.** Tracking scripts are processing, and the consent banner must be real.
- **Group access.** Engineers abroad accessing production data is an export even if nothing is "transferred" as a file.
- **Cloud region confusion.** A "China region" of a global cloud may still be operated by a local partner with separate rules — read the contract.

## Penalties

PIPL fines reach ¥50 million or 5% of the previous year's turnover for serious violations, with suspension of service and personal liability for responsible individuals. DSL penalties for data export violations are similarly severe. Enforcement has been uneven but is increasing, and the reputational cost of a public action is often larger than the fine.

:::checklist
- Data map completed before the product launches
- Chinese-language notice and consent flows reviewed against the actual data flows
- Sensitive data identified, with separate consent
- Export volumes tracked per calendar year against the thresholds
- Standard contract filed where applicable, with the impact assessment
- Group company access treated as an export
- Incident response and notification path defined
:::

Next: [the ICP question](/guides/icp-filing-and-hosting-in-china/), or [what you may claim in advertising](/guides/advertising-and-content-rules/).
