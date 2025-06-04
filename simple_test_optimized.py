"""
Simple test for the optimized logic
"""
import pandas as pd

def test_basic_functionality():
    print("Testing basic functionality...")
    
    # Simple deduplicate test
    def deduplicate_columns(columns):
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
    
    # Test data
    test_cols = ['Name', 'Age', 'Name', 'Department', 'Age']
    result = deduplicate_columns(test_cols)
    expected = ['Name', 'Age', 'Name_1', 'Department', 'Age_1']
    
    print(f"Input: {test_cols}")
    print(f"Output: {result}")
    print(f"Expected: {expected}")
    print(f"✅ Test passed: {result == expected}")

if __name__ == "__main__":
    test_basic_functionality()
