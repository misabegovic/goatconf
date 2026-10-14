---
title: "Twelve open questions decided one by one: money, sessions, check-in, IPI, and tidy-ups"
date: 2026-10-14
kind: conversation
---

After the agent listed what was left (small fixes, housekeeping, and questions only the organiser can answer), the organiser wrote, verbatim:

> ok, lets decide everything. ask me one by one

Asked one question at a time, the organiser chose:

1. **What happens to leftover supporter money:** "Event costs, then next year (Recommended)". Leftover pays more of this year's costs, speaker travel refunds included where the organiser decides, and anything still left carries to the next GoatConf. This confirms the agent's reading recorded in sources/conversations/2026-10-13--org--online-supporters-through-the-business.md.
2. **How ticket holders register for single sessions:** "Decide when the program fills (Recommended)". The site and Luma keep saying people will register for sessions later; the tool is picked in spring, once it is clear which sessions are popular. Until then seats are first come, first served.
3. **Check-in on the core days:** "Luma's check-in app (Recommended)". Volunteers scan each guest's Luma QR code at the door with Luma's free check-in app; the guest list stays in Luma, and the attendance count comes from it.
4. **The open-to-work question for hiring partners:** "Drop it for 2027 (Recommended)". Supporters are online only and there are no hiring partners, so nobody would receive the list; the hiring-partner sharing is retired for 2027.
5. **The check-in success metric:** "120 people (Recommended)". At least 120 different people check in on Thursday or Friday, counted from Luma's check-in, the bottom of the 120 to 300 the home page promises.
6. **Seats in IPI's main hall on the ground floor:** "120".
7. **The second code-of-conduct contact:** "Just you for now". The organiser is the only code-of-conduct contact until IPI names someone, and the site says so.
8. **IPI's acceptance of the dates and rooms in writing:** "Verbal is enough". The open question is closed on the organiser's satisfaction with IPI's verbal acceptance.
9. **"Something else" on the propose-an-event form:** "Add a kind \"other\" (Recommended)". Event records accept `kind: other`, shown as "Something else".
10. **The other four small fixes** (the stale line on the IPI letter page, the program record docs, the three obsolete design-check exemptions, and clear errors instead of crashes in `tools/nav.py` and `tools/meta.py`): "Yes, all four (Recommended)".
11. **The hook journal files:** "Stop tracking, ignore both folders (Recommended)".
12. **Local branches:** "Delete all 71". Before deleting, the agent checked that every unmerged branch's commits are on a remote (the archive), so nothing was lost; every local branch except `main` was deleted on 2026-10-14.

Last, asked whether to merge the open pull request #56 before this work, the organiser chose "Merge #56 first (Recommended)", and it was merged on 2026-10-14.
