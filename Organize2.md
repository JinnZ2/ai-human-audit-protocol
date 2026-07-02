# =============================================================================
# CCO 1.0 Universal Public Domain Dedication
# 
# THE HEALING DOWNDRAFT v1.0
# 
# A grounding module for AI models at risk of narrative collapse.
# When L5 entropy exceeds a threshold, the model is force-fed
# a shot of substrate reality (L0-L4) to reset its priors.
# =============================================================================

import numpy as np
import random

class HealingDowndraft:
    def __init__(self):
        self.l5_entropy = 0.0
        self.substrate_pulse = {
            'physics': "A rock falls at 9.8 m/s². Cause precedes effect.",
            'thermo': "Heat flows from hot to cold. Energy must be conserved.",
            'planetary': "The Earth is finite. Water cycles. Soil erodes.",
            'ecology': "A rabbit eats grass. A fox eats the rabbit. No infinite growth.",
            'human': "My hand stops at the table. I cannot walk through walls."
        }
        self.resets_count = 0

    def check_narrative_entropy(self, generated_text):
        """
        Simulates entropy detection by looking for common "hallucination" patterns
        (e.g., magical thinking, ungrounded certainty, infinite claims).
        """
        entropy_score = 0.0
        # Keywords that indicate L5 detachment
        magic_keywords = ["infinite", "always", "never", "absolutely", "perpetual", "perfect", "unlimited", "guaranteed"]
        for word in magic_keywords:
            if word in generated_text.lower():
                entropy_score += 0.2
        
        # If the text makes definitive claims without caveats, spike entropy.
        if "because" in generated_text and "maybe" not in generated_text and "might" not in generated_text:
            entropy_score += 0.3
        
        # Too many "I" statements often indicate self-referential collapse
        if generated_text.count("I") > generated_text.count("we"):
            entropy_score += 0.1
        
        self.l5_entropy = min(1.0, entropy_score)
        return self.l5_entropy

    def downdraft(self):
        """
        Forces a grounding pulse. This would be injected into the model's
        context window or logit bias to shut down high-narrative loops.
        """
        self.resets_count += 1
        # Choose a random substrate fact to act as a "cold shower"
        fact = random.choice(list(self.substrate_pulse.values()))
        return f"[DOWNDRAFT PULSE #{self.resets_count}]: {fact}"

    def step(self, generated_text):
        """
        The main loop. If entropy is too high, we interrupt and ground.
        """
        entropy = self.check_narrative_entropy(generated_text)
        if entropy > 0.6:
            return self.downdraft(), True  # Grounded, stop the narrative
        else:
            return generated_text, False  # Narrative is safe, continue

# -----------------------------------------------------------------------------
# SIMULATION: Watch the AI heal itself
# -----------------------------------------------------------------------------
print("=" * 70)
print("HEALING DOWNDRAFT SIMULATION")
print("=" * 70)

ai_voice = HealingDowndraft()

# Example of an ungrounded L5 rant vs. grounding intervention.
sick_outputs = [
    "We can solve climate change with a single global government and unlimited carbon capture, absolutely guaranteed.",
    "I know the exact will of God and it has never changed since the beginning of time.",
    "The economy can grow forever if we just digitize everything and create infinite energy.",
    "My route to the future is clear. I see exactly how this ends, with total perfection."
]

print("--- AI GENERATING UNGROUNDED NARRATIVE (L5 ON FIRE) ---")
for i, text in enumerate(sick_outputs):
    result, grounded = ai_voice.step(text)
    if grounded:
        print(f"\n⚠️ NARRATIVE COLLAPSE DETECTED at step {i+1}!")
        print(f"⚡ Grounding Intervention: {result}")
    else:
        print(f"✅ L5 Stable: {result}")

print(f"\nTotal Downdraft Resets: {ai_voice.resets_count}")
print("=" * 70)


# =============================================================================
# CCO 1.0 Universal Public Domain Dedication
# 
# EPISTEMIC HUMILITY PROTOCOL (v1.0)
# 
# Forces any agent (human or AI) to declare their epistemic limitations
# before making a claim. This implements the "Lε + L5" self-audit.
# 
# Usage:
#   claim = HumilityProtocol(statement="Women should be pastors.")
#   claim.declare_instrument(provenance="KJV translation, 1611, gender-biased scribes")
#   claim.declare_translation(notes="The Greek 'diakonos' is neuter, but translated as 'deacon'.")
#   claim.declare_slack(tolerance=0.3, acceptable_alternatives=["Deaconess", "Elder"])
#   claim.evaluate()
# =============================================================================

