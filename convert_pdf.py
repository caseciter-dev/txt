import os
import requests
from pypdf import PdfReader
from datetime import datetime
import pytz

# Configuration
PDF_URL = "https://cdn.sci-notifier.codechips.in/orders/latest.pdf"
OUTPUT_DIR = "archive"

def download_and_convert():
    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Get current date in IST
    ist = pytz.timezone('Asia/Kolkata')
    current_date = datetime.now(ist).strftime('%Y-%m-%d')
    md_filename = os.path.join(OUTPUT_DIR, f"{current_date}.md")
    
    print(def_msg := f"Fetching PDF for {current_date}...")
    
    try:
        # Download PDF
        response = requests.get(PDF_URL, timeout=30)
        response.raise_for_status()
        
        # Save temporary PDF to parse
        temp_pdf = "temp.pdf"
        with open(temp_pdf, "wb") as f:
            f.write(response.content)
            
        # Extract text
        reader = PdfReader(temp_pdf)
        text_content = []
        
        for i, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text:
                text_content.append(f"## Page {i+1}\n\n{page_text}\n")
                
        # Clean up temp file
        os.remove(temp_pdf)
        
        # Write to Markdown
        with open(md_filename, "w", encoding="utf-8") as md_file:
            md_file.write(f"# Document Log — {current_date}\n\n")
            md_file.write("\n".join(text_content))
            
        print(f"Successfully saved: {md_filename}")
        
    except Exception as e:
        print(f"Error processing PDF: {e}")

if __name__ == "__main__":
    download_and_convert()
