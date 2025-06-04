# 📍 Cell/Row Reference Feature - Detailed Explanation

## 🎯 **Purpose**
This feature allows you to specify which row contains the actual column headers in your Excel file, instead of always assuming they're in row 1.

## 📊 **Real-World Example**

### Before Using Cell Reference:
```
Excel File Structure:
Row 1: "MONTHLY SALES REPORT - JANUARY 2024"     ← Title (not data)
Row 2: "Department: Marketing"                    ← Metadata (not data)  
Row 3: [empty row]                               ← Empty (not data)
Row 4: "Name"    "Age"    "Department"   "Salary" ← ACTUAL COLUMN HEADERS
Row 5: "John"    "25"     "Engineering"  "75000"  ← Data starts here
Row 6: "Jane"    "30"     "Marketing"    "65000"  ← More data
```

**Problem**: Without cell reference, the tool would think:
- Column 1 is named "MONTHLY SALES REPORT - JANUARY 2024"
- Column 2 is named "Department: Marketing"
- And so on...

### After Using Cell Reference (Enter "4"):
The tool correctly identifies:
- Column 1 is named "Name"
- Column 2 is named "Age" 
- Column 3 is named "Department"
- Column 4 is named "Salary"

## 🔧 **How the Logic Works**

### Step 1: User Input
```python
col_header_cell = st.text_input(
    "(Optional) Enter row number where column names start (e.g., 4):",
    value="",
    key=f"{item['label']}_col_header_cell_{idx}"
)
```
- User enters: `4` (meaning row 4 contains the headers)

### Step 2: Parse and Validate
```python
match = re.match(r"(\d+)", col_header_cell.strip())
if match:
    row_part = match.group(1)  # Extracts "4"
    row_idx = int(row_part) - 1  # Converts to 3 (pandas is 0-based)
```
- Excel uses 1-based indexing (Row 1, 2, 3, 4...)
- Pandas uses 0-based indexing (Index 0, 1, 2, 3...)
- So Row 4 in Excel = Index 3 in pandas

### Step 3: Extract Headers and Data
```python
if 0 <= row_idx < len(input_df):
    if input_df.iloc[row_idx].isnull().all():
        st.warning(f"Row {row_part} is all empty/NaN. Please check your file.")
    else:
        # Use row 4 (index 3) as column names
        input_df.columns = input_df.iloc[row_idx].astype(str).str.strip()
        input_df.columns = deduplicate_columns(input_df.columns)
        # Keep only rows after the header row (row 5 onwards)
        input_df = input_df[row_idx+1:].reset_index(drop=True)
```

**What happens:**
1. **Extract headers**: Takes row 4 values → ["Name", "Age", "Department", "Salary"]
2. **Set as column names**: `input_df.columns = ["Name", "Age", "Department", "Salary"]`
3. **Remove header and above rows**: Keeps only rows 5+ (the actual data)
4. **Reset index**: Makes the data start from index 0 again

### Step 4: Fallback Logic
```python
else:
    # Fallback: if first row is empty, use current logic
    if input_df.iloc[0].isnull().all():
        # If row 1 is empty, assume headers are in row 2
        input_df.columns = input_df.iloc[1].astype(str).str.strip()
        input_df.columns = deduplicate_columns(input_df.columns)
        input_df = input_df[2:].reset_index(drop=True)
```

## 🎯 **Use Cases**

### Case 1: Headers in Row 4
- User enters: `4`
- Result: Uses row 4 as headers, data starts from row 5

### Case 2: Headers in Row 1 (Default)
- User enters: `1` or leaves blank
- Result: Uses row 1 as headers, data starts from row 2

### Case 3: Headers in Row 7
- User enters: `7`
- Result: Uses row 7 as headers, data starts from row 8

## ⚠️ **Error Handling**

### Empty Row Warning
```python
if input_df.iloc[row_idx].isnull().all():
    st.warning(f"Row {row_part} is all empty/NaN. Please check your file.")
```
- If user specifies row 5 but row 5 is completely empty
- Shows warning: "Row 5 is all empty/NaN. Please check your file."

### Out of Bounds
```python
if 0 <= row_idx < len(input_df):
    # Process normally
else:
    st.warning(f"Row {row_part} is out of bounds for this file.")
```
- If user enters row 100 but file only has 50 rows
- Shows warning: "Row 100 is out of bounds for this file."

### Invalid Input
```python
match = re.match(r"(\d+)", col_header_cell.strip())
if match:
    # Process normally
else:
    st.warning("Invalid row number. Please enter a valid integer (e.g., 4).")
```
- If user enters "abc" or "row 4" instead of "4"
- Shows warning about invalid format

## 🔄 **Before vs After Transformation**

### Before (Raw Excel Data):
```
Index  Col1                              Col2               Col3
0      MONTHLY SALES REPORT             [empty]            [empty]
1      Department: Marketing            [empty]            [empty]  
2      [empty]                          [empty]            [empty]
3      Name                             Age                Department
4      John                             25                 Engineering
5      Jane                             30                 Marketing
```

### After (User enters "4"):
```
Index  Name     Age    Department
0      John     25     Engineering
1      Jane     30     Marketing
```

## 💡 **Pro Tips**

1. **Open your Excel file first** to see which row contains the headers
2. **Count from the top**: Row 1 is the very first row you see
3. **Use this feature when**:
   - Your Excel has title rows at the top
   - There are empty rows before headers
   - Headers are not in the first row
4. **Leave blank if headers are in row 1** (most common case)

This feature makes the tool much more flexible for handling real-world Excel files that don't follow the "headers in row 1" convention!
