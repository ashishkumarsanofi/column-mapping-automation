import pandas as pd
import streamlit as st
from file_utils import read_file, fill_missing_columns

def process_mapping_tabs(input_file_sheets, output_file, mapping_file, mapping_file_valid, mapping_df, output_columns):
    """
    Handles the mapping UI and logic for each file/sheet tab. Returns final_dataframes and output_filename.
    Optimized for speed: uses Streamlit caching for file reads and DataFrame operations.
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
            st.subheader(f"Mapping for: {item['label']}")
            # Single master checkbox for select/unselect all
            master_key = f"{item['label']}_master_select_{idx}"
            # Determine if all columns are currently selected
            all_selected = all(st.session_state.get(f"{item['label']}_{col}_inc_{idx}", True) for col in output_columns)
            # Use a local variable to avoid Streamlit's rerun delay
            master_value = st.checkbox("Select/Deselect All Columns", value=all_selected, key=master_key)
            # Only update if the user actually toggled the master checkbox
            if master_value != all_selected:
                for col in output_columns:
                    st.session_state[f"{item['label']}_{col}_inc_{idx}"] = master_value
            if item["sheet"]:
                input_df = cached_read_excel(item["file"], item["sheet"], None)  # Read all columns
            else:
                input_df, validation_errors = cached_read_file(item["file"])
            # Strip whitespace from all input DataFrame column names immediately after reading
            input_df.columns = input_df.columns.str.strip()
            # Only keep columns from input file, not output template
            input_columns = input_df.columns.tolist()
            for col in input_df.columns:
                col_str = str(col)
                if "date" in col_str.lower():
                    try:
                        parsed = pd.to_datetime(input_df[col], errors='coerce', dayfirst=False)
                        if parsed.notna().sum() > len(input_df) // 2:
                            input_df[col] = parsed.dt.strftime('%Y-%m-%d')
                    except Exception:
                        pass
            column_mapping = {col: None for col in output_columns}
            include_flags = {col: True for col in output_columns}
            static_values = {col: "" for col in output_columns}
            date_format_flags = {}
            active_filters = {}
            mapping_dict = {}
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
                mapping_dict = dict(zip(file_mapping['OutputColumn'], file_mapping['InputColumn']))
            # Header row for mapping UI
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
                with cols[0]:
                    include = st.checkbox("Include", value=include_flags[col], key=f"{item['label']}_{col}_inc_{idx}", label_visibility="collapsed")
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
                    # Defensive: If mapped_col is not in input_columns and not --Blank--, set mapped_col to None
                    if mapped_col not in input_columns and mapped_col != "--Blank--":
                        mapped_col = None
                with cols[3]:
                    static_val = st.text_input("Static Value", static_values[col], key=f"{item['label']}_{col}_static_{idx}", label_visibility="collapsed")
                with cols[4]:
                    # Simple filter section: all values selected by default, but UI appears empty
                    if mapped_col in ("--Select--", "--Blank--") or not mapped_col:
                        st.caption("Select an input column to enable filtering.")
                    elif mapped_col not in input_df.columns:
                        st.caption(f"Column '{mapped_col}' not found in input data.")
                    else:
                        unique_vals = input_df[mapped_col].astype(str).unique().tolist()
                        if len(unique_vals) < 500:
                            filter_key = f"{item['label']}_{col}_filter_{idx}"
                            # Show empty by default, but treat empty as 'all selected' in logic
                            filter_values = st.multiselect(
                                "Filter values (optional)",  # Use Unicode hair space to minimize label height
                                options=unique_vals,
                                default=[],
                                key=filter_key
                            )
                            # Only filter if user has selected something
                            if filter_values:
                                active_filters[mapped_col] = filter_values
                        else:
                            st.caption("Too many unique values to filter interactively.")
                with cols[5]:
                    show_date_checkbox = ("date" in col.lower() or (mapped_col and mapped_col != "--Select--" and "date" in mapped_col.lower()))
                    if show_date_checkbox:
                        date_format_flags[col] = st.checkbox("Format as yyyy-mm-dd", value=True, key=f"{item['label']}_{col}_datefmt_{idx}")
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
            final_dataframes.append({"file": item["file"], "label": item["label"], "sheet": item.get("sheet"), "input_df": filtered_df, "column_mapping": column_mapping, "include_flags": include_flags, "static_values": static_values, "date_format_flags": date_format_flags})
    output_filename = st.text_input("📄 Enter Output File Name:", value="final_output", help="This will be the name of your output Excel and TXT files", key="output_file_name")
    return final_dataframes, output_filename

def process_final_output(final_dataframes, output_columns, output_filename):
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
                        # Defensive: Only use mapped_col if it exists in input_df.columns
                        if mapped_col == "--Blank--":
                            df_output[col] = [""] * len(input_df)
                            continue  # Skip further checks if --Blank-- is selected
                        if not mapped_col and not static_values[col]:
                            all_mapping_errors.append(f"❌ <b>{col}</b> in <b>{file_data['label']}</b> is included but not mapped to any input column and has no static value.")
                        elif mapped_col and static_values[col]:
                            all_mapping_errors.append(f"⚠️ <b>{col}</b> in <b>{file_data['label']}</b> has both a mapping and a static value. Please provide only one.")
                        elif mapped_col:
                            if mapped_col in input_df.columns:
                                df_output[col] = input_df[mapped_col].values
                            else:
                                all_mapping_errors.append(f"❌ <b>{col}</b> in <b>{file_data['label']}</b> is mapped to '<b>{mapped_col}</b>', which does not exist in the input data.")
                                df_output[col] = ""
                        elif static_values[col]:
                            df_output[col] = static_values[col]
                        else:
                            df_output[col] = ""
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
                for col in combined_df.columns:
                    if file_data["date_format_flags"].get(col, False):
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
                        mapping_rows.append({"FileName": file_name, "SheetName": sheet_name, "OutputColumn": col, "InputColumn": mapped_col})
                mapping_export_df = pd.DataFrame(mapping_rows, columns=["FileName", "SheetName", "OutputColumn", "InputColumn"])
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
