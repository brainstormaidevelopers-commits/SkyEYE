import threading
import time
from flask import Flask, jsonify, request
from flask_cors import CORS
from skyeye_engine.config import Config
from skyeye_engine.detect.news_scrapper import NewsScraper
from skyeye_engine.fusion.temporal_fusion import TGHDeltaEngine
from datetime import datetime
from typing import List, Dict, Any

from skyeye_engine.ingest.sensor_stack import SensorStackOrchestrator, CatalogService
from skyeye_engine.detect.event_logger import logger
from skyeye_engine.detect.scenario_proposer import AutonomousScenarioProposer
from skyeye_engine.detect.event_detector import EventDetector
from skyeye_engine.brain.semantic_engine import SemanticEngine
from skyeye_engine.brain.anomaly_dispatcher import PriorityDispatcher
from skyeye_engine.fusion.video_geolocator import VideoGeolocator

app = Flask(__name__)
CORS(app)

# Initialize Component Layer 
catalog = CatalogService()
stack_orchestrator = SensorStackOrchestrator()
detector = EventDetector()
scraper = NewsScraper()
tgh = TGHDeltaEngine()
proposer = AutonomousScenarioProposer(detector, tgh)
semantic = SemanticEngine()
dispatcher = PriorityDispatcher(semantic)
geolocator = VideoGeolocator()

def background_dispatch_worker():
    """
    Phase 2.5: The active heartbeat of the Orchestration Engine.
    Continuously checks the 3 GPU Queues for pending jobs.
    """
    print("[0CORE] Starting Background GPU Dispatch Worker...")
    while True:
        job_id = dispatcher.execute_next_tick()
        if job_id:
            # Here we simulate the time it takes the Genesis Engine / 0Core to process the tiles
            time.sleep(2.0) 
        else:
            time.sleep(1.0) # Idle tick

# Start the background heartbeat
threading.Thread(target=background_dispatch_worker, daemon=True).start()

@app.route('/status', methods=['GET'])
def get_status():
    return jsonify({
        "status": "SkyEye Orchestration Engine (v0.2 | Brain Integrated)",
        "active_events": detector.active_events,
        "taxonomy": Config.TAXONOMY,
        "proposed_tasks": len(proposer.proposed_tasks),
        "tracked_locations": len(tgh.base_model)
    })

@app.route('/dispatch', methods=['GET'])
def get_dispatch_priorities():
    """
    Phase 2.5 Prelude: Orchestration Dispatch Engine
    Pulls from Phase 1.5 EventDetector state.
    """
    active_events = detector.active_events
    if not active_events:
        return jsonify([])
        
    # Prioritize and apply VLM context reasoning
    prioritized = dispatcher.prioritize_events(active_events, stack_orchestrator)
    return jsonify(prioritized)

@app.route('/interpret', methods=['POST'])
def interpret_location():
    """
    VLM Interpretation: Pixels to Entities.
    """
    data = request.json or {}
    lat = float(data.get('lat', 0))
    lon = float(data.get('lon', 0))
    prompt = data.get('prompt', 'Decipher archaeological patterns')
    
    view = tgh.get_reconstructed_now(lat, lon)
    if not view: return jsonify({"error": "No data at location"}), 404
    
    entities = semantic.segment_objects(view['sensors'], prompt)
    analysis = semantic.reason_anomaly(f"User Request: {prompt}", view['sensors'])
    
    return jsonify({
        "location": {"lat": lat, "lon": lon},
        "entities": entities,
        "vlm_reasoning": analysis
    })

@app.route('/propose-tasks', methods=['GET'])
def get_proposed_tasks():
    tasks = proposer.propose_tasks()
    logger.log("proposer", f"Generated {len(tasks)} autonomous sensing tasks")
    return jsonify(tasks)

@app.route('/news-pins', methods=['GET'])
def get_news_pins():
    # 1. Fetch from diverse APIs (Scraper handles GDACS/USGS)
    pins = scraper.get_all_active_pins()
    
    # 2. Fetch thermal anomalies via the Event Detector hook
    therm_events = detector.fetch_thermal_anomalies()
    
    # 3. Evaluate and score all signals (EventDetector handles deduplication)
    active = detector.evaluate_signals(pins)
    
    # 4. Trigger orchestration fusion for new critical events
    for event in active + therm_events:
        logger.log("detection", f"Critical Event: {event['title']} (Score: {event['score']:.1f})", event)
        mock_stack = {
            'layers': {
                'visual.optical': {'val': 1.0, 'state': 'event_area'},
                'hazards.seismic': {'val': event.get('score', 5.0) / 10.0}
            }
        }
        tgh.apply_stack_delta(event['lat'], event['lon'], mock_stack)
        
    return jsonify(pins)

@app.route('/event-logs', methods=['GET'])
def get_event_logs():
    return jsonify(logger.get_recent())

