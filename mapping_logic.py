"""
mapping_logic.py

Contains the main logic for mapping, processing, and exporting data using Streamlit UI.
"""

import pandas as pd
import streamlit as st
from file_utils import read_file, fill_missing_columns

# Utility: Deduplicate columns

def deduplicate_columns(columns):
    """
    Ensures column names are unique by appending a suffix to duplicates.
    Args:
        columns (list): List of column names.
    Returns:
        list: List of unique column names.
    """
    counts = {}
    new_cols = []
    for col in columns:
        col_str = str(col)
        if col_str in counts:
            counts[col_str] += 1
            new_cols.append(f"{col_str}_{counts[col_str]}")
        else:
            counts[col_str] = 0
            new_cols.append(col_str)
    return new_cols

# Main function: Handles mapping UI and logic

def process_mapping_tabs(input_file_sheets, output_file, mapping_file, mapping_file_valid, mapping_df, output_columns):
    """
    Handles the mapping UI and logic for each file/sheet tab. Returns final_dataframes and output_filename.
    Optimized for speed: uses Streamlit caching for file reads and DataFrame operations.
    Args:
        input_file_sheets (list): List of dicts with file/sheet info.
        output_file: Output template file object.
        mapping_file: Optional mapping file object.
        mapping_file_valid (bool): Whether mapping file is valid.
        mapping_df (pd.DataFrame): Mapping DataFrame.
        output_columns (list): List of output column names.
    Returns:
        tuple: (final_dataframes, output_filename)
    """
    @st.cache_data(show_spinner=False, max_entries=20)
    def cached_read_file(file):
        return read_file(file)

    @st.cache_data(show_spinner=False, max_entries=20)
    def cached_read_excel(file, sheet_name, usecols):
        # Optimize Excel reading: use openpyxl, only read necessary columns, avoid dtype conversion if not needed
        return pd.read_excel(file, sheet_name=sheet_name, usecols=usecols, engine='openpyxl')

    final_dataframes = []
    active_file_sheets = input_file_sheets
    tab_labels = [f"🗂 {item['label']}" for item in active_file_sheets]
    if not tab_labels:
        st.info("No files/sheets to map. Please upload or add a file.")
        return [], st.session_state.get("output_file_name", "final_output")
    tabs = st.tabs(tab_labels)
    for idx, (item, tab) in enumerate(zip(active_file_sheets, tabs)):
        with tab:
            st.subheader(f"Mapping for: {item['label']}")            # Master control buttons for select/deselect all
            col1, col2, col3 = st.columns([1, 1, 4])
            with col1:
                if st.button("✅ Select All Columns", key=f"{item['label']}_select_all_{idx}"):
                    for col in output_columns:
                        st.session_state[f"{item['label']}_{col}_inc_{idx}"] = True
                    st.rerun()
            with col2:
                if st.button("❌ Deselect All Columns", key=f"{item['label']}_deselect_all_{idx}"):
                    for col in output_columns:
                        st.session_state[f"{item['label']}_{col}_inc_{idx}"] = False
                    st.rerun()
            if item["sheet"]:
                input_df = cached_read_excel(item["file"], item["sheet"], None)  # Read all columns
            else:
                input_df, validation_errors = cached_read_file(item["file"])            # --- STRIP WHITESPACE BEFORE DEDUPLICATION ---
            input_df.columns = input_df.columns.str.strip()
            
            # Helper function to process header row and update DataFrame
            def process_header_row(df, header_row_idx):
                """Extract headers from specified row and return updated DataFrame"""
                if header_row_idx < 0 or header_row_idx >= len(df):
                    return df, f"Row {header_row_idx + 1} is out of bounds for this file."
                
                header_row = df.iloc[header_row_idx]
                if header_row.isnull().all():
                    return df, f"Row {header_row_idx + 1} is all empty/NaN. Please check your file."
                
                # Set new column names from the specified row
                df.columns = header_row.astype(str).str.strip()
                df.columns = deduplicate_columns(df.columns)
                # Keep data from rows after the header row
                df = df[header_row_idx + 1:].reset_index(drop=True)
                return df, None
              # Show preview of first few rows to help user identify header row
            st.markdown("**📋 File Preview** (to help identify header row):")
            preview_rows = min(5, len(input_df))
            preview_data = []
            for i in range(preview_rows):
                row_content = input_df.iloc[i].astype(str).tolist()
                # Truncate long content for display
                row_display = [content[:30] + "..." if len(content) > 30 else content for content in row_content]
                preview_data.append({
                    "Row": f"Row {i + 1}",
                    "Content": " | ".join(row_display[:3]) + (" | ..." if len(row_display) > 3 else "")
                })
            
            preview_df = pd.DataFrame(preview_data)
            st.dataframe(preview_df, use_container_width=True, hide_index=True)
            
            # Option for user to specify which row contains column headers
            header_row_input = st.text_input(
                "📍 (Optional) Which row contains the column headers?",
                value="",
                key=f"{item['label']}_header_row_{idx}",
                help="Enter the row number that contains your column headers (e.g., if headers are in Row 3, enter '3'). Leave empty to use Row 1 as headers.",
                placeholder="Enter row number (e.g., 3)"
            )
            
            # Process header row specification
            if header_row_input.strip():
                try:
                    header_row_number = int(header_row_input.strip())
                    if header_row_number < 1:
                        st.error("❌ Row number must be 1 or greater.")
                    elif header_row_number > len(input_df):
                        st.error(f"❌ Row {header_row_number} doesn't exist. File only has {len(input_df)} rows.")
                    else:
                        header_row_idx = header_row_number - 1  # Convert to 0-based index
                        
                        # Show what will be used as headers for confirmation
                        header_preview = input_df.iloc[header_row_idx].astype(str).tolist()
                        st.info(f"🔍 **Row {header_row_number} content:** {' | '.join(header_preview[:5])}")
                        
                        input_df, error_msg = process_header_row(input_df, header_row_idx)
                        if error_msg:
                            st.warning(f"⚠️ {error_msg}")
                        else:
                            st.success(f"✅ Using Row {header_row_number} as column headers. Headers: {', '.join(list(input_df.columns)[:5])}")
                except ValueError:
                    st.error("❌ Please enter a valid row number (e.g., 3).")
            else:
                # Auto-detect: if first row is empty, try to find the first non-empty row for headers
                if len(input_df) > 0 and input_df.iloc[0].isnull().all():
                    # Look for the first non-empty row to use as headers
                    header_found = False
                    for check_idx in range(1, min(len(input_df), 5)):  # Check first 5 rows max
                        if not input_df.iloc[check_idx].isnull().all():
                            input_df, error_msg = process_header_row(input_df, check_idx)
                            if not error_msg:
                                excel_row_num = check_idx + 1  # Convert back to Excel row number
                                st.info(f"ℹ️ First row was empty, automatically using row {excel_row_num} as headers.")
                                header_found = True
                                break
                    
                    if not header_found:
                        st.warning("⚠️ Could not find non-empty row for headers in the first 5 rows.")
            # Only keep columns from input file, not output template
            input_columns = input_df.columns.tolist()
            # Build a mapping of base column names to their occurrences (for deduplication)
            col_occurrences = {}
            for idx_col, col in enumerate(input_columns):
                base = str(col)
                if '_' in base and base.rsplit('_', 1)[-1].isdigit():
                    base_name = '_'.join(base.split('_')[:-1])
                else:
                    base_name = base
                col_occurrences.setdefault(base_name, []).append(col)
            # Add logging to verify col_occurrences and mapping logic
            import logging
            logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
            # Log col_occurrences after it is populated
            logging.debug(f"col_occurrences: {col_occurrences}")            # Add detailed logging to debug mapping logic
            logging.debug(f"Input columns (deduplicated): {input_columns}")
            logging.debug(f"col_occurrences: {col_occurrences}")
            
            # Removed automatic date formatting - user controls this with checkboxes
            column_mapping = {col: None for col in output_columns}
            include_flags = {col: True for col in output_columns}
            static_values = {col: "" for col in output_columns}
            date_format_flags = {}
            active_filters = {}
            mapping_dict = {}
            static_value_dict = {}
            filter_dict = {}
            date_format_dict = {}
            include_dict = {}
            
            if mapping_df is not None and mapping_file_valid:
                file_name = item["file"].name
                sheet_name = item["sheet"] or ""
                mapping_df['FileName_norm'] = mapping_df['FileName'].fillna("").astype(str).str.strip().str.lower()
                mapping_df['SheetName_norm'] = mapping_df['SheetName'].fillna("").astype(str).str.strip().str.lower()
                file_name_norm = str(file_name).strip().lower()
                sheet_name_norm = str(sheet_name).strip().lower()
                
                # Allow mapping to apply to all files if FileName is blank or 'NA', and all sheets if SheetName is blank or 'NA'
                file_mapping = mapping_df[
                    ((mapping_df['FileName_norm'] == file_name_norm) | (mapping_df['FileName_norm'].isin(["", "na"]))) &
                    ((mapping_df['SheetName_norm'] == sheet_name_norm) | (mapping_df['SheetName_norm'].isin(["", "na"])))
                ]
                
                # Build dictionaries for all configuration options
                mapping_dict = dict(zip(file_mapping['OutputColumn'], file_mapping['InputColumn']))
                
                # Handle optional enhanced columns
                if 'StaticValue' in mapping_df.columns:
                    static_value_dict = dict(zip(file_mapping['OutputColumn'], file_mapping['StaticValue'].fillna("")))
                
                if 'FilterValues' in mapping_df.columns:
                    filter_dict = {}
                    for _, row in file_mapping.iterrows():
                        if pd.notna(row['FilterValues']) and str(row['FilterValues']).strip():
                            # Parse filter values (assuming they're stored as comma-separated)
                            filter_values = [v.strip() for v in str(row['FilterValues']).split(',') if v.strip()]
                            if filter_values:
                                filter_dict[row['OutputColumn']] = filter_values
                
                if 'DateFormatFlag' in mapping_df.columns:
                    date_format_dict = dict(zip(file_mapping['OutputColumn'], file_mapping['DateFormatFlag'].fillna(False)))
                    # Convert string representations to boolean
                    for key, value in date_format_dict.items():
                        if isinstance(value, str):
                            date_format_dict[key] = value.lower() in ['true', '1', 'yes', 'on']
                
                if 'IncludeFlag' in mapping_df.columns:
                    include_dict = dict(zip(file_mapping['OutputColumn'], file_mapping['IncludeFlag'].fillna(True)))
                    # Convert string representations to boolean
                    for key, value in include_dict.items():
                        if isinstance(value, str):
                            include_dict[key] = value.lower() in ['true', '1', 'yes', 'on']            # Header row for mapping UI
            header_cols = st.columns([1, 2, 3, 2, 2.5, 2])
            with header_cols[0]:
                st.markdown("**Include**")
            with header_cols[1]:
                st.markdown("**Output Column**")
            with header_cols[2]:
                st.markdown("**Map to Input Column**")
            with header_cols[3]:
                st.markdown("**Static Value**")
            with header_cols[4]:
                st.markdown("**Filter**")
            with header_cols[5]:
                st.markdown("**Date Format**")
            
            for col in output_columns:
                cols = st.columns([1, 2, 3, 2, 2.5, 2])
                
                # Get values from mapping file or use defaults
                default_include = include_dict.get(col, True)
                default_static = static_value_dict.get(col, "")
                default_date_format = date_format_dict.get(col, ("date" in col.lower()))
                mapped_filter_values = filter_dict.get(col, [])
                
                with cols[0]:
                    include = st.checkbox("Include", value=default_include, key=f"{item['label']}_{col}_inc_{idx}", label_visibility="collapsed")
                with cols[1]:
                    st.markdown(f"<span style='line-height: 2.5'>{col}</span>", unsafe_allow_html=True)
                with cols[2]:
                    # Always use stripped input_columns for mapping options
                    mapping_options = ["--Select--", "--Blank--"] + input_columns
                    default_map = mapping_dict.get(col, "--Select--")
                    # If default_map is not in mapping_options, try stripping it
                    if default_map not in mapping_options and isinstance(default_map, str):
                        default_map = default_map.strip()
                    mapped_col = st.selectbox("Map to Input Column", mapping_options, index=mapping_options.index(default_map) if default_map in mapping_options else 0, key=f"{item['label']}_{col}_map_{idx}", label_visibility="collapsed")
                    
                    # --- FIXED LOGIC: Robust to whitespace and matches deduplicated columns ---
                    mapped_col_original = mapped_col  # Save for UI display
                    if mapped_col:
                        mapped_col = mapped_col.strip()
                    # --- FIX: If user selects '--Blank--', preserve it exactly ---
                    if mapped_col == "--Blank--":
                        pass  # Do not change mapped_col if it's --Blank--
                    else:
                        col_occurrences_stripped = {k.strip(): [c.strip() for c in v] for k, v in col_occurrences.items()}
                        input_columns_stripped = [c.strip() for c in input_columns]
                        if mapped_col and mapped_col not in input_columns_stripped:
                            import re
                            match = re.match(r"^(.*?)(?:_(\d+))?$", mapped_col)
                            if match:
                                base_name = match.group(1).strip()
                                idx_num = int(match.group(2)) if match.group(2) is not None else 0
                                if base_name in col_occurrences_stripped and len(col_occurrences_stripped[base_name]) > idx_num:
                                    mapped_col = col_occurrences_stripped[base_name][idx_num]
                                else:
                                    mapped_col = None
                    # Defensive: If mapped_col is not in input_columns and not --Blank--, set mapped_col to None
                    if mapped_col not in input_columns and mapped_col != "--Blank--":
                        mapped_col = None
                        
                with cols[3]:
                    static_val = st.text_input("Static Value", default_static, key=f"{item['label']}_{col}_static_{idx}", label_visibility="collapsed")
                    
                with cols[4]:
                    # Use the resolved mapped_col for filter UI and checks
                    if mapped_col in ("--Select--", "--Blank--") or not mapped_col:
                        st.caption("Select an input column to enable filtering.")
                    elif mapped_col not in input_df.columns:
                        st.caption(f"Column '{mapped_col}' not found in input data.")
                    else:
                        # Defensive: Only proceed if mapped_col is a string and in input_df.columns
                        if isinstance(mapped_col, str) and mapped_col in input_df.columns:
                            unique_vals = input_df[mapped_col].astype(str).unique().tolist()
                            if len(unique_vals) < 500:
                                filter_key = f"{item['label']}_{col}_filter_{idx}"
                                # Use pre-selected filter values from mapping file if available
                                default_filter_values = mapped_filter_values if mapped_filter_values else []
                                filter_values = st.multiselect(
                                    "Filter values (optional)",
                                    options=unique_vals,
                                    default=default_filter_values,
                                    key=filter_key
                                )
                                if filter_values:
                                    active_filters[mapped_col] = filter_values
                            else:
                                st.caption("Too many unique values to filter interactively.")
                        else:
                            st.caption(f"Column '{mapped_col}' not found or invalid in input data.")
                            
                with cols[5]:
                    show_date_checkbox = ("date" in col.lower() or (mapped_col and mapped_col != "--Select--" and "date" in mapped_col.lower()))
                    if show_date_checkbox:
                        date_format_flags[col] = st.checkbox("Format as yyyy-mm-dd", value=default_date_format, key=f"{item['label']}_{col}_datefmt_{idx}")
                    else:
                        date_format_flags[col] = False
                        
                # Always assign mapped_col, including '--Blank--' and '--Select--'
                column_mapping[col] = mapped_col
                include_flags[col] = include
                static_values[col] = static_val
            filtered_df = input_df.copy()
            for filter_col, filter_vals in active_filters.items():
                # Defensive: Only filter if filter_col is in input_df.columns
                if filter_vals and filter_col in filtered_df.columns:
                    filtered_df = filtered_df[filtered_df[filter_col].astype(str).isin(filter_vals)]
            final_dataframes.append({"file": item["file"], "label": item["label"], "sheet": item.get("sheet"), "input_df": filtered_df, "column_mapping": column_mapping, "include_flags": include_flags, "static_values": static_values, "date_format_flags": date_format_flags, "active_filters": active_filters})
    output_filename = st.text_input("📄 Enter Output File Name:", value="final_output", help="This will be the name of your output Excel and TXT files", key="output_file_name")
    return final_dataframes, output_filename

