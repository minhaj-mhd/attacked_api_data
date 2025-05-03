# 🌐 Cyber Attack Monitoring API

A Django REST API built with MongoEngine for tracking, analyzing, and visualizing global cyber attacks. It includes support for filtering, statistics, and interactive map data via GeoJSON.

---

## 🚀 Features

- List and filter cyber attacks by date, type, severity, and region
- Fetch most recent attack records
- Aggregate statistics by country
- Generate GeoJSON data for map/globe visualization
- Auto-generated API documentation (Swagger & ReDoc)

---

## 📦 Tech Stack

- Django + Django REST Framework
- MongoDB with MongoEngine
- drf-spectacular for OpenAPI docs

---

## ⚙️ Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/attack-monitoring-api.git
   cd attack-monitoring-api
    ```
2. **Create a virtual environment**

    ```bash
    python -m venv env
    source env/bin/activate  # or `env\Scripts\activate` on Windows
    ```
3. **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```
4. **Configure MongoDB**

Make sure MongoDB is running locally or update your connect() call in mongoengine_connection.py to match your remote/local config.

5.  **Run the server**

    ```bash

    python manage.py runserver
    ```
6.  **Access API Docs**

Swagger UI: http://localhost:8000/api/docs/swagger/

ReDoc: http://localhost:8000/api/docs/redoc/

OpenAPI schema: http://localhost:8000/api/schema/

***🧪 Running Tests**
```bash

python manage.py test
```

***📘 API Endpoints Overview***
**🔍 List Attacks**


**GET /api/attacks/**

Query Parameters:

- page, page_size: Pagination controls

- attack_type: Filter by type (e.g., "DDoS", "Phishing")

- severity: Filter by numeric severity

- region: Filter by country (source location)

- start_date, end_date: ISO 8601 datetime strings for filtering by range

**🕒 Recent Attacks**

**GET /api/attacks/recent/?limit=5**

Returns the most recent n attacks (default limit is 10).

**📊 Attack Statistics by Country**
**GET /api/attacks/statistics/**
Returns a dictionary of { country: total_attacks }.

**🗺️ GeoJSON Visualization Data**
**GET /api/attacks/visualization-data/?view_type=globe**
Returns a GeoJSON FeatureCollection of recent attacks for map/globe rendering.