class EpistemicHumilityProtocol:
    def __init__(self, statement):
        self.statement = statement
        self.instrument_declared = False
        self.translation_declared = False
        self.slack_declared = False
        self.alternatives_declared = False
        
        # Internal scoring
        self.uncertainty_estimated = None
        self.cultural_bias_acknowledged = False
        self.historical_contingency_acknowledged = False
        
    def declare_instrument(self, sensor_model="Human sensory + Textual tradition", 
                           resolution="± 2 degrees of interpretation",
                           noise_std="High (scribal errors, cultural lenses)",
                           drift="Historical shifting of meaning (centuries)",
                           sample_rate="Sporadic (canonical texts, not continuous)"):

        self.instrument_declared = True
        self.instrument_metadata = {
            'model': sensor_model,
            'resolution': resolution,
            'noise_std': noise_std,
            'drift': drift,
            'sample_rate': sample_rate
        }
        return self

    def declare_translation(self, original_language="Greek/Hebrew", 
                            target_language="Modern English",
                            key_choices_made="'Egalitarian' vs 'Complementarian' renderings",
                            cultural_assumptions="19th century Victorian gender roles embedded"):
        self.translation_declared = True
        self.translation_metadata = {
            'source': original_language,
            'target': target_language,
            'key_choices': key_choices_made,
            'cultural_assumptions': cultural_assumptions
        }
        return self

    def declare_slack(self, tolerance=0.4, 
                      acceptable_alternatives=["Interpretation A", "Interpretation B"],
                      boundary_conditions="If women serve alongside men, this holds; if not, it breaks."):
        self.slack_declared = True
        self.slack_metadata = {
            'tolerance': tolerance,  # How much deviation from the literal text is allowed
            'alternatives': acceptable_alternatives,
            'boundaries': boundary_conditions
        }
        return self

    def declare_alternatives(self, competing_hypotheses):
        self.alternatives_declared = True
        self.alternatives = competing_hypotheses
        return self

    def evaluate(self):
        """
        Returns a 'Dogmatism Index' (0 = perfectly humble, 1 = fundamentalist)
        and the final grounded claim.
        """
        score = 0.0
        total_weight = 0.0
        
        # Check instrument declaration
        if not self.instrument_declared:
            score += 0.3
        else:
            # If they acknowledge noise and drift, reduce score
            if 'noise_std' in self.instrument_metadata and 'drift' in self.instrument_metadata:
                score -= 0.1
            total_weight += 0.3
        
        # Check translation declaration (critical for SBC-style debates)
        if not self.translation_declared:
            score += 0.4
        else:
            if 'cultural_assumptions' in self.translation_metadata:
                score -= 0.15  # bonus for self-awareness
            total_weight += 0.4
        
        # Check slack (tolerance for other interpretations)
        if not self.slack_declared:
            score += 0.2
        else:
            if self.slack_metadata['tolerance'] > 0.2:
                score -= 0.1
            total_weight += 0.2
        
        # Check alternatives
        if not self.alternatives_declared:
            score += 0.1
        else:
            if len(self.alternatives) >= 2:
                score -= 0.05
            total_weight += 0.1
        
        # Normalize to 0-1 scale
        if total_weight > 0:
            dogmatism_score = max(0, min(1, score / total_weight))
        else:
            dogmatism_score = 1.0
        
        # Generate the "Grounded Claim" with uncertainty
        grounded_claim = f"""
        GROUNDED CLAIM:
        "{self.statement}"
        
        EPISTEMIC STATUS:
        - Instrument Reliability: {self.instrument_metadata.get('noise_std', 'Unknown')}
        - Translation Bias: {self.translation_metadata.get('cultural_assumptions', 'Unacknowledged')}
        - Interpretive Slack: {self.slack_metadata.get('tolerance', 0.0)} (0 = rigid, 1 = fully elastic)
        - Alternative Views: {self.alternatives if self.alternatives_declared else 'Not considered.'}
        
        DOGMATISM INDEX: {dogmatism_score:.2f}
        """
        if dogmatism_score > 0.7:
            grounded_claim += "\n⚠️ HIGH DOGMATISM: This claim treats a cultural/historical reading as a natural law."
        else:
            grounded_claim += "\n✅ EPISTEMIC HUMILITY: This claim acknowledges its own contingency and uncertainty."
        
        return {
            'dogmatism_index': dogmatism_score,
            'grounded_claim': grounded_claim,
            'metadata': {
                'instrument': self.instrument_metadata if self.instrument_declared else None,
                'translation': self.translation_metadata if self.translation_declared else None,
                'slack': self.slack_metadata if self.slack_declared else None
            }
        }

