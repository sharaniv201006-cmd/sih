# AI-Based Predictive Modelling for Early Forecasting of Bovine Mastitis in Indian Dairy Farms

![SIH 2026 Project](https://img.shields.io/badge/SIH-2026-emerald.svg)
![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)
![XGBoost](https://img.shields.io/badge/XGBoost-90.8%25%20Accuracy-orange.svg)
![React](https://img.shields.io/badge/Frontend-React%20%2B%20Vite%20%2B%20Recharts-61dafb.svg)

An end-to-end intelligent veterinary decision-support software platform engineered for the early detection and forecasting of bovine mastitis in Indian dairy farms. The system pairs physical wearable biometrics, on-farm milking telemetry, and environmental pathogen exposure proxies through a trained **XGBoost Multi-Class Machine Learning Classifier** and an interactive **React + Vite** operational dashboard.

---

## Architecture Flow

```
+-------------------------------------------------------------+
|              Excel Dataset (data/mastitis_dataset.xlsx)     |
|          (12,000 Records x 30 Sensor & Biometric Features)  |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|                Pandas In-Memory Data Service                |
|              (No External Database Dependency)              |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|              Scikit-learn Preprocessing Pipeline            |
|       (StandardScaler + OneHotEncoder + Robust Encoding)    |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|             XGBoost Multi-Class ML Classifier               |
|            (Accuracy: 90.79%, F1-Score: 90.74%)             |
|   (Classes: No Risk, Low Risk, Moderate Risk, High Risk)    |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|                FastAPI REST API Microservice                |
|       (GET /api/dashboard, GET /api/animals, POST /predict) |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|               React.js + Vite + Recharts Dashboard          |
|      (Surveillance, IoT Simulator, Telemetry & Alerts)      |
+-------------------------------------------------------------+
```

---

## Key Features

1. **Direct Excel Data Engine**:
   - In-memory processing using Pandas directly from `data/mastitis_dataset.xlsx` (12,000 records across Indian dairy cattle breeds: Jersey Cross, HF Cross, Gir, Sahiwal, Murrah).
   - Zero reliance on external databases (Supabase, Firebase, or MongoDB) for clean offline or cloud deployments.

2. **XGBoost Machine Learning Pipeline**:
   - Multi-class classifier predicting mastitis risk levels (`No_Risk`, `Low`, `Moderate`, `High`).
   - Calibrated 0-100% continuous risk scoring.
   - Dynamic physiological feature deviation scoring (Milk Conductivity, Core Body Temp, Udder Surface Temp, Pathogen Proxy Exposure).
   - Evaluated on a stratified 20% test split: **90.79% Accuracy**, **90.71% Precision**, **90.79% Recall**, **90.74% F1-Score**.

3. **Interactive IoT Sensor Simulator**:
   - Realistic hardware demonstration mode labeled **“DEMO / SIMULATED SENSOR DATA”**.
   - Presets for Healthy Normal, Early Subclinical Warning, and Acute High-Risk states.
   - Real-time POST `/api/predict` execution.

4. **Barn Microclimate & Environmental Surveillance**:
   - Real-time Temperature-Humidity Index (THI) calculation.
   - Scientifically grounded pathogen-favorable condition indicator without falsely claiming direct bacterial detection.

5. **Decision-Support Alert System**:
   - Configurable high-risk threshold alert center.
   - Non-prescriptive veterinary suggestions (California Mastitis Test screening, quarter isolation, hygiene review).

---

## Project Structure

```
project/
|-- backend/
|   |-- app/
|   |   |-- __init__.py
|   |   |-- main.py                     # FastAPI application & lifespan
|   |   |-- config.py                   # Application settings & CORS
|   |   |-- schemas.py                  # Pydantic request/response models
|   |   |-- routes/
|   |   |   |-- health.py               # GET /api/health
|   |   |   |-- dashboard.py            # GET /api/dashboard
|   |   |   |-- animals.py              # GET /api/animals, /api/animals/{id}
|   |   |   |-- predictions.py          # POST /api/predict, /api/predictions/{id}
|   |   |   |-- sensor_data.py          # GET /api/sensor-data/{id}
|   |   |   |-- model_info.py           # GET /api/model-performance
|   |   |-- services/
|   |   |   |-- data_service.py         # Pandas dataset caching & filtering
|   |   |-- ml/
|   |       |-- preprocess.py           # Scikit-learn ColumnTransformer
|   |       |-- train.py                # XGBoost training & evaluation
|   |       |-- predict.py              # Inference, risk score & feature attribution
|   |       |-- model/
|   |           |-- mastitis_xgb_model.joblib
|   |           |-- pipeline.joblib
|   |           |-- model_metrics.json
|   |           |-- feature_importance.json
|   |-- requirements.txt
|   |-- .env.example
|
|-- data/
|   |-- mastitis_dataset.xlsx           # 12,000-row Excel dataset
|   |-- mastitis_dataset.csv            # CSV dataset mirror
|
|-- frontend/
|   |-- src/
|   |   |-- components/
|   |   |   |-- Navbar.jsx
|   |   |   |-- MetricCard.jsx
|   |   |   |-- RiskBadge.jsx
|   |   |   |-- EnvironmentalCard.jsx
|   |   |   |-- AlertBanner.jsx
|   |   |-- pages/
|   |   |   |-- Dashboard.jsx
|   |   |   |-- Animals.jsx
|   |   |   |-- AnimalDetail.jsx
|   |   |   |-- LiveSensorMonitoring.jsx
|   |   |   |-- PredictionsHistory.jsx
|   |   |   |-- Alerts.jsx
|   |   |   |-- ModelPerformance.jsx
|   |   |-- services/
|   |   |   |-- api.js
|   |   |-- App.jsx
|   |   |-- main.jsx
|   |   |-- index.css
|   |-- package.json
|   |-- vite.config.js
|   |-- tailwind.config.js
|   |-- postcss.config.js
|   |-- .env.example
|
|-- README.md
|-- .gitignore
```

---

## Quick Start Guide

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# (Optional) Train/Re-train ML model
python -m app.ml.train

# Start FastAPI server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

- API Health Check: `http://localhost:8000/api/health`
- Interactive Swagger Docs: `http://localhost:8000/docs`

---

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start Vite dev server
npm run dev
```

- Dashboard UI: `http://localhost:5173`

---

## REST API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Backend status & ML model readiness |
| `GET` | `/api/dashboard` | Executive summary, herd averages, risk breakdown & alerts |
| `GET` | `/api/animals` | Paginated, searchable, and filterable list of cows |
| `GET` | `/api/animals/{animal_id}` | Detailed animal profile, live model prediction & risk factors |
| `GET` | `/api/sensor-data/{animal_id}` | 7-day longitudinal sensor telemetry (Conductivity, Temp, Yield) |
| `GET` | `/api/predictions/{animal_id}` | Direct model inference result for a specific animal |
| `POST` | `/api/predict` | Live inference on arbitrary / simulated IoT sensor payload |
| `GET` | `/api/model-performance` | Accuracy, confusion matrix & feature importances |

---

## Deployment Instructions

### Frontend (Vercel)
1. Import the repository in Vercel.
2. Set Root Directory to `frontend`.
3. Build Command: `npm run build`
4. Output Directory: `dist`
5. Set Environment Variable: `VITE_API_URL=https://your-backend-api-url.onrender.com`

### Backend (Render / Railway)
1. Create a Web Service pointing to the repository.
2. Root Directory: `backend`
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Set Environment Variable: `DATA_FILE_PATH=../data/mastitis_dataset.xlsx`

---

## Veterinary Decision-Support Disclaimer

> [!NOTE]
> This software system is intended as an AI-powered surveillance and decision-support tool for dairy herd management. Sensor-derived risk classifications indicate statistical and physiological anomalies (such as elevated milk conductivity or udder temperature) and should be validated through on-farm diagnostic procedures (e.g. California Mastitis Test) and professional clinical evaluation by a licensed veterinarian.
