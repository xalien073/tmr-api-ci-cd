FROM python:3.11-alpine

WORKDIR /app

COPY requirements.txt .
RUN apk add --no-cache zlib-dev libffi-dev && pip install --no-cache-dir -r requirements.txt

COPY . .

HEALTHCHECK CMD curl --fail http://localhost:8000/ || exit 1

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


# FROM tiangolo/uvicorn-gunicorn:python3.11-slim

# WORKDIR /app

# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

# # Optionally add a health check
# HEALTHCHECK CMD curl --fail http://localhost:8000/ || exit 1

# # Optionally expose the port
# EXPOSE 8000

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
