import time
from typing import Dict, List, Any
from collections import deque
from skyeye_engine.brain.semantic_engine import SemanticEngine
from skyeye_engine.detect.event_logger import logger

class GPUResourcePool:
    """
    Simulates local VRAM orchestration for 0Core.
    """
    def __init__(self, max_concurrent: int = 2):
        self.capacity = max_concurrent
        self.active_jobs = 0

    def allocate(self) -> bool:
        if self.active_jobs < self.capacity:
            self.active_jobs += 1
            return True
        return False

    def release(self):
        if self.active_jobs > 0:
            self.active_jobs -= 1

class PriorityDispatcher:
    """
    AI Anomaly Dispatcher (Phase 2.5)
    Prioritizes global events and manages 3 execution queues.
    """
    def __init__(self, semantic_engine: SemanticEngine):
        self.engine = semantic_engine
        self.gpu_pool = GPUResourcePool()
        # 3-Tier Queue System
        self.queues = {
            "IMMEDIATE": deque(),
            "NORMAL": deque(),
            "LOW": deque()
        }

    def _determine_pipeline(self, event_type: str) -> str:
        """Phase 2.5 Pipeline Selector"""
        if event_type in ['flood', 'weather']:
            return "SPH" # Smoothed Particle Hydrodynamics
        elif event_type in ['seismic', 'landslide']:
            return "MPM" # Material Point Method
        return "PBD" # Position Based Dynamics (Default)

    def prioritize_events(self, pins: List[Dict[str, Any]], sensor_manager) -> List[Dict[str, Any]]:
        """Scores and explicitly routes events into the Execution Queues."""
        ranked = []
        for pin in pins:
            context = sensor_manager.gather_all_sensors(pin['lat'], pin['lon'])
            reasoning = self.engine.reason_anomaly(pin.get('title', ''), context['layers'])
            
            # Phase 1.5 Integration: EventDetector assigns base 'score' out of 10.0
            base_score = pin.get('score', 5.0)
            gravity = base_score + (reasoning['priority_boost'] / 10.0)
            
            solver = self._determine_pipeline(pin.get('type', 'generic'))
            
            status = "MONITORING"
            if gravity >= 8.5:
                status = "QUEUED_IMMEDIATE"
                self.queues["IMMEDIATE"].append(pin['id'])
            elif gravity >= 6.0:
                status = "QUEUED_NORMAL"
                self.queues["NORMAL"].append(pin['id'])
            elif gravity >= 3.0:
                status = "QUEUED_LOW"
                self.queues["LOW"].append(pin['id'])

            ranked.append({
                **pin,
                "gravity_score": round(gravity, 2),
                "vlm_analysis": reasoning['analysis'],
                "dispatch_status": status,
                "solver_pipeline": solver
            })
            
        return sorted(ranked, key=lambda x: x['gravity_score'], reverse=True)

    def execute_next_tick(self):
        """Called by the main loop to pop queues and allocate GPU."""
        for q_name in ["IMMEDIATE", "NORMAL", "LOW"]:
            if self.queues[q_name]:
                if self.gpu_pool.allocate():
                    job_id = self.queues[q_name].popleft()
                    logger.log("dispatch", f"Allocated 0Core VRAM for Job {job_id} from {q_name} queue.")
                    # In a real system, this triggers async Celery/0Core handoff
                    # self.trigger_reconstruction(job_id)
                    time.sleep(0.5) # Simulate handoff delay
                    self.gpu_pool.release()
                    return job_id
        return None
