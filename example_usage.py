#!/usr/bin/env python3
"""
Example usage of the Excel to PDF converter
This script creates a sample Excel file and then converts it to PDFs
"""

import pandas as pd
import os
from excel_to_pdf import excel_to_pdf_matplotlib, excel_to_pdf_reportlab

def create_sample_excel():
    """Create a sample Excel file with multiple sheets for testing"""
    
    # Create sample data for different sheets
    sales_data = {
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'Revenue': [10000, 12000, 15000, 14000, 16000, 18000],
        'Expenses': [8000, 9000, 11000, 10000, 12000, 13000],
        'Profit': [2000, 3000, 4000, 4000, 4000, 5000]
    }
    
    employee_data = {
        'Name': ['John Doe', 'Jane Smith', 'Bob Johnson', 'Alice Brown', 'Charlie Wilson'],
        'Department': ['Sales', 'Marketing', 'IT', 'HR', 'Finance'],
        'Salary': [50000, 55000, 60000, 45000, 65000],
        'Years_Experience': [3, 5, 7, 2, 8]
    }
    
    inventory_data = {
        'Product': ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headphones'],
        'Quantity': [50, 200, 150, 30, 100],
        'Price': [800, 25, 50, 300, 80],
        'Total_Value': [40000, 5000, 7500, 9000, 8000]
    }
    
    # Create DataFrames
    df_sales = pd.DataFrame(sales_data)
    df_employees = pd.DataFrame(employee_data)
    df_inventory = pd.DataFrame(inventory_data)
    
    # Create Excel file with multiple sheets
    excel_filename = 'sample_data.xlsx'
    
    with pd.ExcelWriter(excel_filename, engine='openpyxl') as writer:
        df_sales.to_excel(writer, sheet_name='Sales_Data', index=False)
        df_employees.to_excel(writer, sheet_name='Employee_Data', index=False)
        df_inventory.to_excel(writer, sheet_name='Inventory_Data', index=False)
    
    print(f"✓ Created sample Excel file: {excel_filename}")
    return excel_filename

def main():
    """Main function to demonstrate the Excel to PDF conversion"""
    print("Excel to PDF Converter - Example Usage")
    print("=" * 50)
    
    # Create sample Excel file
    excel_file = create_sample_excel()
    
    # Create output directory
    output_dir = 'pdf_output'
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\nConverting Excel file to PDFs...")
    print(f"Output directory: {output_dir}")
    
    # Convert using matplotlib method
    print("\n1. Converting using Matplotlib method:")
    matplotlib_pdfs = excel_to_pdf_matplotlib(excel_file, output_dir)
    
    # Convert using ReportLab method
    print("\n2. Converting using ReportLab method:")
    reportlab_pdfs = excel_to_pdf_reportlab(excel_file, output_dir)
    
    print(f"\n✓ Conversion complete!")
    print(f"Matplotlib PDFs created: {len(matplotlib_pdfs)}")
    print(f"ReportLab PDFs created: {len(reportlab_pdfs)}")
    
    print(f"\nAll PDF files have been saved to the '{output_dir}' directory.")
    print("You can now open and view the generated PDF files.")

if __name__ == "__main__":
    main() 