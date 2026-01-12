import requests
import json

base = 'http://127.0.0.1:8000'

print('POST /predict')
payload = {
    'temperature': 26.0,
    'humidity': 65.0,
    'sunlight_hours': 6.5,
    'water_ph': 6.2,
    'air_quality_index': 80,
    'wind_speed': 1.4
}
try:
    r = requests.post(base + '/predict/', json=payload, timeout=5)
    print('Status', r.status_code)
    try:
        print(json.dumps(r.json(), indent=2))
    except Exception:
        print(r.text)
except Exception as e:
    print('Predict request failed:', e)

print('\nPOST /placement')
payload2 = {
    'farm_length': 20.0,
    'farm_width': 20.0,
    'min_spacing': 2.5,
    'max_towers': 15
}
try:
    r2 = requests.post(base + '/placement/', json=payload2, timeout=10)
    print('Status', r2.status_code)
    try:
        print(json.dumps(r2.json(), indent=2))
    except Exception:
        print(r2.text)
except Exception as e:
    print('Placement request failed:', e)
