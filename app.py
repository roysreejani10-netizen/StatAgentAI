import streamlit as st
from modules.data_loader import load_dataset
from modules.eda import (
    data_quality_report,
    ai_dataset_explainer_llm,
)
from modules.decision_agent import (
    dataset_understanding,
    planning_agent
)

from modules.ml_engine import (
    execution_engine,
    evaluate_models,
    select_best_model,
    reflection_agent
)
from modules.report_generator import generate_pdf_report

# ==========================================================
# CONFIG
# ==========================================================
st.set_page_config(
    page_title="StatAgent AI",
    page_icon="🤖",
    layout="wide"
)

# ==========================================================
# SIDEBAR
# ==========================================================
st.sidebar.title("🤖 StatAgent AI")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "📂 Upload Dataset",
        "📊 EDA Dashboard",
        "🧠 Statistical Decision Agent",
        "🚀 ML Model Selection Engine",
        "📄 Download Report"
    ]
)

# ==========================================================
# HOME
# ==========================================================
if page == "🏠 Home":

    st.title("🤖 StatAgent AI")

    st.markdown("""
## Welcome!

Your AI-powered data analysis assistant.

### Features

- 📂 Upload datasets (CSV / Excel)
- 📊 Exploratory Data Analysis (EDA)
- 🧠 AI Dataset Insights
- 🧠 Automatic Dataset Understanding
- 📈 Statistical Test Recommendations
- 🤖 ML Model Recommendations
- 🚀 Automated Model Selection Engine
- 📄 Download Report              
""")

# ==========================================================
# UPLOAD DATASET
# ==========================================================
elif page == "📂 Upload Dataset":

    st.title("📂 Upload Dataset")

    uploaded_file = st.file_uploader(
        "Choose a CSV or Excel file",
        type=["csv", "xlsx"]
    )

    if uploaded_file is not None:

        df = load_dataset(uploaded_file)

        if df is not None:

            st.success("✅ Dataset uploaded successfully!")

            st.session_state["df"] = df

            # Reset cached information
            st.session_state["problem"] = None
            st.session_state["target"] = None

        else:
            st.error("❌ Failed to load dataset.")

    else:
        st.info("Upload a dataset to begin.")

    if "df" in st.session_state:
        st.subheader("Dataset Preview")
        st.dataframe(st.session_state["df"].head())

# ==========================================================
# EDA DASHBOARD
# ==========================================================
elif page == "📊 EDA Dashboard":

    st.title("📊 Exploratory Data Analysis")

    if "df" not in st.session_state:
        st.warning("Please upload a dataset first.")
        st.stop()

    df = st.session_state["df"]

    # Display EDA
    data_quality_report(df)

    st.divider()

    # Generate AI Analysis
    if st.button("🧠 Generate AI Analysis"):

        with st.spinner("Generating AI insights..."):

            st.session_state["ai_analysis"] = ai_dataset_explainer_llm(df)

    # Display saved AI Analysis
    if "ai_analysis" in st.session_state:

        st.divider()

        with st.expander("🤖 AI Interpretation", expanded=True):

            st.write(st.session_state["ai_analysis"])
# ==========================================================
# DECISION AGENT
# ==========================================================
elif page == "🧠 Statistical Decision Agent":

    st.title("🧠 Statistical Decision Agent")

    if "df" not in st.session_state:
        st.warning("Please upload a dataset first.")
        st.stop()

    problem_info = dataset_understanding(st.session_state["df"])

    problem_type = problem_info["problem"]["problem"]

    st.session_state["problem"] = problem_type
    st.session_state["target"] = problem_info["target"]

    plan = planning_agent(problem_type)

    st.session_state["plan"] = plan

    st.success("Analysis complete!")
# ==========================================================
# ML MODEL SELECTION ENGINE
# ==========================================================
elif page == "🚀 ML Model Selection Engine":

    st.title("🚀 ML Model Selection Engine")

    if "df" not in st.session_state:
        st.warning("Please upload a dataset first.")
        st.stop()

    if st.session_state["problem"] is None:
        st.warning("Please run the Statistical Decision Agent first.")
        st.stop()

    if "plan" not in st.session_state:
        st.warning("Please run the Statistical Decision Agent first.")
        st.stop()

    # Retrieve information from session state
    df = st.session_state["df"]
    target = st.session_state["target"]
    problem_type = st.session_state["problem"]
    plan = st.session_state["plan"]

    # -------------------------
    # Execute ML Pipeline
    # -------------------------
    models, X_test, y_test = execution_engine(
        df,
        target,
        problem_type,
        plan
    )

    # -------------------------
    # Evaluate Models
    # -------------------------
    scores = evaluate_models(
        models,
        X_test,
        y_test,
        problem_type
    )

    # -------------------------
    # Select Best Model
    # -------------------------
    best = select_best_model(scores)

    st.success(
        f"🏆 Best Model: {best['best_model']} "
        f"(Score: {best['best_score']:.4f})"
    )

    # Display all model scores
    st.subheader("📊 Model Performance")

    for model, score in scores.items():
        st.write(f"**{model}** : {score:.4f}")

    # -------------------------
    # Reflection Agent
    # -------------------------
    reflection = reflection_agent(
        best,
        problem_type
    )

    st.markdown(reflection)

    # -------------------------
    # Save for PDF Report
    # -------------------------
    st.session_state["scores"] = scores
    st.session_state["best_model"] = best
    st.session_state["reflection"] = reflection

    st.success("✅ Analysis completed successfully!")
# ==========================================================
# DOWNLOAD REPORT
# ==========================================================
elif page == "📄 Download Report":

    st.title("📄 Download Analysis Report")

    if "best_model" not in st.session_state:
        st.warning("Please run the ML Model Selection Engine first.")
        st.stop()

    pdf = generate_pdf_report(
    df=st.session_state["df"],
    problem_type=st.session_state["problem"],
    target=st.session_state["target"],
    plan=st.session_state["plan"],
    scores=st.session_state["scores"],
    best=st.session_state["best_model"],
    reflection=st.session_state["reflection"]
)

    st.success("✅ Report generated successfully!")

    st.download_button(
        label="📥 Download PDF Report",
        data=pdf,
        file_name="StatAgent_Report.pdf",
        mime="application/pdf"
    )