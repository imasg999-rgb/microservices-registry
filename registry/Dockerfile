# Stage 1 Bun Build Frontend
FROM oven/bun:1 AS frontend-builder

WORKDIR /app
COPY ./frontend ./frontend

WORKDIR /app/frontend
RUN bun install
RUN bun run build

# Stage 2 - Build Flask App
FROM python:3.10-slim
WORKDIR /reg
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV FLASK_APP=index.py

RUN mkdir -p ./static
COPY --from=frontend-builder /app/frontend/dist ./static

EXPOSE 4152
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:4152", "index:app"]
