---
title: "ICP filing, hosting and why the server location matters"
description: "A website on a mainland server needs an ICP filing before it can resolve. A commercial one may need a licence that is effectively closed to foreign control. What each actually requires."
category: "Access"
layer: 2
answer: "Any site hosted on mainland Chinese servers must complete ICP filing with the telecom authority before it can be reached — three to six weeks, filed through the hosting provider. A site that sells, charges or runs ads also needs an ICP licence, which is practically unavailable to a foreign-controlled company. Hosting offshore avoids both, at the cost of speed and some integrations."
updated: 2026-11-23
read: 9
---

Two different permits get called "ICP", and confusing them wastes months.

- **ICP filing (ICP备案)** — a registration, required for any website or app served from mainland infrastructure.
- **ICP licence (ICP许可证)** — a commercial licence for internet information services, required for sites that charge users, sell advertising or operate a paid platform.

Most foreign founders need the first and cannot get the second in their own name.

## The filing

Filing is done through the hosting provider, not directly with the telecom administration. The provider verifies the company, the domain and the site, then submits to the provincial communications administration.

It requires:

- The business licence of a Chinese company — a foreign company cannot file.
- Legal representative's ID, and the site responsible person's ID. Some provinces accept a foreign passport for the site responsible person; many require a Chinese ID, which is why agencies offer a local responsible person.
- Domain registered in the company's name, with real-name verification completed.
- A hosting contract with a licensed provider, for a server in the mainland.
- A site that is actually built and reachable, with content that matches the declared purpose.
- Sometimes a premises photo and a phone verification.

Processing is usually 15–20 working days after the provider accepts the file, and providers commonly take a week to review before submitting. Plan three to six weeks end to end.

After the filing is approved, the site must display the filing number in the footer, linked to `beian.miit.gov.cn`. A **public security filing** (公安备案) is also required within 30 days of the site going live, through the local public security bureau's online system.

:::warn
Do not put the site live on a mainland server before the filing is approved. Providers will suspend the domain, and repeated violations can cost the account. Build and test on a staging domain that is not publicly indexed.
:::

## The licence

The ICP licence (增值电信业务经营许可证, commonly "ICP证") covers commercial internet information services: paid content, memberships, advertising sales, marketplace operation, paid services delivered online.

This is where foreign ownership bites. Value-added telecom is a restricted sector, foreign investment is capped and approval is discretionary, and in practice a foreign-controlled company rarely obtains an ICP licence on its own. Common workarounds:

- Operate through a domestic company with Chinese shareholders, with contracts that allocate economics but not control — the VIE pattern, which carries its own enforceability and regulatory risk.
- Use a licensed domestic partner for the commercial layer, and keep the foreign entity as a technology or content supplier.
- Structure the product so it is not an internet information service — for example, software licensed to a domestic distributor.

None of these is a casual decision. If the business depends on the licence, take advice before incorporating, not after.

## App filing

Mobile apps distributed in China also require filing, and app stores enforce it: an app without a filing number is removed or refused. The filing is tied to the company, the domain and the app's content category, and updates can require a new filing.

## Hosting offshore

A site on a server outside the mainland does not need an ICP filing. That is the main reason foreign companies start there.

The costs are real:

- Latency: 150–300ms round trips from Chinese cities, worse on mobile networks.
- Some Chinese cloud services, payment integrations and WeChat features require a domestic entity and a filed domain.
- The site may be slow or intermittently unreachable depending on routing.
- Users see a foreign experience, which affects trust and conversion.

A common pattern is a marketing site offshore, and a product or transactional site on a domestic entity with a filing and, where needed, a licence.

## What gets rejected

1. **Domain owner mismatch** — the domain is in the founder's name, not the company's.
2. **Content mismatch** — the declared purpose is "company website" but the site sells products or hosts user content.
3. **No real address** — the filing uses a virtual address the provider cannot verify.
4. **Site responsible person** — a foreign passport not accepted in that province, or no local contact.
5. **Hosting provider unlicensed** or the server outside the province the company is registered in.
6. **Trademark or name in the domain** that the company cannot show rights to.

## Sequence for a new company

| Week | Step |
|---|---|
| 1 | Domain registered in the company name, real-name verification |
| 1–2 | Mainland hosting purchased; site built and staged |
| 2–4 | Provider review and submission to the provincial administration |
| 4–6 | Filing approved; number displayed; public security filing started |
| 6+ | Payment, WeChat and other integrations that need a filed domain |
| As needed | ICP licence assessment if the model is commercial |

:::checklist
- Model classified first: corporate site, content site, or commercial platform
- Domain owned by the Chinese company, not the founder personally
- Hosting provider licensed and chosen before the site is built
- Site responsible person acceptable to the province
- Filing number displayed and linked; public security filing within 30 days
- App filing completed before store submission
- Licence question settled before the revenue model goes live
:::

Next: [data and personal information rules](/guides/data-compliance-pipl/), or [what the advertising rules allow you to claim](/guides/advertising-and-content-rules/).
