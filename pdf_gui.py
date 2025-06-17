import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from pdf_operations import split_pdf, merge_pdfs
from tkinterdnd2 import DND_FILES, TkinterDnD

class PDFApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Accutive Security PDF Merge Tool")
        self.root.geometry("600x400")
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure('TButton', padding=5)
        self.style.configure('TLabel', padding=5)
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Selection mode frame
        self.mode_frame = ttk.Frame(self.main_frame)
        self.mode_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.selection_mode = tk.StringVar(value="manual")
        self.manual_radio = ttk.Radiobutton(self.mode_frame, text="Browse Target Directory", 
                                          variable=self.selection_mode, value="manual",
                                          command=self.update_selection_mode)
        self.manual_radio.grid(row=0, column=0, padx=10)
        
        self.drag_radio = ttk.Radiobutton(self.mode_frame, text="Drag and Drop PDF Files", 
                                        variable=self.selection_mode, value="drag",
                                        command=self.update_selection_mode)
        self.drag_radio.grid(row=0, column=1, padx=10)
        
        # Directory selection
        self.dir_frame = ttk.LabelFrame(self.main_frame, text="Directory Selection", padding="5")
        self.dir_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.dir_path = tk.StringVar()
        self.dir_entry = ttk.Entry(self.dir_frame, textvariable=self.dir_path, width=50)
        self.dir_entry.grid(row=0, column=0, padx=5)
        
        self.browse_btn = ttk.Button(self.dir_frame, text="Browse", command=self.browse_directory)
        self.browse_btn.grid(row=0, column=1, padx=5)
        
        # Drop zone
        self.drop_frame = ttk.LabelFrame(self.main_frame, text="Drop PDF Files Here", padding="5")
        self.drop_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        self.drop_frame.grid_remove()  # Hide drop zone initially
        
        self.drop_label = ttk.Label(self.drop_frame, text="Drag and drop PDF files here")
        self.drop_label.grid(row=0, column=0, padx=20, pady=40)
        
        # Configure drop zone for drag and drop
        self.drop_frame.drop_target_register(DND_FILES)
        self.drop_frame.dnd_bind('<<Drop>>', self.handle_drop)
        
        # PDF List
        self.list_frame = ttk.LabelFrame(self.main_frame, text="PDF Files", padding="5")
        self.list_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.pdf_listbox = tk.Listbox(self.list_frame, height=8)
        self.pdf_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar for listbox
        scrollbar = ttk.Scrollbar(self.list_frame, orient=tk.VERTICAL, command=self.pdf_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.pdf_listbox['yscrollcommand'] = scrollbar.set
        
        # Buttons
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        self.process_btn = ttk.Button(self.button_frame, text="Process PDFs", command=self.process_pdfs)
        self.process_btn.grid(row=0, column=0, padx=5)
        
        self.merge_btn = ttk.Button(self.button_frame, text="Merge PDFs", command=self.merge_pdfs)
        self.merge_btn.grid(row=0, column=1, padx=5)
        
        self.clear_btn = ttk.Button(self.button_frame, text="Clear", command=self.clear_selection)
        self.clear_btn.grid(row=0, column=2, padx=5)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(self.main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        self.status_bar.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=2)
        self.main_frame.rowconfigure(2, weight=1)
        self.list_frame.columnconfigure(0, weight=1)
        self.list_frame.rowconfigure(0, weight=1)

    def handle_drop(self, event):
        """Handle dropped files"""
        files = self.root.tk.splitlist(event.data)
        pdf_files = []
        
        for file in files:
            # Remove curly braces if present (Windows file paths)
            file = file.strip('{}')
            if file.lower().endswith('.pdf'):
                pdf_files.append(file)
        
        if pdf_files:
            # Update directory path to the directory of the first PDF
            first_pdf_dir = os.path.dirname(pdf_files[0])
            self.dir_path.set(first_pdf_dir)
            
            # Clear and update the listbox
            self.pdf_listbox.delete(0, tk.END)
            for pdf in pdf_files:
                self.pdf_listbox.insert(tk.END, os.path.basename(pdf))
            
            self.status_var.set(f"Added {len(pdf_files)} PDF files")
        else:
            messagebox.showwarning("Warning", "No PDF files were dropped")

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.dir_path.set(directory)
            self.update_pdf_list()

    def update_pdf_list(self):
        self.pdf_listbox.delete(0, tk.END)
        directory = self.dir_path.get()
        if os.path.isdir(directory):
            pdf_files = [f for f in os.listdir(directory) if f.lower().endswith('.pdf')]
            for pdf in pdf_files:
                self.pdf_listbox.insert(tk.END, pdf)
            self.status_var.set(f"Found {len(pdf_files)} PDF files")

    def process_pdfs(self):
        directory = self.dir_path.get()
        if not os.path.isdir(directory):
            messagebox.showerror("Error", "Please select a valid directory")
            return
        
        self.status_var.set("Processing PDFs...")
        final_list = []
        
        for pdf_file in self.pdf_listbox.get(0, tk.END):
            full_path = os.path.join(directory, pdf_file)
            pages = split_pdf(full_path)
            final_list.extend(pages)
        
        self.status_var.set(f"Processed {len(final_list)} pages from all PDFs")
        messagebox.showinfo("Success", f"Successfully processed {len(final_list)} pages")

    def merge_pdfs(self):
        """Merge selected PDF files"""
        if self.pdf_listbox.size() == 0:
            messagebox.showwarning("Warning", "No PDF files to merge")
            return
        
        directory = self.dir_path.get()
        if not os.path.isdir(directory):
            messagebox.showerror("Error", "Please select a valid directory")
            return
        
        # Get full paths of all PDFs in the listbox
        pdf_files = [os.path.join(directory, pdf) for pdf in self.pdf_listbox.get(0, tk.END)]
        
        self.status_var.set("Merging PDFs...")
        
        # Merge the PDFs
        output_path = merge_pdfs(pdf_files, directory)
        
        if output_path:
            self.status_var.set(f"Successfully merged PDFs into {os.path.basename(output_path)}")
            messagebox.showinfo("Success", f"PDFs merged successfully!\nSaved as: {os.path.basename(output_path)}")
        else:
            self.status_var.set("Failed to merge PDFs")
            messagebox.showerror("Error", "Failed to merge PDFs")

    def update_selection_mode(self):
        """Update the visibility of directory and drop zone based on selection mode"""
        if self.selection_mode.get() == "manual":
            self.dir_frame.grid()
            self.drop_frame.grid_remove()
        else:
            self.dir_frame.grid_remove()
            self.drop_frame.grid()
            
        # Clear the current selection when switching modes
        self.clear_selection()

    def clear_selection(self):
        """Clear the directory path and PDF list"""
        self.dir_path.set("")
        self.pdf_listbox.delete(0, tk.END)
        self.status_var.set("Ready")

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = PDFApp(root)
    root.mainloop() 