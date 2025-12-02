FROM python:3.10-slim

WORKDIR /svc

COPY microservices/currency_converter/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy full microservices folder including cert.pem and key.pem
COPY microservices /svc/microservices

EXPOSE 8443

CMD ["python", "-m", "microservices.currency_converter.index"]
