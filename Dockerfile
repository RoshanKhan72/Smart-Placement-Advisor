# --- Base image: small Debian-based Python 3.10 (matches common prod targets) ---
FROM python:3.10-slim

# Prevent Python from writing .pyc and buffer stdout/stderr (better logs in containers)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# --- Install dependencies first (layer caches well when only app code changes) ---
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# --- Application code ---
COPY app.py .

# Streamlit default port
EXPOSE 8501

# Run the app
CMD ["streamlit", "run", "app.py", "--server.headless", "true", "--server.port", "8501", "--server.address", "0.0.0.0"]

# --- Run Streamlit bound to all interfaces so the container port is reachable ---
# --server.headless true avoids browser assumptions in containers; --server.address=0.0.0.0 is required in Docker
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless", "true"]
