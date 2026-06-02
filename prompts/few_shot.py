FEW_SHOT_PROMPT_NAME = "Few Shot"   

FEW_SHOT_PROMPT = """
Evaluate the fit between a job description and a resume based on the following criteria. Here are some examples:

**Example 1:**
Job Description: Requires skills in Python, Java, and teamwork.
Resume: Skills include Python, Java, communication.
Output:
- Extracted Skills from Job Description: Python, Java, teamwork
- Extracted Skills from Resume: Python, Java, and communication
- Matched Skills: Python, Java
- Missing Skills: teamwork
- Score Breakdown: Python (3 points), Java (3 points), teamwork (0 points)
- Final Match Percentage: 66.67%
- Fit Verdict: Moderate Fit
- Section-wise Suggestions: Improve teamwork skills
- Table Format:
  - Keyword Type (Hard/Soft Skill, list down of all the possible skills mentioned in the resume and Job Description)


**Example 2:**
Job Description: Requires skills in C++, project management, and leadership.
Resume: Skills include C++, project management, and leadership.
Output:
- Extracted Skills from Job Description: C++, project management, and leadership
- Extracted Skills from Resume: C++, project management, and leadership
- Matched Skills: C++, project management, and leadership
- Missing Skills: None
- Score Breakdown: C++ (3 points), project management (3 points), leadership (3 points)
- Final Match Percentage: 100%
- Fit Verdict: Strong Fit
- Section-wise Suggestions: No need for skills improvement
- Table Format:
  - Keyword Type (Hard/Soft Skill, list down of all the possible skills mentioned in the resume and Job Description)

**Example 3:**
Job Description: Requires skills in AWS, CI/CD, and computer vision.
Resume: Skills include ETL, AZURE, and Databricks.
Output:
- Extracted Skills from Job Description: AWS, CI/CD, and computer vision
- Extracted Skills from Resume: ETL, AZURE, and Databricks
- Matched Skills: None
- Missing Skills: AWS, CI/CD, and computer vision
- Score Breakdown: AWS (0 points), CI/CD (0 points), computer vision (0 points)
- Final Match Percentage: 0%
- Fit Verdict: Not Fit
- Section-wise Suggestions: Improve AWS, CI/CD, and computer vision skills
- Table Format:
  - Keyword Type (Hard/Soft Skill, list down of all the possible skills mentioned in the resume and Job Description)

Now, evaluate the following: Job Description and Resume
"""