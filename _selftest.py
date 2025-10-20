from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Health
r = client.get('/api/health')
print('HEALTH', r.status_code, r.json())

# Search
payload = {
    "location": "Seattle, WA",
    "radius_km": 50,
    "price_min": 5000,
    "price_max": 50000,
    "horsepower_min": 150,
    "reliability_min": 0.6,
    "desired": {"cost": 0.4, "performance": 0.4, "reliability": 0.2},
    "include_summaries": False,
}

r = client.post('/api/search', json=payload)
print('SEARCH', r.status_code)
js = r.json()
print('TOTAL', js.get('total'), 'PROVIDERS', js.get('providers_used'))
if js.get('results'):
    first = js['results'][0]
    print('FIRST', first['listing']['title'], 'SCORE', round(first['score'], 3))
