# Car Finder with Preference Triangle

An interactive app that aggregates car listings and visualizes them on a Cost vs Performance vs Reliability triangle. Users set their preference inside the triangle, filter by budget and specs, and get a ranked list of cars.

## Features
- Aggregated listings via pluggable providers (mock provider included)
- Triangle visualization using barycentric coordinates
- Filters: location, radius, price range, min horsepower, min reliability
- Optional AI-generated summaries (OpenAI) for each result
- FastAPI backend, React + Vite frontend

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+

### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Health check: `http://localhost:8000/api/health`

### Frontend
```bash
cd frontend
npm install
npm run dev
```
Dev server: `http://localhost:5173`

The dev frontend queries the backend at `http://localhost:8000`.

### Environment Variables
Copy `.env.example` to `.env` and fill in any keys you have. OpenAI key is optional; without it, we fall back to a concise heuristic summary.

### Notes on Providers
- Real sources like AutoTempest, Cars.com, Carvana, and Facebook Marketplace typically require scraping or private APIs. This project includes a clean provider interface and a `MockProvider` for development.
- To add a real provider, implement `Provider.search()` in `app/providers/your_provider.py` and register it in `services/aggregator.py`.

### Triangle Logic
- Each listing is mapped to a triangle using normalized price (Cost), horsepower (Performance), and an estimated reliability score (Reliability).
- We rank results by Euclidean distance between the listing's placement and the user's desired point inside the triangle.

## Build for Production
- Build the frontend: `npm run build` in `frontend/`
- The FastAPI app serves `frontend/dist` if present.

## License
MIT
