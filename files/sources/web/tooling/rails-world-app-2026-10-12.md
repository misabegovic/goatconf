---
url: https://github.com/TelosLabs/rails-world
pulled: 2026-10-12
fetched_via: GitHub API (repository metadata, README, app/models, db/schema.rb), excerpts quoted verbatim
source_kind: docs
title: "The Rails World conference app (TelosLabs/rails-world): what it does and needs"
---

Read on 2026-10-12 through the GitHub API.

- Repository description: "Official App for the Rails World 2025 Conference". Licence: GPL-3.0. Last push: 2026-02-20. Not archived.
- README: "Rails application that allows you to create and manage conferences. You can use it to create a conference, add speakers and sessions. Attendees can register for the conference, view the schedule, receive notifications and more."
- README, the stack: Ruby on Rails 8.0, Ruby 3.3.x, SQLite3, SolidQueue, Hotwire, import maps, Tailwind CSS. Deployment: "This application is set up for deployment using [Kamal 2]". The staging setup uses AppSignal, MailPace, Avo, and Amazon for storage.
- app/models/session.rb: a session `belongs_to :location`, `belongs_to :conference`, and `has_and_belongs_to_many :attendees, class_name: "User", join_table: "sessions_users"`.
- app/models/user.rb: users have an email and a password (`validates :password, length: {minimum: 8}`) and `has_and_belongs_to_many :sessions`.
- db/schema.rb has no capacity or seat column on sessions or locations.

Also: the Rails World 2025 app's App Store listing describes a full event schedule, session details with speaker bios, a bookmarkable personal agenda and push notifications (https://apps.apple.com/mx/app/rails-world/id6748968952).
