import streamlit as st

def show_upload_section(SANOFI_COLORS):
    st.markdown(f'<h2 style="color: {SANOFI_COLORS["secondary"]};">1. Upload Files</h2>', unsafe_allow_html=True)
    input_files = st.file_uploader(
        "Upload One or More Input Files (CSV or Excel)", 
        type=["csv", "xlsx"], 
        accept_multiple_files=True,
        key="input_files_uploader"
    )
    output_file = st.file_uploader(
        "Upload Output Template File (CSV or Excel)", 
        type=["csv", "xlsx"],
        key="sample_file_uploader"
    )
    mapping_file = st.file_uploader(
        "Upload Optional Column Mapping Reference (CSV or Excel)", 
        type=["csv", "xlsx"],
        key="mapping_file_uploader"
    )
    st.caption("📦 Max upload size per file: 1GB")
    return input_files, output_file, mapping_file

def show_footer():
    st.markdown("""
    <style>
    .footer-ashish {color: rgba(180,180,180,0.35); background: transparent; text-align: right; font-size: 0.72rem; padding: 0 8px 2px 0; margin-top: 10px; margin-bottom: 2px; user-select: none; letter-spacing: 0.01em;}
    </style>
    <div class="footer-ashish">Made with ❤️ by Ashish Kumar</div>
    """, unsafe_allow_html=True)

def show_guide():
    with st.expander("📖 How to Use This Tool - Click to Expand"):
        st.markdown("""
        ### Step-by-Step Guide

        #### 1. Prepare Your Files
        - **Input Files**: Prepare one or more CSV/Excel files that contain your source data.
        - **Output Template**: Create a template file with your desired output column structure.
        - **Optional Mapping File**: If you have a pre-defined mapping, prepare a CSV/Excel with columns:
            - `FileName`: Name of your input file (e.g., `data.xlsx`, `input.csv`)
            - `SheetName`: Sheet name for Excel files (e.g., `Sheet1`). Leave blank or write `NA` for CSV files.
            - `OutputColumn`: Column name from output template
            - `InputColumn`: Corresponding column name in input file or sheet

          **Example:**
          | FileName   | SheetName | OutputColumn | InputColumn |
          |------------|-----------|--------------|-------------|
          | data.xlsx  | Sheet1    | Name         | Full Name   |
          | data.xlsx  | Sheet2    | Age          | Years       |
          | input.csv  |           | Name         | Name        |
          | input.csv  | NA        | Age          | Age         |

        > **📝 Tip:**  
        > If you want a mapping to apply to all sheets in a file, leave `SheetName` blank or `"NA"`.  
        > If you want a mapping to apply to a specific sheet, fill in the `SheetName`.

        #### 2. Upload Files
        - Upload your input files (CSV/Excel)
        - Upload your output template file (CSV/Excel)
        - Optionally upload a mapping reference file

        #### 3. Map Columns for Each File
        For each input file or sheet, you'll see a tab where you can:
        - ☑️ **Include/Exclude**: Toggle columns you want in the output
        - 📍 **Output Column**: View the target column names
        - 🔄 **Map to Input Column**: Select which input column maps to each output column
        - 📝 **Static Value**: Optionally enter a fixed value instead of mapping
        """)
