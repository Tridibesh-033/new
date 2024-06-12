import fitz  # PyMuPDF
import os
import pytesseract as tess
from PIL import Image

# Set Tesseract path
tess.pytesseract.tesseract_cmd = r'C:\Users\User\AppData\Local\Programs\Tesseract-OCR\tesseract'

def parse_pdf_with_images(pdf_path, output_folder):
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    
    # Loop through each page
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        
        # Extract text blocks
        text_blocks = page.get_text("blocks")
        
        # Extract images
        image_list = page.get_images(full=True)
        
        # Extract and save images
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            
            # Save the image
            image_filename = f"{output_folder}/page_{page_num+1}_img_{img_index+1}.{image_ext}"
            with open(image_filename, "wb") as img_file:
                img_file.write(image_bytes)
            print(f"Saved image {image_filename}")

            # Perform OCR on the extracted image
            img_path = image_filename
            img = Image.open(img_path)
            text = tess.image_to_string(img)
            
            # Save OCR text to a file
            with open(f"{output_folder}/page_{page_num+1}_img_{img_index+1}_text.txt", "w", encoding="utf-8") as text_file:
                text_file.write(text)
            print(f"Saved OCR text from {image_filename}")

            # Remove the text file
            text_filename = f"{output_folder}/page_{page_num+1}_text.txt"
            if os.path.exists(text_filename):
                os.remove(text_filename)

# Example usage
pdf_path = 'cheque.pdf'  # Path to your PDF file
output_folder = 'D:\infosys_spring\project_python\Automating-Bank-Check-Extraction-from-Scanned-PDFs_May_2024'  # Folder to save parsed content
parse_pdf_with_images(pdf_path, output_folder)
