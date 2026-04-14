---
tags:
  - interview-kit
  - interview-kit/software-dev
up: [[sd-antasya]]
---

*[[00-dashboard|Home]] > [[10-pillar-software-dev|Software Dev]] > [[sd-antasya|ANTASYA]] > C#/C++ — AVL*

# C#/C++ — AVL

> [!warning] **Soru:** "Embedded experience?" / "IoT experience?"

At Antasya, I worked on public transport software for Istanbul's IETT — the city's public transport agency. We built an AVL (Automatic Vehicle Location) system that tracked every bus and tram in the fleet in real time. The backend was C# and C++, and the system was deployed for both IETT in Istanbul and Malatya Municipality.

I also worked on in-vehicle digital signage — Android 4.4 devices mounted inside buses and trains that showed route information and media content. This was a partnership with Modyo, who provided the hardware. I built the Web UI components and handled the Android device integration.

One interesting project was the Green Stop research — we were evaluating E-Ink displays powered by solar panels for transit stops. The idea was passenger information screens that didn't need a power connection. Low power consumption, readable in sunlight.

This sits in my software development experience because building for constrained embedded hardware with unreliable connectivity is a fundamentally different kind of engineering than web development — and it shaped how I think about reliability.

## Sorulursa

> [!faq]- "What was challenging about the AVL system?"
> The main challenge was reliability. These devices are in vehicles that run 18 hours a day, go through tunnels, have spotty cellular connections. The system had to buffer GPS data locally when there was no connection and sync when connectivity came back. We also had to handle the sheer volume — thousands of vehicles reporting every few seconds.

> [!faq]- "Why C++ alongside C#?"
> The C++ parts were closer to the hardware — parsing raw GPS data, communicating with the on-board units. The C# parts were the backend services and the web dashboard. It was a practical split based on what each language is good at.

> [!faq]- "What did you learn from working on embedded/IoT?"
> That you can't assume a stable environment. Building real-time systems for constrained hardware with unreliable connectivity taught me things web development never would. Network drops, devices restart, firmware has bugs you can't patch easily. You have to design for failure from day one — local buffering, retry logic, graceful degradation. This mindset carried over to everything I built after.

> [!faq]- "Technical: AVL system architecture"
> AVL (Automatic Vehicle Location) systems follow a standard architecture: on-board unit collects GPS coordinates + vehicle telemetry → sends over cellular (GPRS/3G) to a central server → server processes and stores → dashboard displays real-time positions. The challenge is the "last mile" — cellular connectivity in tunnels, underground garages, and dense urban areas. We used store-and-forward: the on-board unit buffered data locally when offline and synced when connectivity returned. The protocol was binary (not JSON) to minimize cellular data usage — important when you have thousands of vehicles each sending data every few seconds.

> [!faq]- "How did you handle thousands of vehicles reporting simultaneously?"
> The central server used a message queue to decouple receiving from processing. GPS data came in via TCP connections from on-board units, got queued, and workers processed them asynchronously. This way, a spike in data (like when all buses start their routes in the morning) didn't overwhelm the processing layer. Similar pattern to what I later used with Redis Streams at KocSistem, but here it was a custom TCP server with an internal queue.

> [!faq]- "What was the E-Ink research about?"
> E-Ink displays (like Kindle screens) are readable in direct sunlight and consume almost no power — they only use energy when changing the display. Combined with a solar panel and a small embedded PC, you could run a passenger information display at a bus stop without any power connection. The research was about feasibility: battery sizing, solar panel capacity, display refresh rates, and whether the embedded PC could handle real-time data updates over cellular. It was a research project, not a shipped product.

---

*[[00-dashboard|Home]] > [[10-pillar-software-dev|Software Dev]] > [[sd-antasya|ANTASYA]]*
