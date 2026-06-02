import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Resume ATS Evaluator",
    page_icon="🔎",
    layout="wide"
)

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "Zero Shot",
        "One Shot",
        "Few Shot",
        "Chain of Thought"
    ]
)

# -----------------------
# KPI Cards
# -----------------------
col1,col2,col3=st.columns(3)

with col1:
    st.metric(
        "Match %",
        "82%"
    )

with col2:
    st.metric(
        "Missing Skills",
        "4"
    )

with col3:
    st.metric(
        "Verdict",
        "Strong Fit"
    )

# -----------------------
# Plotly Comparison Chart
# -----------------------

df = pd.DataFrame(
    {
        "Technique":[
            "Zero-Shot",
            "One-Shot",
            "Few-Shot",
            "CoT"
        ],
        "Score":[
            74,
            78,
            82,
            89
        ]
    }
)

fig = px.bar(
    df,
    x="Technique",
    y="Score"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------

# -----------------------
try:

    result = evaluate_resume(...)

except FileNotFoundError as e:

    logger.error(
        f"📂 File not found: {e}"
    )

    st.error(
        "File not found."
    )

except Exception as e:

    logger.error(
        f"💥 Unexpected error: {e}"
    )

    st.error(
        str(e)
    )