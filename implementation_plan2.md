# SKYEYE: Master Implementation Plan (Reprioritized)

This document outlines the Phase 0-7 architectural roadmap for SkyEye, rigorously reprioritized to focus on the **Living System Orchestration Engine** (Event Detection, Dispatch, Streaming, Provenance) over "nice-to-have" enhancements. It strictly follows the `AI_SYSTEM_DESIGN_DOCTRINE`.

## Critical Dependencies (The Core Engine)
These phases **cannot be skipped** or the system remains a static batch processor rather than a living intelligence platform:
* **Event Detection (1.5):** Triggers reconstructions.
* **Dispatch Layer (2.5):** Executes reconstructions.
* **Streaming Engine (4.5):** Pushes live updates to the UI.
* **Provenance (3.5):** Establishes trust in outputs.
* **Geolocation (1.2):** Processes un-tagged video.

## Deferrable Enhancements (Future Scope)
* Neural Super-Resolution (5.1) -> Nice to have.
* Collaboration (6.5) -> MVP is single-user.
* Training Loop (7.x) -> Models work initially, improve later.

---

## Immediate Roadmap (4-Week Agile Plan)

### Week 1: Event Detection (Phase 1.5)
**Goal:** Build the missing trigger mechanism.
- [ ] Implement [EventDetector](file:///f:/2026%20BUSINESS%20IDEAS/BRAINSTORM/SKYEYE/skyeye_engine/detect/event_detector.py#4-50) class.
- [ ] Connect to news APIs (Reuters, AP) alongside GDACS/USGS.
- [ ] Add thermal anomaly detection (Landsat/MODIS hooks).
- [ ] Create priority scoring algorithm.
- [ ] Test on historical events (e.g., Beirut explosion).

### Week 2: Dispatch Layer (Phase 2.5)
**Goal:** Build the orchestration controller.
- [ ] Implement `PriorityDispatcher` with 3 queues (Immediate/Normal/Low).
- [ ] Create `GPUResourcePool` (local GPUs first/0Core infrastructure).
- [ ] Build `PipelineSelector` logic.
- [ ] Add status tracking dashboard metrics for the Agent Uplink.
- [ ] Test end-to-end: ingest → detect → dispatch → reconstruct.

### Week 3: Geolocation Pipeline (Phase 1.2)
**Goal:** Handle GPS-less videos.
- [ ] Implement landmark matching (feature extraction + satellite baseline).
- [ ] Add shadow analysis (sun angle calculation).
- [ ] Build crowdsourced verification UI.
- [ ] Test on known-location videos first.

### Week 4: Streaming Engine (Phase 4.5)
**Goal:** Make updates live in the 3-Panel UI.
- [ ] Set up WebSocket server.
- [ ] Implement viewport tracking (Sync Cesium camera to backend).
- [ ] Add push notification logic (UI Action: "New Telemetry Received").
- [ ] Build client-side tile blending (Cesium imagery layer opacity transitions).
- [ ] Test with simulated reconstruction updates.

---

## The Complete Master Architecture (Phases 0-7)

### Phase 0: Foundation
- [ ] 0.1: Development Environment Setup
- [ ] 0.2: Database Schema (events, reconstructions, tiles, users)
- [ ] 0.3: Cloud Infrastructure (AWS/GCP accounts, S3 buckets, GPU quotas)
- [ ] 0.4: CI/CD Pipeline (automated testing, deployment)

### Phase 1: Ingest Layer
- [x] 1.1: Satellite Stream Monitors (COMPLETE)
- [ ] **1.2: Video Geolocation Engine (CRITICAL)**
- [x] 1.3: News API Scrapers (GDACS/USGS)
- [ ] 1.4: Citizen Upload Portal
- [ ] **1.5: Event Detection System (CRITICAL - WEEK 1)**
- [ ] 1.6: Data Standardization
- [x] 1.7: STAC Integration (Microsoft Planetary Computer)
- [ ] 1.8: Content Moderation (NEW)

### Phase 2: Fusion Layer
- [x] 2.1: TGH Temporal Hierarchy (COMPLETE)
- [ ] 2.2: Satellite Change Detection (NEW)
- [x] 2.3: Multi-Sensor Fusion
- [ ] 2.4: Confidence Propagation
- [ ] **2.5: Dispatch & Resource Orchestration (CRITICAL - WEEK 2)**

### Phase 3: Reconstruction Layer
- [ ] 3.1: Temporal Physics Validation (NEW)
- [ ] 3.2: Multi-View Photogrammetry Pipeline (NEW)
- [ ] 3.3: Single-View Monocular Pipeline
- [ ] 3.4: Genesis Physics Validator (PROGRESSING)
- [ ] **3.5: Confidence Tracking & Provenance (CRITICAL)**
- [ ] 3.6: Dither3D LOD Generation
- [ ] 3.7: Tile Generation (3D Tiles format)
- [ ] 3.8: Error Handling & Graceful Degradation (NEW)

### Phase 4: Frontend Layer (Doctrine Compliant)
- [x] 4.1: 3-Panel UI Architecture (Doctrine Created, Dev Pending)
- [x] 4.2: Cesium Integration
- [x] 4.3: Sensor Toggle Controls
- [ ] 4.4: Timeline Scrubber
- [ ] **4.5: Live Streaming & Push Updates (CRITICAL - WEEK 4)**
- [ ] 4.6: Confidence Visualization
- [ ] 4.7: Mobile Optimization

### Phase 5: Enhancement Layer (DEFERRED)
- [ ] 5.1: Neural Super-Resolution (DEFERRED)
- [ ] 5.2: AR Integration
- [ ] 5.3: VR Integration
- [ ] 5.4: Voice Commands
- [ ] 5.5: Authentication & Access Control (NEW)
- [ ] 5.6: Multi-Language Support
- [ ] 5.7: Accessibility Features
- [ ] 5.8: Export Tools & API (NEW)

### Phase 6: Operations Layer
- [ ] 6.1: Monitoring Dashboard (Agent Uplink)
- [ ] 6.2: Alert System
- [ ] 6.3: Cost Optimization
- [ ] 6.4: Auto-Scaling Logic
- [ ] 6.5: Collaboration Features (DEFERRED)

### Phase 7: Improvement Layer (DEFERRED)
- [ ] 7.1: Training Data Collection (NEW)
- [ ] 7.2: Model Retraining
- [ ] 7.3: A/B Testing Framework
- [ ] 7.4: Performance Analytics
