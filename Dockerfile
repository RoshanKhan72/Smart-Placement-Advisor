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
# Copy all necessary backend and frontend files
COPY backend.py .
COPY index.html .
COPY style.css .
COPY script.js .

# Flask default port
EXPOSE 5000

# Run the app with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "backend:app"]
