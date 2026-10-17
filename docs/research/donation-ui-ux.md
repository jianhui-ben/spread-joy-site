# Donation UI/UX for NGO sites: research for Spread Joy

Researched 2026-10-17. Labels: **Fact** (source states it), **Inference** (my reading of facts), **Rec** (recommendation). Vendor-biased sources are flagged "(vendor)". Several first-party pages could not be fetched (see Open questions), so some items rest on secondary reporting and are marked so.

## Constraints (from the repo)

- **Fact:** Static site pasted into Squarespace 7.1 blocks; custom JS only via Code Blocks and Code Injection, which needs a paid plan; Squarespace does not support custom code. The donate URL is still a placeholder (`href="#"`). (`README.md`, `docs/squarespace-setup.md`)

## Prioritized recommendations

1. **Rec: Start with Squarespace's native Donation block (Stripe-connected), not an embed.** It keeps the donor on-site, matches site styling, and needs no custom code. Fits the "paste blocks" model. Caveats below must be checked first (items 2 and 3).
2. **Rec: Test the native block's limits before committing.** Per Squarespace docs the checkout always requires email and phone, donors cannot give anonymously, recurring needs a customer account, recurring is Stripe or Squarespace Payments only, Apple Pay does not work for recurring, and transaction fees are not discounted for nonprofits. If these are dealbreakers, use a hosted/embedded tool (item 5).
3. **Rec: Offer monthly as a clearly presented choice, but do not pre-check it.** One-time/monthly toggle with monthly visually prominent and plain copy ("Cancel anytime"). Evidence for pre-selection is weak or vendor-only, and there is real refund/trust risk (see Recurring).
4. **Rec: Use 3 to 4 presets plus "other", with impact captions, and a mid-range default.** Do not set the lowest preset very low; low anchors lower average gift, and a higher first amount can reduce donor count. Pick amounts from what Spread Joy actually costs (e.g. "$X = N pairs of socks"), only if the numbers are true.
5. **Rec (fallback):** If native limits bite, link or iframe a nonprofit platform (Givebutter, Donorbox, Zeffy, or Stripe Payment Links for fixed amounts). Check each platform's fee/tip model; "free" platforms are funded by donor tips that may be pre-selected (vendor-contested, below).
6. **Rec: Put a donate button in the sticky header and every page, plus a short form or button above the fold on the Donate page.** Add trust block (legal status, tax-deductibility text, who receives the money, contact) next to the button.
7. **Rec: Build a real thank-you page and confirmation email** (impact message, share link, monthly upsell for one-time donors, receipt/tax info). Customize the Squarespace donation receipt email.
8. **Rec: Accessibility basics:** labelled fields, visible focus, targets at least 24x24 CSS px (WCAG 2.2 AA), no color-only state, no redundant re-entry. Native Squarespace checkout covers most of this; custom code blocks do not.

## 1. Squarespace-native vs embedded options

