---
tags:
  - interview-kit
  - interview-kit/reference
up: [[00-dashboard]]
---

*[[00-dashboard]]*

# OPC/UA — Quick Reference

> [!info] How I've used it: At Toyota, OPC/UA for industrial device communication between the T-ONE forklift orchestration system and warehouse hardware — PLCs, sensors, conveyor systems.

## Quick Scan
| Topic | One-liner | Topic | One-liner |
|-------|----------|-------|----------|
| [[#What OPC/UA Is\|OPC/UA]] | industrial protocol, client-server, pub/sub, secure | [[#Why It Matters for T-ONE\|for T-ONE]] | PLCs, sensors, conveyor systems, forklift orchestration |
| [[#Integration Pattern at Toyota\|integration]] | domain events from hardware → RabbitMQ → microservices | | |

## HOW WE USED IT

At Toyota, T-ONE didn't just control forklifts — it integrated with warehouse infrastructure via OPC/UA. The `Tmhls.OPCUA` service handled communication with PLCs (Programmable Logic Controllers), sensors, and conveyor systems. Domain events like `NodeStatusChangedEvent` and `NodeValueChangedEvent` flowed through RabbitMQ when hardware state changed.

**What the system did:**
- Read/write OPC/UA nodes — query sensor values, send commands to PLCs
- React to hardware state changes — `NodeStatusChangedEventHandler` processed status updates from industrial devices
- Rate limiting — event handlers had rate limiting behaviors to prevent flooding when sensors sent rapid updates
- Node repository — MongoDB stored OPC/UA node definitions and server configurations

---

## Key Concepts

### What OPC/UA Is
- **OPC/UA (Open Platform Communications Unified Architecture)** — Industry standard protocol for industrial automation. Like HTTP for factories — lets software talk to PLCs, sensors, robots.
- **Nodes** — Everything in OPC/UA is a node: variables (sensor readings), objects (devices), methods (commands). Organized in a hierarchical address space.
- **Subscriptions** — Client subscribes to node changes. Server pushes updates when values change — no polling needed.

### Why It Matters for T-ONE
- Forklifts don't operate in isolation — they interact with warehouse infrastructure: doors, conveyors, charging stations
- When a forklift approaches a door, T-ONE sends an OPC/UA command to open it
- When a conveyor finishes loading, the PLC sends a status change via OPC/UA, T-ONE assigns a forklift to pick up
- Without OPC/UA, you'd need custom integrations for every hardware vendor

### Integration Pattern at Toyota
- `Tmhls.OPCUA` service — dedicated microservice for OPC/UA communication
- Domain events bridge — hardware state changes become RabbitMQ events that other T-ONE services consume
- Separation of concerns — business logic doesn't know about OPC/UA. It reacts to domain events (`NodeStatusChanged`). The OPCUA service handles the protocol translation.

## Sorulursa

> [!faq]- "How does OPC/UA compare to MQTT or REST for industrial IoT?"
> OPC/UA is the enterprise/industrial standard — built-in security (encryption, authentication), rich data modeling (typed nodes, hierarchies), and discovery. MQTT is lighter — pub/sub over TCP, popular for edge IoT but less structured. REST is too heavyweight for real-time industrial communication. For Toyota's use case (PLC integration in a warehouse), OPC/UA was the industry standard choice.

> [!faq]- "Did you write OPC/UA code or just consume it?"
> Mostly consumed. The `Tmhls.OPCUA` service was already built when I joined. I worked on the domain event handlers that reacted to OPC/UA state changes — NodeStatusChangedEventHandler, NodeValueChangedEventHandler — and on the rate limiting behaviors that prevented event flooding from rapid sensor updates.

---

*[[00-dashboard]]*
