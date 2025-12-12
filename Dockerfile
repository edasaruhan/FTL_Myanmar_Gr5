FROM python:3.10-slim

EXPOSE 8080
WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    ffmpeg \
    libsm6 \
    libgl1 \
    libglib2.0-0 \
    libavformat-dev \
    libavcodec-dev \
    libavdevice-dev \
    libavfilter-dev \
    libavutil-dev \
    libswscale-dev \
    libswresample-dev \
    libopus-dev \
    libvpx-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*
    
COPY src/Schema ./Schema
COPY src/Fine_tuned ./Fine_tuned
COPY src/RAG_pipeline ./RAG_pipeline
COPY src/Deployment/api_endpoint/main.py ./main.py
COPY src/Deployment/api_endpoint/mental_health.txt ./mental_health.txt

COPY requirements.txt .
RUN pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
