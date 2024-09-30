import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

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

def main():
    try:
        html_content = get_reservoir_water_level()
        
        with open('response.html', 'w', encoding='utf-8') as html_file:
            html_file.write(html_content)
        
        print("HTML content has been saved to response.html")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()