FROM python:3.10-slim

WORKDIR /svc

COPY microservices/flight_search/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY microservices /svc/microservices

CMD ["python", "-m", "microservices.flight_search.index"]
