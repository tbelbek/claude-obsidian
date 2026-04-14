---
tags:
  - interview-kit
  - interview-kit/leadership
up: [[ls-kocsistem]]
---

*[[00-dashboard|Home]] > [[12-pillar-leadership|Leadership & Soft Skills]] > [[ls-kocsistem|KOCSISTEM]] > INITIATIVE*

# INITIATIVE

> [!warning] **Soru:** "Tell me about going above and beyond"

At KocSistem, I was hired as a backend developer. The team had no production visibility — when something broke, we'd get a vague report like "system is slow" and spend 3 hours digging through logs trying to find the problem. I decided to go beyond my job description to solve a problem the whole team felt.

Nobody asked me to fix this. But I was tired of wasting hours on something that proper metrics would solve in 3 minutes. I spent weekends learning monitoring tools, built a proof-of-concept showing our services' latency, memory usage, and error rates. Showed it to my lead — his reaction was "why don't we have this already?"

Got approval to deploy it properly. Wrote alert rules, set up dashboards, documented everything. To get the team to actually use it, I started every standup with "here's what the dashboard showed overnight." After a few weeks where we caught issues before users reported them, the team started checking it on their own.

Detection time went from hours to minutes. It became the standard for every new service. And it eventually led to my promotion to Dev Lead.

I bring this up under leadership because going beyond your job description is how you create lasting impact — the monitoring I built wasn't my responsibility, but it changed how the entire team worked.

## Sorulursa

> [!faq]- "Why did you spend your own time on this?"
> Because the pain was real. I was the one spending 3 hours debugging something that should take 3 minutes. The cost of not having monitoring was higher than the cost of building it. Also, I was curious — I wanted to learn how monitoring tools worked.

> [!faq]- "How did you get people to use the dashboards?"
> You can't just build a dashboard and expect people to look at it. I made it part of the routine — first thing in standup, 30 seconds of "here's what the dashboard shows." After the third time we caught a problem early because someone checked the dashboard, people started looking at it on their own.

> [!faq]- "What monitoring stack did you use?"
> At KocSistem, I started with Prometheus for metrics collection and Grafana for dashboards. Prometheus scrapes metrics endpoints on your services (pull-based model). I added basic instrumentation: request latency histograms, error counters, memory/CPU gauges. For alerting, Prometheus Alertmanager with Slack integration. The setup follows the USE method (Utilization, Saturation, Errors) by Brendan Gregg and the RED method (Rate, Errors, Duration) by Tom Wilkie — two complementary frameworks for choosing what to monitor.

> [!faq]- "How did you decide what to monitor?"
> I started with the RED method: for each service, track request Rate, Error rate, and Duration (latency). These three tell you 80% of what you need to know. Then I added USE metrics for infrastructure: CPU utilization, memory saturation, disk errors. I avoided monitoring everything — too many metrics means too many dashboards means nobody looks at any of them. Start with what tells you if the service is healthy, then add detail as needed.

## Also relevant to

- [[ref-dora#HOW WE USED IT]] — The monitoring/observability work I built, evolved into DORA metrics tracking
- [[11-pillar-devops|DevOps Pillar]] — Prometheus, Grafana, alerting setup

---

*[[00-dashboard|Home]] > [[12-pillar-leadership|Leadership & Soft Skills]] > [[ls-kocsistem|KOCSISTEM]]*
