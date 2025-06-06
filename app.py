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
    'primary': '#2C3E50',      # Soft dark blue-gray
    'secondary': '#3498DB',    # Gentle blue
    'accent': '#2ECC71',       # Soft green
    'background': '#F8F9FA',   # Light gray background
    'text': '#34495E'          # Readable dark gray
}

st.markdown("""
<style>
    .stButton>button {background-color: #2980B9; color: white; border-radius: 6px; padding: 0.5rem 1rem; border: none; transition: all 0.3s ease; font-weight: 500;}
    .stButton>button:hover {background-color: #1F618D; transform: translateY(-1px); box-shadow: 0 4px 8px rgba(0,0,0,0.2);}
    .mapping-header {color: #2C3E50; font-weight: bold; padding: 12px; background-color: #F8F9FA; border-left: 4px solid #3498DB; border-radius: 4px;}
    .sample-column {background-color: #F8F9FA; padding: 12px; border-left: 4px solid #2ECC71; margin: 8px 0; border-radius: 4px;}
    .error-message {color: #E74C3C; background-color: #FADBD8; border-left: 4px solid #E74C3C; font-size: 0.95rem; padding: 8px 14px; margin: 6px 0; border-radius: 4px;}
    .success-message {color: #27AE60; padding: 12px; border-left: 4px solid #2ECC71; background-color: #D5F4E6; margin: 8px 0; border-radius: 4px;}
    .footer-ashish {color: rgba(52, 73, 94, 0.4); background: transparent; text-align: right; font-size: 0.72rem; padding: 0 8px 2px 0; margin-top: 12px; margin-bottom: 2px; user-select: none; letter-spacing: 0.01em;}
    
    /* Enhanced styling for 3-column upload layout */
    div[data-testid="column"] {
        padding: 0 12px;
        border-radius: 8px;
    }
    div[data-testid="column"] h4 {
        margin-bottom: 8px !important;
        color: #3498DB;
        font-weight: 600;
    }
    div[data-testid="column"] .element-container p {
        margin-top: 0 !important;
        margin-bottom: 12px !important;
        font-style: italic;
        color: #7F8C8D;
        font-size: 0.9rem;
    }
    .stFileUploader label {
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        color: #34495E;
    }
      /* Overall app styling improvements */
    .main .block-container {
        padding-top: 2rem;
        max-width: 1200px;
    }
    h1 {
        color: #1E88E5 !important;
        margin-bottom: 1rem !important;
        font-weight: 700 !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }
    h2 {
        color: #3498DB !important;
    }
    h3 {
        color: #3282B8 !important;
    }
</style>
""", unsafe_allow_html=True)

show_guide()

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
    extended_mapping_cols = {"StaticValue", "FilterValues", "DateFormatFlag", "IncludeFlag"}
    
    if mapping_file:
        mapping_df, _ = read_file(mapping_file)
        mapping_df.columns = [str(col).strip() for col in mapping_df.columns]
        
        # Check if basic required columns exist
        if not required_mapping_cols.issubset(set(mapping_df.columns)):
            mapping_file_valid = False
            st.warning("⚠️ The mapping file is missing required columns: `FileName`, `SheetName`, `OutputColumn`, `InputColumn`.")
            st.dataframe(pd.DataFrame({"FileName": ["data.xlsx", "input.csv"], "SheetName": ["Sheet1", ""], "OutputColumn": ["Name", "Age"], "InputColumn": ["Full Name", "Years"]}))
        else:
            # Add optional columns if they don't exist (for backward compatibility)
            for col in extended_mapping_cols:
                if col not in mapping_df.columns:
                    if col == "StaticValue":
                        mapping_df[col] = ""
                    elif col == "FilterValues":
                        mapping_df[col] = ""
                    elif col == "DateFormatFlag":
                        mapping_df[col] = False
                    elif col == "IncludeFlag":
                        mapping_df[col] = True
              # Show info about extended format if detected
            has_extended_cols = any(col in mapping_df.columns for col in extended_mapping_cols)
            if has_extended_cols:
                st.info("📋 Enhanced mapping file detected with additional configuration options!")
    
    if input_file_sheets and output_file and (mapping_file is None or mapping_file_valid):
        st.markdown("---")
        st.markdown(f'<h3 style="color: {SANOFI_COLORS["secondary"]}; font-weight: 600; margin-bottom: 1rem;">2.Output Settings</h3>', unsafe_allow_html=True)
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
