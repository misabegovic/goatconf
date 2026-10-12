---
url: https://developers.cloudflare.com/pages/platform/limits/
pulled: 2026-10-07
fetched_via: curl, HTML converted to text by a local script; excerpt verbatim
source_kind: docs
title: "Limits - Cloudflare Pages docs"
---

Limits · Cloudflare Pages docs

[...]

Limits
Choose a data or storage product ↗︎
Changelog
Known issues
Migrate to Workers ↗︎
Agent resources
Agent setup ↗︎

[...]

Users
Projects
Below are limits observed by the Cloudflare Free plan. For more details on removing these limits, refer to the
Cloudflare plans
↗︎
page.
Need a higher limit?
To request an adjustment to a limit, complete the
Limit Increase Request Form
↗︎
. If the limit can be increased, Cloudflare will contact you with next steps.
Builds
Each time you push new code to your Git repository, Pages will build and deploy your site. Build limits depend on your plan:
Free
Pro
Business
Builds
1 build at a time
5 concurrent builds
20 concurrent builds
Builds per month
500
5,000
20,000
Builds will timeout after 20 minutes. Concurrent builds are counted per account.
Custom domains
Based on your Cloudflare plan type, a Pages project is limited to a specific number of custom domains. This limit is on a per-project basis.
Free
Pro
Business
Enterprise
100
250
500
500
1
Files
Pages uploads each file on your site to Cloudflare's globally distributed network to deliver a low latency experience to every user that visits your site. Cloudflare Pages sites can contain up to 20,000 files on the Free plan.
Paid plans (such as Pro, Business, and Enterprise plans) can have up to 100,000 files per site. To enable this increased limit, set the environment variable
PAGES_WRANGLER_MAJOR_VERSION=4
in your Pages project settings.
File size
The maximum file size for a single Cloudflare Pages site asset is 25 MiB.
Larger Files
To serve larger files, consider uploading them to
R2
