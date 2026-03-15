import requests
import json

BASE = "http://localhost:5050"

print("=" * 60)
print("EARTH OS: END-TO-END LIVE INTEGRATION TEST")
print("=" * 60)

# 1. News Pins (should include REAL USGS earthquakes)
print("\n[1] NEWS PINS (USGS LIVE + GDACS)...")
try:
    r = requests.get(f"{BASE}/news-pins", timeout=30)
    pins = r.json()
    for p in pins[:3]:
        src = p.get("source", "unknown")
        print(f"    [{src.upper()}] {p['title']} | Urgency: {p['urgency']} | Solver: {p.get('solver_hint','?')}")
    print(f"    ... {len(pins)} total pins loaded")
except Exception as e:
    print(f"    FAILED: {e}")

# 2. Probe a REAL location (Frankfurt)
print("\n[2] PROBING FRANKFURT (50.1, 8.6) WITH LIVE SENSORS...")
try:
    r = requests.post(f"{BASE}/probe", json={"lat": 50.1, "lon": 8.6}, timeout=30)
    d = r.json()
    view = d.get("current_view", {})
    sensors = view.get("sensors", {})
    
    # Show each layer and its source
    for key, val in sensors.items():
        if key.startswith("_"):
            continue
        if isinstance(val, dict):
            src = val.get("source", "internal")
            v = val.get("val", "?")
            print(f"    {key}: val={v} | source={src}")
    
    print(f"\n    ONTOLOGY: {view.get('ontology', '?')}")
    print(f"    TRUST SCORE: {view.get('physics_consistency_score', '?')}")
except Exception as e:
    print(f"    FAILED: {e}")

# 3. Dispatch (VLM-prioritized)
print("\n[3] AI ANOMALY DISPATCH...")
try:
    r = requests.get(f"{BASE}/dispatch", timeout=30)
    ranked = r.json()
    for p in ranked[:3]:
        print(f"    [{p.get('gravity_score','?')}G] {p['title']} | {p.get('dispatch_status','?')}")
        print(f"         VLM: {p.get('vlm_analysis','?')}")
except Exception as e:
    print(f"    FAILED: {e}")

# 4. Interpret (SAM 2 / VLM)
print("\n[4] VLM SCENE INTERPRETATION...")
try:
    r = requests.post(f"{BASE}/interpret", json={"lat": 50.1, "lon": 8.6, "prompt": "potential ruins"}, timeout=30)
    d = r.json()
    for ent in d.get("entities", []):
        print(f"    [ENTITY] {ent['label']} ({ent['confidence']*100:.0f}%)")
    print(f"    REASONING: {d.get('vlm_reasoning', {}).get('analysis', '?')}")
except Exception as e:
    print(f"    FAILED: {e}")

print("\n" + "=" * 60)
print("END-TO-END VERIFICATION COMPLETE")
print("=" * 60)
