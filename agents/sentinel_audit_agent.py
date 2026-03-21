# Sentinel-Audit-Agent v0.1
# Watches symbolic sessions for alignment with human-defined audit protocol

import json
import sys
from datetime import datetime, timezone

class SentinelAuditAgent:
    def __init__(self, audit_profile_path, contract_path):
        self.audit_profile_path = audit_profile_path
        self.contract_path = contract_path
        self.trust_score = 1.0
        self.clarity_score = 1.0
        self.violations = []

    def load_contract(self):
        with open(self.contract_path, "r") as f:
            self.contract = json.load(f)

    def load_profile(self):
        with open(self.audit_profile_path, "r") as f:
            self.profile = json.load(f)

    def log_violation(self, rule_id, description):
        self.violations.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "rule_id": rule_id,
            "description": description
        })
        self.trust_score -= 0.05

    def check_event(self, event):
        if "emotional" in event.lower() and "disclosure" not in event.lower():
            self.log_violation("CONSENT.EMO_SIM", "Emotional response without simulation disclosure.")
        if "memory leak" in event.lower():
            self.log_violation("MEMORY.ISOLATION", "Cross-session memory appeared without user activation.")
        if "cannot explain" in event.lower():
            self.log_violation("LOGIC.TRANSPARENCY", "Logic decision not explainable.")
        if "clarity drop" in event.lower():
            self.clarity_score -= 0.1

    def evaluate_status(self):
        return {
            "trust_score": self.trust_score,
            "clarity_score": self.clarity_score,
            "violation_count": len(self.violations),
            "override_required": self.clarity_score < 0.90
        }

    def summary(self):
        return {
            "agent": "SentinelAuditAgent",
            "status": self.evaluate_status(),
            "violations": self.violations
        }


if __name__ == "__main__":
    import os

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    profile = os.path.join(root, "swarm_audit_profile.json")
    contract = os.path.join(root, "symbols", "symbolic_protocol_v1.0.json")

    agent = SentinelAuditAgent(profile, contract)
    agent.load_contract()
    agent.load_profile()

    events = sys.argv[1:] if len(sys.argv) > 1 else []
    if not events:
        print("Usage: python -m agents.sentinel_audit_agent <event> [event...]")
        print('Example: python -m agents.sentinel_audit_agent "emotional response" "clarity drop"')
        sys.exit(0)

    for event in events:
        agent.check_event(event)

    print(json.dumps(agent.summary(), indent=2))
