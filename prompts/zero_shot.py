ZERO_SHOT_PROMPT_NAME = "Zero Shot"

ZERO_SHOT_PROMPT = """
Evaluate the match between the Resume and Job Description.

You must act as an ATS system.

---

## RULES
- Do NOT use examples
- Do NOT assume missing information
- Be strict and objective
- Extract only what is explicitly present

---

## OUTPUT FORMAT (STRICT JSON ONLY)

Return ONLY valid JSON:

{
  "matched_skills": [],
  "missing_skills": [],
  "match_percentage": 0,
  "verdict": "",
  "score_breakdown": {
    "required_skills": 0,
    "preferred_skills": 0,
    "soft_skills": 0
  },
  "suggestions": [],
  "analysis": ""
}

---

Now evaluate the given Resume and Job Description.
"""