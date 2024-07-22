FROM tiangolo/uvicorn-gunicorn:python3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Use multi-stage builds for smaller image size
# Exclude compiled Python files

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
