# Build Frontend
FROM node:20-alpine AS frontend-builder

WORKDIR /app

COPY microservices/destination_wishlist/frontend ./frontend

WORKDIR /app/frontend

#installing dependencies
RUN npm install
RUN npm run build

# backend Python
FROM python:3.10-slim

WORKDIR /svc

COPY microservices/destination_wishlist/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY microservices/destination_wishlist microservices/destination_wishlist
COPY microservices/utils microservices/utils

RUN mkdir -p microservices/destination_wishlist/static

COPY --from=frontend-builder /app/frontend/build \
  /svc/microservices/destination_wishlist/static

EXPOSE 5002

CMD ["python", "-m", "microservices.destination_wishlist.index"]
