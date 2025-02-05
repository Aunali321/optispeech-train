# Use a base image with Python 3.12 or later
FROM python:3.12-slim

# Install system dependencies for espeak (if needed by your model)
RUN apt-get update && apt-get install -y --no-install-recommends \
    espeak-ng \
    && rm -rf /var/lib/apt/lists/*

# Install ospeech with gradio and espeak support
RUN pip install --no-cache-dir ospeech[gradio,espeak]

# Create a directory for the app
WORKDIR /app

# Download the ONNX model
RUN wget https://github.com/Aunali321/optispeech-train/releases/download/v0.1.0/last.onnx -O /app/last.onnx

# Expose the default Gradio port
EXPOSE 7860

# Command to run the Gradio app
CMD ["ospeech-gradio", "/app/last.onnx", "--host", "0.0.0.0"]
