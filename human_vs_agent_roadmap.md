# SKYEYE: Work Breakdown (Agents vs Humans)

This document explicitly splits the remaining Master Architecture Roadmap between **AI Agents** (coding logic, orchestration, UI) and the **Local Human Team** (DevOps, API access, Databases).

---

## 🤖 What the AI Agents Build (Software & Logic)

The AI agents (like me and your local 0Core wrappers) should focus entirely on writing the complex, stateful software logic.

### 1. The Dispatch Layer (Phase 2.5) - *Immediate Next AI Task*
*   **Target:** [skyeye_engine/brain/anomaly_dispatcher.py](file:///f:/2026%20BUSINESS%20IDEAS/BRAINSTORM/SKYEYE/skyeye_engine/brain/anomaly_dispatcher.py)
*   **What AI will do:** Build the `PriorityDispatcher` queue logic. When the Event Detector scores a wildfire at 9.5, the AI writes the code that pushes it to the front of the local GPU processing queue.
*   **What AI will do:** Write the `PipelineSelector` so the system autonomously knows to use the Particle-Based Dynamics (PBD) solver for floods vs the Material Point Method (MPM) solver for landslides.

### 2. The Streaming Engine (Phase 4.5)
*   **Target:** [skyeye_engine/controller.py](file:///f:/2026%20BUSINESS%20IDEAS/BRAINSTORM/SKYEYE/skyeye_engine/controller.py) & [index.html](file:///f:/2026%20BUSINESS%20IDEAS/BRAINSTORM/SKYEYE/index.html)
*   **What AI will do:** Implement a WebSocket server so that when the dispatch layer finishes processing an anomaly, it *pushes* the new 3D data directly to the Frictionless Earth Interface without the user having to refresh.

### 3. Geolocation Pipeline (Phase 1.2)
*   **Target:** `skyeye_engine/fusion/video_geolocator.py`
*   **What AI will do:** Write the shadow-geometry analysis and feature-matching math to place un-tagged citizen video onto the Cesium globe automatically.

---

## 🧑‍💻 What the Local Human Team Builds (DevOps & Infrastructure)

Humans are currently much better at navigating red tape, securing API quotas, and spinning up foundational infrastructure.

### 1. API Securitization (Phase 0.3) - *Immediate Next Human Task*
The AI just built the Event Detector, but it is currently relying on mocked thermal data. The human team must:
*   Register for a **NASA Earthdata** account to get production FIRMS (Fire Information for Resource Management System) streaming keys.
*   Register for **Planet Labs** or **Maxar** developer accounts for high-resolution optical imagery.
*   *Handoff to AI:* Place these keys securely in the local [.env](file:///f:/2026%20BUSINESS%20IDEAS/BRAINSTORM/SKYEYE/skyeye_engine/.env) file so the AI can write the fetch requests.

### 2. Database Scaffold (Phase 0.2)
Right now, the SkyEye Engine is stateless. If you restart the Python server, all active tracked events disappear.
*   **Task:** The human team needs to install a local PostgreSQL or MongoDB instance.
*   **Handoff to AI:** Provide the AI with the connection string (`DATABASE_URL=postgres://...`) so the AI can write the SQLAlchemy/Pydantic schemas to save events permanently.

### 3. CI/CD & GPU Slicing (Phase 0.4)
*   **Task:** Ensure the local Windows machine running 0Core has its Nvidia CUDA drivers properly exposed to the Python environment.
*   **Task:** Set up a local Github/Gitea runner so that as the AI pushes new Python code, it automatically restarts the [controller.py](file:///f:/2026%20BUSINESS%20IDEAS/BRAINSTORM/SKYEYE/skyeye_engine/controller.py) Flask server.

---

## The Handoff Plan
If you want to keep momentum, **I (the AI) should start writing Phase 2.5 (The Dispatch Queue) right now.** 

Simultaneously, you should hand this document to your local human team and tell them to start hunting down the NASA FIRMS and Planet Labs API keys (Phase 0.3).
