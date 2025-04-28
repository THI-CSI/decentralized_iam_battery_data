import requests
import json

# URL von deinem lokalen FastAPI-Server
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

# Funktion zum Senden der Dummy-Daten
def send_dummy_data():
    try:
        response = requests.put(url, headers=headers, data=json.dumps(dummy_data))
        
        if response.status_code == 200:
            print("✅ Success:")
            print(response.json())
        else:
            print(f"❌ Error {response.status_code}:")
            print(response.text)
    except Exception as e:
        print("❌ Exception occurred:", str(e))

# Hauptfunktion
if __name__ == "__main__":
    send_dummy_data()
