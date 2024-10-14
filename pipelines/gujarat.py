from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import requests
import os
import re

download_url = "https://wrd.guj.nic.in/dam/"
download_directory = "../files"

if not os.path.exists(download_directory):
    os.makedirs(download_directory)

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=chrome_options)
driver.get(download_url)

time.sleep(5)

table = driver.find_element(By.ID, "waterrelease")
first_tr = table.find_element(By.XPATH, ".//tbody/tr[1]")
a_tag = first_tr.find_element(By.TAG_NAME, "a")
href_value = a_tag.get_attribute("href")

print(href_value)

# Sanitize the file name
file_name = "gujarat_reservoir_report.pdf"

response = requests.get(href_value)

with open(os.path.join(download_directory, file_name), 'wb') as file:
    file.write(response.content)

driver.quit()
