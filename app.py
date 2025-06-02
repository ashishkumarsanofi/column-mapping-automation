"""
app.py

Main entry point for the Streamlit Column Mapping & Transformation Tool.
Coordinates file uploads, sheet selection, mapping, and output generation.
"""

import os
import streamlit as st
import pandas as pd
import io
import warnings
import time
from file_utils import read_file, fill_missing_columns
from ui_sections import show_upload_section, show_footer, show_guide
from mapping_logic import process_mapping_tabs, process_final_output

# Set max upload size
os.environ["STREAMLIT_SERVER_MAX_UPLOAD_SIZE"] = "1024"

st.set_page_config(page_title="📊 Column Mapping Tool", layout="wide")
st.title("📊 Advanced Column Mapping & Transformation Tool")
st.write("Streamlit version:", st.__version__)

SANOFI_COLORS = {
    'primary': '#000000',
    'secondary': '#7A0056',
    'accent': '#4B0082',
    'background': '#FFFFFF',
    'text': '#000000'
}

st.markdown("""
<style>
    .stButton>button {background-color: #7A0056; color: white; border-radius: 5px; padding: 0.5rem 1rem; border: none;}
    .stButton>button:hover {background-color: #4B0082;}
    .mapping-header {color: #7A0056; font-weight: bold; padding: 10px; background-color: #F8F9FA; border-left: 3px solid #7A0056;}
    .sample-column {background-color: #F8F9FA; padding: 10px; border-left: 3px solid #7A0056; margin: 5px 0;}
    .error-message {color: #a94442; background-color: #f9eaea; border-left: 3px solid #e6a1a1; font-size: 0.95rem; padding: 6px 12px; margin: 4px 0; border-radius: 4px;}
    .success-message {color: #008000; padding: 10px; border-left: 3px solid #008000; background-color: #E6FFE6; margin: 5px 0;}
    .footer-ashish {color: rgba(180,180,180,0.35); background: transparent; text-align: right; font-size: 0.72rem; padding: 0 8px 2px 0; margin-top: 10px; margin-bottom: 2px; user-select: none; letter-spacing: 0.01em;}
</style>
""", unsafe_allow_html=True)



st.markdown("Upload multiple input files and a sample file to map and consolidate your data with optional static values.")
show_guide()
    # Suggest converting Excel files to CSV for faster processing before uploading
st.info("💡 Tip: Convert Excel files to CSV format for faster processing before uploading.")
# --- Upload Section ---
input_files, output_file, mapping_file = show_upload_section(SANOFI_COLORS)
print("upload-done")  # Step marker

# --- Sheet selection logic (keep in app.py for now for clarity) ---
input_file_sheets = []
if input_files:
    for file in input_files:
        if file.name.endswith(".xlsx"):
            try:
                xls = pd.ExcelFile(file)
                sheet_names = xls.sheet_names
                selected_sheets = st.multiselect(
                    f"Select sheet(s) from {file.name} to use as input:",
                    options=sheet_names,
                    default=sheet_names[:1],
                    key=f"{file.name}_sheets"
                )
                for sheet in selected_sheets:
                    input_file_sheets.append({"file": file, "sheet": sheet, "label": f"{file.name} - {sheet}"})
            except Exception as e:
                st.error(f"Could not read sheets from {file.name}: {e}")
        else:
            input_file_sheets.append({"file": file, "sheet": None, "label": file.name})
print("sheet-done")  # Step marker

if input_file_sheets and output_file:
    output_df, _ = read_file(output_file)
    output_columns = output_df.columns.tolist()
    mapping_df = None
    mapping_file_valid = True
    required_mapping_cols = {"FileName", "SheetName", "OutputColumn", "InputColumn"}
    if mapping_file:
        mapping_df, _ = read_file(mapping_file)
        mapping_df.columns = [str(col).strip() for col in mapping_df.columns]
        if not required_mapping_cols.issubset(set(mapping_df.columns)):
            mapping_file_valid = False
            st.warning("⚠️ The mapping file is missing required columns: `FileName`, `SheetName`, `OutputColumn`, `InputColumn`.")
            st.dataframe(pd.DataFrame({"FileName": ["data.xlsx", "input.csv"], "SheetName": ["Sheet1", ""], "OutputColumn": ["Name", "Age"], "InputColumn": ["Full Name", "Years"]}))
    if input_file_sheets and output_file and (mapping_file is None or mapping_file_valid):
        st.markdown("---")
        st.markdown("### Output Settings")
        final_dataframes, output_filename = process_mapping_tabs(
            input_file_sheets, output_file, mapping_file, mapping_file_valid, mapping_df, output_columns
        )
        print("mapping-done")  # Step marker
        process_final_output(final_dataframes, output_columns, output_filename)
        print("output-done")  # Step marker
    else:
        if mapping_file and not mapping_file_valid:
            st.info("❌ Please upload a valid mapping file before proceeding.")
        elif not (input_file_sheets and output_file):
            st.info("👆 Please upload at least one input file (and select at least one sheet if Excel) and one output template file to begin.")
else:
    st.info("👆 Please upload at least one input file (and select at least one sheet if Excel) and one output template file to begin.")

if st.button("🔄 Reset All"):
    st.warning("Please manually refresh your browser page to reset the app (your Streamlit version does not support automatic reset).")


show_footer()

start = time.time()
# (Place this after all processing and UI rendering is done)
end = time.time()
elapsed = end - start
if elapsed < 1:
    st.caption(f"⚡ App loaded instantly!")
elif elapsed < 60:
    st.caption(f"⏱️ Page processed in {elapsed:.2f} seconds.")
else:
    mins = int(elapsed // 60)
    secs = int(elapsed % 60)
    st.caption(f"⏱️ Page processed in {mins} min {secs} sec.")
