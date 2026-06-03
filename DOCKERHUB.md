<p align="center">
  <a href="https://github.com/weby-homelab/air-quality-dashboard/blob/main/README_ENG.md">
    <img src="https://img.shields.io/badge/🇬🇧_English-00D4FF?style=for-the-badge&logo=readme&logoColor=white" alt="English README">
  </a>
  <a href="https://github.com/weby-homelab/air-quality-dashboard/blob/main/README.md">
    <img src="https://img.shields.io/badge/🇺🇦_Українська-FF4D00?style=for-the-badge&logo=readme&logoColor=white" alt="Українська версія">
  </a>
</p>

<br>

# 🌬️ Air Quality & Weather Bento Dashboard

<p align="center">
  <a href="https://hub.docker.com/r/webyhomelab/air-quality-dashboard"><img src="https://img.shields.io/docker/pulls/webyhomelab/air-quality-dashboard?style=for-the-badge&logo=docker&color=0db7ed" alt="Docker Pulls"></a>
  <a href="https://github.com/weby-homelab/air-quality-dashboard/releases/latest"><img src="https://img.shields.io/github/v/release/weby-homelab/air-quality-dashboard?style=for-the-badge&logo=github&color=0072ff" alt="Latest Release"></a>
  <a href="https://github.com/weby-homelab/air-quality-dashboard/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge" alt="License"></a>
</p>

---

## 🎯 What is this?

**Air Quality Dashboard** is a modern, lightweight, and responsive web application designed to track air quality metrics and local weather patterns in real-time. Initially crafted for the residents of Kyiv (Southern Borshchahivka), it has evolved into a fully dynamic platform that adapts to any environmental monitoring station globally, querying and mapping variables on the fly.

Built on top of a beautiful **Glassmorphism Bento design**, it fits seamlessly on all screens, offering premium UX and Progressive Web App (PWA) integration for native-like usage on mobile devices.

---

## ✨ Key Features

- **📊 Dynamic Monitoring:** Pulls data every 10 minutes from the **SaveEcoBot API** for any station configured via `STATION_ID`.
- **🗺️ Geolocation Weather:** Coordinates are resolved dynamically from the station's metadata and passed directly to **Open-Meteo API** to calculate wind and local temperature metrics.
- **📈 Trend Visualizations:** Displays hourly historical changes over the last 24 hours and daily averages over the past 7 days.
- **🧪 Detailed Analytics:** Tracks AQI, PM2.5, PM10, PM1, Gamma-background Radiation, CO2, NO2, O3, SO2, Temp, Humidity, Pressure, and Ambient Noise.
- **📱 PWA & Offline Support:** Service Workers cache static assets and latest measurements, allowing offline readability.
- **🔍 Automated SEO & Metadata:** Dynamically generates pages, robots.txt, sitemaps, and Open Graph previews tailored for the target station and domain.

---

## 🚀 Deployment (Docker Compose)

Create a `docker-compose.yml` file:

```yaml
version: '3.8'

services:
  air-quality-dashboard:
    image: webyhomelab/air-quality-dashboard:latest
    container_name: air-quality-dashboard
    restart: unless-stopped
    ports:
      - "8000:8000"
    environment:
      - STATION_ID=24185          # Your SaveEcoBot Station ID
      - DOMAIN=ecobot-2.srvrs.top  # Your public hostname for SEO
      - TZ=Europe/Kyiv
    volumes:
      - ./history.json:/app/history.json
```

Initialize an empty history database file to prevent Docker from creating it as a directory:

```bash
echo '{}' > history.json
docker compose up -d
```

Access the dashboard at `http://localhost:8000`.

---

## 🇺🇦 Розгортання українською

Для швидкого запуску дашборду створіть файл конфігурації `docker-compose.yml` (див. приклад вище). Створіть порожній файл бази даних історії на хості перед стартом:

```bash
echo '{}' > history.json
docker compose up -d
```

Дашборд автоматично підтягне назву та координати вашої еко-станції SaveEcoBot та прогноз погоди. Доступний на порту `8000` вашого хоста.

---
<p align="center">
  <b>Made with ❤️ in Kyiv under air raid sirens and blackouts.</b><br>
  Weby Homelab - Your Environment, Under Your Control.
</p>