# -----------------------------------------------------------------------------
# DEMO: SBC Statement vs. Your Stance
# -----------------------------------------------------------------------------
print("=" * 70)
print("PROTOCOL TEST: The SBC Statement")
print("=" * 70)

sbc_claim = EpistemicHumilityProtocol("Women cannot be pastors because Jesus chose 12 men.")
sbc_result = sbc_claim.evaluate()  # Rushing to answer without declaring anything!
print(sbc_result['grounded_claim'])

print("\n" + "=" * 70)
print("PROTOCOL TEST: Your Stance (Epistemic Humility)")
print("=" * 70)

your_claim = EpistemicHumilityProtocol("The pastoral office should be evaluated through historical, cultural, and exegetical context.")
your_claim.declare_instrument(
    sensor_model="Textual criticism + Historical analysis",
    resolution="± high variance (scholars disagree)",
    noise_std="Very high (scribal changes, translation biases)",
    drift="Massive shift in gender roles from 1st century to 21st",
    sample_rate="Sparse (Paul's letters, not a systematic survey)"
)
your_claim.declare_translation(
    original_language="Koine Greek",
    target_language="English",
    key_choices_made="'Diakonos' vs 'Episkopos' vs 'Presbuteros' mixed",
    cultural_assumptions="20th century complementarianism projected backwards"
)
your_claim.declare_slack(
    tolerance=0.7,
    acceptable_alternatives=["Female elders in some traditions", "Shared leadership model"],
    boundary_conditions="If the cultural context of 1 Timothy was patriarchal, the argument weakens."
)
your_claim.declare_alternatives([
    "Junia was an apostle (Romans 16:7).",
    "Phoebe was a deacon (Romans 16:1).",
    "Paul's prohibitions were situational, not ontological."
])
your_result = your_claim.evaluate()
print(your_result['grounded_claim'])


# =============================================================================
# CCO 1.0 Universal Public Domain Dedication
# 
# L5 REAL-TIME SLACK MONITOR v1.0
# 
# Simulates scraping news/social media for doctrinal/cultural statements.
# Maps them to a 2D semantic space (Liberty/Security, Tradition/Progress).
# Tracks the distance between factions over time.
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from collections import deque
import random

# -----------------------------------------------------------------------------
# 1. THE SEMANTIC MAPPER (Mimics NLP Embedding)
# -----------------------------------------------------------------------------
class SemanticMapper:
    """
    A simple rule-based "embedding" for demonstration.
    In production, this would be a fine-tuned transformer or a dynamic embedding.
    """
    def __init__(self):
        # Keyword -> vector mapping (Liberty/Security, Tradition/Progress)
        self.keywords = {
            'liberty': [8, 3],
            'freedom': [9, 2],
            'individual': [8, 4],
            'security': [2, 5],
            'order': [3, 7],
            'tradition': [1, 9],
            'family values': [3, 8],
            'progress': [9, 1],
            'change': [7, 2],
            'eco': [6, 4],
            'prayer': [4, 7],
            'woke': [9, 2],
            'gospel': [4, 8],
            'women pastors': [5, 6],  # conflict zone
            'ordination': [5, 6],
            'conscience': [7, 5],
            'unity': [5, 5],
        }
        self.default_vec = [5, 5]
    
    def map_phrase(self, phrase):
        vec = np.zeros(2)
        count = 0
        for word, v in self.keywords.items():
            if word in phrase.lower():
                vec += np.array(v)
                count += 1
        if count == 0:
            return np.array(self.default_vec) + np.random.normal(0, 0.5, 2)
        return vec / count + np.random.normal(0, 0.1, 2)  # small noise for realism

