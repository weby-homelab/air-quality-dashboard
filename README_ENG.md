# 🌬️ ECO-STATION: Air Quality Monitoring (Kyiv)

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

A modern, lightweight, and informative dashboard for real-time air quality tracking. Designed for residents of Kyiv (Southern Borshchahivka) using cutting-edge web technologies.

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-v0.100+-009688.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🚀 Key Features

- **📊 Real-time Data:** Updated every 10 minutes from station **24185 (SaveEcoBot)**.
- **📈 Trends & History:** Visualization of hourly changes over the last 24 hours and daily averages over 7 days.
- **🧪 Comprehensive Metrics:** AQI, PM2.5, PM10, PM1, Radiation (gamma background), CO2, NO2, O3, SO2, Temperature, Humidity, Pressure, and Noise.
- **☁️ Weather Integration:** Open-Meteo integration for wind speed and direction.
- **📱 PWA (Progressive Web App):** Installable on mobile or desktop. Works offline (caching latest data).
- **🎨 Bento Design:** Ultra-modern Glassmorphism-style interface with a responsive grid.

---

## 🛠️ Tech Stack

- **Backend:** [FastAPI](https://fastapi.tiangolo.com/) (Python) — fast and asynchronous framework.
- **Frontend:** [Jinja2](https://palletsprojects.com/p/jinja/) Templates + Vanilla CSS/JS.
- **Scheduler:** [APScheduler](https://apscheduler.readthedocs.io/) for background data updates.
- **Data Fetching:** [HTTPX](https://www.python-httpx.org/) for asynchronous API requests.
- **PWA:** Service Workers + Manifest for mobile integration.

---

## 📂 Project Structure

```text
air-quality-dashboard/
├── app/
│   └── main.py          # Main server and parsing logic
├── static/
│   ├── manifest.json    # PWA configuration
│   ├── sw.js           # Service Worker for offline mode
│   └── icon.png        # Graphic assets
├── templates/
│   └── index.html       # Main page (Bento UI)
├── history.json         # Local history storage (automatic)
├── requirements.txt     # Dependencies
└── dashboard.log        # Operation logs
```

---

## 📦 Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/weby-homelab/air-quality-dashboard.git
cd air-quality-dashboard
```

### 2. Environment Setup
```bash
python -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run the Server
```bash
python -m app.main
```
The dashboard will be available at: `http://localhost:8000`

---

## 🗺️ Data Sources

1. **Air Quality:** [SaveEcoBot API](https://www.saveecobot.com/) (Station №24185).
2. **Weather:** [Open-Meteo API](https://open-meteo.com/) (Kyiv coordinates).

---

## 📝 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
*Developed with care for the environment and clean air. 🌍*

---

<br>
<p align="center">
  Built in Ukraine under air raid sirens &amp; blackouts ⚡<br>
  &copy; 2026 Weby Homelab
</p>
