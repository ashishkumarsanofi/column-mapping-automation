# 📊 Advanced Column Mapping & Transformation Tool
## Complete Architecture & Flow Guide

**Document Version:** 1.0  
**Date:** June 4, 2025  
**Author:** Technical Documentation  

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [File Structure & Responsibilities](#file-structure--responsibilities)
3. [Application Flow Sequence](#application-flow-sequence)
4. [Inter-Module Dependencies](#inter-module-dependencies)
5. [Key Processing Points](#key-processing-points)
6. [User Journey Flow](#user-journey-flow)
7. [Technical Details](#technical-details)
8. [Enhanced Features](#enhanced-features)

---

## Executive Summary

The Advanced Column Mapping & Transformation Tool is a Streamlit-based web application designed to help users map, transform, and consolidate data from multiple input files into a single output file. The tool provides an intuitive interface for managing column mappings, applying filters, handling static values, and formatting data with enhanced mapping file support for configuration reusability.

**Key Capabilities:**
- Multi-file data consolidation
- Dynamic column mapping
- Advanced filtering capabilities
- Static value assignment
- Date formatting controls
- Enhanced mapping file format with backward compatibility
- Real-time error validation
- Multiple export formats (Excel, TXT, CSV)

---

## File Structure & Responsibilities

### 1. `app.py` - Main Orchestrator (Entry Point)
**Primary Role:** Central controller that coordinates the entire application workflow

**Key Responsibilities:**
- **Application Configuration:** Sets up Streamlit page configuration, layout, and styling
- **File Upload Management:** Handles file uploads for input files, output templates, and mapping configurations
- **Sheet Selection Logic:** Manages Excel sheet selection for multi-sheet workbooks
- **Mapping File Validation:** Validates and processes both basic and enhanced mapping file formats
- **Workflow Coordination:** Orchestrates the complete data processing pipeline by calling functions from specialized modules
- **Enhanced Features Support:** Detects and enables advanced mapping capabilities when enhanced mapping files are provided

**Key Code Sections:**
```python
# Configuration and Setup
st.set_page_config(page_title="📊 Column Mapping Tool", layout="wide")

# File Upload Processing
input_files, output_file, mapping_file = show_upload_section(SANOFI_COLORS)

# Enhanced Mapping File Detection
if has_extended_cols:
    st.info("📋 Enhanced mapping file detected with additional configuration options!")
```

### 2. `ui_sections.py` - User Interface Components
**Primary Role:** Provides reusable UI components for clean code separation

**Key Responsibilities:**
- **File Upload Interface:** Creates the file upload section with proper styling and validation
- **User Guide Display:** Renders comprehensive help documentation with examples
- **Footer Management:** Displays application footer and branding
- **UI Consistency:** Ensures consistent styling and user experience across components

**Key Functions:**
- `show_upload_section()`: File upload interface with support for multiple file types
- `show_guide()`: Expandable user guide with detailed examples of basic and enhanced mapping formats
- `show_footer()`: Application footer with author information

### 3. `file_utils.py` - File Operations & Utilities
**Primary Role:** Handles all file reading and data validation operations

**Key Responsibilities:**
- **File Reading:** Efficiently reads CSV and Excel files with optimized performance
- **Data Validation:** Handles file format validation and error reporting
- **Column Management:** Ensures required columns exist in DataFrames
- **Error Handling:** Provides comprehensive error reporting for file-related issues

**Key Functions:**
```python
def read_file(file):
    """Efficiently read CSV or Excel file with proper error handling"""
    
def fill_missing_columns(df, required_cols):
    """Ensures all required columns exist in DataFrame"""
```

### 4. `mapping_logic.py` - Core Business Logic Engine
**Primary Role:** The heart of the application - contains all mapping and processing logic

**Key Responsibilities:**
- **Mapping Interface Creation:** Builds dynamic tabbed interface for each input file/sheet
- **Enhanced Mapping Support:** Processes and applies enhanced mapping configurations
- **Data Processing:** Handles filtering, static value assignment, and date formatting
- **Output Generation:** Creates final consolidated output with multiple export options
- **Configuration Export:** Exports current mapping configurations for reuse
- **Real-time Validation:** Provides immediate feedback on mapping errors

**Core Functions:**
- `process_mapping_tabs()`: Creates the main mapping interface
- `process_final_output()`: Generates final consolidated output
- `deduplicate_columns()`: Handles duplicate column name resolution

### 5. `requirements.txt` - Dependency Management
**Primary Role:** Defines required Python packages for the application

**Dependencies:**
- `streamlit`: Web application framework
- `pandas`: Data manipulation and analysis
- `openpyxl`: Excel file handling and creation

---

## Application Flow Sequence

### Phase 1: Initialization & Setup
```
1. Application Startup (app.py)
   ├── Import all required dependencies
   │   ├── streamlit (web framework)
   │   ├── pandas (data processing)
   │   ├── Custom modules (ui_sections, file_utils, mapping_logic)
   │   └── Standard libraries (os, io, warnings, time)
   ├── Configure Streamlit application
   │   ├── Set page title and layout
   │   ├── Define color schemes and CSS styling
   │   └── Set maximum upload size limits
   └── Display application header and introduction
```

### Phase 2: File Upload & Validation
```
2. File Upload Process (ui_sections.py → app.py)
   ├── Display upload interface via show_upload_section()
   │   ├── Input files uploader (accepts multiple CSV/Excel files)
   │   ├── Output template uploader (single CSV/Excel file)
   │   └── Optional mapping file uploader (CSV/Excel with mapping config)
   ├── Validate uploaded files
   │   ├── Check file formats and extensions
   │   ├── Verify file accessibility and readability
   │   └── Report any upload errors to user
   └── Store file objects for processing

3. Sheet Selection Logic (app.py)
   ├── Process Excel files to extract sheet information
   │   ├── Use pandas.ExcelFile to read sheet names
   │   ├── Display multiselect widget for each Excel file
   │   ├── Allow users to select specific sheets for processing
   │   └── Create file/sheet combinations for mapping
   ├── Handle CSV files (no sheet selection needed)
   └── Build input_file_sheets list with all file/sheet combinations
```

### Phase 3: Mapping File Processing & Enhancement Detection
```
4. Mapping File Analysis (app.py)
   ├── Read and validate mapping file structure
   │   ├── Use file_utils.read_file() for file reading
   │   ├── Check for required basic columns:
   │   │   ├── FileName (input file identifier)
   │   │   ├── SheetName (sheet identifier for Excel)
   │   │   ├── OutputColumn (target column name)
   │   │   └── InputColumn (source column name)
   │   └── Validate column presence and data integrity
   ├── Enhanced Feature Detection
   │   ├── Check for optional enhanced columns:
   │   │   ├── StaticValue (fixed values for columns)
   │   │   ├── FilterValues (comma-separated filter criteria)
   │   │   ├── DateFormatFlag (date formatting preferences)
   │   │   └── IncludeFlag (column inclusion/exclusion)
   │   ├── Add missing columns with defaults for backward compatibility
   │   └── Notify user when enhanced features are detected
   └── Set mapping_file_valid flag for downstream processing
```

### Phase 4: Core Mapping Interface Generation
```
5. Dynamic Mapping Interface Creation (mapping_logic.py)
   ├── process_mapping_tabs() orchestrates the complete mapping process
   ├── For each input file/sheet combination:
   │   ├── Create dedicated tab in Streamlit interface
   │   ├── Read and process input data
   │   │   ├── Use cached reading for performance optimization
   │   │   ├── Handle column header detection and row offset
   │   │   ├── Strip whitespace and deduplicate column names
   │   │   └── Build column occurrence mapping for deduplication
   │   ├── Parse enhanced mapping configuration
   │   │   ├── Extract mapping dictionaries from mapping file
   │   │   ├── Process static values, filters, and formatting flags
   │   │   ├── Handle boolean conversions for flag fields
   │   │   └── Apply file/sheet-specific mappings
   │   └── Build comprehensive mapping interface
   │       ├── Include/Exclude checkboxes with master select/deselect
   │       ├── Output column display with clear labeling
   │       ├── Input column mapping dropdowns with validation
   │       ├── Static value text inputs with default values
   │       ├── Dynamic filter multiselects (when applicable)
   │       └── Date formatting checkboxes (context-aware)
   └── Return final_dataframes with all mapping configurations
```

### Phase 5: Data Processing & Output Generation
```
6. Final Output Processing (mapping_logic.py)
   ├── process_final_output() handles final data consolidation
   ├── Data Processing Loop
   │   ├── For each mapped file/sheet:
   │   │   ├── Apply user-selected filters to input data
   │   │   ├── Create output DataFrame with proper structure
   │   │   ├── Process column mappings with comprehensive logic:
   │   │   │   ├── Static values → Fill with specified static value
   │   │   │   ├── Column mappings → Copy data from input columns
   │   │   │   ├── Blank mappings → Fill with empty strings
   │   │   │   └── Validation errors → Report missing mappings
   │   │   ├── Apply date formatting when enabled
   │   │   └── Validate all mappings for completeness
   │   └── Combine all processed DataFrames into final result
   ├── Error Handling and Validation
   │   ├── Collect and display all mapping errors
   │   ├── Prevent output generation if errors exist
   │   └── Provide actionable error messages to users
   └── Multi-Format Export Generation
       ├── Excel file creation with formatted output
       ├── TXT file generation (pipe-separated format)
       └── Enhanced mapping configuration export for reuse
```

---

## Inter-Module Dependencies

### Import Hierarchy
```
app.py (Main Entry Point)
├── Imports from file_utils
│   ├── read_file() - File reading functionality
│   └── fill_missing_columns() - Data validation
├── Imports from ui_sections
│   ├── show_upload_section() - File upload interface
│   ├── show_footer() - Application footer
│   └── show_guide() - User documentation
└── Imports from mapping_logic
    ├── process_mapping_tabs() - Main mapping interface
    └── process_final_output() - Output generation

mapping_logic.py (Core Logic)
├── Imports from file_utils
│   ├── read_file() - Cached file reading
│   └── fill_missing_columns() - Column validation
└── Uses streamlit for all UI components

ui_sections.py (UI Components)
└── Uses streamlit for interface creation

file_utils.py (Utilities)
├── Uses pandas for data operations
└── Uses streamlit for error reporting
```

### Data Flow Pipeline
```
Input Files → file_utils.read_file() → Raw DataFrames
    ↓
Output Template → file_utils.read_file() → Output Column Structure
    ↓
Enhanced Mapping File → app.py validation → Configuration Dictionaries
    ↓
Combined Data → mapping_logic.process_mapping_tabs() → User Mapping Interface
    ↓
User Configurations → mapping_logic.process_final_output() → Final Consolidated Output
    ↓
Export Options → Multiple formats (Excel, TXT, Enhanced Mapping CSV)
```

---

## Key Processing Points

### 1. Enhanced Mapping File Support
**Backward Compatibility Implementation:**
- Automatically detects mapping file format (basic vs enhanced)
- Adds missing enhanced columns with appropriate defaults
- Maintains full compatibility with existing basic mapping files
- Provides clear user feedback when enhanced features are available

**Enhanced Features:**
- **Static Values:** Assign fixed values to output columns
- **Filter Values:** Apply comma-separated filter criteria to input data
- **Date Format Flags:** Control date formatting on a per-column basis
- **Include Flags:** Control column inclusion/exclusion in output

### 2. Dynamic User Interface Generation
**Adaptive Interface:**
- Creates tabs dynamically based on uploaded files and selected sheets
- Generates mapping controls contextually based on data types
- Provides real-time validation with immediate error feedback
- Implements master select/deselect functionality for efficient column management

**Performance Optimization:**
- Uses Streamlit caching for file reading operations
- Implements efficient DataFrame operations
- Minimizes unnecessary UI redraws
- Optimizes Excel reading with selective column loading

### 3. Advanced Data Processing Capabilities
**Multi-file Consolidation:**
- Combines data from multiple input sources seamlessly
- Handles different file formats (CSV and Excel) uniformly
- Manages sheet-specific processing for Excel workbooks
- Maintains data integrity throughout the consolidation process

**Intelligent Error Handling:**
- Comprehensive validation of all mapping configurations
- Clear, actionable error messages with HTML formatting
- Prevention of output generation when errors exist
- Real-time feedback during user interaction

### 4. Export and Configuration Management
**Multiple Export Formats:**
- **Excel Output:** Professional formatting with proper data types
- **TXT Output:** Pipe-separated format for legacy system compatibility
- **Enhanced Mapping Export:** Complete configuration preservation for reuse

**Configuration Reusability:**
- Exports current mapping state including all enhanced features
- Enables teams to share complex mapping configurations
- Supports iterative refinement of data transformation processes
- Provides documentation trail for data processing workflows

---

## User Journey Flow

### Complete User Workflow
```
1. Application Access
   ├── User navigates to Streamlit application
   ├── Application loads with styled interface
   └── User guide expander available for reference

2. File Preparation and Upload
   ├── User prepares input files (CSV/Excel with source data)
   ├── User creates or obtains output template (defines target structure)
   ├── User optionally prepares enhanced mapping file (for automation)
   └── User uploads files through intuitive interface

3. Configuration and Mapping
   ├── User selects relevant Excel sheets (if applicable)
   ├── User reviews and configures mapping for each file/sheet:
   │   ├── Toggles column inclusion/exclusion
   │   ├── Maps input columns to output columns
   │   ├── Assigns static values where needed
   │   ├── Applies filters to input data
   │   └── Configures date formatting preferences
   └── User receives real-time validation feedback

4. Output Generation and Export
   ├── User clicks "Generate Final Output" button
   ├── Application processes all configurations and data
   ├── User receives immediate feedback on any errors
   ├── Upon successful processing, user can download:
   │   ├── Final consolidated Excel file
   │   ├── TXT file for legacy systems
   │   └── Enhanced mapping configuration for reuse
   └── User can iterate and refine mappings as needed
```

### Error Handling and User Support
- **Proactive Validation:** Real-time checking prevents common errors
- **Clear Error Messages:** HTML-formatted messages with specific guidance
- **User Guide Integration:** Comprehensive help available within the application
- **Example-Driven Documentation:** Practical examples of both basic and enhanced mapping formats

---

## Technical Details

### Performance Optimizations
- **Streamlit Caching:** File reading operations cached for faster subsequent access
- **Efficient DataFrame Operations:** Optimized pandas operations for large datasets
- **Selective Column Loading:** Excel reading optimized to load only necessary columns
- **Memory Management:** Careful handling of large datasets to prevent memory issues

### Security Considerations
- **File Type Validation:** Strict validation of uploaded file types
- **Size Limitations:** Configurable upload size limits to prevent abuse
- **Error Containment:** Comprehensive exception handling prevents application crashes
- **Data Sanitization:** Proper handling of user input and file content

### Scalability Features
- **Modular Architecture:** Clean separation of concerns enables easy maintenance
- **Extensible Design:** New features can be added without disrupting existing functionality
- **Configuration-Driven:** Behavior controlled through configuration rather than hard-coding
- **Cache Management:** Intelligent caching prevents memory bloat during long sessions

---

## Enhanced Features

### Advanced Mapping Capabilities
The application now supports sophisticated mapping configurations that go beyond simple column-to-column mapping:

**Static Value Assignment:**
- Assign fixed values to output columns regardless of input data
- Useful for adding metadata, status indicators, or constant values
- Supports both manual entry and configuration file specification

**Dynamic Filtering:**
- Apply filters to input data before mapping
- Support for multiple filter values per column
- Comma-separated filter specification in mapping files
- Real-time filter application with immediate preview

**Intelligent Date Formatting:**
- Context-aware date format detection
- User-controlled date formatting with yyyy-mm-dd output
- Per-column date formatting control
- Automatic date detection with manual override capability

**Column Management:**
- Include/exclude flags for fine-grained output control
- Master select/deselect for efficient bulk operations
- Configuration persistence through enhanced mapping files
- Support for complex column transformation workflows

### Configuration Management
**Enhanced Mapping File Format:**
- Backward compatible with existing basic mapping files
- Extended with optional columns for advanced features
- Comprehensive configuration export including all user settings
- Team collaboration support through shareable configuration files

**Example Enhanced Mapping Configuration:**
```csv
FileName,SheetName,OutputColumn,InputColumn,StaticValue,FilterValues,DateFormatFlag,IncludeFlag
data.xlsx,Sheet1,CustomerName,Full_Name,,,False,True
data.xlsx,Sheet1,Status,,Active,,False,True
data.xlsx,Sheet1,ProcessDate,Order_Date,,,True,True
data.xlsx,Sheet1,Category,Product_Type,,Premium,Standard,False,True
```

This architecture provides a robust, scalable, and user-friendly solution for complex data mapping and transformation tasks while maintaining simplicity for basic use cases.

---

**Document End**

*This document provides a comprehensive technical overview of the Advanced Column Mapping & Transformation Tool architecture. For additional technical details or specific implementation questions, refer to the source code documentation within each module.*
