import requests
from datetime import datetime, timedelta
import os

# Function to download PDF from dynamically generated URL
def download_pdf():
    # Calculate yesterday's date in "dd-mm-yyyy" format
    yesterday = datetime.now() - timedelta(days=1)
    formatted_date = yesterday.strftime("%d-%m-%Y")

    # Generate the dynamic URL for the PDF
    base_url = "https://wrd.maharashtra.gov.in/Upload/PDF/Today's-Storage-ReportEng-{}.pdf"
    pdf_url = base_url.format(formatted_date)

    # Make a request to download the PDF
    pdf_response = requests.get(pdf_url)

    pdf_filename = "../files/maharashtra_reservoir_report.pdf"
    
    if pdf_response.status_code == 200:
        with open(pdf_filename, 'wb') as pdf_file:
            pdf_file.write(pdf_response.content)
        print(f"PDF downloaded and saved as {pdf_filename}")
    else:
        print(f"Failed to download PDF for {formatted_date}, Status code: {pdf_response.status_code}")

if __name__ == "__main__":
    download_pdf()
