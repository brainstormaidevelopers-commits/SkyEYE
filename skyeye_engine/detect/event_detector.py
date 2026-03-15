from datetime import datetime
from skyeye_engine.config import Config

class EventDetector:
    """
    Monitors data signals (Thermal spikes, GDACS, USGS)
    to trigger the Orchestration Dispatcher.
    """
    
    def __init__(self):
        self.active_events = []
        self._seen_ids = set()

    def evaluate_signals(self, signals):
        """
        Expects a list of signal dicts:
        [{'type': 'seismic', 'lat': x, 'lon': y, 'urgency': 7, 'title': '...'}, ...]
        """
        detected = []
        for signal in signals:
            sig_id = signal.get('id', '')
            if sig_id in self._seen_ids:
                continue

            score = self.calculate_priority(signal)
            
            if score >= Config.EVENT_SCORE_MIN:
                event = {
                    'id': f"EVT_{sig_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    'lat': signal.get('lat'),
                    'lon': signal.get('lon'),
                    'score': score,
                    'type': signal.get('type'),
                    'title': signal.get('title', 'Unknown Event'),
                    'timestamp': datetime.now().isoformat(),
                    'source': signal.get('source', 'unknown')
                }
                print(f"[DETECT] Critical Event Triggered! {event['title']} (Score: {score:.1f})")
                self.active_events.append(event)
                self._seen_ids.add(sig_id)

                # Persist to Database
                try:
                    from skyeye_engine.db import db_manager, EventModel
                    session = db_manager.Session()
                    db_event = EventModel(
                        external_id=sig_id,
                        title=event['title'],
                        lat=event['lat'],
                        lon=event['lon'],
                        score=event['score'],
                        category=event['type'],
                        data=signal
                    )
                    session.add(db_event)
                    session.commit()
                    session.close()
                except Exception as e:
                    print(f"[DETECT] Database save failed: {e}")

                detected.append(event)
        return detected

    def calculate_priority(self, signal):
        """
        Scoring logic for Phase 1.5 event detection.
        Assigns 1-10 scores based on urgency and type.
        """
        score = 0.0
        sig_type = signal.get('type', '')
        
        # Base urgency often provided by scraper (e.g. earthquake magnitude * 2)
        base_urgency = float(signal.get('urgency', 1.0))
        
        if sig_type == 'thermal':
            # Thermal spikes (wildfires, explosions) are high priority
            val = float(signal.get('value', 0))
            if val > Config.THERMAL_ANOMALY_THRESHOLD:
                score = 6.0 + (val / 10.0)
        elif sig_type == 'seismic':
            # Earthquakes (USGS)
            score = base_urgency * 1.2
        elif sig_type == 'flood' or sig_type == 'weather':
            # Natural disasters (GDACS)
            score = base_urgency * 1.0
        elif sig_type == 'rss_news':
            # General breaking news
            score = base_urgency * 0.8
        elif sig_type == 'video_cluster':
            score = 6.0
            
        # Cap score at 10.0
        return min(10.0, score)

    def fetch_thermal_anomalies(self):
        """
        Phase 1.5: Hook to fetch FIRMS / MODIS thermal anomalies.
        Currently mocked for structural scaffolding.
        """
        # In a production environment, this would hit Earthdata FIRMS API
        mock_anomalies = [
            {'id': 'therm_ca_1', 'type': 'thermal', 'lat': 34.0522, 'lon': -118.2437, 'value': 25.0, 'title': 'CA Wildfire Indicator', 'source': 'mock-firms'}
        ]
        return self.evaluate_signals(mock_anomalies)

if __name__ == "__main__":
    detector = EventDetector()
    mock_signals = [
        {'id': 'eq1', 'type': 'seismic', 'lat': 35.0, 'lon': -120.0, 'urgency': 8, 'title': 'M8.0 Earthquake'},
        {'id': 'news1', 'type': 'rss_news', 'lat': 50.0, 'lon': 30.0, 'urgency': 5, 'title': 'Local Protest'}
    ]
    detected = detector.evaluate_signals(mock_signals)
    print(f"Detected {len(detected)} critical events.")
