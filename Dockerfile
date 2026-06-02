FROM python:3.12-slim

# Install tzdata for timezone configuration
RUN apt-get update && apt-get install -y --no-install-recommends \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

ENV TZ=Europe/Kyiv
ENV PYTHONUNBUFFERED=1
ENV PORT=8000
ENV STATION_ID=24185

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "-m", "app.main"]
