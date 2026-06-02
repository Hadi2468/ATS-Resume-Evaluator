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
    Compare ATS Resume Evaluation using:

    - Zero-Shot Prompting
    - One-Shot Prompting
    - Few-Shot Prompting
    - Chain of Thought Prompting
    """
)
# --------------------------------------------------
# Model and Temperature Settings
# --------------------------------------------------
with st.sidebar:

    st.header("⚙️ Settings")

    model_name = st.selectbox(
        "LLM Model",
        [
            "gpt-4o-mini",
            "gpt-4.1-mini",
            "gpt-4.1"
        ]
    )

    temperature = st.slider(
        "Temperature",
        0.0,
        1.0,
        0.2
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
    "🧠 Select Prompting Technique",
    [
        "Zero Shot",
        "One Shot",
        "Few Shot",
        "Chain of Thought"
    ],
    horizontal=True
)

# --------------------------------------------------
# PROMPT MAPPING
# --------------------------------------------------

PROMPT_MAP = {
    "Zero Shot": ZERO_SHOT_PROMPT,
    "One Shot": ONE_SHOT_PROMPT,
    "Few Shot": FEW_SHOT_PROMPT,
    "Chain of Thought": COT_PROMPT
}

# --------------------------------------------------
# BUTTON
# --------------------------------------------------

if st.button("🔍 Evaluate Resume", use_container_width=True):

    try:

        if resume_file is None:
            st.warning("⚠️ Please upload a resume")
            st.stop()

        if jd_file is None:
            st.warning("⚠️ Please upload a job description")
            st.stop()

        logger.info("📄 Reading Resume")

        resume_text = extract_text(
            resume_file
        )

        logger.info("📋 Reading Job Description")

        jd_text = extract_text(
            jd_file
        )

        selected_prompt = PROMPT_MAP[
            prompt_type
        ]

        logger.info(
            f"🧠 Selected Technique: {prompt_type}"
        )

        with st.spinner(
            f"🚀 Running {prompt_type} Evaluation..."
        ):

            result = evaluate_resume(
                prompt_template=selected_prompt,
                resume_text=resume_text,
                jd_text=jd_text,
                system_prompt=SYSTEM_PROMPT
            )

        logger.success(
            "✅ Evaluation Completed"
        )

        st.success(
            "🎉 Evaluation Finished Successfully"
        )

        # ----------------------------------
        # OUTPUT
        # ----------------------------------

        st.subheader(
            "📊 ATS Evaluation Result"
        )

        st.markdown(result)

    except Exception as e:

        logger.error(
            f"💥 Error: {str(e)}"
        )

        st.error(str(e))
