FROM python:3.10-slim

EXPOSE 8080
WORKDIR /app

COPY src/Schema ./Schema
COPY src/Fine_tuned ./Fine_tuned
COPY src/RAG_pipeline ./RAG_pipeline
COPY src/Deployment/api_endpoint/main.py ./main.py
COPY src/Deployment/api_endpoint/mental_health.txt ./mental_health.txt

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