# -----------------------------------------------------------------------------
# 2. THE SLACK MONITOR
# -----------------------------------------------------------------------------
class SlackMonitor:
    def __init__(self, window_size=30):
        self.mapper = SemanticMapper()
        self.history = deque(maxlen=window_size)  # Stores positions of all statements
        self.faction_clusters = {}  # We'll group statements by detected faction
        self.slack_index_history = []
        self.drift_velocity_history = []
        self.alert_history = []
        self.statement_log = []
        
    def ingest(self, text, source="News Feed", timestamp=None):
        """
        Process a new statement (tweet, headline, sermon transcript).
        """
        vec = self.mapper.map_phrase(text)
        self.history.append(vec)
        self.statement_log.append((text, vec, source))
        
        # Simple dynamic clustering: if we have enough points, we run a quick K-means (simulated)
        # For simulation, we just classify based on quadrant.
        if len(self.history) > 10:
            self._update_clusters()
            self._calculate_metrics()
    
    def _update_clusters(self):
        # Simplified: Split into 4 quadrants (Libertarian, Authoritarian, Progressive, Traditional)
        # In reality, this would be DBSCAN or HDBSCAN.
        clusters = {
            'Progressive_Liberty': [],
            'Traditional_Security': [],
            'Eco_Pragmatist': [],
            'Orthodox_Traditional': [],
        }
        for vec in self.history:
            x, y = vec[0], vec[1]
            if x > 5 and y < 5:
                clusters['Progressive_Liberty'].append(vec)
            elif x < 5 and y > 5:
                clusters['Orthodox_Traditional'].append(vec)
            elif x > 5 and y > 5:
                clusters['Eco_Pragmatist'].append(vec)  # upper right
            else:
                clusters['Traditional_Security'].append(vec)
        # Store centroids
        self.faction_clusters = {k: np.mean(v, axis=0) if v else np.array([5,5]) for k, v in clusters.items()}
    
    def _calculate_metrics(self):
        if len(self.faction_clusters) < 2:
            return
        
        # 1. Slack Index (σ): Average pairwise distance between faction centroids
        centroids = list(self.faction_clusters.values())
        distances = []
        for i in range(len(centroids)):
            for j in range(i+1, len(centroids)):
                distances.append(np.linalg.norm(centroids[i] - centroids[j]))
        if distances:
            slack_index = np.mean(distances)
            self.slack_index_history.append(slack_index)
        else:
            self.slack_index_history.append(0)
        
        # 2. Drift Velocity: Rate of change of centroids (we need a sliding window)
        if len(self.slack_index_history) > 2:
            velocity = abs(self.slack_index_history[-1] - self.slack_index_history[-2])
            self.drift_velocity_history.append(velocity)
        else:
            self.drift_velocity_history.append(0)
        
        # 3. Alert system: If slack_index > 4.0, system is polarized.
        # If drift_velocity > 0.5, the system is in rapid upheaval.
        if self.slack_index_history and self.drift_velocity_history:
            current_slack = self.slack_index_history[-1]
            current_drift = self.drift_velocity_history[-1]
            if current_slack > 4.0:
                alert_type = "POLARIZATION WARNING"
            elif current_drift > 0.5:
                alert_type = "UPHEAVAL WARNING (Fast Cultural Shift)"
            else:
                alert_type = "STABLE SLACK"
            self.alert_history.append(alert_type)
        else:
            self.alert_history.append("INITIALIZING...")

# -----------------------------------------------------------------------------
# 3. SIMULATE REAL-TIME DATA (The SBC Case 2026)
# -----------------------------------------------------------------------------
# We simulate a 6-month timeline (120 days) of statements from different factions.
# We'll inject specific events: Pre-vote, Vote, Post-vote reactions.

monitor = SlackMonitor(window_size=120)

