FROM python:3.10-slim

WORKDIR /svc

COPY microservices/destination_wishlist/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY microservices /svc/microservices

EXPOSE 5002

CMD ["python", "-m", "microservices.destination_wishlist.index"]
