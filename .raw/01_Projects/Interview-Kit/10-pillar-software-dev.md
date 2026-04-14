---
tags:
  - interview-kit
  - interview-kit/pillar
up: [[00-dashboard]]
---

*[[00-dashboard]]*

# Pillar: Software Development

> [!info] 10 years of production .NET — from .NET Core 3.0 to .NET 9. Enterprise backends, distributed real-time systems, embedded IoT, and public transport. Always hands-on: I design systems, write the code, profile the slow parts, and fix the root cause.

## Quick Scan

| | | | |
|---|---|---|---|
| **[[sd-combination\|COMBINATION AB]]** <br> [[sd-graphql-migration\|GRAPHQL — Migration]] · REST→GraphQL, 6mo, zero breaking <br> [[sd-ai-tools\|AI TOOLS — Cursor + Claude Code]] · when to trust vs verify <br> [[ag-adaptability\|OWNERSHIP — Quarter Planning]] · stepped in, completed early <br> [[ref-testing-strategy#Test Pyramid\|TESTING — Strategy]] · Testcontainers, E2E, breaking changes <br> [[ref-graphql#Federation (HotChocolate Fusion)\|GraphQL]] · [[ref-grpc#Protocol Buffers\|gRPC]] · [[ref-kafka#Core Model\|Kafka]] · [[ref-rest#Design Principles\|REST]] <br> *60+ .NET 9 microservices, federated GraphQL* | **[[sd-toyota\|TOYOTA]]** <br> [[sd-rabbitmq-splitbrain\|RABBITMQ — Split-Brain]] · messages lost, chaos tests added <br> [[ag-resilience\|RESILIENCE — Learning from Failure]] · docs ≠ understanding <br> [[ref-mongodb#Document Model\|MONGODB — Fleet State]] · vehicle/transport/mission, custom extensions <br> [[ref-ddd-cqrs#Domain-Driven Design\|DDD/CQRS]] · [[ref-rabbitmq#Core Model\|RabbitMQ]] · [[ref-opcua#Integration Pattern at Toyota\|OPC/UA]] <br> *T-ONE autonomous forklifts, 30+ svc* | **[[sd-kocsistem\|KOCSISTEM]]** <br> [[sd-redis-scaling\|REDIS — Scaling]] · 50→500 trucks, stream+batch fix <br> [[ref-sql-databases#Dapper vs Entity Framework\|MSSQL — Data Access]] · Dapper GPS, EF CRUD, Oracle ERP <br> [[ref-redis#Redis Streams (What I Used)\|Redis Streams]] · [[ref-elasticsearch#Core Model\|Elasticsearch]] · [[ref-dapper#What Dapper Is\|Dapper]] <br> *GPS tracking, 500+ trucks, IDC Award* | **[[sd-antasya\|ANTASYA]]** <br> [[sd-avl\|C#/C++ — AVL]] · Istanbul fleet tracking, Android 4.4 signage |

---

## [[sd-combination|COMBINATION AB]] — Current Role

Senior Software Engineer since April 2025. Building and maintaining microservices in **.NET 9** — 60+ microservices, each owning one domain. I choose the API style based on who's calling: **GraphQL** for the web frontend (flexible data fetching, no over-fetching), **gRPC** for [[ref-grpc#When to Use|service-to-service]] (typed, fast, no JSON overhead), **REST** for external partners (simple, well-documented). **[[ref-kafka#Core Model|Kafka]]** handles async events between services, and we use **federated GraphQL via [[ref-graphql#Federation (HotChocolate Fusion)|HotChocolate Fusion]]**. Everything containerized in **[[ref-docker#HOW WE USE IT|Docker]]** on **Kubernetes**, deployed multiple times a day through **Azure DevOps** and **GitHub Actions**.

I own the API layer, the performance profiling, and the AI tooling workflow. When something's slow, I dig into query plans, serialization costs, and [[ref-graphql#DataLoader & N+1 Problem|resolver]] patterns — recently fixed an [[ref-graphql#DataLoader & N+1 Problem|N+1]] hidden in a GraphQL resolver that dropped response time from 3s to 200ms. Testing is standardized across all services — [[ref-testing-strategy#Test Pyramid|test pyramid]] from unit to E2E, [[ref-testing-strategy#Testcontainers|Testcontainers]] for real MongoDB in tests, and [[ref-testing-strategy#Breaking Change Detection|breaking change detection]] in CI for gRPC protos and GraphQL schemas. I use **[[sd-ai-tools|Cursor and Claude Code]]** daily and have built a disciplined workflow around [[ref-ai-tooling#Risks — Where AI Makes Things Worse|where AI helps and where it makes things worse]]. I also maintain the **[[ref-cdeploy#What CDeploy Manages|Python CDeploy framework]]** for deployment orchestration and infrastructure automation. I also work with [[ref-observability-stack#OpenTelemetry (OTel)|OpenTelemetry]] for distributed tracing (Tempo) and log aggregation ([[ref-observability-stack#Grafana Loki (Log Aggregation)|Loki]]), and [[ref-rest#Design Principles|REST]] for external partner APIs.

---

## [[sd-toyota|TOYOTA MATERIAL HANDLING]] — Distributed Systems

Senior Software Engineer, Nov 2023 – Apr 2025. Worked on **T-ONE** — Toyota's platform for controlling autonomous forklifts in warehouses. Backend in **.NET 8** with **[[ref-ddd-cqrs#Domain-Driven Design|DDD]]/[[ref-ddd-cqrs#CQRS (Command Query Responsibility Segregation)|CQRS]] patterns**, **[[ref-mongodb#Document Model|MongoDB]]** for fleet state, **[[ref-rabbitmq#Core Model|RabbitMQ]]** for real-time messaging, and **[[ref-opcua#What OPC/UA Is|OPC/UA]]** for industrial device integration between the central system and forklifts. Messages had to arrive reliably and in order — a forklift waiting for a command that never comes is expensive and dangerous.

I shipped backend features in a [[ref-agile-ceremonies#Scrum Roles|cross-functional]] Agile team, tracked down bugs before they became incidents, and did code reviews that gave real feedback. What I owned long-term was the test infrastructure — **Python test frameworks** that simulated fleet scenarios with 50, 100, 200 forklifts running at once in different warehouse layouts. These caught regressions that unit tests couldn't find because the bugs only showed up under concurrent load. The system also used [[ref-texttest#What TextTest Is|TextTest]] for acceptance testing.

---

## [[sd-kocsistem|KOCSISTEM]] — Enterprise Backend & Architecture

Senior Software Developer, Mar 2018 – Feb 2020. Built a **GPS-based warehouse management system** — card access at gates, production band audit, real-time truck tracing. **.NET Core** with **[[ref-redis#Caching Patterns|Redis]]** for caching, **[[ref-elasticsearch#Core Model|Elasticsearch]]** for searching millions of records, **RabbitMQ** for async event processing. Used **[[ref-dapper#What Dapper Is|Dapper]]** and **Entity Framework** for data access, some legacy **Visual Basic** integration.

Consulted directly for KocSistem's biggest clients across Turkey and internationally — **Arcelik** (appliances), **Beko** (home electronics), **Bosch Siemens Hausgerate** (home appliances), **Aygaz** (LPG distribution). Each client had different warehouse layouts and [[ref-automotive-compliance#Compliance in Agile|compliance]] needs. I helped the team make architecture decisions, gave technical direction, and built reusable modules (auth, logging, API patterns) that got adopted into KocSistem's **company-wide project framework**. Project won the **2019 IDC Award** and a Customer Satisfaction Award. I also worked with [[ref-sql-databases#Oracle Integration|Oracle]] for client ERP integrations.

---

## [[sd-antasya|ANTASYA]] — Embedded & IoT

Senior Software Developer, Dec 2016 – Mar 2018. Built public transport software in **C# and C++** for Istanbul's **IETT** — the city's public transport agency running buses, trams, and ferries. Partnered with **Modyo** for in-vehicle digital signage.

Shipped an **AVL** (Automatic Vehicle Location) system deployed for **IETT Istanbul** and **Malatya Municipality** — real-time tracking of every vehicle in the fleet. Built Web UI components using **MVC** and integrated **Android 4.4** embedded devices for in-vehicle screens. Delivered the final development phase of Modyo's next-generation signage platform. Researched the **Green Stop Project** — E-Ink displays with solar-powered embedded PCs at transit stops. Used **Jenkins** for CI and **Azure** for hosting.

---

**Related:** [[11-pillar-devops]] | [[12-pillar-leadership]] | [[13-pillar-agile]]

*[[00-dashboard]]*
