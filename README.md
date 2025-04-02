# URL Shortening Service

A simple URL shortening service built with FastAPI and SQLite.

## Prerequisites

- Docker installed on your system
- Alternatively, Python 3.9+ for local development

## Running with Docker

### Build the Docker Image

```bash
docker build -t url-shortener .
```

### Run the Service

```bash
docker run -d -p 8000:8000 --name url-shortener-service url-shortener
```

### Stop the Service

```bash
docker stop url-shortener-service
```

### Remove the Container

```bash
docker rm url-shortener-service
```

## Running Locally (Without Docker)

1. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the service:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

The service runs on `http://localhost:8000` and provides the following endpoints:

- `POST /shorten`: Create a shortened URL
  - Request body: `{"url": "https://your-long-url.com"}`
  - Returns: Shortened URL

- `GET /shorten/{short_url}`: Resolve shortened URL to the orignial long URL
  - Returns: Original URL or 404 if not found



