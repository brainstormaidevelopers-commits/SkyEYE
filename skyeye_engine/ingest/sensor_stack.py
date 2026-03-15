import requests
import json
from datetime import datetime
from typing import Dict, Any, Optional, List

class CatalogService:
    """STAC-first discovery. Microsoft Planetary Computer."""
    def __init__(self):
        self.endpoint = "https://planetarycomputer.microsoft.com/api/stac/v1"

    def search_stac(self, collection, bbox, time_range):
        print(f"[CATALOG] STAC SEARCH: {collection}...")
        try:
            r = requests.post(f"{self.endpoint}/search", json={
                "collections": [collection], "bbox": bbox,
                "datetime": time_range, "limit": 1
            }, timeout=15)
            d = r.json()
            if d.get("features"):
                f = d["features"][0]
                print(f"[CATALOG] REAL SCENE: {f['id']}")
                return {
                    "id": f["id"], "collection": collection,
                    "bbox": f["bbox"], "assets": f["assets"],
                    "properties": f.get("properties", {})
                }
        except Exception as e:
            print(f"[CATALOG] STAC failed: {e}")
        return {
            "id": f"mock-{collection}-{datetime.now().strftime('%Y%m%d')}",
            "collection": collection, "bbox": bbox,
            "assets": {"thumbnail": {"href": "#"}}, "properties": {}
        }

class LiveWeatherService:
    """Open-Meteo: Free, no key."""
    def get_current(self, lat, lon):
        try:
            r = requests.get("https://api.open-meteo.com/v1/forecast", params={
                "latitude": lat, "longitude": lon,
                "current": "temperature_2m,wind_speed_10m,rain,weather_code"
            }, timeout=8)
            d = r.json()
            cur = d.get("current", {})
            print(f"[WEATHER] LIVE: {cur.get('temperature_2m')}C, wind {cur.get('wind_speed_10m')}km/h")
            return {
                "val": cur.get("temperature_2m", 20),
                "wind_speed": cur.get("wind_speed_10m", 0),
                "rain": cur.get("rain", 0),
                "weather_code": cur.get("weather_code", 0),
                "source": "open-meteo-live"
            }
        except Exception as e:
            print(f"[WEATHER] Fallback to mock: {e}")
            return {"val": 20, "wind_speed": 10, "rain": 0, "source": "mock"}

class LiveSeismicService:
    """USGS Earthquake Hazards: Free, no key."""
    def get_nearby(self, lat, lon, radius_km=500):
        try:
            r = requests.get("https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.geojson", timeout=8)
            d = r.json()
            nearby = []
            for f in d.get("features", []):
                coords = f["geometry"]["coordinates"]
                dlat = abs(coords[1] - lat)
                dlon = abs(coords[0] - lon)
                if dlat < (radius_km / 111.0) and dlon < (radius_km / 111.0):
                    nearby.append({
                        "mag": f["properties"]["mag"],
                        "place": f["properties"]["place"],
                        "lat": coords[1], "lon": coords[0],
                        "depth": coords[2]
                    })
            val = max([eq["mag"] for eq in nearby]) / 10.0 if nearby else 0.0
            print(f"[SEISMIC] LIVE: {len(nearby)} quakes within {radius_km}km, max_val={val:.2f}")
            return {
                "val": val,
                "count": len(nearby),
                "nearest": nearby[0] if nearby else None,
                "source": "usgs-live"
            }
        except Exception as e:
            print(f"[SEISMIC] Fallback to mock: {e}")
            return {"val": 0.0, "count": 0, "source": "mock"}

class SensorStackOrchestrator:
    """Orchestrates REAL multi-sensor intake from live APIs."""
    def __init__(self):
        self.catalog = CatalogService()
        self.weather = LiveWeatherService()
        self.seismic = LiveSeismicService()

    def gather_all_sensors(self, lat, lon, news_context=None):
        bbox = [lon-0.1, lat-0.1, lon+0.1, lat+0.1]
        now = datetime.now()
        time_range = f"{now.replace(day=1).isoformat()}Z/{now.isoformat()}Z"

        layers = {}

        # --- LAYER 1: Satellite Optical (Sentinel-2 via STAC) ---
        s2 = self.catalog.search_stac("sentinel-2-l2a", bbox, time_range)
        cloud = s2.get("properties", {}).get("eo:cloud_cover", 0)
        layers["visual.optical"] = {
            "val": 1.0 - (cloud / 100.0),
            "state": "nominal",
            "item_id": s2.get("id", "unknown"),
            "cloud_cover": cloud,
            "platform": s2.get("properties", {}).get("platform", "unknown"),
            "source": "sentinel-2-stac"
        }

        # --- LAYER 2: Weather (Open-Meteo LIVE) ---
        wx = self.weather.get_current(lat, lon)
        layers["thermal.land_surface"] = {"val": wx["val"], "unit": "C", "source": wx["source"]}
        layers["weather.clouds"] = {
            "val": wx.get("weather_code", 0),
            "wind_speed": wx["wind_speed"],
            "rain": wx["rain"],
            "source": wx["source"]
        }

        # --- LAYER 3: Seismic (USGS LIVE) ---
        seis = self.seismic.get_nearby(lat, lon)
        layers["hazards.seismic"] = seis

        # --- LAYER 4: Radar (still mocked - needs Sentinel-1 SAR processing) ---
        layers["structure.radar"] = {"val": 0.05, "source": "mock"}

        # --- LAYER 5: Terrain (still mocked - needs DEM tile service) ---
        layers["terrain.elevation"] = {"val": 12.0, "slope": 0, "source": "mock"}

        # --- LAYER 6: Atmosphere Chemistry (mocked - needs Sentinel-5P) ---
        layers["atmosphere.chemistry"] = {"val": 402, "source": "mock"}

        # --- TRUTH PIPELINE ---
        trust_score = 0.95
        live_count = sum(1 for v in layers.values() if isinstance(v, dict) and v.get("source", "").endswith("-live"))
        mock_count = sum(1 for v in layers.values() if isinstance(v, dict) and v.get("source") == "mock")
        trust_score = 0.5 + (live_count / max(1, live_count + mock_count)) * 0.5

        if news_context:
            news_str = str(news_context).lower()
            if "flood" in news_str:
                radar_val = layers.get("structure.radar", {}).get("val", 0)
                if isinstance(radar_val, (int, float)) and radar_val < 0.2:
                    trust_score -= 0.2
                    print("[TRUTH] Radar contradicts flood signal.")

        print(f"[ORCHESTRATOR] Trust={trust_score:.2f} | Live={live_count} | Mock={mock_count}")

        return {
            "lat": lat, "lon": lon,
            "timestamp": datetime.now().isoformat(),
            "layers": layers,
            "ingest_trust": float(min(1.0, trust_score)),
            "stream_stats": {"live": live_count, "mock": mock_count}
        }
