from dotenv import load_dotenv
import os
import PyPDF2

load_dotenv()

PDF_FOLDER = os.getenv('PDF_FOLDER')

for filename in os.listdir(PDF_FOLDER):
    if filename.endswith(".pdf"):
        pdf_file_obj = open(os.path.join(PDF_FOLDER, filename), 'rb')
        pdf_reader = PyPDF2.PdfReader(pdf_file_obj)
        content = ""
        for page in pdf_reader.pages:
            content += page.extract_text()
        print(content)  # print extracted text

        # Closing the PDF file object
        pdf_file_obj.close()
