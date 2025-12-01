# Stage 1 Bun Build Frontned
FROM oven/bun:1 AS frontend-builder

WORKDIR /app
COPY microservices/flight_search/frontend ./frontend

WORKDIR /app/frontend
RUN bun install
RUN bun run build

# Stage 2 Backend
FROM python:3.10-slim

WORKDIR /svc

COPY microservices/flight_search/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY microservices/flight_search microservices/flight_search
COPY microservices/utils microservices/utils

RUN mkdir -p microservices/flight_search/static
COPY --from=frontend-builder /app/frontend/dist \
  /svc/microservices/flight_search/static

CMD ["python", "-m", "microservices.flight_search.index"]
