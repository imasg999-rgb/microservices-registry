# Build Frontend
FROM node:20-alpine AS frontend-builder

WORKDIR /app

COPY microservices/currency_converter/frontend ./frontend

WORKDIR /app/frontend

#installing dependencies
RUN npm install
RUN npm run build

# backend Python
FROM python:3.10-slim

WORKDIR /svc

COPY microservices/currency_converter/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY microservices/currency_converter microservices/currency_converter
COPY microservices/utils microservices/utils

RUN mkdir -p microservices/currency_converter/static

COPY --from=frontend-builder /app/frontend/build \
  /svc/microservices/currency_converter/static

EXPOSE 8443

CMD ["python", "-m", "microservices.currency_converter.index"]
