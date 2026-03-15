import json
import os
from datetime import datetime
from skyeye_engine.config import Config

class SkyEyeEventLogger:
    """
    Real-time Event Logger for SkyEye Engine.
    Records every Detection, Reconstruction, and Delta Update.
    """
    def __init__(self):
        self.log_file = os.path.join(Config.BASE_DIR, "output", "event_log.jsonl")
        self.memory_logs = [] # Keep last 100 in memory for fast UI access
        self.socketio = None # To be injected by controller.py

    def log(self, category, message, data=None):
        entry = {
            'timestamp': datetime.now().isoformat(),
            'category': category,
            'message': message,
            'data': data or {}
        }
        
        # Save to memory
        self.memory_logs.append(entry)
        if len(self.memory_logs) > 100:
            self.memory_logs.pop(0)
            
        # Save to disk (Append mode)
        try:
            with open(self.log_file, 'a') as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            print(f"[LOGGER] Error writing to disk: {e}")

        # Save to Database
        try:
            from skyeye_engine.db import db_manager, LogModel
            session = db_manager.Session()
            db_log = LogModel(
                category=category,
                message=message,
                data=data or {}
            )
            session.add(db_log)
            session.commit()
            session.close()
        except Exception as e:
            # We don't want to crash the whole app if the DB is down
            print(f"[LOGGER] Database logging failed: {e}")
            
        # Emit via WebSockets for real-time UI Pulse
        if self.socketio:
            self.socketio.emit('tactical_alert', entry)

        print(f"[{category.upper()}] {message}")
        return entry

    def get_recent(self, limit=50):
        return self.memory_logs[-limit:]

# Global Logger Instance
logger = SkyEyeEventLogger()
