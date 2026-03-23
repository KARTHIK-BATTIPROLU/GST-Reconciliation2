FROM python:3.11-slim

WORKDIR /app

# Install dependencies (cached layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/ backend/
COPY frontend/ frontend/
COPY .env.example .

# Environment Defaults
ENV PORT=8001
ENV WORKERS=4

# Expose ports
EXPOSE 8001 8502

# Startup script
CMD python -m uvicorn backend.main:app --host 0.0.0.0 --port $PORT --workers $WORKERS & \
    streamlit run frontend/dashboard.py --server.port 8502 --server.address 0.0.0.0
