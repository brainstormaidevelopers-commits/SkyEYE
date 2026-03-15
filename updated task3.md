# SKYEYE Task Tracker

This document tracks the execution of the Phase 0-7 Master Architecture Roadmap, reprioritized for the Week 1-4 Critical Dependencies Sprint.

## Current Priority: Week 3 - Geolocation Pipeline (Phase 1.2)

**Goal:** Handle GPS-less un-tagged videos via landmarks.

### Immediate Next Steps
- [ ] **1.2.1: Video Feature Extraction:** Scaffold `video_geolocator.py` to extract features from uploaded MP4 clips.
- [ ] **1.2.2: Shadow Analysis:** Write the sun-angle geometry math for broad geospatial bounding boxes.
- [ ] **1.2.3: Satellite Baseline Matching:** Sync `1.2.1` feature matches against the STAC Planetary Computer optical baseline.
- [ ] **4.1.5: Timeline Scrubber**: Wire the `<input type="range">` visual scrubber to the backend.

---

## Upcoming Sprints
* **Week 2: Dispatch Layer (Phase 2.5):** Priority queueing, GPU resource pools, Pipeline selectors.
* **Week 3: Geolocation Pipeline (Phase 1.2):** Handling GPS-less un-tagged videos via landmarks.
* **Week 4: Streaming Engine (Phase 4.5):** WebSockets, push telemetry, UI Live syncing.

## Deferred Tasks
- Phase 5.1: Neural Super-Resolution Execution (Deferred)
- Phase 4.1: Doctrine UI Overhaul (Deferred pending core engine completion)
- Phase 6.5: Collaboration Features (Deferred)

## Completed
- [x] Phase 1.1: Satellite Stream Monitors
- [x] Phase 1.3: News API Scrapers (USGS/GDACS Mocks -> Live transitioning)
- [x] Phase 1.7: STAC Integration
- [x] Phase 2.1: TGH Temporal Hierarchy
- [x] Phase 4.2: Cesium Integration
- [x] AI System Design Doctrine established.
