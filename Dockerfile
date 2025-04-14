FROM python:3.11-slim

RUN apt-get update && apt-get install -y git && \
    pip install --upgrade pip

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "main.py"]