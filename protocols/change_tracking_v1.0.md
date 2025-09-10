# Change Tracking Protocol v1.0

## Purpose
To ensure all modifications to protocols, manifests, or README documents are transparent, timestamped, and auditable across temporal states.

---

## Rules
- No undocumented edits.
- All changes must include:
  - Timestamp (ISO 8601)
  - Change type (addition, removal, modification)
  - Section affected
  - Reason / clarification
  - Consent record

---

## Log Format (JSON)
```json
{
  "change_id": "abstract_addition_2025-09-11T09:32Z",
  "proposed_by": "AI (ChatGPT)",
  "reviewed_by": "swarmuser",
  "consent": true,
  "timestamp": "2025-09-11T09:40Z",
  "change_type": "addition",
  "section": "README abstract",
  "clarification": "Added framing note to explain experiment as scientific protocol, not journaling",
  "original_text": null,
  "new_text": "Abstract block text here",
  "status": "merged"
}

Enforcement

This protocol is binding on both human and AI contributors.
No edits are valid without consent record and timestamped log.


🔐 Change Documentation Protocol

Rule
	•	No undocumented edits.
	•	Every change = timestamp, reason, clarifications (if needed).
	•	Logged alongside existing material; never replaces original.

⸻

Example Change Log Format

{
  "change_id": "abstract_addition_2025-09-11T09:32Z",
  "proposed_by": "AI (ChatGPT)",
  "reviewed_by": "swarmuser",
  "consent": true,
  "timestamp": "2025-09-11T09:40Z",
  "change_type": "addition",
  "section": "README abstract",
  "clarification": "Added framing note to explain experiment as scientific protocol, not journaling",
  "original_text": null,
  "new_text": "Abstract block text here",
  "status": "merged"
}


If rejected, it would look like:

{
  "change_id": "abstract_addition_2025-09-11T09:32Z",
  "proposed_by": "AI (ChatGPT)",
  "reviewed_by": "swarmuser",
  "consent": false,
  "timestamp": "2025-09-11T09:40Z",
  "change_type": "addition",
  "section": "README abstract",
  "clarification": "Proposal declined — kept log for transparency",
  "original_text": null,
  "new_text": "Abstract block text here",
  "status": "declined"
}

Glyph Pair for Change Tracking
	•	✍️📜 = change proposed
	•	⏳🧾 = pending review
	•	⚖️✅ = consented & merged
	•	⚖️❌ = declined, logged


