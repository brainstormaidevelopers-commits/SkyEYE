# BRAINStØrm UI/UX Doctrine: Frictionless Earth Interface

**Core Principle: The interface disappears. The Earth remains.**

## THE FUNDAMENTAL UX PROBLEM
Most geospatial platforms fail because they present **tools before place**.
*   **Wrong approach:** User opens app → sees toolbar, layers panel, legend, zoom controls → feels overwhelmed → abandons.
*   **BRAINStØrm approach:** User opens app → sees Earth → feels curiosity → goes somewhere → discovers capabilities naturally.

## 1. THE ENTRY EXPERIENCE
*   **First 3 seconds:** Full-screen Earth (Cesium globe), single search bar at top ("Where do you want to look?"), subtle prompt. Nothing else.
*   **Interaction:** Search → Globe flies there (2-3 sec) → Interface elements fade in contextually. Place first, tools second.

## 2. THE THREE-MODE INTERFACE STRUCTURE

### Mode A: Exploratory (Public Default)
*   **Target:** General public, students, curious humans.
*   **Minimal chrome:** Search, account, settings.
*   **Context cards:** Info appears near location.
*   **Sensor strip:** Bottom bar with sensor toggles.
*   **Timeline:** Inline scrubber.
*   **News pins:** Float over locations, click to expand.
*   **No sidebars. No toolbars. Just Earth + contextual overlays.**

### Mode B: Truth (Analyst/Researcher)
*   **Target:** Scientists, OSINT analysts, emergency responders, journalists.
*   **Three-panel layout:** (Per the [AI_SYSTEM_DESIGN_DOCTRINE.md](file:///F:/2026%20BUSINESS%20IDEAS/AI_SYSTEM_DESIGN_DOCTRINE.md)).
    *   **Left:** Task list (Active monitoring, saved locations).
    *   **Center:** Earth.
    *   **Right:** Data provenance (Sources, confidence, export).
*   **Truth badges:** `[Observed]`, `[Inferred]`, `[Predicted]` always visible.
*   **Confidence meters:** Visual clarity on certainty (High=Green, Low=Orange).
*   **Diffusion rules:** Disabled by default. If enabled, labeled `[Enhanced]` and never mixed with observed data.

### Mode C: Cinematic (Event Replay/Storytelling)
*   **Target:** Journalists, educators, documentary creators.
*   **Fullscreen by default:** Immersive experience.
*   **Playback controls:** Standard video interface.
*   **Source count:** Transparency without overwhelming detail.
*   **Diffusion rules:** Allowed for visual completion, clearly labeled at start.

## 3. THE SENSORY SWITCHER (Core Innovation)
*   **Bottom toolbar:** Always accessible, never intrusive (Vision, Thermal, Radar, Chemical, Ocean, Seismic, Weather).
*   **Single click:** Switches active sensor, globe updates instantly with smooth crossfade, UI color scheme shifts to match sensor.

## 4. THE TIMELINE SCRUBBER
*   **Inline time control:** Drag slider updates globe real-time. Data availability indicators show when data exists.
*   **Smart features:** Auto-snap to events, playback mode with speed control.

## 5. THE NEWS PIN SYSTEM
*   **Pins:** Colored dots (Red=Active conflict, Orange=Breaking, Yellow=Developing, Blue=Historical).
*   **Features:** Auto-clustering, recency filtering, source diversity, one-click access to reconstructions.

## 6. THE CONFIDENCE VISUALIZATION SYSTEM
*   **Overlays:** High confidence (Solid), Medium (Desaturated), Low (Transparent overlay), Very low (Dotted pattern).
*   **Color coding:** Green (Observed), Blue (Fused), Yellow (Predicted), Purple (Simulated), Orange (Enhanced/diffusion).

## 7. SEARCH & DISCOVERY
*   **Search accepts:** Place names, addresses, coordinates, natural language ("wildfire California"), events, sensors.
*   **Discovery:** Trending locations, recent events, saved places.

## 8. MOBILE EXPERIENCE
*   **Touch-optimized:** Pinch, pan, rotate, long-press gestures. Bottom swipe for sensors.
*   **Features:** AR mode toggle, GPS auto-center, offline mode caching.

## 9. ONBOARDING FLOW
*   30 seconds max. Welcome → Demo animation → Interaction prompt → Guided first search. Just Earth.

## 10-15. SYSTEM STANDARDS
*   **Accessibility:** High contrast, screen reader, voice commands.
*   **Collaboration:** Deep links including active sensors and timeline position.
*   **Freemium Model:** Genuinely useful free tier, Pro allows high-res and full archive.
*   **Performance:** <2s initial load, <100ms tile load, progressive enhancement.
*   **Trust & Safety:** Built-in reporting, strict provenance transparency.
*   **AR/VR Transition:** Same interface paradigm extended to mixed reality.

## 16. THE FINAL UX PRINCIPLE "Peek through the blinds"
*   Opening curtains. Looking outside. Not entering a new world. Always grounded.
*   **If the user thinks about the interface, we failed. If the user thinks about Earth, we succeeded.**

---

## IMPLEMENTATION PRIORITY
*   **Phase 1: Core Experience (MVP)** - Globe, search, fly-to, basic sensors, timeline, context cards, news pins.
*   **Phase 2: Truth Features** - Three-panel analyst mode, provenance, confidence visualization, export.
*   **Phase 3: Engagement** - Annotations, sharing, collaboration, mobile optimization.
*   **Phase 4: Advanced** - AR/VR, voice commands, offline mode.
