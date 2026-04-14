---
tags:
  - interview-kit
  - interview-kit/software-dev
up: [[10-pillar-software-dev]]
---

*[[00-dashboard|Home]] > [[10-pillar-software-dev|Software Dev]] > ANTASYA*

# ANTASYA — Software Development

Antasya was a software consultancy focused on public transport and IoT solutions. I worked here from December 2016 to March 2018, partnering with IETT (Istanbul's public transport agency) and Modyo (an in-vehicle digital signage provider).

My main project was an [[sd-avl|AVL (Automatic Vehicle Location) system]] — real-time tracking of every bus and tram in the city fleet. The backend was C# and C++ — C++ for the low-level parts like parsing raw GPS data from on-board units and handling binary protocols over TCP, C# for the backend services and web dashboard built with MVC. I shipped the AVL solution for both IETT in Istanbul and Malatya Municipality. We used Git for version control and Jenkins for CI, with deployments going to Azure.

What I owned long-term was the Modyo partnership. I delivered the final development phase of their next-generation digital signage platform — screens inside buses and trains showing route information and media content. I built the Web UI components and integrated Android 4.4 embedded devices. These devices ran 18 hours a day in vibrating vehicles with limited memory and slow processors. Writing reliable code for that environment taught me things you do not learn building web apps.

I also researched the Green Stop Project — E-Ink displays powered by solar panels at bus stops. No power connection needed. It was a feasibility study: could a small solar panel and battery keep an embedded PC and E-Ink display running 24/7 in Istanbul's climate? An interesting problem at the intersection of hardware constraints and software design.

## Key Experiences
- [[sd-avl|C#/C++ — AVL — Istanbul fleet tracking, Android 4.4 signage]]

---

*[[00-dashboard|Home]] > [[10-pillar-software-dev|Software Dev]]*