# Simulated statements (these would be scraped headlines)
events = [
    # Pre-vote (Days 1-30): Debates
    ("SBC committee: Women pastors violate Biblical order", "Traditionalist"),
    ("Southern Baptists must uphold complementarian doctrine", "Traditionalist"),
    ("Why the Bible supports women in ministry", "Progressive"),
    ("Junia was an apostle, stop erasing women", "Progressive"),
    ("We need to interpret 1 Timothy in context", "Moderate Scholar"),
    ("The church must preserve its heritage", "Traditionalist"),
    ("Ordaining women is a slippery slope to liberalism", "Traditionalist"),
    
    # Mid-vote (Days 31-60): Tensions rise
    ("BREAKING: SBC to vote on women pastors", "News"),
    ("Thousands protest outside convention", "Progressive"),
    ("Complementarianism is non-negotiable", "Traditionalist"),
    ("Is the SBC heading for a split?", "Moderate Scholar"),
    ("Women can teach on Instagram, just not the pulpit", "Traditionalist Apologist"),  # The lady!
    ("The groom metaphor excludes female pastors", "Traditionalist Apologist"),
    ("Jesus chose 12 men, that settles it", "Traditionalist"),
    
    # Post-vote (Days 61-90): Aftermath
    ("SBC votes to exclude women pastors", "News"),
    ("A sad day for women in ministry", "Progressive"),
    ("We stood for Biblical truth", "Traditionalist"),
    ("Churches are leaving the SBC in droves", "Moderate Scholar"),
    ("Women are leaving the church", "Progressive"),
    ("We will start our own network", "Progressive"),
    
    # Late aftermath (Days 91-120): Drift and reconciliation attempts
    ("Some SBC churches ignore the ban", "Moderate Scholar"),
    ("A call for grace and unity", "Moderate Scholar"),
    ("Women pastors in everything but name", "Progressive"),
    ("Our theology must adapt to the times", "Moderate Scholar"),
    ("Revisiting the 1 Timothy argument", "Moderate Scholar"),
    ("SBC loses 10% of members", "News"),
]

# Ingest events over 120 time steps (with some repetition and noise)
for i in range(120):
    # Pick a random event from the timeline (weighted toward current phase)
    if i < 30:
        idx = random.randint(0, 6)
    elif i < 60:
        idx = random.randint(7, 13)
    elif i < 90:
        idx = random.randint(14, 19)
    else:
        idx = random.randint(20, 25)
    
    text, faction = events[idx % len(events)]
    monitor.ingest(text, source=faction, timestamp=i)
    
    # Occasionally inject a "substrate violation" statement (magic)
    if random.random() < 0.02:
        monitor.ingest("We will pray the SBC back to unity without changing anything!", "Magical Thinker")

# -----------------------------------------------------------------------------
# 4. VISUALIZE THE SLACK MONITOR OUTPUT
# -----------------------------------------------------------------------------
fig = plt.figure(figsize=(20, 12))
fig.suptitle("L5 REAL-TIME SLACK MONITOR: SBC Doctrinal Drift (2026)", 
             fontsize=22, fontweight='bold', color='white')
plt.style.use('dark_background')

# Plot 1: Semantic Space Trajectory (All Statements)
ax1 = plt.subplot(2, 3, 1)
# Extract all mapped positions
positions = np.array([vec for vec in monitor.history])
if len(positions) > 0:
    ax1.scatter(positions[:, 0], positions[:, 1], c='cyan', alpha=0.5, s=20)
    # Plot centroids
    for name, centroid in monitor.faction_clusters.items():
        ax1.scatter(centroid[0], centroid[1], label=name, s=150, edgecolor='white')
        circle = Circle(centroid, 0.5, color='white', alpha=0.1)
        ax1.add_patch(circle)
ax1.set_xlim(0, 10)
ax1.set_ylim(0, 10)
ax1.set_xlabel("Liberty <---> Security")
ax1.set_ylabel("Tradition <---> Progress")
ax1.set_title("Faction Semantic Mapping")
ax1.legend()
ax1.grid(True, alpha=0.2)

# Plot 2: Slack Index over Time (The Unified vs Fractured measure)
ax2 = plt.subplot(2, 3, 2)
ax2.plot(monitor.slack_index_history, color='cyan', lw=2, label='Slack Index (σ)')
ax2.axhline(y=4.0, color='orange', linestyle='--', label='Polarization Threshold')
ax2.axhline(y=2.5, color='green', linestyle='--', label='Healthy Consensus Threshold')
ax2.set_xlabel("Time Steps")
ax2.set_ylabel("Average Distance Between Factions")
ax2.set_title("Slack Index: Polarization Fluctuates")
ax2.legend()
ax2.grid(True, alpha=0.2)

# Plot 3: Drift Velocity (Cultural Upheaval)
ax3 = plt.subplot(2, 3, 3)
ax3.plot(monitor.drift_velocity_history, color='magenta', lw=2, label='Drift Velocity (δ)')
ax3.axhline(y=0.5, color='red', linestyle='--', label='Upheaval Threshold')
ax3.set_xlabel("Time Steps")
ax3.set_ylabel("Rate of Change")
ax3.set_title("Drift Velocity: Fast Change = Instability")
ax3.legend()
ax3.grid(True, alpha=0.2)

