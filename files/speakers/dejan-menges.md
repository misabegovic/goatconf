---
name: Dejan Menges
role: Staff Engineer at Vinted, author of Enola
photo: img/speakers/dejan-menges.jpg
links:
  - https://menges.dev/
  - https://github.com/dejo1307
  - https://www.linkedin.com/in/dejanmenges/
  - https://x.com/djn_mngs
talk: Teaching Twenty Languages to Describe One System
talk_about: |
  A software system may span a Go backend, a TypeScript frontend, a Swift or Flutter application, Terraform modules, API specifications, and several repositories. To us, these pieces form one system. To most tools, they are unrelated collections of files and strings.

  While building Enola, an open-source tool that constructs a structural model of software directly from source code, I tried to give those different ecosystems a shared vocabulary: modules, symbols, routes, storage, services, and the relationships between them. That turned out to be much harder than defining a graph schema. A route may be assembled across several functions. A Go type can implement an interface without naming it. A framework can hide dependencies in decorators, templates, configuration, or generated code. Even seemingly universal ideas such as “module,” “call,” and “loop” mean different things in different languages.

  This talk is about the engineering lessons from that work, including the approaches that failed. We will look at how to decide what belongs in the common ontology and what must remain language-specific; how to establish identity across files and repositories; how to distinguish measured facts from inference; and why unresolved relationships and extraction coverage must be modeled explicitly rather than silently omitted.

  You will leave with a practical way to think about structural models of software - whether you are building developer tools, architecture checks, code intelligence for agents, or simply trying to understand a large polyglot system. No knowledge of ontologies, graph databases, or Enola is required.
talk_area: [engineering, data]
talk_for: anyone working with real-life codebases
order: 3
publish: yes
support_them:
  - text: "Try Enola, his open-source architecture tool"
    url: "https://github.com/enola-labs/enola"
  - text: "Check your files with augur, his open-source tool for hidden prompts and characters"
    url: "https://checkwithaugur.com/"
  - text: "Work with him: software architecture consulting and workshops"
    url: "https://menges.dev/services/"
  - text: "Read his writing on distributed systems and architecture"
    url: "https://menges.dev/writing/"
  - text: "Work with him at Vinted: open positions"
    url: "https://careers.vinted.com/"
---

Dejan Menges is a staff engineer with more than twenty-five years spent designing distributed systems. He works on moving organisations from monoliths to scalable, event-driven architectures, and builds Enola, an open-source architecture intelligence tool for developers and coding agents.
