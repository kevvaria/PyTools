# PyTools
Python Methods for performing PDF modifications and Excel to PDF conversions

## Features

### Excel to PDF Converter
Convert Excel files (.xlsx, .xls) to individual PDF files for each sheet.

#### Installation
```bash
pip install -r requirements.txt
```

#### Usage

**Command Line Usage:**
```bash
python excel_to_pdf.py [excel_file_path]
```

**Interactive Usage:**
```bash
python excel_to_pdf.py
# Then follow the prompts to enter file path and options
```

**Programmatic Usage:**
```python
from excel_to_pdf import excel_to_pdf_matplotlib, excel_to_pdf_reportlab

# Convert using matplotlib (better for data visualization)
pdfs = excel_to_pdf_matplotlib('your_file.xlsx', 'output_directory')

# Convert using ReportLab (better for text-heavy data)
pdfs = excel_to_pdf_reportlab('your_file.xlsx', 'output_directory')
```

#### Example
Run the example script to see the converter in action:
```bash
python example_usage.py
```

This will:
1. Create a sample Excel file with multiple sheets
2. Convert each sheet to individual PDF files
3. Save the PDFs in a `pdf_output` directory

#### Conversion Methods

1. **Matplotlib Method** (`excel_to_pdf_matplotlib`)
   - Better for data visualization
   - Creates visually appealing tables with styling
   - Good for charts and formatted data

2. **ReportLab Method** (`excel_to_pdf_reportlab`)
   - Better for text-heavy data
   - More control over formatting
   - Professional document layout

#### Features
- ✅ Supports multiple Excel sheets
- ✅ Automatic sheet name sanitization for filenames
- ✅ Duplicate filename handling
- ✅ Error handling for empty sheets
- ✅ Customizable output directory
- ✅ Progress feedback during conversion
- ✅ Two different conversion methods

### PDF Operations
Existing PDF manipulation tools for splitting and merging PDF files.

#### Usage
```bash
python pdf_operations.py
```

## Dependencies
- pandas >= 1.5.0
- matplotlib >= 3.5.0
- reportlab >= 3.6.0
- openpyxl >= 3.0.0
- xlrd >= 2.0.0
- PyPDF2 (for PDF operations)

## File Structure
```
PyTools/
├── excel_to_pdf.py      # Main Excel to PDF converter
├── example_usage.py     # Example script with sample data
├── pdf_operations.py    # PDF manipulation tools
├── pdf_gui.py          # GUI for PDF operations
├── requirements.txt    # Python dependencies
└── README.md          # This file
```