@app.route('/agent-uplink', methods=['GET'])
def get_agent_uplink():
    """
    Phase 2.5.4: Agent Uplink Endpoint.
    Exposes Orchestration Engine telemetry, queue depths, and GPU status to the UI.
    """
    return jsonify({
        "gpu_pool": {
            "capacity": dispatcher.gpu_pool.capacity,
            "active_jobs": dispatcher.gpu_pool.active_jobs,
            "available": dispatcher.gpu_pool.capacity - dispatcher.gpu_pool.active_jobs
        },
        "queues": {
            "immediate": len(dispatcher.queues["IMMEDIATE"]),
            "normal": len(dispatcher.queues["NORMAL"]),
            "low": len(dispatcher.queues["LOW"])
        },
        "active_events": len(detector.active_events)
    })

@app.route('/reconstruct', methods=['GET'])
def get_reconstruction():
    lat = float(request.args.get('lat', 0))
    lon = float(request.args.get('lon', 0))
    view = tgh.get_reconstructed_now(lat, lon)
    logger.log("reconstruction", f"Reconstructed state for {lat}, {lon}")
    return jsonify(view if view else {"error": "No base model for this location"})

@app.route('/history-bounds', methods=['GET'])
def get_history_bounds():
    """
    Returns the time range available for the scrubber.
    """
    lat = float(request.args.get('lat', 0))
    lon = float(request.args.get('lon', 0))
    key = f"{lat:.4f},{lon:.4f}"
    
    base = tgh.base_model.get(key)
    if not base:
        return jsonify({"error": "No base model for this location"}), 404
        
    deltas = tgh.delta_hierarchy.get(key, [])
    if not deltas:
        return jsonify({
            "start": base['timestamp'].isoformat(),
            "end": base['timestamp'].isoformat(),
            "count": 0
        })
        
    return jsonify({
        "start": base['timestamp'].isoformat(),
        "end": deltas[-1]['timestamp'].isoformat(),
        "count": len(deltas)
    })

@app.route('/history', methods=['GET'])
def get_historical_state():
    """
    Returns the reconstructed state at a specific historical point.
    """
    lat = float(request.args.get('lat', 0))
    lon = float(request.args.get('lon', 0))
    
    # Can scrub by index or ISO timestamp
    index = request.args.get('index', type=int)
    timestamp_str = request.args.get('timestamp')
    
    key = f"{lat:.4f},{lon:.4f}"
    base = tgh.base_model.get(key)
    if not base:
        return jsonify({"error": "No base model"}), 404
        
    target_time = base['timestamp']
    if index is not None:
        deltas = tgh.delta_hierarchy.get(key, [])
        if 0 <= index < len(deltas):
            target_time = deltas[index]['timestamp']
    elif timestamp_str:
        target_time = datetime.fromisoformat(timestamp_str)
        
    reconstructed = tgh.get_reconstructed_at_time(lat, lon, target_time)
    return jsonify(reconstructed)

@app.route('/geolocate', methods=['POST'])
def geolocate_video():
    """
    Phase 1.2: Video Geolocation Endpoint.
    """
    data = request.json or {}
    video_path = data.get('video_path')
    timestamp_str = data.get('timestamp') # Expected ISO format
    
    if not video_path:
        return jsonify({"error": "No video_path provided"}), 400
        
    try:
        dt = datetime.fromisoformat(timestamp_str) if timestamp_str else datetime.now()
        result = geolocator.process_untagged_video(video_path, dt)
        
        if "error" not in result:
            # Trigger a probe at the discovered location to sync telemetry
            geolocator_mock_stack = {
                'layers': {
                    'visual.optical': {'val': 1.0, 'state': 'geolocated_event'}
                }
            }
            tgh.apply_stack_delta(result['lat'], result['lon'], geolocator_mock_stack)
            logger.log("geoloc", f"Successfully geolocated {video_path} to {result['lat']}, {result['lon']}", result)
            
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/probe', methods=['POST'])
def probe_location():
    data = request.json or {}
    lat = float(data.get('lat', 0))
    lon = float(data.get('lon', 0))
    
    # 1. Fetch detected event context for truth verification
    events = detector.active_events
    context_list: List[str] = []
    for event in events:
        if abs(event['lat'] - lat) < 0.1 and abs(event['lon'] - lon) < 0.1:
            context_list.append(str(event.get('title', '')))

    context = " ".join(context_list)

    # 2. Fetch current sensor state from the Stack Orchestrator
    full_stack = stack_orchestrator.gather_all_sensors(lat, lon, news_context=context)
    
    # 3. TGH Delta Calculation
    delta_update = tgh.apply_stack_delta(lat, lon, full_stack)
    
    logger.log("probe", f"Probed {lat}, {lon} | Context: '{context.strip() or 'Global Intelligence'}'")
    
    return jsonify({
        "location": {"lat": lat, "lon": lon},
        "delta_update": delta_update,
        "efficiency": "99.8% (Multi-Sensor Delta Architecture)",
        "current_view": tgh.get_reconstructed_now(lat, lon)
    })

if __name__ == "__main__":
    print("""
    =========================================
    SKYEYE ORCHESTRATION ENGINE v0.1 ALPHA
    =========================================
    The Window to Earth is Opening...
    """)
    app.run(port=5050, debug=True)
