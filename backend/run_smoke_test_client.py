from fastapi.testclient import TestClient
import app.main as main

client = TestClient(main.app)

print('POST /predict')
payload = {
    'temperature': 26.0,
    'humidity': 65.0,
    'sunlight_hours': 6.5,
    'water_ph': 6.2,
    'air_quality_index': 80,
    'wind_speed': 1.4
}
resp = client.post('/predict/', json=payload)
print('Status', resp.status_code)
try:
    print(resp.json())
except Exception:
    print(resp.text)

print('\nPOST /placement')
payload2 = {
    'farm_length': 20.0,
    'farm_width': 20.0,
    'min_spacing': 2.5,
    'max_towers': 15
}
resp2 = client.post('/placement/', json=payload2)
print('Status', resp2.status_code)
try:
    print(resp2.json())
except Exception:
    print(resp2.text)
