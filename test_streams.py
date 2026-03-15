import requests
import json

print("=" * 60)
print("EARTH OS: LIVE DATA STREAM VERIFICATION")
print("=" * 60)

# 1. USGS Earthquake Feed (NO KEY)
print("\n[1] USGS EARTHQUAKE FEED...")
try:
    r = requests.get("https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_day.geojson", timeout=10)
    d = r.json()
    count = len(d["features"])
    print(f"    STATUS: LIVE | {count} M4.5+ earthquakes in last 24h")
    if count > 0:
        eq = d["features"][0]
        props = eq["properties"]
        coords = eq["geometry"]["coordinates"]
        print(f"    LATEST: M{props['mag']} at {props['place']}")
        print(f"    COORDS: lat={coords[1]}, lon={coords[0]}, depth={coords[2]}km")
except Exception as e:
    print(f"    FAILED: {e}")

# 2. Open-Meteo Weather (NO KEY)
print("\n[2] OPEN-METEO WEATHER...")
try:
    r = requests.get("https://api.open-meteo.com/v1/forecast", params={
        "latitude": 50.1, "longitude": 8.6,
        "current": "temperature_2m,wind_speed_10m,rain,weather_code",
    }, timeout=10)
    d = r.json()
    cur = d["current"]
    print(f"    STATUS: LIVE")
    print(f"    TEMP: {cur['temperature_2m']}C | WIND: {cur['wind_speed_10m']}km/h | RAIN: {cur['rain']}mm")
except Exception as e:
    print(f"    FAILED: {e}")

# 3. Microsoft Planetary Computer STAC (NO KEY for search)
print("\n[3] PLANETARY COMPUTER STAC (Sentinel-2)...")
try:
    r = requests.post("https://planetarycomputer.microsoft.com/api/stac/v1/search", json={
        "collections": ["sentinel-2-l2a"],
        "bbox": [8.5, 50.0, 8.7, 50.2],
        "datetime": "2026-02-01T00:00:00Z/2026-03-15T00:00:00Z",
        "limit": 1
    }, timeout=15)
    d = r.json()
    if d.get("features"):
        f = d["features"][0]
        props = f["properties"]
        print(f"    STATUS: LIVE")
        print(f"    SCENE: {f['id']}")
        print(f"    CLOUD: {props.get('eo:cloud_cover', '?')}%")
        print(f"    PLATFORM: {props.get('platform', '?')}")
        print(f"    DATE: {props.get('datetime', '?')}")
        assets = list(f.get("assets", {}).keys())[:5]
        print(f"    ASSETS: {assets}")
    else:
        print("    STATUS: OK but no scenes found in date range (try wider range)")
except Exception as e:
    print(f"    FAILED: {e}")

print("\n" + "=" * 60)
print("STREAM VERIFICATION COMPLETE")
print("=" * 60)
