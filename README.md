# 📊 Advanced Column Mapping & Transformation Tool

Welcome to the **Advanced Column Mapping & Transformation Tool**! This tool is designed to help you map, transform, and consolidate data from multiple input files into a single output file with ease. Built with Streamlit, it provides an intuitive interface for managing column mappings, applying filters, and handling static values.

---

## ✨ Features

- **Multi-File Support**: Upload multiple input files (Excel or CSV) and map them to a single output template.
- **Sheet Selection**: Choose specific sheets from Excel files for processing.
- **Column Mapping**: Map input columns to output columns with optional static values.
- **Filters**: Apply filters to input data for precise transformations.
- **Date Formatting**: Format date columns to `yyyy-mm-dd` with user control.
- **Enhanced Mapping Files**: Save and reuse mapping configurations including filters, static values, and formatting preferences.
- **Error Handling**: Highlights mapping errors and provides actionable feedback.
- **Download Options**: Export the final output as Excel or TXT (pipe-concatenated) files.

---

## 🚀 How to Use

1. **Upload Files**:
   - Upload one or more input files (Excel or CSV).
   - Upload an output template file to define the desired column structure.

2. **Select Sheets**:
   - For Excel files, select the sheets you want to process.

3. **Map Columns**:
   - Use the intuitive interface to map input columns to output columns.
   - Add static values or apply filters as needed.

4. **Generate Output**:
   - Click the "Generate Final Output" button to process the files.
   - Download the final output as Excel or TXT.

5. **Tips**:
   - 💡 Convert Excel files to CSV format for faster processing before uploading.

---

## 📋 Enhanced Mapping File Format

The tool supports an enhanced mapping file format that allows you to save and reuse complex mapping configurations. This format is backward compatible with the basic format.

### Basic Format (Required Columns)
- `FileName`: Name of your input file
- `SheetName`: Sheet name for Excel files (leave blank for CSV)
- `OutputColumn`: Target column name in output
- `InputColumn`: Source column name in input file

### Enhanced Format (Optional Additional Columns)
- `StaticValue`: Fixed value to assign to the column (leave blank if mapping from input)
- `FilterValues`: Comma-separated values to filter the input data by
- `DateFormatFlag`: `True` to format dates as yyyy-mm-dd, `False` otherwise
- `IncludeFlag`: `True` to include the column in output, `False` to exclude

### Example Enhanced Mapping File
```csv
FileName,SheetName,OutputColumn,InputColumn,StaticValue,FilterValues,DateFormatFlag,IncludeFlag
data.xlsx,Sheet1,Name,Full Name,,,False,True
data.xlsx,Sheet1,Status,,Active,,False,True
data.xlsx,Sheet1,Date,Birth Date,,,True,True
data.xlsx,Sheet1,Category,Type,,A,B,Premium,False,True
```

### Benefits
- **Reusability**: Save complex mappings for repeated use
- **Consistency**: Ensure the same mapping logic across multiple runs
- **Automation**: Reduce manual configuration time
- **Documentation**: Mapping files serve as documentation of your data transformation logic

---

## 📁 Project Structure

- `app.py`: Main entry point for the Streamlit app. Coordinates file uploads, mapping, and output generation.
- `file_utils.py`: Utility functions for reading files and ensuring required columns are present.
- `mapping_logic.py`: Main logic for mapping, processing, and exporting data using Streamlit UI.
- `ui_sections.py`: Streamlit UI components for file upload, footer, and user guide sections.
- `requirements.txt`: Python dependencies for the project.
- `README.md`: Project documentation and usage instructions.

> **Note:** `__pycache__/` contains Python cache files and can be ignored.

---

## 🛠️ Requirements

- Python 3.10+
- Streamlit
- Pandas
- OpenPyXL

Install dependencies using:
```bash
pip install -r requirements.txt
```

---

## 📜 Version Control

### Version 1.1
- Initial release with support for multi-file uploads, column mapping, and output generation.

### Version 1.4
- Added support for handling empty first rows in input files.
- Improved error handling for missing columns in mapping files.
- Changed TXT file encoding from UTF-8 to UTF-16.
- Added a suggestion to convert Excel files to CSV for faster processing.

### Version 1.5
- Added Cell Reference

### Version 1.5.1
- Fixed duplicate column names in same row

### Version 1.6
- Whitespace is now stripped from all column names before deduplication. This ensures that columns like 'fruit ' and 'fruit' are treated as the same column, and mapping to duplicate columns (e.g., 'fruit', 'fruit_1') works robustly even if there are extra spaces in the Excel file. This fixes mapping and filter issues for columns with trailing or leading spaces.

### Version 1.7
- **Fixed Date Formatting Bug**: Resolved issue where date formatting checkbox was not working properly. Previously, columns with "date" in their names were automatically formatted to `yyyy-mm-dd` regardless of user selection.
- **Improved User Control**: Date formatting now properly respects user checkbox selections - dates are only formatted when explicitly checked by the user.
- **Multi-file Date Handling**: Fixed date format flag logic to properly consolidate date formatting preferences across multiple input files.
- **Enhanced Reliability**: Removed automatic date formatting override that was ignoring user preferences, giving users full control over date column formatting.

### Version 1.8
- **Enhanced Mapping File Format**: Extended mapping files to support filters, static values, date formatting flags, and include/exclude preferences for complete configuration reusability.
- **Backward Compatibility**: Existing mapping files with basic format continue to work seamlessly while supporting new enhanced features.
- **Filter Persistence**: Filter values can now be saved in mapping files as comma-separated values and automatically applied when loading configurations.
- **Complete State Preservation**: All UI settings (include flags, static values, date formatting, filters) can now be saved and restored from mapping files.
- **Improved Documentation**: Updated user guide with detailed examples of both basic and enhanced mapping file formats.
---

## 🚦 Limits & Recommendations

- **Number of Input Files:**
  - There is no hard-coded limit on the number of input files you can upload. However, uploading a very large number of files (e.g., dozens or more) may slow down the app or hit browser/memory limits, depending on your system resources.

- **Excel Sheets per File:**
  - You can select and process any number of sheets from each Excel file. There is no explicit limit, but performance may degrade with very large or complex workbooks.

- **File Size Limit:**
  - Streamlit's default file uploader supports files up to 200MB. For best performance, keep individual files under 50MB. Large files may cause slow uploads, memory errors, or browser crashes.
  - You can increase the file size limit by setting `server.maxUploadSize` in your `.streamlit/config.toml` (see Streamlit documentation).

- **Recommended Data Size:**
  - For smooth operation, keep total data (all files combined) under 100,000 rows. Larger datasets may work but could be slow or unstable, depending on your hardware.

- **Other Notes:**
  - Only Excel (`.xlsx`) and CSV files are supported as input.
  - Avoid using files with extremely wide tables (hundreds of columns), as UI and memory issues may occur.
  - If you encounter performance issues, try splitting your data into smaller files or converting Excel to CSV for faster processing.

---

## 💡 Future Enhancements

- Add support for additional file formats (e.g., JSON, XML).
- Enable advanced filtering options with custom logic.
- Provide real-time previews of transformations.

---

## 🖋️ Author
Developed by Ashish Kumar. Feel free to reach out for feedback or contributions!
