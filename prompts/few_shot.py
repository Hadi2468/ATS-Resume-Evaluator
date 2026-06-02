FEW_SHOT_PROMPT_NAME = "Few Shot"

FEW_SHOT_PROMPT = """
Evaluate Resume vs Job Description using ATS scoring logic.

You are given multiple examples.

---

## EXAMPLE 1
Job: Python, Java, teamwork
Resume: Python, Java, communication

Output:
{
  "matched_skills": ["Python", "Java"],
  "missing_skills": ["teamwork"],
  "match_percentage": 66,
  "verdict": "Moderate Fit"
}

---

## EXAMPLE 2
Job: C++, leadership, project management
Resume: C++, leadership, project management

Output:
{
  "matched_skills": ["C++", "leadership", "project management"],
  "missing_skills": [],
  "match_percentage": 100,
  "verdict": "Strong Fit"
}

---

## EXAMPLE 3
Job: AWS, CI/CD, computer vision
Resume: Azure, ETL, Databricks

Output:
{
  "matched_skills": [],
  "missing_skills": ["AWS", "CI/CD", "computer vision"],
  "match_percentage": 0,
  "verdict": "Not Fit"
}

---

## RULES
- Learn pattern from examples
- Apply same logic
- Return ONLY JSON

---

Now evaluate the given Resume and Job Description.
"""