from PyPDF2 import PdfReader, PdfWriter
import os

def split_pdf(input_path):
    """
    Read a PDF file and return a list of its pages.
    
    Args:
        input_path (str): Path to the input PDF file
    
    Returns:
        list: List of pages from the PDF
    """
    try:
        # Create a PDF reader object
        reader = PdfReader(input_path)
        pages = []
        
        # Extract each page and add to the list
        for page in reader.pages:
            pages.append(page)
            
        print(f"Successfully processed {len(pages)} pages from {os.path.basename(input_path)}")
        return pages
        
    except Exception as e:
        print(f"Error processing {input_path}: {str(e)}")
        return []

def merge_pdfs(input_files, output_dir):
    """
    Merge multiple PDF files into a single PDF.
    
    Args:
        input_files (list): List of paths to PDF files to merge
        output_dir (str): Directory where the merged PDF will be saved
    
    Returns:
        str: Path to the merged PDF file, or None if merge failed
    """
    try:
        # Create a PDF writer object
        writer = PdfWriter()
        
        # Add pages from each input file
        for pdf_file in input_files:
            reader = PdfReader(pdf_file)
            for page in reader.pages:
                writer.add_page(page)
        
        # Generate output filename
        output_filename = "merged_document.pdf"
        output_path = os.path.join(output_dir, output_filename)
        
        # Ensure unique filename
        counter = 1
        while os.path.exists(output_path):
            output_filename = f"merged_document_{counter}.pdf"
            output_path = os.path.join(output_dir, output_filename)
            counter += 1
        
        # Write the merged PDF to file
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        print(f"Successfully merged {len(input_files)} PDFs into {output_filename}")
        return output_path
        
    except Exception as e:
        print(f"Error merging PDFs: {str(e)}")
        return None

if __name__ == "__main__":
    # Get the directory path from user input
    directory_path = input("Please enter the directory path containing PDF files: ").strip()
    
    # Validate if directory exists
    if not os.path.isdir(directory_path):
        print(f"Error: Directory '{directory_path}' does not exist.")
        exit(1)
    
    # List to store all pages from all PDFs
    final_list = []
    
    # Scan directory for PDF files
    pdf_files = [f for f in os.listdir(directory_path) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print("No PDF files found in the specified directory.")
        exit(1)
    
    print(f"\nFound {len(pdf_files)} PDF files in the directory.")
    
    # Process each PDF file
    for pdf_file in pdf_files:
        full_path = os.path.join(directory_path, pdf_file)
        print(f"\nProcessing: {pdf_file}")
        
        # Get pages from current PDF and append to final list
        pages = split_pdf(full_path)
        final_list.extend(pages)
    
    # Print summary
    print(f"\nTotal pages from all PDFs: {final_list}") 
    print(f"\nTotal pages collected from all PDFs: {len(final_list)}") 