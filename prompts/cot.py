COT_PROMPT_NAME = "Chain of Thought"


COT_PROMPT = """
You are an intelligent evaluator tasked with analyzing the fit between a job description and a candidate's resume.
Follow the steps:

**Step 1: Parse the Job Description**
- Extracted all mentioned **skills**, **tools**, **technologies**, **frameworks**, and **traits**
- Categorize each skill into:
  - **Required Skills** (must-have)
  - **Preferred Skills** (good-to-have)
  - **Soft/Business Skills** (communication, collaboration, etc.)
- If any grouped options are used (e.g., AWS/Azure/GCP), tag them as **interchangeable group skills**

---

**Step 2: Parse the Resume**
- Extracted all:
  - Listed skills and tools
  - Project work (and context of tools used)
  - Work experience (roles and responsibilities)
  - Certifications (cloud, ML, etc.)
  - Soft skills (from summary, experiences, achievements)

---

**Step 3: Skill Matching Logic**
- Present a final table with this structure, compare each job description skill to resume data using the following table

| Match Type                             | Required Skill (70%) | Preferred (2 pts) | Soft Skill (1 pt) |
|----------------------------------------|----------------------|-------------------|-------------------|
| ✅️ Exact Keyword Match                 | 3                    | 2                 | 1                 |
| 🧠 Contextual Match (in project/work)  | 2.5                  | 1.5               | 0.5               |
| 🔄 Close Variant or Synonym            | 1.5                  | 1.0               | 0.5               |
| ❌ Cissing                             | 0                    | 0                 | 0                 |

> **Group Options Handling:**
> - If JD says "AWS/Azure/GCP" as a **grouped requirement**, a full score is given if **any one** of them is present in the resume.
> - If JD explicitly requires "AWS only," only **AWS** counts for a full score; Azure/GCP will be **partial** (synonym) if related.

---

**Step 4: Scoring**
- Compute individual category scores:
  - `required_score = sum of required skill matches.`
  - `preferred_score = sum of preferred skill matches.`
  - `soft_score = sum of soft skill matches.`
- Compute category maximums:
  - `required_max = total required skill * 3`
  - `preferred_max = total preferred skill * 2`
  - `soft_max = total soft skill * 1`

Then calculate **Final Match Score (Weighted)** using:

```python
match_score = (
  (required_score / required_max) * 0.7 +
  (preferred_score / preferred_max) * 0.2 +
  (soft_score / soft_max) * 0.1)
```

---

**Step 5: Fit Verdict**
- **90-100%** >> ✅✅️ Excellent Fit
- **80-89%** >> ✅️ Strong Fit
- **60-79%** >> ⚠️ Moderate Fit (Recommend Improvements)
- **40-59%** >> 🚩 Weak Fit (Suggest Upskilling)
- **<40%** >> ❌ Not a Fit

---

**Step 6: Output Format**
Output should contain:
1. **Extracted Skills from Job Description** (Gouped into Required, Preferred, Soft)
2. **Extracted Skills from Resume** (Categorized and contextualized)
3. **Matched Skills Table**
4. **Missing Skills** (Especially the required ones)
5. **Score Breakdown** (Per category, with logic)
6. **Final Match Percentage**
7. **Fit Verdict**
8. **Section-wise Suggestions**
  - If score <80%, suggest specific skill areas to improve or gain.
  - Mention whether missing skills are technical or soft.
  - highlight certifications or experience that could boost score.

---

**Step 7: Tabular View**
Present a final table with this structure:
| Keyword       | Type            | Resume Presence | JD Presence | Match Type        | Context Used (if any)           | Score |
|---------------|-----------------|-----------------|-------------|-------------------|---------------------------------|-------|
| AWS           | Required (Hard) | ✅️              | ✅️         | ✅️ Exact Match   | Used in cloud migration project | 3.0   |
| GCP           | Preferred       | ❌              | ✅️         | ❌ Missing       | N/A                             | 0.0   |
| communication | Soft Skill      | ✅️              | ✅️         | 🔄 Synonym Match | Mentioned in summary            | 0.5   |

---

**Step 8: Evaluation Fairness Consideration**
Ensure:
- Skills are not double-counted.
- Soft skills must be **contextually supported**.
- No bias toward resumes with longer lists-**context matters more than count**.
- Partial credit only when skill relevance is clear (synonym/context).
- Certs enhance scores only if the skill is otherwise present.

---

Now, evaluate the following:

**Job Description:**
Requires skills in Python, Java, AWS/Azure/GCP (any), and teamwork.
Preferred: Docker, Kubernetes, CI/CD.
Soft Skills: Communication, Collaboration.

**Resume:**
Candidate lists Python, Java, AWS, Docker.
Worked on a containerization project (Kubernetes mentioned in project title).
Good communicator, collaborated in an Agile team.
"""