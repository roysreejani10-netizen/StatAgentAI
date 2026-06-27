import pandas as pd
import streamlit as st


def load_dataset(uploaded_file):
    """
    Load CSV or XLSX files into a pandas DataFrame.
    """

    file_name = uploaded_file.name.lower()

    try:

        if file_name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)

        elif file_name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file, engine="openpyxl")

        else:
            st.error("❌ Unsupported file format. Please upload CSV or XLSX.")
            return None

        if df.empty:
            st.error("❌ File is empty.")
            return None

        return df

    except Exception as e:
        st.error(f"❌ Error loading dataset:\n{e}")
        return None