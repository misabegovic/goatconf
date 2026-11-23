---
url: https://paolino.me/optimizing-rubyllm-for-coding-agents/
pulled: 2026-11-23
fetched_via: curl -sSL of https://paolino.me/, https://paolino.me/about/, https://paolino.me/optimizing-rubyllm-for-coding-agents/, https://paolino.me/rubyllm-2-2/, https://rubyllm.com/ and https://rubygems.org/api/v1/gems/ruby_llm.json; tags stripped with a local script; verbatim excerpts. sha256 of the fetched files, in that order: e51cbf966eca204932879ea19e90dcdb1a3da633da3334b80a01901d166ce0be, 76872557602bcd171889fd6e8b9bbc36728754f3dc379b69539bbd5636f00335, 3ed96a1c031b55e6da5344095873c06853d9bda40a3ba3160d3a79f48e09b18e, a9bfee6edd6d0f00fbae88b8b5809cc368abb7571957e4f7f9f036d1dba70654, 48aa982540040373335c4b793211361f093253112d2f0557197e9b1843d94a57, ac79a96681e0e04b4294be80842b1a35e41f8e0eecf9bf216859337a36500132. https://api.github.com/repos/crmne/ruby_llm answered 403 to the fetch, so no star count is recorded.
source_kind: personal-site
title: "Carmine Paolino: RubyLLM 2.2, his benchmark of frameworks against coding agents, and RubyLLM's downloads"
---

Pulled on 2026-11-23 for a rewrite of Carmine Paolino's drumbeat spotlight,
on the organiser's choice (sources/conversations/2026-11-23--org--carmine-spotlight-rewrite.md).

## https://paolino.me/ (changed since sources/web/speakers/paolino-me-2026-10-14.md)

> At Plenty, I build AI frameworks, products, native apps, and developer tools: RubyLLM, Chat with Work, Solco, Spotifast, ZapFast, ArchSpec, Kamal Backup, and more. I help organize Berlin.rb, founded Floppy Disco, and make house and disco as Crimson Lake.

Latest posts, as listed: "How I Optimized RubyLLM for Coding Agents" (Nov 12, 2026); "RubyLLM 2.2: The AI Framework for Coding Agents" (Nov 10, 2026); "Solco: Stop Preparing Your Tracks, Start Preparing Your Gigs" (Oct 28, 2026); "I Get 215 GitHub Notifications a Day, So I Built a Bot to Triage Them" (Oct 23, 2026).

The first post's summary on the home page:

> My own framework lost to no framework at first: the coding agent couldn't see how to use it. What I changed, what worked, and how I measured it.

## https://paolino.me/about/ (changed since sources/web/speakers/paolino-me-2026-10-14.md)

One sentence differs from the October snapshot, which the site's profile quotes word for word. It now reads:

> I created RubyLLM, a framework for building AI applications in Ruby, and build Chat with Work, AI bots in Europe that work across your team’s tools while you decide.

Unchanged, and used in the spotlight:

> I wrote my first scripts at 5 to automate launching my favorite games. I’ve been hooked ever since.
> I got into open source early, running the Italian Gentoo Linux community as a teenager.

## "How I Optimized RubyLLM for Coding Agents" (Nov 12, 2026)

> You’ve heard it this year. Maybe you’ve said it yourself: “You don’t need frameworks anymore. Just let the agent write it. Why would you depend on somebody else’s gem?”

> I think it’s bullshit, and I wanted to prove it, not just say it.
> So I took a coding agent, Codex on GPT-6 Astra, a really good one, and gave it the same app to build four times: with RubyLLM on Rails, with LangChain and LangGraph, with the Vercel AI SDK, and with no framework at all, just plain Ruby with no AI libraries or provider SDKs.

> The app is a real chat app, built over eleven steps, each a new agent session on the same project [...] After each step, a test suite the agent never sees drives the app in a real browser and reruns every check on every provider, 198 checks by the end.

> Without a framework, the agent got there. Streaming on Bedrock? Done. Tools on Gemini? No problem. Honestly, it’s really good at it.
> But every line it writes is a line you own, for every feature on every provider

> So this cycle I treated coding agents as RubyLLM’s main users, and turned the benchmark into a loop: agents build the app on RubyLLM’s main branch, I read the transcripts for where they stumble or write code they shouldn’t need, I fix the cause where it lives (the gem, a generator, the docs or the skill), and I run it again. I’m 28 rounds in, and here’s what I learned.

> Most of the improvement, from 0 of 5 clean first attempts to 8 of 8, came from fixing RubyLLM itself, because what the agents tripped on were real bugs and bad defaults

> With RubyLLM the agent wrote about 420 lines of app code; with no framework, 867.

> On the held-out task with Codex, the RubyLLM run cost $12.34 and the no-framework run $12.78. On the chat app, the final RubyLLM runs cost about $21 each, the no-framework runs between $17 and $24. With Claude Opus on the held-out task, RubyLLM came out at 1,088 lines against 2,969, but cost $19 against $11.

His own limits on the result:

> One kind of app. Chat apps with tools, files and providers are what RubyLLM is built for, and I wrote the benchmark.
> A handful of attempts per stack, one model at a time. The spread between attempts is real.

His conclusion:

> Same bill, then, but a quarter of the code, and the code is what stays. The agent leaves when it’s done, and the responsibility for what it wrote stays with you.

> Everything from this loop shipped in RubyLLM 2.2, which I released on stage at SF Ruby, where I first told this story.

## "RubyLLM 2.2: The AI Framework for Coding Agents" (Nov 10, 2026)

> RubyLLM 2.2 is out! I released it on stage at SF Ruby, and it’s the release I’m proudest of.

> It’s also the first release I built for a new kind of user: the coding agent. More and more of the code that uses RubyLLM is written by Claude Code, Codex and Cursor, so I spent as much time making RubyLLM easy for them to use as I did on features. The talk was about that, and about the idea that you don’t need frameworks anymore.

## https://rubyllm.com/ (title: "Ruby AI Framework for LLMs, Agents, Chat and Rails | RubyLLM")

> The Ruby AI framework
> Build AI features the Ruby way: models, tools, agents, sandboxed code, evaluations, and Rails conventions, designed together, with one consistent API.
> 23 providers. One API.

The page's download and star counts are filled in by a script and were not in the fetched HTML.

## https://rubygems.org/api/v1/gems/ruby_llm.json

On 2026-11-23: `"downloads": 16692109`, `"version": "2.2.3"`, `"version_created_at": "2026-11-18T18:36:51.416Z"`.
