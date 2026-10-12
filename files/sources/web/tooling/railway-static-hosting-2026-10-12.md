---
url: https://railway.com/pricing
pulled: 2026-10-12
fetched_via: WebFetch and WebSearch, excerpts quoted verbatim where marked
source_kind: docs
title: "Railway: pricing, static sites and custom domains (excerpts)"
---

Pages read: https://railway.com/pricing, https://docs.railway.com/guides/public-networking, https://railpack.com/languages/staticfile, https://station.railway.com/questions/apex-zone-root-custom-domains-the-cna-3c1bdf89 and https://station.railway.com/questions/root-domain-cannot-be-configured-with-cn-87d5a4d8.

Notes taken from the pages above on 2026-10-12. Short quotes are verbatim; the rest is a summary.

## Pricing (railway.com/pricing)

- Free Trial: 0 USD, a one-time 5 USD credit that expires after 30 days; 1 custom domain.
- Free: 0 USD with 1 USD of monthly usage credits; no custom domains.
- Hobby: 5 USD a month, including 5 USD of monthly usage; usage above that is charged; 2 custom domains.
- Pro: 20 USD a month per workspace.

## Custom domains (docs.railway.com/guides/public-networking)

- "configure a custom domain by adding the `CNAME` and `TXT` records Railway provides to your DNS - both are required."
- SSL certificates are provisioned and renewed automatically, free.

## Root (apex) domains (Railway docs as quoted on Railway Station)

- Railway supports root domains through CNAME flattening or dynamic ALIAS records at the DNS provider.
- Where the provider supports neither, Railway staff point to moving the nameservers to Cloudflare, which flattens at the root. Railway publishes no static IPs for A records.

## Static sites (railpack.com/languages/staticfile)

- Railpack treats a project as a static site if an `index.html` is in the root directory (or a `Staticfile`, a `public` directory, or `RAILPACK_STATIC_FILE_ROOT` is set), and serves the files with Caddy.
