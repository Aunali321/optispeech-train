FROM python:3.11-slim

# Install system dependencies for espeak
RUN apt-get update && apt-get install -y --no-install-recommends \
    espeak-ng \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip

# Install dependencies with specific versions to avoid conflicts
RUN pip install --no-cache-dir \
    piper-phonemize==1.1.0 \
    ospeech[gradio]==1.4.0

WORKDIR /app

# Download the ONNX model
RUN wget https://github.com/Aunali321/optispeech-train/releases/download/v0.1.0/last.onnx -O /app/last.onnx

EXPOSE 7860

CMD ["ospeech-gradio", "/app/last.onnx", "--host", "0.0.0.0"]
