#!/usr/bin/env python3
"""
Test script for the advanced Excel to PDF converter with formatting preservation
"""

from excel_to_pdf_advanced import create_sample_excel_with_formatting, excel_to_pdf_advanced
import os

def main():
    """Test the advanced Excel to PDF converter"""
    print("Advanced Excel to PDF Converter - Format Preservation Test")
    print("=" * 60)
    
    # Create sample Excel file with rich formatting
    print("\n1. Creating sample Excel file with formatting...")
    excel_file = create_sample_excel_with_formatting()
    
    # Create output directory
    output_dir = 'advanced_pdf_output'
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\n2. Converting Excel file to PDF with preserved formatting...")
    print(f"Output directory: {output_dir}")
    
    # Convert using advanced formatting
    created_pdfs = excel_to_pdf_advanced(excel_file, output_dir)
    
    print(f"\n✓ Conversion complete!")
    print(f"PDFs created: {len(created_pdfs)}")
    
    if created_pdfs:
        print("\nCreated files:")
        for pdf_path in created_pdfs:
            print(f"  - {os.path.basename(pdf_path)}")
        
        print(f"\nAll PDF files have been saved to the '{output_dir}' directory.")
        print("The PDFs should preserve:")
        print("  ✓ Cell colors and backgrounds")
        print("  ✓ Text colors and formatting")
        print("  ✓ Number formats (currency, percentages, dates)")
        print("  ✓ Bold and italic text")
        print("  ✓ Cell borders and alignment")
    else:
        print("\n⚠️  No PDFs were created. Check the error messages above.")

if __name__ == "__main__":
    main() 