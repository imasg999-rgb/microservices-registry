FROM python:3.10-slim
WORKDIR /reg
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV FLASK_APP=index.py
EXPOSE 7993
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:7993", "index:app"]
