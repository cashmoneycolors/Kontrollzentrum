FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1
ENV SECRET_KEY=production-secret-key

EXPOSE 8000

CMD ["python", "main.py", "api"]
