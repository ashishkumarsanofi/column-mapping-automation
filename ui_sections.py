"""
ui_sections.py

Streamlit UI components for file upload, footer, and user guide sections.
"""

import streamlit as st
import pandas as pd

def show_upload_section(SANOFI_COLORS):
    """
    Renders the file upload section in the Streamlit UI with a 3-column layout.
    Args:
        SANOFI_COLORS (dict): Color palette for UI styling.
    Returns:
        tuple: (input_files, output_file, mapping_file)
    """
    st.markdown(f'<h3 style="color: {SANOFI_COLORS["secondary"]};">1. Upload Files</h3>', unsafe_allow_html=True)
    
    # Create 3 columns for the upload sections
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 📁 Input Files")
        st.markdown("*Your source data files*")
        input_files = st.file_uploader(
            "Upload your data files (CSV or Excel)", 
            type=["csv", "xlsx"], 
            accept_multiple_files=True,
            key="input_files_uploader",
            help="Upload one or more CSV or Excel files containing your source data"
        )
    
    with col2:
        st.markdown("#### 🎯 Output Template")
        st.markdown("*Define your target structure*")
        output_file = st.file_uploader(
            "Upload output template file (CSV or Excel)", 
            type=["csv", "xlsx"],
            key="sample_file_uploader",
            help="Upload a template file that defines your desired output column structure"
        )
    
    with col3:
        st.markdown("#### 🗂️ Mapping File")
        st.markdown("*Optional pre-configured mappings*")
        mapping_file = st.file_uploader(
            "Upload mapping reference (Optional)", 
            type=["csv", "xlsx"],
            key="mapping_file_uploader",
            help="Optional: Upload a pre-configured mapping file to speed up the process"
        )
    
    # Add a subtle note about file size limits
    st.caption("💡 Tip: Files up to 200MB supported • Convert Excel to CSV for faster processing")
    return input_files, output_file, mapping_file

def show_footer():
    """
    Renders the custom footer in the Streamlit UI.
    """
    st.markdown("""
    <style>
    .footer-ashish {color: rgba(180,180,180,0.35); background: transparent; text-align: right; font-size: 0.71rem; padding: 0 8px 2px 0; margin-top: 10px; margin-bottom: 2px; user-select: none; letter-spacing: 0.01em;}
    </style>
    <div class="footer-ashish">Made with ❤️ by Ashish Kumar</div>
    """, unsafe_allow_html=True)

def show_guide():
    """
    Renders the step-by-step user guide in an expandable section.
    """
    with st.expander("📖 How to Use This Tool - Click to Expand"):
        st.markdown("""
        ### Step-by-Step Guide 
        #### 1. Prepare Your Files
        - **Input Files**: Prepare one or more CSV/Excel files that contain your source data.
        - **Output Template**: Create a template file with your desired output column structure.
        - **Optional Mapping File**: If you have a pre-defined mapping, prepare a CSV/Excel with columns:
            
            **Basic Format (Required Columns):**
            - `FileName`: Name of your input file (e.g., `data.xlsx`, `input.csv`)
            - `SheetName`: Sheet name for Excel files (e.g., `Sheet1`). Leave blank or write `NA` for CSV files.
            - `OutputColumn`: Column name from output template
            - `InputColumn`: Corresponding column name in input file or sheet
                    
            **Enhanced Format (Additional Optional Columns):**
            - `StaticValue`: Fixed value to use instead of mapping from input (leave blank if mapping)
            - `FilterValues`: Comma-separated values to filter input data by (e.g., "A,B,Premium")
            - `DateFormatFlag`: `True` to format as yyyy-mm-dd, `False` otherwise
            - `IncludeFlag`: `True` to include column in output, `False` to exclude

          **Basic Example:**
          | FileName   | SheetName | OutputColumn | InputColumn |
          |------------|-----------|--------------|-------------|
          | data.xlsx  | Sheet1    | Name         | Full Name   |
          | data.xlsx  | Sheet2    | Age          | Years       |
          | input.csv  |           | Name         | Name        |

          **Enhanced Example:**
          | FileName   | SheetName | OutputColumn | InputColumn | StaticValue | FilterValues | DateFormatFlag | IncludeFlag |
          |------------|-----------|--------------|-------------|-------------|--------------|----------------|-------------|
          | data.xlsx  | Sheet1    | Name         | Full Name   |             |              | False          | True        |
          | data.xlsx  | Sheet1    | Status       |             | Active      |              | False          | True        |
          | data.xlsx  | Sheet1    | Date         | Birth Date  |             |              | True           | True        |
          | data.xlsx  | Sheet1    | Category     | Type        |             | A,B,Premium  | False          | True        |

        > **📝 Tips:**  
        > - If you want a mapping to apply to all sheets in a file, leave `SheetName` blank or `"NA"`.  
        > - If you want a mapping to apply to a specific sheet, fill in the `SheetName`.
        > - Enhanced format is backward compatible - you can mix basic and enhanced mappings.
        > - Filter values should be comma-separated without spaces around commas.

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
        - 🗂️ **Filter**: Apply filters to input data (optional)
        - 📅 **Date Format**: Enable date formatting to yyyy-mm-dd format (optional)

        #### 4. Generate Output
        - Review your mappings and click "Generate Final Output"
        - Download the consolidated Excel or TXT file

        #### 5. Save Your Configuration
        - Download the mapping configuration file for future use
        - Reuse saved configurations to speed up repeated tasks
        """)
        
        # Add sample mapping file download section
        st.markdown("---")
        st.markdown("#### 📥 Download Sample Mapping Files")
        st.markdown("Get started quickly with these pre-configured mapping file templates:")
        
        # Create sample mapping data
        sample_basic_data = {
            'FileName': ['input_data.xlsx', 'input_data.xlsx', 'sales_data.csv', 'sales_data.csv'],
            'SheetName': ['Sheet1', 'Sheet1', '', ''],
            'OutputColumn': ['Customer_Name', 'Order_Date', 'Product_ID', 'Revenue'],
            'InputColumn': ['Full Name', 'Date', 'SKU', 'Total Amount']
        }
        
        sample_enhanced_data = {
            'FileName': ['input_data.xlsx', 'input_data.xlsx', 'input_data.xlsx', 'sales_data.csv', 'sales_data.csv'],
            'SheetName': ['Sheet1', 'Sheet1', 'Sheet1', '', ''],
            'OutputColumn': ['Customer_Name', 'Status', 'Order_Date', 'Product_Category', 'Revenue'],
            'InputColumn': ['Full Name', '', 'Date', 'Category', 'Total Amount'],
            'StaticValue': ['', 'Active', '', '', ''],
            'FilterValues': ['', '', '', 'Electronics,Books', ''],
            'DateFormatFlag': [False, False, True, False, False],
            'IncludeFlag': [True, True, True, True, True]
        }
        
        # Create download buttons in two columns
        col1, col2 = st.columns(2)
        
        with col1:
            basic_df = pd.DataFrame(sample_basic_data)
            basic_csv = basic_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Basic Sample",
                data=basic_csv,
                file_name="sample_basic_mapping.csv",
                mime="text/csv",
                help="Download a basic mapping file template with required columns only"
            )
            st.caption("✅ Basic format with essential columns")
        
        with col2:
            enhanced_df = pd.DataFrame(sample_enhanced_data)
            enhanced_csv = enhanced_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Enhanced Sample",
                data=enhanced_csv,
                file_name="sample_enhanced_mapping.csv",
                mime="text/csv",
                help="Download an enhanced mapping file template with all optional features"
            )
            st.caption("🚀 Enhanced format with all features")
