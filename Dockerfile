FROM python:3.11-slim

# Installer git + pip
RUN apt-get update && apt-get install -y git && \
    pip install --upgrade pip

WORKDIR /app

COPY . .
COPY .env .env

RUN pip install -r requirements.txt

CMD ["python", "main.py"]