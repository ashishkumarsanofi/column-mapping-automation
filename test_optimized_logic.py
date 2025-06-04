"""
Test script for the optimized cell/row reference logic
"""
import pandas as pd
import sys
import os

# Add the main directory to path so we can import the modules
sys.path.append(r"c:\Users\U1079110\Downloads\Local Disk D\Mapping tool code")

from mapping_logic import deduplicate_columns

def test_cell_reference_logic():
    """Test the optimized helper function logic"""
    
    print("🧪 Testing optimized cell/row reference logic...")
    
    # Create test DataFrame
    test_data = {
        'Col1': ['TITLE ROW', 'Metadata', '', 'Name', 'John', 'Jane'],
        'Col2': ['', '', '', 'Age', '25', '30'],
        'Col3': ['', '', '', 'Department', 'Engineering', 'Marketing']
    }
    df = pd.DataFrame(test_data)
    print("📊 Test DataFrame:")
    print(df)
    print()
    
    # Test the helper function logic manually
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
    
    # Test Case 1: Valid row (row 4, index 3)
    print("🔍 Test Case 1: Using row 4 as headers (index 3)")
    result_df, error = process_header_row(df.copy(), 3)
    if error:
        print(f"❌ Error: {error}")
    else:
        print("✅ Success! Headers extracted from row 4:")
        print("Column names:", list(result_df.columns))
        print("Data rows:")
        print(result_df)
    print()
    
    # Test Case 2: Out of bounds
    print("🔍 Test Case 2: Out of bounds row (row 10, index 9)")
    result_df, error = process_header_row(df.copy(), 9)
    if error:
        print(f"✅ Correctly caught error: {error}")
    else:
        print("❌ Should have failed!")
    print()
    
    # Test Case 3: Empty row (row 3, index 2)
    print("🔍 Test Case 3: Empty row (row 3, index 2)")
    result_df, error = process_header_row(df.copy(), 2)
    if error:
        print(f"✅ Correctly caught empty row: {error}")
    else:
        print("❌ Should have detected empty row!")
    print()
    
    # Test input validation
    print("🔍 Test Case 4: Input validation logic")
    
    def validate_input(user_input):
        """Test the input validation logic"""
        if not user_input.strip():
            return None, "Empty input - will use auto-detection"
        
        try:
            header_row_number = int(user_input.strip())
            if header_row_number < 1:
                return None, "❌ Row number must be 1 or greater."
            else:
                return header_row_number - 1, f"✅ Will use row {header_row_number} as headers"
        except ValueError:
            return None, "❌ Please enter a valid row number (e.g., 3)."
    
    test_inputs = ["4", "0", "-1", "abc", "  5  ", ""]
    for test_input in test_inputs:
        row_idx, message = validate_input(test_input)
        print(f"Input '{test_input}' -> {message}")
    
    print("\n🎉 All tests completed!")

if __name__ == "__main__":
    test_cell_reference_logic()
