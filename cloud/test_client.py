import requests
import json
import time

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
            response = requests.put(url, headers=headers, data=json.dumps(data))
            
            if response.status_code == 200:
                print("✅ Success:")
                print(response.json())
                return response.json()

            elif 400 <= response.status_code < 500:
                print(f"❌ Client Error {response.status_code}:")
                print(response.text)
                return None  # Kein Retry bei Client-Fehlern

            else:
                print(f"⚠️ Server Error {response.status_code}, retrying...")

        except requests.exceptions.RequestException as e:
            print(f"❌ Network Exception: {str(e)}")

        attempt += 1
        print(f"🔁 Retry {attempt}/{max_retries} in 2s...\n")
        time.sleep(2)

    print("❌ Max retries reached. Giving up.")
    return None

# Hauptfunktion
if __name__ == "__main__":
    send_dummy_data_with_retry(dummy_data)
