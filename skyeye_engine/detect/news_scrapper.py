import requests
from datetime import datetime
from typing import List, Dict, Any

class NewsScraper:
    """
    Live News-Pin Scraper for Earth OS.
    Pulls REAL earthquake data from USGS + mocked GDACS events.
    """
    def __init__(self):
        self.usgs_feed = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_day.geojson"

    def get_all_active_pins(self) -> List[Dict[str, Any]]:
        pins = []

        # --- REAL: USGS Earthquake Feed ---
        try:
            r = requests.get(self.usgs_feed, timeout=8)
            d = r.json()
            for f in d.get("features", [])[:5]:
                props = f["properties"]
                coords = f["geometry"]["coordinates"]
                pins.append({
                    "id": f["id"],
                    "title": f"M{props['mag']} {props.get('place', 'Unknown')}",
                    "type": "seismic",
                    "lat": coords[1],
                    "lon": coords[0],
                    "urgency": min(10, int(props["mag"] * 2)),
                    "solver_hint": "PBD",
                    "description": f"Depth: {coords[2]}km | {props.get('type', 'earthquake')}",
                    "source": "usgs-live"
                })
            print(f"[SCRAPER] Pulled {len(pins)} LIVE earthquakes from USGS")
        except Exception as e:
            print(f"[SCRAPER] USGS failed ({e}), using mocks")

        # --- REAL: GDACS Live RSS Feed ---
        import xml.etree.ElementTree as ET
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            r_gdacs = requests.get("https://www.gdacs.org/xml/rss.xml", timeout=8, headers=headers)
            root = ET.fromstring(r_gdacs.content)
            
            namespaces = {'geo': 'http://www.w3.org/2003/01/geo/wgs84_pos#'}
            
            for item in root.findall('.//item')[:5]:
                title = item.find('title').text
                description = item.find('description').text
                geo_point = item.find('geo:Point', namespaces)
                
                if geo_point is not None:
                    lat_str = geo_point.find('geo:lat', namespaces).text
                    lon_str = geo_point.find('geo:long', namespaces).text
                    lat, lon = float(lat_str), float(lon_str)
                    
                    pins.append({
                        "id": title[:10].replace(" ", "_"),
                        "title": "GDACS: " + title,
                        "type": "rss_news",
                        "lat": lat,
                        "lon": lon,
                        "urgency": 7,
                        "solver_hint": "SPH",
                        "description": description[:100],
                        "source": "gdacs-live"
                    })
            print(f"[SCRAPER] Pulled {len(pins) - len(d.get('features', [])[:5])} LIVE RSS pins from GDACS")
        except Exception as e:
            print(f"[SCRAPER] GDACS XML parsing failed ({e}), using fallback mocks")
            pins.extend([
                {
                    "id": "gdacs_storm_001",
                    "title": "Hurricane Alpha Approach",
                    "type": "weather",
                    "lat": 12.5, "lon": -65.0,
                    "urgency": 9,
                    "solver_hint": "PBD",
                    "description": "High wind speeds detected.",
                    "source": "gdacs-mock"
                }
            ])

        return pins

    def log_global_awareness(self):
        print(f"[SCRAPER] {datetime.now().isoformat()}: Multi-modal signals gathered.")
