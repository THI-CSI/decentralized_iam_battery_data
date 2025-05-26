import http, requests
import time
from requests import Timeout, RequestException

# Hardcoded API URLs
CLOUD_API_URL = 'http://127.0.0.1:8000/batterypass/'
BLOCKCHAIN_API_URL = 'http://localhost:8080/api/dids/'

def get_data(did):
    params=None
    retries = 0
    # Send the GET request
    while retries < 3:
        try:
            response = requests.get(BLOCKCHAIN_API_URL + did, params=params)

            if response.status_code == 200:
                print(f'Success:', response.json())
                return response.json()  # Return the JSON response
            elif 400 <= response.status_code < 500:
                print(f'Client error ({response.status_code}):', response.text)
                return None  # No retry for 4XX errors
            elif 500 <= response.status_code < 600:
                print(f'Server error ({response.status_code}), retrying...')
            else:
                print(f'Error:', response.status_code, response.text)

        except Timeout:
            print(f'Request timed out, retrying...')
        except RequestException as e:
            print(f'Request failed: {e}, retrying...')

        retries += 1
        if retries < 3:
            time.sleep(3)  # Wait before retrying

    print(f'Max retries exceeded')
    return None  # Max retries exceeded

def post_data(data):
    retries = 0
    # Send the POST request with JSON data
    while retries < 3:
        try:
            response = requests.post(CLOUD_API_URL, json=data)

            if response.status_code == 200:
                print(f'Success:', response.json())
                return None  # No retry necessary
            elif 400 <= response.status_code < 500:
                print(f'Client error ({response.status_code}):', response.text)
                return None  # No retry for 4XX errors
            elif 500 <= response.status_code < 600:
                print(f'Server error ({response.status_code}), retrying...')
            else:
                print(f'Error:', response.status_code, response.text)

        except Timeout:
            print(f'Request timed out, retrying...')
        except RequestException as e:
            print(f'Request failed: {e}, retrying...')

        retries += 1
        if retries < 3:
            time.sleep(3)  # Wait before retrying

    print(f'Max retries exceeded')
    #return None  # Max retries exceeded

