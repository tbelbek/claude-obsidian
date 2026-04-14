---
tags:
  - interview-kit
  - interview-kit/software-dev
up: [[10-pillar-software-dev]]
---

*[[00-dashboard|Home]] > [[10-pillar-software-dev|Software Dev]] > KOCSISTEM*

# KOCSISTEM — Software Development

KocSistem is one of Turkey's largest IT services companies, part of the Koc Group — the country's biggest industrial conglomerate. I worked here as a Senior Developer from March 2018 to February 2020, building a GPS-based warehouse management system for logistics clients.

## Tools I Used Here
| Tool | Ref | Tool | Ref |
|------|-----|------|-----|
| [[ref-redis\|Redis]] | Streams, caching, Sentinel | [[ref-sql-databases\|SQL Server]] | SqlBulkCopy, indexed views |
| [[ref-elasticsearch\|Elasticsearch]] | full-text search, millions of records | [[ref-dapper\|Dapper]] | micro-ORM for GPS throughput |
| [[ref-rabbitmq\|RabbitMQ]] | async event processing | | |

The system handled card access at warehouse gates, production band auditing on the floor, and real-time GPS tracking of every truck. The stack was .NET Core 3.0 with [[ref-redis#Caching Patterns|Redis]] for caching, [[ref-elasticsearch#Core Model|Elasticsearch]] for searching across millions of records, and RabbitMQ for async event processing. **SQL Server** (MSSQL) with both **[[ref-dapper#What Dapper Is|Dapper]]** for high-throughput GPS data and **Entity Framework** for application logic. I did not just write features — I helped the team make architecture decisions and gave technical direction where needed.

I also worked with **Oracle** databases for client ERP integrations — Arcelik and Bosch had Oracle-based systems that our platform needed to sync with.

What I owned long-term was the platform itself and the client relationships. I consulted directly for KocSistem's biggest clients — Arcelik, Beko, Bosch Siemens Hausgerate, Aygaz — understanding their warehouse operations and adapting the system to fit. Each client had different warehouse layouts, different truck types, different compliance needs. I had to make the system flexible enough to handle all of them without custom forks.

I also built reusable framework modules — standardized authentication, logging, and API patterns — that got adopted into KocSistem's company-wide project framework. Other teams across the company used what I built in their own projects. The project won the 2019 IDC Award and a Customer Satisfaction Award in Turkey.

The biggest technical challenge was [[sd-redis-scaling|scaling from 50 to 500+ trucks]] — the architecture that worked fine in testing broke completely in production.

## Key Experiences
- [[sd-redis-scaling|REDIS — Scaling — 50→500 trucks froze dashboard, stream + batch fix]]

---

*[[00-dashboard|Home]] > [[10-pillar-software-dev|Software Dev]]*
