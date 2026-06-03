# 🌬️ ECO-STATION: Air Quality Monitoring

<p align="center">
  <a href="README_ENG.md">
    <img src="https://img.shields.io/badge/🇬🇧_English-00D4FF?style=for-the-badge&logo=readme&logoColor=white" alt="English README">
  </a>
  <a href="README.md">
    <img src="https://img.shields.io/badge/🇺🇦_Українська-FF4D00?style=for-the-badge&logo=readme&logoColor=white" alt="Українська версія">
  </a>
</p>

<br>

![Dashboard Screenshot](ECO-BOT_dashboard.png)

A modern, lightweight, and informative dashboard for real-time air quality and weather tracking. The system automatically adapts to any chosen environmental monitoring station.

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-v0.100+-009688.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker Image](https://img.shields.io/badge/Docker_Hub-webyhomelab/air--quality--dashboard-0db7ed.svg?logo=docker&logoColor=white)](https://hub.docker.com/r/webyhomelab/air-quality-dashboard)

---

## 🚀 Key Features

- **📊 Real-time Data:** Automatically pulls data every 10 minutes from the **SaveEcoBot** API for any specified monitoring station.
- **🗺️ Auto-Geolocation:** Reads latitude and longitude coordinates directly from the selected station to query wind and weather patterns.
- **📈 Trends & History:** Records and visualizes hourly variations over the last 24 hours and daily averages over the past 7 days.
- **🧪 Comprehensive Metrics:** AQI, PM2.5, PM10, PM1, Radiation (gamma background), CO2, NO2, O3, SO2, Temperature, Humidity, Pressure, and Noise.
- **☁️ Weather Integration:** Connects with the Open-Meteo API to fetch wind speed and direction based on the station's geographic coordinates.
- **📱 PWA (Progressive Web App):** Installable on mobile devices or desktops. Works offline using cached data.
- **🎨 Bento Design:** Modern Glassmorphism-style UI with a fully responsive grid and auto-adjusted contrast levels.
- **🔍 Full Dynamic SEO:** Automatically generates `sitemap.xml`, `robots.txt`, canonical URLs, meta tags, and Open Graph / Twitter cards relative to the running domain and station name.

---

## 🛠️ Tech Stack

- **Backend:** [FastAPI](https://fastapi.tiangolo.com/) (Python 3.12).
- **Frontend:** [Jinja2](https://palletsprojects.com/p/jinja/) Templates + Vanilla CSS/JS.
- **Scheduler:** [APScheduler](https://apscheduler.readthedocs.io/) for background data extraction.
- **Data Fetching:** [HTTPX](https://www.python-httpx.org/) for async API requests.
- **PWA:** Service Workers + Manifest for mobile and OS-level integration.

---

## 📂 Project Structure

```text
air-quality-dashboard/
├── app/
│   └── main.py          # FastAPI logic, background workers, and API parsers
├── static/
│   ├── manifest.json    # PWA configuration (app icons, colors, scope)
│   ├── sw.js           # Service Worker for offline support and assets caching
│   └── icon.svg/png     # Graphic assets and logos
├── templates/
│   └── index.html       # Main Bento UI dashboard template
├── history.json         # Local database for tracking histories (bind-mounted)
├── requirements.txt     # Python dependencies
├── Dockerfile           # Multi-stage container builder (Debian slim, tzdata)
└── docker-compose.yml   # Multi-container startup orchestration file
```

---

## 📦 Installation & Setup (Docker)

The project has transitioned to a Docker-only architecture. You can run the dashboard with a single command.

### 1. Clone the Repository
```bash
git clone https://github.com/weby-homelab/air-quality-dashboard.git
cd air-quality-dashboard
```

### 2. Initialize the History Database
Before starting the container, create an empty `history.json` file on the host to prevent Docker from creating it as a directory:
```bash
echo '{}' > history.json
```

### 3. Run the Container
Start the container in detached mode:
```bash
docker compose up -d
```
The dashboard will be available at: `http://localhost:8000`

---

## ⚙️ Configuration & Environment Variables

You can customize the dashboard's target station and domain name by modifying the environment variables in `docker-compose.yml`:

| Environment Variable | Default Value | Description |
| :--- | :--- | :--- |
| `STATION_ID` | `24185` | The SaveEcoBot monitoring station identifier. |
| `DOMAIN` | `ecobot-2.srvrs.top` | Your public domain name (used for canonical URLs, sitemaps, and robots.txt). |
| `TZ` | `Europe/Kyiv` | System timezone to ensure accurate timestamp tracking in history charts. |

### 🔍 How to Find Your `STATION_ID`?
1. Open the [SaveEcoBot Map](https://www.saveecobot.com/maps).
2. Find and select your local air quality monitoring station.
3. In the browser's address bar, look at the URL: `https://www.saveecobot.com/station/XXXXX`.
4. The number `XXXXX` at the end of the URL is your `STATION_ID`. Copy it, update it in `docker-compose.yml`, and restart your container.

---

## 🗺️ Data Sources

1. **Air Quality:** [SaveEcoBot API](https://www.saveecobot.com/) (updates dynamically based on the configured `STATION_ID`).
2. **Weather:** [Open-Meteo API](https://open-meteo.com/) (query parameters are resolved using the station's metadata coordinates).

---

## 📝 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
<p align="center">
  Built in Ukraine under air raid sirens &amp; blackouts ⚡<br>
  &copy; 2026 Weby Homelab
</p>
