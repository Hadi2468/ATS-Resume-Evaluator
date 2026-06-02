import json
import streamlit as st
import pandas as pd
import plotly.express as px

from utils.file_parser import extract_text
from utils.logger import logger

from services.evaluator import evaluate_resume

from prompts.zero_shot import ZERO_SHOT_PROMPT
from prompts.one_shot import ONE_SHOT_PROMPT
from prompts.few_shot import FEW_SHOT_PROMPT
from prompts.cot import COT_PROMPT
from prompts.system_prompt import SYSTEM_PROMPT


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="ATS Resume Evaluator",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 ATS Resume Evaluator")

st.markdown(
    """
    Compare ATS Resume Evaluation using Prompt Engineering Techniques:

    - Zero-Shot
    - One-Shot
    - Few-Shot
    - Chain of Thought (CoT)
    """
)

# --------------------------------------------------
# SIDEBAR SETTINGS
# --------------------------------------------------

with st.sidebar:

    st.header("⚙️ Settings LLM Model")

    model_name = st.selectbox(
        "LLM Model",
        [
            "gpt-4o-mini",
            "gpt-4o",
            "gpt-4.1-nano",
            "gpt-4.1-mini",
            "gpt-4.1",
            "gpt-4",
            "gpt-5"
        ]
    )

    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.5,
        step=0.05
    )

# --------------------------------------------------
# FILE UPLOADS
# --------------------------------------------------

col1, col2 = st.columns(2)

with col1:
    resume_file = st.file_uploader(
        "📄 Upload Resume",
        type=["pdf", "docx"]
    )

with col2:
    jd_file = st.file_uploader(
        "📋 Upload Job Description",
        type=["pdf", "docx"]
    )

# --------------------------------------------------
# PROMPT SELECTION
# --------------------------------------------------

prompt_type = st.radio(
    "✔️ Select Prompting Technique",
    ["Zero Shot", "One Shot", "Few Shot", "Chain of Thought"],
    horizontal=True
)

st.info(
    f"""
💥 Technique: {prompt_type}

🧠 Model: {model_name}

🌡️ Temperature: {temperature}
"""
)

# --------------------------------------------------
# PROMPT MAP
# --------------------------------------------------

PROMPT_MAP = {
    "Zero Shot": ZERO_SHOT_PROMPT,
    "One Shot": ONE_SHOT_PROMPT,
    "Few Shot": FEW_SHOT_PROMPT,
    "Chain of Thought": COT_PROMPT
}

# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def clean_json_response(text: str) -> str:
    """Remove markdown fences if model returns ```json"""
    return (
        text.replace("```json", "")
            .replace("```", "")
            .strip()
    )

def verdict_badge(score: float):
    if score >= 90:
        st.success("🟢 Excellent Fit")
    elif score >= 80:
        st.success("🟢 Strong Fit")
    elif score >= 60:
        st.warning("🟡 Moderate Fit")
    else:
        st.error("🔴 Weak Fit")

# --------------------------------------------------
# BUTTON
# --------------------------------------------------

if st.button("🔍 Evaluate Resume", use_container_width=True):

    try:

        if not resume_file:
            st.warning("⚠️ Upload a resume first")
            st.stop()

        if not jd_file:
            st.warning("⚠️ Upload a job description first")
            st.stop()

        logger.info("📄 Extracting resume text")
        resume_text = extract_text(resume_file)

        logger.info("📋 Extracting JD text")
        jd_text = extract_text(jd_file)

        selected_prompt = PROMPT_MAP[prompt_type]

        logger.info(f"🧠 Prompt selected: {prompt_type}")

        with st.spinner(f"🚀 Running {prompt_type} evaluation..."):

            result = evaluate_resume(
                prompt_template=selected_prompt,
                resume_text=resume_text,
                jd_text=jd_text,
                system_prompt=SYSTEM_PROMPT,
                model_name=model_name,
                temperature=temperature
            )

        logger.success("✅ Evaluation completed")

        # --------------------------------------------------
        # PARSE JSON
        # --------------------------------------------------

        try:
            result_json = json.loads(clean_json_response(result))

        except json.JSONDecodeError:
            logger.error("❌ Invalid JSON from model")
            st.error("Model did not return valid JSON")
            st.code(result)
            st.stop()

        # --------------------------------------------------
        # KPI DASHBOARD
        # --------------------------------------------------

        st.subheader("📊 ATS Evaluation Results")

        col1, col2, col3 = st.columns(3)

        with col1:
            score = result_json.get("match_percentage", 0)
            st.metric("🎯 Match %", f"{score}%")
            verdict_badge(score)

        with col2:
            st.metric(
                "❌ Missing Skills",
                len(result_json.get("missing_skills", []))
            )

        with col3:
            st.metric(
                "🏆 Verdict",
                result_json.get("verdict", "Unknown")
            )

        # --------------------------------------------------
        # SKILLS
        # --------------------------------------------------

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("✅ Matched Skills")

            matched = result_json.get("matched_skills", [])

            if matched:
                st.success(", ".join(matched))
            else:
                st.warning("No matched skills found")

        with col2:
            st.subheader("❌ Missing Skills")

            missing = result_json.get("missing_skills", [])

            if missing:
                st.error(", ".join(missing))
            else:
                st.success("No missing skills")

        # --------------------------------------------------
        # SCORE BREAKDOWN
        # --------------------------------------------------

        score_breakdown = result_json.get("score_breakdown", {})

        if score_breakdown:

            st.subheader("📈 Score Breakdown")

            df = pd.DataFrame(
                score_breakdown.items(),
                columns=["Category", "Score"]
            )

            fig = px.bar(
                df,
                x="Category",
                y="Score",
                title="ATS Skill Score Breakdown"
            )

            st.plotly_chart(fig, use_container_width=True)

        # --------------------------------------------------
        # SUGGESTIONS
        # --------------------------------------------------

        st.subheader("💡 Suggestions")

        suggestions = result_json.get("suggestions", [])

        if suggestions:
            for s in suggestions:
                st.markdown(f"- {s}")
        else:
            st.success("No improvements needed")

        # --------------------------------------------------
        # ANALYSIS
        # --------------------------------------------------

        st.subheader("🔍 Detailed Analysis")

        st.markdown(result_json.get("analysis", "No analysis provided"))

        # --------------------------------------------------
        # DOWNLOADS
        # --------------------------------------------------

        st.subheader("📥 Download Report")

        col1, col2 = st.columns(2)

        json_report = json.dumps(result_json, indent=4)

        markdown_report = f"""
# ATS Evaluation Report

## Technique
{prompt_type}

## Match Score
{result_json.get("match_percentage")}

## Verdict
{result_json.get("verdict")}

## Matched Skills
{", ".join(result_json.get("matched_skills", []))}

## Missing Skills
{", ".join(result_json.get("missing_skills", []))}
"""

        with col1:
            st.download_button(
                "📄 Download JSON",
                json_report,
                file_name=f"{prompt_type}_ats.json",
                mime="application/json"
            )

        with col2:
            st.download_button(
                "📝 Download Markdown",
                markdown_report,
                file_name=f"{prompt_type}_ats.md",
                mime="text/markdown"
            )

        # --------------------------------------------------
        # RAW JSON
        # --------------------------------------------------

        with st.expander("🧾 Raw JSON Response"):
            st.json(result_json)

    except Exception as e:

        logger.error(f"💥 Error: {str(e)}")
        st.error(str(e))