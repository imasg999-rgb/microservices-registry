FROM python:3.10-slim

WORKDIR /svc

COPY microservices/live_flight/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY microservices /svc/microservices

CMD ["python", "-m", "microservices.live_flight.index"]
