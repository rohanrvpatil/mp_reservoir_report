import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import pandas as pd
from bs4 import BeautifulSoup
from openpyxl import Workbook
from openpyxl.styles import Font, Color, Alignment
from openpyxl.utils.dataframe import dataframe_to_rows

COLOR_MAP = {
    'red': 'FFFF0000',
    'blue': 'FF0000FF',
    'green': 'FF00FF00',
    # Add more colors as needed
}

def get_reservoir_water_level():
    url = 'http://eims1.mpwrd.gov.in/fcmreport/control/reservoirWaterLevel'
    
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-IN,en;q=0.9',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    }
    
    # Create a session with retry mechanism
    session = requests.Session()
    retry = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    
    # Disable SSL verification warnings
    requests.packages.urllib3.disable_warnings()
    
    # Make the request
    response = session.get(url, headers=headers, verify=False)
    response.raise_for_status()  # Raise an exception for bad status codes
    
    return response.text

def convert_html_to_excel(html_content):
    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the table
    table = soup.find('table')

    # Extract data and color information
    data = []
    for row in table.find_all('tr'):
        row_data = []
        for cell in row.find_all(['th', 'td']):
            value = cell.get_text(strip=True)
            color = None
            font_tag = cell.find('font', color=True)
            if font_tag:
                color = font_tag['color']
            colspan = int(cell.get('colspan', 1))
            rowspan = int(cell.get('rowspan', 1))
            row_data.append((value, color, colspan, rowspan))
        data.append(row_data)

    # Process data to handle colspans, rowspans, and create a structured dataset
    max_cols = max(sum(colspan for _, _, colspan, _ in row) for row in data)
    processed_data = [[('', None) for _ in range(max_cols)] for _ in range(len(data))]

    for i, row in enumerate(data):
        col = 0
        for value, color, colspan, rowspan in row:
            while col < max_cols and processed_data[i][col][0]:
                col += 1
            for r in range(rowspan):
                for c in range(colspan):
                    if i + r < len(processed_data) and col + c < max_cols:
                        processed_data[i + r][col + c] = (value, color)
            col += colspan

    # Create a DataFrame
    df = pd.DataFrame(processed_data)

    # Create a new workbook and select the active sheet
    wb = Workbook()
    ws = wb.active

    # Write data to the worksheet with color formatting
    for r_idx, row in enumerate(processed_data, 1):
        for c_idx, (value, color) in enumerate(row, 1):
            cell = ws.cell(row=r_idx, column=c_idx, value=value)
            if color:
                hex_color = COLOR_MAP.get(color.lower(), 'FF000000')  # Default to black if color not found
                cell.font = Font(color=hex_color)

    # Save the workbook
    wb.save('output_colored.xlsx')

def main():
    try:
        # Fetch HTML content
        html_content = get_reservoir_water_level()
        
        # Save HTML content (optional, for debugging)
        with open('response.html', 'w', encoding='utf-8') as html_file:
            html_file.write(html_content)
        
        print("HTML content has been saved to response.html")
        
        # Convert HTML to Excel
        convert_html_to_excel(html_content)
        
        print("Excel file with colored text has been created: output_colored.xlsx")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()