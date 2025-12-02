FROM python:3.10-slim

WORKDIR /svc

COPY microservices/airport_weather_forecast/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY microservices /svc/microservices

CMD ["python", "-m", "microservices.airport_weather_forecast.index"]
