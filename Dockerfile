FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY .env .env

CMD ["python", "-m", "streamlit","run", "main.py"]
