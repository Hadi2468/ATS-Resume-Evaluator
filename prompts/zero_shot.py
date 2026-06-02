ZERO_SHOT_PROMPT_NAME = "Zero Shot"

ZERO_SHOT_PROMPT = """
Evaluate the fit between the provided Job Description and Resume.

Return:

1. Extracted Skills from Job Description
2. Extracted Skills from Resume
3. Matched Skills
4. Missing Skills
5. ATS Match Percentage
6. Fit Verdict
7. Improvement Suggestions

Provide the output in a professional ATS report format.
"""