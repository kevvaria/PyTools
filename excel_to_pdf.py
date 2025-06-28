import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf as pdf_backend
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import os
import sys
from pathlib import Path

def excel_to_pdf_matplotlib(excel_file_path, output_dir=None):
    """
    Convert Excel file to PDF using matplotlib (better for data visualization)
    
    Args:
        excel_file_path (str): Path to the Excel file
        output_dir (str): Directory to save PDF files (optional)
    
    Returns:
        list: List of created PDF file paths
    """
    if output_dir is None:
        output_dir = os.path.dirname(excel_file_path) or '.'
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Read all sheets from Excel file
    excel_file = pd.ExcelFile(excel_file_path)
    created_pdfs = []
    
    print(f"Processing Excel file: {os.path.basename(excel_file_path)}")
    print(f"Found {len(excel_file.sheet_names)} sheets: {excel_file.sheet_names}")
    
    for sheet_name in excel_file.sheet_names:
        try:
            # Read the sheet
            df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
            
            if df.empty:
                print(f"Sheet '{sheet_name}' is empty, skipping...")
                continue
            
            # Create figure and axis
            fig, ax = plt.subplots(figsize=(12, 8))
            ax.axis('tight')
            ax.axis('off')
            
            # Create table
            table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
            table.auto_set_font_size(False)
            table.set_fontsize(9)
            table.scale(1.2, 1.5)
            
            # Style the table
            for i in range(len(df.columns)):
                table[(0, i)].set_facecolor('#4CAF50')
                table[(0, i)].set_text_props(weight='bold', color='white')
            
            # Add title
            plt.title(f'Sheet: {sheet_name}', fontsize=16, fontweight='bold', pad=20)
            
            # Generate output filename
            safe_sheet_name = "".join(c for c in sheet_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            output_filename = f"{safe_sheet_name}.pdf"
            output_path = os.path.join(output_dir, output_filename)
            
            # Ensure unique filename
            counter = 1
            while os.path.exists(output_path):
                output_filename = f"{safe_sheet_name}_{counter}.pdf"
                output_path = os.path.join(output_dir, output_filename)
                counter += 1
            
            # Save as PDF
            plt.savefig(output_path, bbox_inches='tight', dpi=300)
            plt.close()
            
            created_pdfs.append(output_path)
            print(f"✓ Created PDF: {output_filename}")
            
        except Exception as e:
            print(f"✗ Error processing sheet '{sheet_name}': {str(e)}")
    
    return created_pdfs

def excel_to_pdf_reportlab(excel_file_path, output_dir=None):
    """
    Convert Excel file to PDF using ReportLab (better for text-heavy data)
    
    Args:
        excel_file_path (str): Path to the Excel file
        output_dir (str): Directory to save PDF files (optional)
    
    Returns:
        list: List of created PDF file paths
    """
    if output_dir is None:
        output_dir = os.path.dirname(excel_file_path) or '.'
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Read all sheets from Excel file
    excel_file = pd.ExcelFile(excel_file_path)
    created_pdfs = []
    
    print(f"Processing Excel file: {os.path.basename(excel_file_path)}")
    print(f"Found {len(excel_file.sheet_names)} sheets: {excel_file.sheet_names}")
    
    for sheet_name in excel_file.sheet_names:
        try:
            # Read the sheet
            df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
            
            if df.empty:
                print(f"Sheet '{sheet_name}' is empty, skipping...")
                continue
            
            # Generate output filename
            safe_sheet_name = "".join(c for c in sheet_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            output_filename = f"{safe_sheet_name}.pdf"
            output_path = os.path.join(output_dir, output_filename)
            
            # Ensure unique filename
            counter = 1
            while os.path.exists(output_path):
                output_filename = f"{safe_sheet_name}_{counter}.pdf"
                output_path = os.path.join(output_dir, output_filename)
                counter += 1
            
            # Create PDF document
            doc = SimpleDocTemplate(output_path, pagesize=A4)
            styles = getSampleStyleSheet()
            story = []
            
            # Add title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                spaceAfter=30,
                alignment=1  # Center alignment
            )
            title = Paragraph(f"Sheet: {sheet_name}", title_style)
            story.append(title)
            story.append(Spacer(1, 20))
            
            # Convert DataFrame to list of lists for table
            table_data = [df.columns.tolist()] + df.values.tolist()
            
            # Create table
            table = Table(table_data)
            
            # Style the table
            table_style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.green),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ])
            table.setStyle(table_style)
            
            story.append(table)
            
            # Build PDF
            doc.build(story)
            
            created_pdfs.append(output_path)
            print(f"✓ Created PDF: {output_filename}")
            
        except Exception as e:
            print(f"✗ Error processing sheet '{sheet_name}': {str(e)}")
    
    return created_pdfs

def main():
    """Main function to handle user input and process Excel files"""
    print("Excel to PDF Converter")
    print("=" * 50)
    
    # Get Excel file path
    if len(sys.argv) > 1:
        excel_file_path = sys.argv[1]
    else:
        excel_file_path = input("Enter the path to your Excel file: ").strip()
    
    # Validate file exists
    if not os.path.exists(excel_file_path):
        print(f"Error: File '{excel_file_path}' does not exist.")
        return
    
    if not excel_file_path.lower().endswith(('.xlsx', '.xls')):
        print("Error: Please provide a valid Excel file (.xlsx or .xls)")
        return
    
    # Get output directory
    output_dir = input("Enter output directory (press Enter for same directory as Excel file): ").strip()
    if not output_dir:
        output_dir = None
    
    # Choose conversion method
    print("\nChoose conversion method:")
    print("1. Matplotlib (better for data visualization)")
    print("2. ReportLab (better for text-heavy data)")
    
    choice = input("Enter your choice (1 or 2): ").strip()
    
    try:
        if choice == "1":
            created_pdfs = excel_to_pdf_matplotlib(excel_file_path, output_dir)
        elif choice == "2":
            created_pdfs = excel_to_pdf_reportlab(excel_file_path, output_dir)
        else:
            print("Invalid choice. Using Matplotlib as default.")
            created_pdfs = excel_to_pdf_matplotlib(excel_file_path, output_dir)
        
        print(f"\n✓ Successfully created {len(created_pdfs)} PDF files!")
        print("Created files:")
        for pdf_path in created_pdfs:
            print(f"  - {os.path.basename(pdf_path)}")
            
    except Exception as e:
        print(f"Error processing Excel file: {str(e)}")

if __name__ == "__main__":
    main() 