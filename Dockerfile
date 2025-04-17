FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies first to leverage Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Run automated tests at build time to ensure API compliance
RUN pytest --maxfail=1 --disable-warnings -q

# Default command to launch the FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"] 