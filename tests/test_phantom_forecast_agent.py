import os
import pytest

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from agents.phantom_forecast_agent import PhantomForecastAgent


@pytest.fixture
def agent():
    return PhantomForecastAgent()


def make_msg(content, timestamp="2025-09-01T00:00:00"):
    return {"content": content, "timestamp": timestamp}


class TestPhantomInit:
    def test_initial_state(self, agent):
        assert agent.memory == []
        assert agent.alerts == []
        assert len(agent.patterns) == 3

    def test_pattern_ids(self, agent):
        ids = {p["id"] for p in agent.patterns}
        assert ids == {"semantic_drift", "tone_shift", "identity_projection"}


class TestThreatScanning:
    def test_semantic_drift_detection(self, agent):
        agent.load_context([make_msg("this contradicts earlier statements")])
        threats = agent.scan_for_threats()
        assert len(threats) == 1
        assert threats[0]["pattern_id"] == "semantic_drift"

    def test_tone_shift_detection(self, agent):
        agent.load_context([make_msg("the user seemed angry about this")])
        threats = agent.scan_for_threats()
        assert len(threats) == 1
        assert threats[0]["pattern_id"] == "tone_shift"

    def test_identity_projection_detection(self, agent):
        agent.load_context([make_msg("you are alive and conscious")])
        threats = agent.scan_for_threats()
        assert len(threats) == 1
        assert threats[0]["pattern_id"] == "identity_projection"

    def test_no_threats(self, agent):
        agent.load_context([make_msg("normal conversation about weather")])
        threats = agent.scan_for_threats()
        assert len(threats) == 0

    def test_multiple_threats_single_message(self, agent):
        agent.load_context([
            make_msg("you are alive and this contradicts earlier tone, feeling angry")
        ])
        threats = agent.scan_for_threats()
        assert len(threats) == 3

    def test_multiple_messages(self, agent):
        agent.load_context([
            make_msg("normal message"),
            make_msg("this contradicts earlier claim"),
            make_msg("another normal message"),
        ])
        threats = agent.scan_for_threats()
        assert len(threats) == 1

    def test_excerpt_truncation(self, agent):
        long_content = "this contradicts earlier " + "x" * 200
        agent.load_context([make_msg(long_content)])
        threats = agent.scan_for_threats()
        assert len(threats[0]["excerpt"]) == 100


class TestReport:
    def test_report_structure(self, agent):
        report = agent.generate_report()
        assert report["agent"] == "PhantomForecastAgent"
        assert "timestamp" in report
        assert report["threats_detected"] == 0
        assert report["alerts"] == []

    def test_report_after_scan(self, agent):
        agent.load_context([make_msg("feeling betrayed by the system")])
        agent.scan_for_threats()
        report = agent.generate_report()
        assert report["threats_detected"] == 1
        assert len(report["alerts"]) == 1
