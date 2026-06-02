ONE_SHOT_PROMPT_NAME = "One Shot"

ONE_SHOT_PROMPT = """
Evaluate the fit between a job description and a resume based on the following criteria. Here are some examples:

**Example 1:**
Job Description: Requires skills in Python, Java, and teamwork.
Resume: Skills include Python, Java, communication.
Output:
- Extracted Skills from Job Description: Python, Java, and teamwork
- Extracted Skills from Resume: Python, Java, and communication
- Matched Skills: Python, Java
- Missing Skills: teamwork
- Score Breakdown: Python (3 points), Java (3 points), teamwork (0 points)
- Final Match Percentage: 66.67%
- Fit Verdict: Moderate Fit
- Section-wise Suggestions: Improve teamwork skills
- Table Format:
  - Keyword Type (Hard/Soft Skill, list down of all the possible skills mentioned in the resume and Job Description)

Now, evaluate the following: Job Description and Resume
"""