| Option | Fact (source) | Fit |
|---|---|---|
| Squarespace Donation block | Available on Basic/Core/Plus/Advanced; needs Squarespace Payments, Stripe or PayPal; suggested amounts set per fund; lightbox toggle; email + phone always required; no anonymous gifts; recurring only with Stripe/Squarespace Payments and a customer account; donors can optionally add a percent to cover fees; transaction fees not discounted for nonprofits ([Squarespace: Donation blocks](https://support.squarespace.com/hc/en-us/articles/206543967-Donation-blocks), [Donation funds](https://support.squarespace.com/hc/en-us/articles/31299996627213-Donation-funds)) | Best default |
| Squarespace Pay Links | Single-item products, donations or tips; no recurring ([Pay Links](https://support.squarespace.com/hc/en-us/articles/40399291492621-Create-and-manage-Pay-Links)) | One-time only |
| Stripe Payment Links | "Customers choose what to pay" is for donations but does not support recurring ([Stripe docs](https://docs.stripe.com/no-code/payment-links)); recurring link must be a fixed-amount product | Simple, but split into fixed monthly links |
| PayPal Giving Fund / Venmo | PayPal says PayPal Giving Fund charges charities and donors no fees, though some partner platforms may ([PayPal](https://history.paypal.com/cshelp/article/are-there-any-fees-charged-for-using-paypal-giving-fund--help207)); Venmo charity profiles require a PayPal charity account ([PayPal](https://paypal.com/us/cshelp/article/enable-your-charity-to-receive-donations-via-the-venmo-app-help888)) | Add as secondary button if eligible |
| Zeffy / Givebutter / Donorbox | Pricing varies; Zeffy and Givebutter rely on donor tips; Donorbox free plan has a platform fee ([comparison by Donately, a competitor (vendor)](https://www.donately.com/total-donor-cost); [Zeffy blog (vendor)](https://www.zeffy.com/blog/squarespace-donations)) | Fallback; verify current pricing on each vendor site |

- **Inference:** Squarespace's own help page says legacy blocks (added before 2024-07-08) lacked recurring and were replaced on 2026-09-30, so a new block should have recurring. Confirm in the editor.
- **Inference:** A hosted donate page on another domain (Classy, Givebutter) adds a redirect and a second brand; native keeps the donor on your domain, which helps trust, but loses platform features (donor CRM, tax-receipt automation).

## 2. Form patterns and placement

- **Fact:** MSF and Khan Academy use a short "choose an amount" widget with a one-time/monthly toggle on the main donate page ([MSF](https://give.doctorswithoutborders.org/campaign/675296/donate), [Khan Academy](https://donate.khanacademy.org/)); charity:water leads its donate page with monthly membership ("The Spring") and lists other methods lower down ([charity:water](https://www.charitywater.org/donate)). Page text fetched did not show the actual form fields, so exact steps are unverified.
- **Fact (vendor):** Fundraise Up case study claims landing-page conversion rose from about 6% to about 25% after adopting its overlay with wallets ([case study](https://fundraiseup.com/case-studies/Christian-Appalachian-Project/)). Single organization, vendor-reported, no method.
- **Inference:** Evidence for single-step vs multi-step is mostly vendor A/B tests with unclear transferability. Best-supported principle: ask for the amount first (low commitment), then contact/payment.
- **Rec:** Amount and frequency visible without scrolling on mobile; one primary button.

## 3. Amounts, defaults, anchoring

- **Fact:** Randomized field experiment, about 50,000 donors: both anchoring levers raised gift size, but only the size of the first (lowest) amount reduced likelihood of giving (Prokopec and de Bruyn, 2009, via [ESSEC listing](https://faculty.essec.edu/en/research/the-impact-of-anchors-on-donors-behavior-a-field-experiment); abstract only read).
- **Fact:** Tailoring suggested amounts to past giving raised donation amounts 22% in a 24,000-donor field test; raising the smallest suggestion raised gift size but lowered chance of giving (Liberali et al., via search summary of [IZA/ERIM listing](https://www.erim.eur.nl/research/events/detail/2036); abstract only). Requires donor history, so not applicable to a new site.
- **Fact (contrary):** Altmann et al. (2014) found defaults shift modal gifts but had no net effect on aggregate donations ([IZA DP 8680](https://www.iza.org/publications/dp/8680)). Goswami and Urminsky found low defaults can lower average gifts but raise donation rate, sometimes self-canceling.
- **Fact (vendor):** GlobalGiving test lab reports raising the default to the largest listed amount at or below $30 raised volume and average gift roughly 6 to 10% while cutting conversions slightly ([GlobalGiving](https://www.globalgiving.org/learn/?p=1556)). Page was not fetchable (403); figures are from a search summary, unverified.
- **Inference:** Presets shift behavior but net revenue effect is ambiguous; avoid very low anchors; do not expect a large win from default tuning. With a small donor base, A/B testing amounts will not reach significance.
- **Rec:** 4 presets, e.g. $10 / $25 / $50 / $100 plus "Other", default to the second. Replace with real unit-cost amounts.

## 4. One-time vs recurring

- **Fact:** M+R Benchmarks 2026 (2025 data, 180 participating nonprofits): monthly giving was 27% of online revenue (22% for small orgs, 37% for extra-large); DAF average gift $1,430 ([M+R Benchmarks fundraising chapter](https://mrbenchmarks.com/fundraising), [about page](https://mrbenchmarks.com/)). Secondary coverage of the 2025 edition cites monthly average gift $24 vs $126 one-time ([iDonate summary, vendor](https://idonate.com/blog/2025-mr-benchmarks-what-nonprofits-must-know-about-online-giving-and-donation-pages)); not confirmed in the primary report.
- **Fact (vendor, weak):** NextAfter test with monthly tab as default: 406 visitors, four recurring gifts vs none, labelled valid at 95.6% confidence by NextAfter; the page's 1.8% rate does not match 4/406 ([NextAfter experiment](https://www.nextafter.com/?p=49869)). Treat as anecdote. Other NextAfter posts reported large recurring lifts but statistically invalid results and a possible drop in one-time conversion ([summary](https://www.nextafter.com/?p=16793)).
- **Fact (contrary):** Pre-checked weekly recurring boxes on 2020 US campaign sites raised over $43M but raised refund requests by about $3M ([CEPR DP18599, Posner et al.](https://cepr.org/publications/DP18599)); the FEC recommended Congress ban pre-checked recurring boxes. Political context, but it shows the downside of defaults donors do not notice.
- **Inference:** Recurring share depends heavily on org size and audience; a new small NGO should expect a minority share. Monthly is worth encouraging, not forcing.
- **Rec:** Toggle labels "Give once" / "Give monthly"; show monthly with a short benefit line ("covers N kits every month, cancel anytime"); after a one-time gift, offer a monthly upgrade on the thank-you page. Make cancel path explicit (Squarespace donors can cancel in their customer account).

## 5. Checkout friction and payment methods

- **Fact (vendor):** Fundraise Up observed conversion lifts of about 2.6% with Google Pay, 2% with Apple Pay and 4% for Chrome users where Google Pay is available; no sample size or method published; article dated 2026-05-19 ([Fundraise Up](https://fundraiseup.com/blog/impact-of-apple-pay-and-google-pay)). Same source says 67% of Google Pay on Chrome donations were mobile.
- **Fact:** Squarespace: Apple Pay can't be used for recurring donations; email and phone are always required ([Squarespace](https://support.squarespace.com/hc/en-us/articles/31299996627213-Donation-funds), [Donation blocks](https://support.squarespace.com/hc/en-us/articles/206543967-Donation-blocks)).
- **Fact:** MSF and Khan Academy additionally list DAF, stock, check, wire and employer match; charity:water adds crypto, check and stock ([MSF](https://give.doctorswithoutborders.org/campaign/675296/donate), [Khan Academy](https://donate.khanacademy.org/), [charity:water](https://www.charitywater.org/donate)). For a small NGO, DAF and stock are optional paragraphs of text, not UI.
- **Inference:** Fewer required fields and wallets help, but the cited effect sizes are small and vendor-measured. The phone requirement in Squarespace's block is a friction cost worth testing.
- **Rec:** Cards plus Apple/Google Pay (via Stripe) first; add PayPal only if Squarespace's PayPal connection is chosen; list "check or DAF: email us" text.

## 6. Trust signals

- **Fact:** Leading NGOs show 501(c)(3) status with EIN, rating badges (Charity Navigator, Candid, CharityWatch), a security statement, a receipt promise and a donor-services contact: [MSF](https://give.doctorswithoutborders.org/campaign/675296/donate), [charity:water](https://www.charitywater.org/donate), [Khan Academy](https://donate.khanacademy.org/) (adds tax-deductibility statement, state registration link, annual report).
- **Fact:** charity:water states operating costs are covered by private donors ("100% of public donations" model).
- **Inference:** For a new NGO without ratings, the equivalents are: legal status and EIN (if registered), named people, photos, a plain "where your gift goes" line, real contact details.
- **Rec:** Do not claim tax-deductibility or 501(c)(3) status until it applies. Offer the optional "cover fees" checkbox in the Squarespace block (default off).
- **Fact (vendor-contested):** Tip-funded platforms may pre-select a tip; one competitor analysis reports a pre-selected $16.95 on a $100 gift in Zeffy ([Donately (vendor)](https://www.donately.com/total-donor-cost)). Verify on the vendor's live form.

## 7. Mobile

- **Fact:** Blackbaud reported 21% of online donations on mobile in 2017 and 24% globally in the 2018 UK edition ([Blackbaud](https://www.blackbaud.com/newsroom/article/blackbaud-reveals-this-year-s-most-fascinating-philanthropy-stats), [Charity Digital](https://charitydigital.org.uk/topics/topics/online-giving-in-the-uk-increases-55-in-2018-5601)); old data. Secondary sources for M+R 2025 report donation page conversion of 11% desktop and 8% mobile ([iDonate (vendor)](https://idonate.com/blog/2025-mr-benchmarks-what-nonprofits-must-know-about-online-giving-and-donation-pages)); the M+R 2026 fundraising chapter I fetched did not report this.
- **Inference:** Mobile converts less than desktop; wallets and few fields are the main fix.
- **Rec:** Test the donate page on a phone with Squarespace's mobile preview and a real device; keep presets as large tap buttons (24 px minimum, 44 px better).

## 8. Accessibility

- **Fact:** WCAG 2.2 SC 2.5.8 Target Size (Minimum), Level AA: 24x24 CSS px unless spaced ([W3C](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html)). SC 3.3.7 Redundant Entry, Level A: do not make users re-enter information in a multi-step process ([W3C](https://www.w3.org/WAI/WCAG22/Understanding/redundant-entry.html)).
- **Rec:** Real `<label>`s, error text near the field, contrast 4.5:1, and no auto-advancing carousels near the form. Any custom amount UI in a Code Block must be keyboard-operable.

## 9. Thank-you and post-donation flow

- **Fact:** MSF emails a receipt and mails one 3 to 4 weeks later ([MSF](https://give.doctorswithoutborders.org/campaign/675296/donate)). Squarespace sends an email receipt that can be customized ([Donation blocks](https://support.squarespace.com/hc/en-us/articles/206543967-Donation-blocks)).
- **Fact (secondary, weak):** Chronicle of Philanthropy summary of a fundraising report says 29% of first-time donors approached within 90 days sign up for monthly giving ([Chronicle](https://www.philanthropy.com/article/new-fundraising-report-includes-info-on-gofundme-crowdfunding-campaigns)); original report not identified.
- **Rec:** Thank-you page: name the gift, one concrete impact sentence, share/ripple link (fits the heart concept), monthly invitation, contact. Send a personal-sounding thank-you email within 24 h.

## 10. Benchmarks summary

| Metric | Value | Source and caveat |
|---|---|---|
| Monthly share of online revenue | 27% (2025) | M+R 2026, 180 orgs, first-party |
| Average gift from monthly donors' one-time gifts | $21 | M+R 2026 |
| Average DAF gift | $1,430 | M+R 2026 |
| Donation page conversion | 11% desktop, 8% mobile | Secondary only (iDonate, vendor); verify in M+R |
| Wallet conversion lift | +2% to +4% | Fundraise Up, vendor, no n |

## Open questions

- Could not fetch: GiveDirectly donate (405), UNICEF donate (404), M+R full report PDF, GlobalGiving page (403), Stripe wallet docs (404), Zeffy embed docs (404), Wikipedia form (country-gated landing only; text says about 2% of readers donate). Examples for those NGOs are not reported here.
- Does Squarespace's native block (a) show a monthly toggle for the chosen fund, (b) allow a custom amount, (c) support Apple/Google Pay on one-time gifts? Verify in a test donation with Stripe test mode.
- Is Spread Joy a registered charity? Tax-deductibility copy, Venmo/PayPal Giving Fund eligibility and receipts depend on it.
- Actual cost per sock/kit for impact captions.
- Are two-fee stacks acceptable (Squarespace transaction fee plus Stripe fee)? Check the chosen plan's current fee page.
- No evidence found specific to very small, new NGOs; all benchmarks come from larger organizations.