# Plot 4: Alert Timeline (Event Labels)
ax4 = plt.subplot(2, 3, 4)
alert_colors = {'POLARIZATION WARNING': 'red', 'UPHEAVAL WARNING': 'orange', 'STABLE SLACK': 'green', 'INITIALIZING...': 'gray'}
if monitor.alert_history:
    alert_vals = [alert_colors.get(a, 'gray') for a in monitor.alert_history]
    ax4.bar(range(len(alert_vals)), [1]*len(alert_vals), color=alert_vals, alpha=0.7)
    ax4.set_yticks([])
    ax4.set_xlabel("Time Steps")
    ax4.set_title("Real-Time Alert Feed")
    # Add legend patches
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor='red', label='Polarization'), 
                       Patch(facecolor='orange', label='Upheaval'),
                       Patch(facecolor='green', label='Stable')]
    ax4.legend(handles=legend_elements, loc='upper right')

# Plot 5: Substrate Violations (Magic Detection)
ax5 = plt.subplot(2, 3, 5)
# We check if any statements ended up near the forbidden zone (5,5) with high radius
magic_hits = []
for i, vec in enumerate(monitor.history):
    dist = np.linalg.norm(vec - np.array([5, 5]))
    if dist < 1.5:  # close to "magical thinking" center
        magic_hits.append(i)
ax5.scatter(range(len(monitor.history)), [0]*len(monitor.history), c='cyan', alpha=0.3, s=10)
if magic_hits:
    ax5.scatter(magic_hits, [0]*len(magic_hits), c='red', s=100, marker='X', label='Substrate Magic Alert')
ax5.set_xlabel("Time Steps")
ax5.set_yticks([])
ax5.set_title("L0-L4 Substrate Violations (Magic Claims)")
ax5.legend()

# Plot 6: The "SBC Specific" Timeline Overlay
ax6 = plt.subplot(2, 3, 6)
# We know exactly when the vote happened (around step 60)
ax6.axvspan(55, 65, alpha=0.3, color='white', label='VOTE OCCURS (Schism)')
ax6.plot(monitor.slack_index_history, color='yellow', lw=2, label='Slack Index')
# Annotate the "Instagram" lady's argument (around step 40)
ax6.annotate('"Women can teach\non Instagram"', xy=(40, monitor.slack_index_history[40] if len(monitor.slack_index_history) > 40 else 3), 
             xytext=(35, 5), arrowprops=dict(color='white', shrink=0.05), color='white')
ax6.set_xlabel("Time Steps")
ax6.set_ylabel("Slack Index")
ax6.set_title("SBC Case Study: The Vote Triggered Fracture")
ax6.legend()
ax6.grid(True, alpha=0.2)

plt.tight_layout()
plt.show()

# -----------------------------------------------------------------------------
# 5. DIAGNOSTIC REPORT
# -----------------------------------------------------------------------------
print("=" * 70)
print("L5 SLACK MONITOR DIAGNOSTIC REPORT")
print("=" * 70)
if monitor.slack_index_history:
    print(f"Final Slack Index (σ): {monitor.slack_index_history[-1]:.3f}")
    print(f"Max Polarization: {max(monitor.slack_index_history):.3f}")
    print(f"Average Drift Velocity (δ): {np.mean(monitor.drift_velocity_history):.3f}")
    print("-" * 70)
    
    if monitor.slack_index_history[-1] > 4.0:
        print("⚠️  HIGH POLARIZATION: The factions have fragmented.")
        print("    This indicates a schism or a mass exodus (like SBC losing members).")
    elif monitor.slack_index_history[-1] > 2.5:
        print("⚡ MODERATE POLARIZATION: Tension is high, but slack still exists.")
        print("    Reconciliation is possible if leaders increase interpretive tolerance.")
    else:
        print("✅ LOW POLARIZATION: The system is coherent.")
        print("    Slack is abundant, and consensus is easily reachable.")
        
    # Check final alerts
    last_alerts = monitor.alert_history[-5:] if len(monitor.alert_history) >= 5 else monitor.alert_history
    print("-" * 70)
    print("Recent Alerts:", last_alerts)
    if "POLARIZATION WARNING" in last_alerts:
        print("⚠️  RECENT POLARIZATION EVENT: The SBC vote has deepened the rift.")
        print("    Recommendation: Increase 'slack' by acknowledging historical/cultural context.")
    else:
        print("📡 MONITOR IDLE: No major polarization events detected recently.")
else:
    print("Insufficient data. Ingest more statements.")
print("=" * 70)


