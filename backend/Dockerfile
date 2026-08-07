FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Install wget
RUN apt-get update && apt-get install -y wget

# Create rembg model directory
RUN mkdir -p /root/.u2net

# Download the U2Net model
RUN wget https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx \
    -O /root/.u2net/u2net.onnx

COPY . .

EXPOSE 8000

CMD ["python", "app.py"]