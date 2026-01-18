FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Change this line in your Dockerfile
CMD ["python", "-m", "app.monitor"]
