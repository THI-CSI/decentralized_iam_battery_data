import requests
import json
import time
import logging

# Logging konfigurieren
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# URL deines lokalen FastAPI-Servers
url = "http://127.0.0.1:8000/batterypass/"

# Dummy-Daten zum Testen
dummy_data = {
    "name": "TestBattery123",
    "description": "Dummy battery data for testing"
}

# HTTP-Header mit Bearer Token für Authentifizierung
headers = {
    "Authorization": "Bearer secret",  # Dein API Token aus api.py
    "Content-Type": "application/json"
}

# Neue Funktion mit Retry-Mechanismus
def send_dummy_data_with_retry(data, max_retries=3):
    attempt = 0
    while attempt < max_retries:
        try:
            logging.info(f" Attempt {attempt + 1} of {max_retries}")
            response = requests.put(url, headers=headers, data=json.dumps(data))

            if response.status_code == 200:
                logging.info(" Success")
                logging.debug(f"Response: {response.json()}")
                return response.json()

            elif 400 <= response.status_code < 500:
                logging.error(f" Client Error {response.status_code}: {response.text}")
                return None  # Kein Retry bei Client-Fehlern

            else:
                logging.warning(f" Server Error {response.status_code}, retrying...")

        except requests.exceptions.RequestException as e:
            logging.exception(" Network Exception occurred")

        attempt += 1
        logging.info(f" Waiting 2 seconds before retry ({attempt}/{max_retries})...\n")
        time.sleep(2)

    logging.error(" Max retries reached. Giving up.")
    return None

# Hauptfunktion
if __name__ == "__main__":
    send_dummy_data_with_retry(dummy_data)
