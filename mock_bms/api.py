import http, requests
import time
from requests import Timeout, RequestException


'''
Usage examples:
    post_data(CLOUD_API_URL, data) # for posting data
    get_data(BLOCKCHAIN_API_URL + bms_did_id) # for getting data
'''

def get_data(api_url):
    params=None
    retries = 0
    # Send the GET request
    while retries < 3:
        try:
            response = requests.get(api_url, params=params)

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

def post_data(api_url, data):
    retries = 0
    # Send the POST request with JSON data
    while retries < 3:
        try:
            response = requests.post(api_url, json=data, headers={'Content-Type': 'application/json'})

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

