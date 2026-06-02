ONE_SHOT_PROMPT_NAME = "One Shot"

ONE_SHOT_PROMPT = """
Evaluate the match between Resume and Job Description using ATS logic.

You are given ONE example to guide formatting.

---

## EXAMPLE

Job Description:
Requires Python, Java, teamwork.

Resume:
Python, Java, communication.

Output:
{
  "matched_skills": ["Python", "Java"],
  "missing_skills": ["teamwork"],
  "match_percentage": 66,
  "verdict": "Moderate Fit",
  "score_breakdown": {
    "required_skills": 6,
    "preferred_skills": 0,
    "soft_skills": 0
  },
  "suggestions": ["Improve teamwork skills"],
  "analysis": "Partial match of core technical skills."
}

---

## RULES
- Follow the format exactly
- Do NOT add extra text
- Output ONLY JSON

---

Now evaluate the given Resume and Job Description.
"""