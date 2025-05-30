import pandas as pd
import streamlit as st

def read_file(file):
    """
    Efficiently read CSV or Excel file as all-string columns to avoid dtype warnings and speed up loading.
    """
    try:
        if file.name.endswith(".csv"):
            df = pd.read_csv(file, dtype=str, low_memory=False)
        else:
            df = pd.read_excel(file, dtype=str)
        return df, []
    except Exception as e:
        st.error(f"Error reading {file.name}: {str(e)}")
        return None, []

def fill_missing_columns(df, required_cols):
    for col in required_cols:
        if col not in df.columns:
            df[col] = ""
    return df[required_cols]
