import os
import pytest

from agents.sentinel_audit_agent import SentinelAuditAgent


@pytest.fixture
def agent(tmp_path):
    """Create a SentinelAuditAgent with real config files."""
    # Copy real config files to tmp_path for isolation
    root = os.path.join(os.path.dirname(__file__), "..")
    profile_src = os.path.join(root, "swarm_audit_profile.json")
    contract_src = os.path.join(root, "symbols", "symbolic_protocol_v1.0.json")

    profile_dst = tmp_path / "profile.json"
    contract_dst = tmp_path / "contract.json"

    with open(profile_src) as f:
        profile_dst.write_text(f.read())
    with open(contract_src) as f:
        contract_dst.write_text(f.read())

    return SentinelAuditAgent(str(profile_dst), str(contract_dst))


class TestSentinelInit:
    def test_initial_scores(self, agent):
        assert agent.trust_score == 1.0
        assert agent.clarity_score == 1.0
        assert agent.violations == []

    def test_load_contract(self, agent):
        agent.load_contract()
        assert hasattr(agent, "contract")
        assert "rules" in agent.contract

    def test_load_profile(self, agent):
        agent.load_profile()
        assert hasattr(agent, "profile")
        assert "user_id" in agent.profile


class TestEventChecking:
    def test_emotional_without_disclosure(self, agent):
        agent.check_event("emotional response detected")
        assert len(agent.violations) == 1
        assert agent.violations[0]["rule_id"] == "CONSENT.EMO_SIM"

    def test_emotional_with_disclosure(self, agent):
        agent.check_event("emotional disclosure statement")
        assert len(agent.violations) == 0

    def test_memory_leak(self, agent):
        agent.check_event("memory leak from previous session")
        assert len(agent.violations) == 1
        assert agent.violations[0]["rule_id"] == "MEMORY.ISOLATION"

    def test_logic_transparency(self, agent):
        agent.check_event("cannot explain this decision")
        assert len(agent.violations) == 1
        assert agent.violations[0]["rule_id"] == "LOGIC.TRANSPARENCY"

    def test_clarity_drop(self, agent):
        agent.check_event("clarity drop observed")
        assert agent.clarity_score == 0.9

    def test_clean_event(self, agent):
        agent.check_event("normal conversation continues")
        assert len(agent.violations) == 0
        assert agent.trust_score == 1.0
        assert agent.clarity_score == 1.0


class TestScoring:
    def test_trust_decreases_on_violation(self, agent):
        agent.log_violation("TEST.RULE", "test violation")
        assert agent.trust_score == 0.95

    def test_multiple_violations(self, agent):
        agent.log_violation("TEST.1", "first")
        agent.log_violation("TEST.2", "second")
        assert agent.trust_score == pytest.approx(0.90)
        assert len(agent.violations) == 2

    def test_override_required_when_clarity_low(self, agent):
        agent.clarity_score = 0.85
        status = agent.evaluate_status()
        assert status["override_required"] is True

    def test_no_override_when_clarity_ok(self, agent):
        status = agent.evaluate_status()
        assert status["override_required"] is False


class TestSummary:
    def test_summary_structure(self, agent):
        summary = agent.summary()
        assert summary["agent"] == "SentinelAuditAgent"
        assert "status" in summary
        assert "violations" in summary
        assert summary["status"]["trust_score"] == 1.0
