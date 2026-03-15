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
            
        print(f"[{category.upper()}] {message}")
        return entry

    def get_recent(self, limit=50):
        return self.memory_logs[-limit:]

# Global Logger Instance
logger = SkyEyeEventLogger()
