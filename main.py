#!/usr/bin/env python3
"""
PyTools - Main Menu Interface
A comprehensive tool for Excel to PDF conversion and PDF operations
"""

import os
import sys
import subprocess
from excel_to_pdf import excel_to_pdf_matplotlib, excel_to_pdf_reportlab
from pdf_operations import split_pdf, merge_pdfs
from example_usage import create_sample_excel

def print_banner():
    """Print the application banner"""
    print("\n" + "=" * 60)
    print("                    PyTools")
    print("         Excel & PDF Processing Suite")
    print("=" * 60)

def print_menu():
    """Print the main menu options"""
    print("\n📋 MAIN MENU")
    print("-" * 40)
    print("1.  Convert Excel to PDF (Matplotlib)")
    print("2.  Convert Excel to PDF (ReportLab)")
    print("3.  Split PDF into Pages")
    print("4.  Merge Multiple PDFs")
    print("5.  Launch PDF GUI Application")
    print("6.  Create Sample Excel File")
    print("7.  Run Example Usage")
    print("8.  Test Advanced Formatting")
    print("9.  View PDF Output Directory")
    print("0.  Exit")
    print("-" * 40)

def get_user_input(prompt):
    """Get user input with error handling"""
    try:
        return input(prompt).strip()
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)

def validate_file_path(file_path, file_type="file"):
    """Validate if a file or directory exists"""
    if not os.path.exists(file_path):
        print(f"❌ Error: {file_type.capitalize()} '{file_path}' does not exist.")
        return False
    return True

def convert_excel_to_pdf_matplotlib():
    """Handle Excel to PDF conversion using Matplotlib"""
    print("\n🔄 Excel to PDF Conversion (Matplotlib)")
    print("-" * 40)
    
    excel_file = get_user_input("Enter the path to your Excel file: ")
    if not validate_file_path(excel_file, "Excel file"):
        return
    
    output_dir = get_user_input("Enter output directory (press Enter for default): ").strip()
    if not output_dir:
        output_dir = "pdf_output"
    
    try:
        print(f"\nConverting {os.path.basename(excel_file)} to PDF...")
        created_pdfs = excel_to_pdf_matplotlib(excel_file, output_dir)
        
        if created_pdfs:
            print(f"\n✅ Successfully created {len(created_pdfs)} PDF file(s):")
            for pdf_path in created_pdfs:
                print(f"   📄 {os.path.basename(pdf_path)}")
        else:
            print("\n⚠️  No PDF files were created.")
            
    except Exception as e:
        print(f"❌ Error during conversion: {str(e)}")

def convert_excel_to_pdf_reportlab():
    """Handle Excel to PDF conversion using ReportLab"""
    print("\n🔄 Excel to PDF Conversion (ReportLab)")
    print("-" * 40)
    
    excel_file = get_user_input("Enter the path to your Excel file: ")
    if not validate_file_path(excel_file, "Excel file"):
        return
    
    output_dir = get_user_input("Enter output directory (press Enter for default): ").strip()
    if not output_dir:
        output_dir = "pdf_output"
    
    try:
        print(f"\nConverting {os.path.basename(excel_file)} to PDF...")
        created_pdfs = excel_to_pdf_reportlab(excel_file, output_dir)
        
        if created_pdfs:
            print(f"\n✅ Successfully created {len(created_pdfs)} PDF file(s):")
            for pdf_path in created_pdfs:
                print(f"   📄 {os.path.basename(pdf_path)}")
        else:
            print("\n⚠️  No PDF files were created.")
            
    except Exception as e:
        print(f"❌ Error during conversion: {str(e)}")

def split_pdf_operation():
    """Handle PDF splitting operation"""
    print("\n✂️  Split PDF into Pages")
    print("-" * 40)
    
    pdf_file = get_user_input("Enter the path to your PDF file: ")
    if not validate_file_path(pdf_file, "PDF file"):
        return
    
    try:
        print(f"\nProcessing {os.path.basename(pdf_file)}...")
        pages = split_pdf(pdf_file)
        
        if pages:
            print(f"✅ Successfully extracted {len(pages)} pages from {os.path.basename(pdf_file)}")
        else:
            print("⚠️  No pages were extracted.")
            
    except Exception as e:
        print(f"❌ Error during PDF splitting: {str(e)}")