def process_final_output(final_dataframes, output_columns, output_filename):
    """
    Processes the final output by consolidating mapped dataframes, handling errors, and providing download options.
    Args:
        final_dataframes (list): List of dicts with processed data for each file/sheet.
        output_columns (list): List of output column names.
        output_filename (str): Name for the output file.
    Returns:
        pd.DataFrame or None: The final combined DataFrame, or None if errors exist.
    """
    import io, warnings
    import pandas as pd
    st.markdown("---")
    if st.button("🔄 Generate Final Output"):
        with st.spinner("Processing files..."):
            combined_df_list = []
            all_mapping_errors = []
            for file_data in final_dataframes:
                input_df = file_data["input_df"]
                column_mapping = file_data["column_mapping"]
                include_flags = file_data["include_flags"]
                static_values = file_data["static_values"]
                df_output = pd.DataFrame(index=range(len(input_df)))
                for col in output_columns:
                    if include_flags[col]:
                        mapped_col = column_mapping[col].strip() if column_mapping[col] else column_mapping[col]
                        static_val = static_values[col]

                        # 1. If mapped_col is None, '', or '--Select--' and no static value: error
                        if mapped_col in [None, '', '--Select--'] and not static_val:
                            all_mapping_errors.append(f"❌ <b>{col}</b> in <b>{file_data['label']}</b> is included but not mapped to any input column and has no static value.")
                            df_output[col] = [""] * len(input_df)
                            continue
                        # 2. If mapped_col is None, '', or '--Select--' and static value: fill with static value
                        if mapped_col in [None, '', '--Select--'] and static_val:
                            df_output[col] = [static_val] * len(input_df)
                            continue
                        # 3. If mapped_col is '--Blank--' and no static value: fill with empty
                        if mapped_col == '--Blank--' and not static_val:
                            df_output[col] = [""] * len(input_df)
                            continue
                        # 4. If mapped_col is '--Blank--' and static value: error
                        if mapped_col == '--Blank--' and static_val:
                            all_mapping_errors.append(f"⚠️ <b>{col}</b> in <b>{file_data['label']}</b> has both a mapping and a static value. Please provide only one.")
                            df_output[col] = [""] * len(input_df)
                            continue
                        # 5. Normal mapping: mapped_col is a real column name, no static value
                        if static_val and mapped_col not in [None, '', '--Select--', '--Blank--']:
                            all_mapping_errors.append(f"⚠️ <b>{col}</b> in <b>{file_data['label']}</b> has both a mapping to '<b>{mapped_col}</b>' and a static value. Please provide only one.")
                            df_output[col] = [""] * len(input_df)
                        elif mapped_col in input_df.columns:
                            df_output[col] = input_df[mapped_col].values
                        else:
                            all_mapping_errors.append(f"❌ <b>{col}</b> in <b>{file_data['label']}</b> is mapped to '<b>{mapped_col}</b>', which does not exist in the input data.")
                            df_output[col] = [""] * len(input_df)
                        # The loop will continue to the next 'col' after this block.
                df_output = fill_missing_columns(df_output, [col for col in output_columns if include_flags[col]])
                combined_df_list.append(df_output)
            if all_mapping_errors:
                st.warning("⚠️ Please resolve the mapping errors below before proceeding.")
                try: st.toast("⚠️ Mapping errors found! Please check and fix them.", icon="⚠️")
                except Exception: pass
                for err in all_mapping_errors:
                    st.markdown(err, unsafe_allow_html=True)
                return None
            else:
                combined_df = pd.concat(combined_df_list, ignore_index=True)
                
                # Create a consolidated date format flags dictionary from all files
                consolidated_date_flags = {}
                for file_data in final_dataframes:
                    for col, flag in file_data["date_format_flags"].items():
                        # If any file has date formatting enabled for this column, enable it
                        if flag:
                            consolidated_date_flags[col] = True
                        elif col not in consolidated_date_flags:
                            consolidated_date_flags[col] = False
                
                # Apply date formatting only if user checked the checkbox
                for col in combined_df.columns:
                    if consolidated_date_flags.get(col, False):
                        with warnings.catch_warnings():
                            warnings.simplefilter("ignore", UserWarning)
                            try:
                                parsed = pd.to_datetime(combined_df[col], errors='coerce', dayfirst=False)
                                if parsed.notna().sum() > 0:
                                    combined_df[col] = parsed.dt.strftime('%Y-%m-%d')
                            except Exception:
                                pass
                ordered_cols = [col for col in output_columns if col in combined_df.columns]
                combined_df = combined_df[ordered_cols]
                output = io.BytesIO()
                try:
                    with pd.ExcelWriter(output, engine='openpyxl', mode='w') as writer:
                        combined_df.to_excel(writer, index=False, sheet_name='FinalMappedData')
                    output.seek(0)
                    st.download_button(label="📥 Download Final Output File", data=output, file_name=f"{output_filename}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                    st.markdown('<div class="success-message">✅ Final consolidated file generated!</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error generating Excel file: {str(e)}")
                    st.stop()
                combined_df_txt = combined_df.fillna("")
                def escape_pipes(val): return str(val).replace("|", " ")
                header_line = "|".join(combined_df_txt.columns)
                txt_lines = combined_df_txt.astype(str).apply(lambda row: "|".join(escape_pipes(v) for v in row.values), axis=1)
                txt_content = "\n".join([header_line] + txt_lines.to_list())
                txt_content = txt_content.encode("utf-16")
                st.download_button(label="📝 Download as TXT (pipe-concat)", data=txt_content, file_name=f"{output_filename}.txt", mime="text/plain")
                
                mapping_rows = []
                for file_data in final_dataframes:
                    file_name = file_data["file"].name
                    # Use the actual sheet value from file_data, which is set in app.py when user selects sheets
                    sheet_name = file_data.get("sheet", None)
                    if sheet_name is None:
                        sheet_name = ""
                    else:
                        sheet_name = str(sheet_name)
                    for col in output_columns:
                        mapped_col = file_data["column_mapping"].get(col, "")
                        if mapped_col is None:
                            mapped_col = ""
                        
                        static_value = file_data["static_values"].get(col, "")
                        include_flag = file_data["include_flags"].get(col, True)
                        date_format_flag = file_data["date_format_flags"].get(col, False)
                          # For filter values, we need to get them from active_filters based on the mapped column
                        filter_values = ""
                        if mapped_col and mapped_col in file_data.get("active_filters", {}):
                            filter_list = file_data["active_filters"][mapped_col]
                            filter_values = ",".join(filter_list) if filter_list else ""
                        
                        mapping_rows.append({
                            "FileName": file_name, 
                            "SheetName": sheet_name, 
                            "OutputColumn": col, 
                            "InputColumn": mapped_col,
                            "StaticValue": static_value,
                            "FilterValues": filter_values,
                            "DateFormatFlag": date_format_flag,
                            "IncludeFlag": include_flag
                        })
                
                mapping_export_df = pd.DataFrame(mapping_rows, columns=[
                    "FileName", "SheetName", "OutputColumn", "InputColumn", 
                    "StaticValue", "FilterValues", "DateFormatFlag", "IncludeFlag"
                ])
                mapping_csv = mapping_export_df.to_csv(index=False).encode("utf-8")
                col1, col2 = st.columns([3, 1])
                with col2:
                    st.download_button(label="⬇️ Download Mapping File (CSV)", data=mapping_csv, file_name="column_mapping.csv", mime="text/csv")
                st.markdown("#### Preview of Final Output")
                st.dataframe(combined_df.head(10))
                st.markdown(f"<div class='success-message'>Processed <b>{len(final_dataframes)}</b> files/sheets, final output has <b>{combined_df.shape[0]}</b> rows and <b>{combined_df.shape[1]}</b> columns.</div>", unsafe_allow_html=True)
                return combined_df

    # Add custom CSS to align the multiselect with other widgets
    st.markdown("""
        <style>
        /* Reduce the top margin and padding for the multiselect filter */
        div[data-baseweb='select'] > div { min-height: 38px !important; }
        div[data-baseweb='select'] { margin-top: -6px !important; }
        </style>
    """, unsafe_allow_html=True)