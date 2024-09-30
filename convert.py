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

# Load your HTML content
with open('response.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

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

print("Excel file with colored text has been created: output_colored.xlsx")