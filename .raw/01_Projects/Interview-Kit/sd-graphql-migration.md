---
tags:
  - interview-kit
  - interview-kit/software-dev
up: [[sd-combination]]
---

*[[00-dashboard|Home]] > [[10-pillar-software-dev|Software Dev]] > [[sd-combination|COMBINATION AB]] > GRAPHQL — Migration*

# GRAPHQL — Migration

> [!warning] **Soru:** "How did you handle the REST to GraphQL migration?"

We had a growing problem with our REST APIs. Different consumers needed different data — mobile wanted three fields, web wanted twenty — and choosing the right API approach for each while migrating a production system without breaking anything became the central challenge. The frontend team was making 5-6 requests to build a single page, over-fetching data they didn't need, and struggling with version management. We decided to try [[ref-graphql#When NOT to Use GraphQL|GraphQL]], but half the backend team pushed back — they'd spent years building REST endpoints and didn't see the point of changing.

I volunteered to lead the migration even though I wasn't a GraphQL expert. Spent a week building a side project, hit every pain point myself, and wrote down what worked and what didn't. Then I proposed a gradual approach: we'd build new features in GraphQL alongside the existing REST endpoints. No big-bang rewrite, no breaking existing clients.

The turning point was when I paired with the most skeptical developer on the team. We built the first production resolver together. When the frontend team saw it — one request instead of five, exactly the data they needed, no over-fetching — the skeptic changed his mind. From there it spread. We moved most of the API surface over in about 6 months with zero breaking changes for existing clients.

I bring this up under software development because it's the clearest example of how I think about API design — choosing the right tool for each consumer and migrating a live system without breaking anyone.

## Sorulursa

> [!faq]- "Why GraphQL instead of just fixing the REST endpoints?"
> The problem wasn't bad REST design — it was structural. Each page needed data from multiple resources, so the frontend had to make multiple calls and stitch them together. We could've built custom aggregation endpoints, but then every new page would need a new endpoint. GraphQL solved this at the protocol level — the frontend describes what it needs, and gets it in one call.

> [!faq]- "Why not do a big-bang migration?"
> Too risky. We had mobile apps and third-party integrations hitting the REST endpoints. If we broke those, it would be a mess. The gradual approach meant old clients kept working while new features used GraphQL. We migrated existing endpoints one by one when teams were ready.

> [!faq]- "How did you convince the skeptical developer?"
> I didn't try to convince him with slides or articles. I asked him to pair with me on the first resolver. We built it together — he saw the code, he saw the frontend team's reaction, and he formed his own opinion. People change their mind when they experience the benefit, not when you tell them about it.

> [!faq]- "How did you handle the technical migration?"
> We ran HotChocolate with federation (Fusion) alongside our existing REST controllers. Same services, same data layer — just a new API surface. Each domain service (GP-Feed, GP-Entity, GP-Profile, GP-SocialPosts, etc.) exposes its own schema with Query/Mutation/Subscription types, and the GP-GraphQL-Gateway federates them together via the GP-GraphQL-SchemaRegistry — 60+ services composed into one API surface. We started with read-only queries, then added mutations once the team was comfortable. Each resolver called the same service layer as the REST controller, so we weren't duplicating business logic. Service-to-service communication stayed on gRPC with versioned proto files (v1, v2, v3 per service) — GraphQL was only for the frontend-facing API layer. Async events between services go through Kafka, not GraphQL subscriptions. We used DataLoader to fix the N+1 problem — without it, a query for 10 items with related data would hit the database 11 times. With DataLoader, it batches into 2 queries.

> [!faq]- "Technical: GraphQL vs REST trade-offs"
> GraphQL isn't always better than REST. REST is simpler for CRUD APIs, has better caching (HTTP-level), and is easier to rate-limit per endpoint. GraphQL shines when you have multiple consumers with different data needs — mobile wants 3 fields, web wants 20, and you don't want to maintain 5 different endpoints. In our case, we have 60+ microservices each exposing a federated GraphQL schema. The gateway composes them into one API surface. This is the HotChocolate Fusion pattern — similar to Apollo Federation but native to .NET. The N+1 problem is the classic GraphQL trap — Martin Fowler's team writes about this. Without DataLoader (Facebook's batching pattern), a query for 10 users with their orders becomes 11 database calls. DataLoader batches them into 2. We used HotChocolate's built-in DataLoader support for this.

> [!faq]- "What about GraphQL performance and security?"
> GraphQL opens you up to query complexity attacks — someone can write a deeply nested query that takes down your server. We added query depth limiting (max 5 levels) and complexity analysis in HotChocolate. Also disabled introspection in production — you don't want to expose your full schema to the internet. With 60+ services federating through one gateway, query planning becomes critical. The schema registry tracks which service owns which types, and the gateway routes resolver calls to the right service. For caching, we used persisted queries — the client sends a hash instead of the full query, which also prevents arbitrary query attacks.

> [!faq]- "How did you handle versioning in GraphQL?"
> That's one of the big wins. In REST, we had /v1/users and /v2/users. In GraphQL, you don't version the API — you deprecate fields with @deprecated and add new ones. Clients that still use old fields keep working, clients that need new data use new fields. No breaking changes, no version management.

## Also relevant to

- [[ag-adaptability]] — Same migration told from the Agile/change management perspective: stepping up and leading change
- [[13-pillar-agile|Agile Pillar]] — Adaptability and leading without authority

---

*[[00-dashboard|Home]] > [[10-pillar-software-dev|Software Dev]] > [[sd-combination|COMBINATION AB]]*
