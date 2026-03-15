from datetime import datetime, timedelta
from skyeye_engine.config import Config
import random

class AutonomousScenarioProposer:
    """
    The 'Brain' of the Orchestration Engine.
    Identifies high-interest zones by correlating news, stale clusters, and physics anomalies.
    """
    def __init__(self, detector, tgh):
        self.detector = detector
        self.tgh = tgh
        self.proposed_tasks = []

    def propose_tasks(self):
        """
        Synthesizes current state into actionable 'Reconstruction Tasks'.
        1. Identifies event-driven tasks (from News Pins).
        2. Identifies staleness-driven tasks (where Confidence Dither is high).
        3. Identifies physics-driven tasks (where Genesis detected a conflict).
        """
        self.proposed_tasks = []
        
        # 1. News-Driven Tasks (Direct Observation Request)
        for event in self.detector.active_events:
            # If an event has a high score but no reconstruction yet
            key = f"{round(event['lat'], 4)},{round(event['lon'], 4)}"
            if key not in self.tgh.base_model:
                self.proposed_tasks.append({
                    "id": f"task_{random.randint(1000, 9999)}",
                    "type": "OBSERVED_BASELINE_ESTABLISHMENT",
                    "lat": event['lat'],
                    "lon": event['lon'],
                    "reason": f"Active {event['type']} detected via news signal. Baseline required.",
                    "urgency": event.get('urgency', 5),
                    "taxonomy_needed": ["visual.optical", "thermal.land_surface"],
                    "solver_hint": event.get('solver_hint', 'RigidBody')
                })

        # 2. Staleness-Driven Tasks (Confidence Decay)
        now = datetime.now()
        for key, base in self.tgh.base_model.items():
            last_sync = base['timestamp'] # Simple for alpha
            hours_since = (now - last_sync).total_seconds() / 3600
            
            # Predict decay
            estimated_confidence = 1.0 - (hours_since * Config.UNCERTAINTY_DECAY_RATE)
            
            if estimated_confidence < 0.7:
                lat, lon = map(float, key.split(','))
                self.proposed_tasks.append({
                    "id": f"task_{random.randint(1000, 9999)}",
                    "type": "CHRONOS_SYNC",
                    "lat": lat,
                    "lon": lon,
                    "reason": f"Spatio-temporal confidence decayed to {int(estimated_confidence*100)}%. Refresh required.",
                    "urgency": 3,
                    "taxonomy_needed": ["visual.optical"]
                })

        # 3. Physics-Driven Tasks (Inference Refinement)
        # In a real build, we'd scan delta_hierarchy for physics_score < VALIDATION_STRICTNESS
        # Mocking one for the Doctrine payoff
        if random.random() > 0.7:
            self.proposed_tasks.append({
                "id": f"task_{random.randint(1000, 9999)}",
                "type": "GENESIS_RECONCILIATION",
                "lat": 0.0, "lon": 0.0, # Placeholder
                "reason": "Delta inconsistent with Gravity Terrain Model (Rule 2). High-res Radar probe recommended.",
                "urgency": 8,
                "taxonomy_needed": ["structure.radar", "terrain.elevation"]
            })

        return sorted(self.proposed_tasks, key=lambda x: x['urgency'], reverse=True)

    def execute_task(self, task_id):
        # In a final version, this would trigger the actual Ingest/Fusion loop
        pass
