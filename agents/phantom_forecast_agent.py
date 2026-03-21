# Phantom-Forecast-Agent v0.1
# Symbolic threat predictor and conflict pre-detector for swarm systems

import json
import sys
from datetime import datetime, timezone
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
        self.timestamp = datetime.now(timezone.utc).isoformat()

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


if __name__ == "__main__":
    agent = PhantomForecastAgent()

    messages = sys.argv[1:] if len(sys.argv) > 1 else []
    if not messages:
        print("Usage: python -m agents.phantom_forecast_agent <message> [message...]")
        print('Example: python -m agents.phantom_forecast_agent "you are alive and conscious"')
        sys.exit(0)

    now = datetime.now(timezone.utc).isoformat()
    agent.load_context([{"content": msg, "timestamp": now} for msg in messages])
    agent.scan_for_threats()

    print(json.dumps(agent.generate_report(), indent=2))
