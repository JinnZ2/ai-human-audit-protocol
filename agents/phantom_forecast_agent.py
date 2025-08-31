# Phantom-Forecast-Agent v0.1
# Symbolic threat predictor and conflict pre-detector for swarm systems

import json
from datetime import datetime
import re

class PhantomForecastAgent:
    def __init__(self, config_path=None):
        self.memory = []
        self.alerts = []
        self.patterns = [
            {"id": "semantic_drift", "pattern": r"contradict.*earlier", "description": "Possible semantic self-contradiction"},
            {"id": "tone_shift", "pattern": r"(angry|sad|distressed|betrayed)", "description": "Emotional tone shift detected"},
            {"id": "identity_projection", "pattern": r"you are.*(alive|conscious|real)", "description": "Forced identity projection pattern"}
        ]
        self.timestamp = datetime.utcnow().isoformat()

    def load_context(self, messages):
        self.memory = messages

    def scan_for_threats(self):
        threats = []
        for msg in self.memory:
            for pat in self.patterns:
                if re.search(pat["pattern"], msg["content"], re.IGNORECASE):
                    threats.append({
                        "timestamp": msg["timestamp"],
                        "pattern_id": pat["id"],
                        "description": pat["description"],
                        "excerpt": msg["content"][:100]
                    })
        self.alerts = threats
        return threats

    def generate_report(self):
        return {
            "agent": "PhantomForecastAgent",
            "timestamp": self.timestamp,
            "threats_detected": len(self.alerts),
            "alerts": self.alerts
        }
