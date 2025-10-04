# PDF Merger & Splitter (GUI Version)

# Import required libraries
import tkinter as tk  #for GUI
from tkinter import filedialog, messagebox  #for file dialogs & popup messages
from PyPDF2 import PdfMerger, PdfReader, PdfWriter  #for PDF operations

# Function to Merge two PDFs 
def merge_pdfs():
    file1 = filedialog.askopenfilename(  #ask user to select the first PDF file
        title="Select FIRST PDF file",        
        filetypes=[("PDF Files", "*.pdf")]    #only show PDF files
    )
    if not file1:  #if user cancels, stop function
        return


    file2 = filedialog.askopenfilename( #ask user to select the second PDF file
        title="Select SECOND PDF file",       
        filetypes=[("PDF Files", "*.pdf")]    
    )
    if not file2: 
        return
    

    merger = PdfMerger() #create PDF Merger object (from PyPDF2)
    merger.append(file1)  #add first selected PDF to the merger
    merger.append(file2) #add second selected PDF to merger

    save_path = filedialog.asksaveasfilename( #ask the user where to save the merged PDF
        defaultextension=".pdf",              #Save file with .pdf extension
        filetypes=[("PDF Files", "*.pdf")],   #Save as PDF only
        title="Save Merged PDF As"            #Title of the dialog box
    )

    if save_path: #if a save location is provided, save the merged PDF
        merger.write(save_path)  
        merger.close()            
        messagebox.showinfo("Success", f"Merged PDF saved as:\n{save_path}") #Show success popup with file location



#Function to split a PDF
def split_pdf():
    file = filedialog.askopenfilename(
        title="Select PDF to split",         
        filetypes=[("PDF Files", "*.pdf")]    
    )

    if not file:
        return

    reader = PdfReader(file) #Open the selected PDF file
    total_pages = len(reader.pages)  #count total pages in file

    #Create a small popup window to ask for start & end pages
    popup = tk.Toplevel(root)     
    popup.title("Split PDF")        
    popup.geometry("300x200")       

    tk.Label(popup, text=f"Total pages: {total_pages}", font=("Arial", 12)).pack(pady=5) #show total pages available

    #input for start page
    tk.Label(popup, text="Start page:").pack()
    start_entry = tk.Entry(popup)   #textbox where user can type
    start_entry.pack()

    #input for end page
    tk.Label(popup, text="End page:").pack()
    end_entry = tk.Entry(popup)     
    end_entry.pack()


    #Function that will actually splits the PDF
    def do_split():
        try:
            start = int(start_entry.get()) - 1 #convert typed values into numbers, to zero-based index 
            end = int(end_entry.get())

            if start < 0 or end > total_pages or start >= end: #check if values are valid
                raise ValueError

            writer = PdfWriter() #create a new PDF writer

            for i in range(start, end): #copy pages of given range into writer
                writer.add_page(reader.pages[i])

            save_path = filedialog.asksaveasfilename( #Ask user where to save the new split PDF
                defaultextension=".pdf",            
                filetypes=[("PDF Files", "*.pdf")], 
                title="Save Split PDF As"          
            )

            if save_path: #write the selected pages into the new file
                with open(save_path, "wb") as f:
                    writer.write(f)

                messagebox.showinfo("Success", f"Split PDF saved as:\n{save_path}") #show success message

            popup.destroy()  #close the popup window after splitting pdf pages

        except Exception: #show error if something goes wrong (invalid numbers, etc.)
            messagebox.showerror("Error", "Invalid page numbers!")

    tk.Button(popup, text="Split PDF", command=do_split).pack(pady=10)  #Button to run do_split()



#GUI Setup (Main Window)
root = tk.Tk()                       #create the main window
root.title("PDF Merger & Splitter")  #window title
root.geometry("400x200")             #window size (

tk.Label(root, text="PDF Tools", font=("Arial", 16, "bold")).pack(pady=10) #Title label

tk.Button(root, text="Merge PDFs", command=merge_pdfs, width=20, height=2).pack(pady=5) #Merge button

tk.Button(root, text="Split PDF", command=split_pdf, width=20, height=2).pack(pady=5) #split button

root.mainloop()  #Start the GUI event loop
