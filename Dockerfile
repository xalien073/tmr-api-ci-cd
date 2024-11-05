# Stage 1: Build stage
FROM python:3.11-slim as builder

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Stage 2: Final stage (Distroless)
FROM gcr.io/distroless/python3.11

WORKDIR /app

# Copy only necessary files from builder
COPY --from=builder /app /app
COPY --from=builder /root/.local /root/.local

# Use non-root user for security (optional)
USER nonroot

# Expose port 8000 and start the app
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


# FROM tiangolo/uvicorn-gunicorn:python3.11-slim

# WORKDIR /app

# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

# # Use multi-stage builds for smaller image size
# # Exclude compiled Python files

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
