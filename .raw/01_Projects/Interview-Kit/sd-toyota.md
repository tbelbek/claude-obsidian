---
tags:
  - interview-kit
  - interview-kit/software-dev
up: [[10-pillar-software-dev]]
---

*[[00-dashboard|Home]] > [[10-pillar-software-dev|Software Dev]] > TOYOTA MATERIAL HANDLING*

# TOYOTA MATERIAL HANDLING — Software Development

Toyota Material Handling builds autonomous forklifts — real robots moving pallets around warehouses. The software that orchestrates them is called T-ONE. I worked here as a Senior Software Engineer from November 2023 to April 2025, in a [[ref-agile-ceremonies#Scrum Roles|cross-functional]] Agile team with developers, testers, and domain experts.

## Tools I Used Here
| Tool | Ref | Tool | Ref |
|------|-----|------|-----|
| [[ref-rabbitmq\|RabbitMQ]] | custom NuGet, typed events | [[ref-mongodb\|MongoDB]] | fleet state, custom extensions |
| [[ref-ddd-cqrs\|DDD/CQRS]] | 30+ services, bounded contexts | [[ref-texttest\|TextTest]] | fleet simulation, BDD |
| [[ref-opcua\|OPC/UA]] | industrial device integration | [[ref-docker\|Docker]] | containerized services |

My main responsibility was backend development in .NET 8 — about 30 microservices following [[ref-ddd-cqrs#Domain-Driven Design|Domain-Driven Design]] with [[ref-ddd-cqrs#CQRS (Command Query Responsibility Segregation)|CQRS]] patterns. The system tells forklifts where to go, coordinates routes so they do not collide, and tracks what each forklift is carrying. The messaging layer was [[ref-rabbitmq#Core Model|RabbitMQ]] — using a custom Tmhls.Communication.RabbitMQ NuGet package with typed publishers, consumers, and APM diagnostic filters — for real-time communication between the central system and the forklifts. Fleet state lived in [[ref-mongodb#Document Model|MongoDB]], with a custom Tmhls.MongoDb.Extensions package providing repository pattern, ACID transactions, and health checks. Everything ran in [[ref-docker#Multi-Stage Builds|Docker]] containers. The system also used [[ref-opcua#Integration Pattern at Toyota|OPC/UA]] integration for industrial device communication. In this system, a lost message means a forklift stops on the warehouse floor, so attention to detail matters more than speed.

What I owned long-term was the test infrastructure. I built Python test frameworks — TextTest-based acceptance testing with BDD scenarios, plus fleet simulators supporting multiple AGV types (SEW Palletrunner, Kollmorgen, Toyota forklifts) — that simulated fleet scenarios — 50, 100, 200 forklifts running at the same time, different warehouse layouts, various load patterns. These were not unit tests. They were full integration tests that caught bugs only visible under concurrent load. The team relied on these to catch regressions before they reached production.

I also did the steady, unglamorous work that keeps a system healthy — tracking down bugs before they became incidents, doing code reviews that were actually useful, and making sure the team stayed on top of quality in an Agile workflow. The [[sd-rabbitmq-splitbrain|RabbitMQ split-brain incident]] was the hardest thing I dealt with here and changed how I think about distributed systems.

## Tools Used
| | | |
|---|---|---|
| [[ref-rabbitmq\|RabbitMQ]] | [[ref-mongodb\|MongoDB]] | [[ref-ddd-cqrs\|DDD/CQRS]] |
| [[ref-docker\|Docker]] | [[ref-texttest\|TextTest]] | [[ref-opcua\|OPC/UA]] |
| [[ref-csharp\|C# .NET 8]] | [[ref-python\|Python]] | [[ref-agile-ceremonies\|Agile]] |

## Key Experiences
- [[sd-rabbitmq-splitbrain|RABBITMQ — Split-Brain — cluster partitioned, messages lost, chaos tests added]]

---

*[[00-dashboard|Home]] > [[10-pillar-software-dev|Software Dev]]*