def merge_pdfs_operation():
    """Handle PDF merging operation"""
    print("\n🔗 Merge Multiple PDFs")
    print("-" * 40)
    
    directory = get_user_input("Enter the directory path containing PDF files: ")
    if not validate_file_path(directory, "directory"):
        return
    
    # Find PDF files in the directory
    pdf_files = [f for f in os.listdir(directory) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print("❌ No PDF files found in the specified directory.")
        return
    
    print(f"\nFound {len(pdf_files)} PDF files:")
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"   {i}. {pdf_file}")
    
    try:
        # Get full paths of all PDF files
        full_paths = [os.path.join(directory, pdf) for pdf in pdf_files]
        
        print(f"\nMerging {len(full_paths)} PDF files...")
        output_path = merge_pdfs(full_paths, directory)
        
        if output_path:
            print(f"✅ Successfully merged PDFs into: {os.path.basename(output_path)}")
        else:
            print("❌ Failed to merge PDFs.")
            
    except Exception as e:
        print(f"❌ Error during PDF merging: {str(e)}")

def launch_pdf_gui():
    """Launch the PDF GUI application"""
    print("\n🖥️  Launching PDF GUI Application")
    print("-" * 40)
    
    try:
        # Check if tkinter is available
        import tkinter
        from pdf_gui import PDFApp
        from tkinterdnd2 import TkinterDnD
        
        print("Starting PDF GUI...")
        root = TkinterDnD.Tk()
        app = PDFApp(root)
        root.mainloop()
        
    except ImportError as e:
        print(f"❌ Error: Required GUI dependencies not found: {str(e)}")
        print("Please install tkinterdnd2: pip install tkinterdnd2")
    except Exception as e:
        print(f"❌ Error launching GUI: {str(e)}")

def create_sample_excel_file():
    """Create a sample Excel file for testing"""
    print("\n📊 Creating Sample Excel File")
    print("-" * 40)
    
    try:
        excel_file = create_sample_excel()
        print(f"✅ Successfully created sample Excel file: {excel_file}")
        print("This file contains sample data for Sales, Employee, and Inventory sheets.")
        
    except Exception as e:
        print(f"❌ Error creating sample Excel file: {str(e)}")

def run_example_usage():
    """Run the example usage script"""
    print("\n📖 Running Example Usage")
    print("-" * 40)
    
    try:
        # Import and run the example usage
        from example_usage import main as example_main
        example_main()
        
    except Exception as e:
        print(f"❌ Error running example usage: {str(e)}")

def test_advanced_formatting():
    """Test the advanced formatting functionality"""
    print("\n🎨 Testing Advanced Formatting")
    print("-" * 40)
    
    try:
        # Check if the advanced module exists
        from test_advanced_formatting import main as advanced_main
        advanced_main()
        
    except ImportError:
        print("❌ Advanced formatting module not found.")
        print("This feature requires additional dependencies.")
    except Exception as e:
        print(f"❌ Error testing advanced formatting: {str(e)}")

def view_pdf_output_directory():
    """View the contents of the PDF output directory"""
    print("\n📁 PDF Output Directory Contents")
    print("-" * 40)
    
    output_dir = "pdf_output"
    
    if not os.path.exists(output_dir):
        print(f"❌ Output directory '{output_dir}' does not exist.")
        return
    
    pdf_files = [f for f in os.listdir(output_dir) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print(f"No PDF files found in '{output_dir}' directory.")
        return
    
    print(f"Found {len(pdf_files)} PDF file(s) in '{output_dir}':")
    for i, pdf_file in enumerate(pdf_files, 1):
        file_path = os.path.join(output_dir, pdf_file)
        file_size = os.path.getsize(file_path)
        print(f"   {i}. {pdf_file} ({file_size:,} bytes)")

def main():
    """Main function with menu loop"""
    print_banner()
    
    while True:
        print_menu()
        
        try:
            choice = get_user_input("\nEnter your choice (0-9): ")
            
            if choice == "0":
                print("\n👋 Thank you for using PyTools!")
                print("Goodbye!")
                break
            elif choice == "1":
                convert_excel_to_pdf_matplotlib()
            elif choice == "2":
                convert_excel_to_pdf_reportlab()
            elif choice == "3":
                split_pdf_operation()
            elif choice == "4":
                merge_pdfs_operation()
            elif choice == "5":
                launch_pdf_gui()
            elif choice == "6":
                create_sample_excel_file()
            elif choice == "7":
                run_example_usage()
            elif choice == "8":
                test_advanced_formatting()
            elif choice == "9":
                view_pdf_output_directory()
            else:
                print("❌ Invalid choice! Please select a valid option (0-9).")
                
        except KeyboardInterrupt:
            print("\n\n👋 Thank you for using PyTools!")
            print("Goodbye!")
            break
        except Exception as e:
            print(f"❌ An unexpected error occurred: {str(e)}")
        
        # Pause before showing menu again
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main() 