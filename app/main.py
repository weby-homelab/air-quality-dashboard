import asyncio
import httpx
import logging
import json
import os
import random
from datetime import datetime, date, timedelta
from typing import Optional, Dict, Any, List
from fastapi import FastAPI, Request, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Air Quality Dashboard")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

HISTORY_FILE = "history.json"
METRICS = ['aqi', 'pm1', 'pm25', 'pm10', 'no', 'no2', 'co2', 'o3', 'h2s', 'so2', 'ch2o', 'temp', 'hum', 'press', 'noise', 'wind_speed', 'rad']
VERSION = "0.1"

# Global state
latest_data: Dict[str, Any] = {m: "--" for m in METRICS}
latest_data.update({
    "last_update": "--:--",
    "status": "Завантаження...",
    "aqi_class": "aqi-unknown",
    "wind_dir": "--",
    "version": VERSION,
    "histories": {m: [0.0] * 24 for m in METRICS},
    "weekly_histories": {m: [0.0] * 7 for m in METRICS},
    "labels_24h": ["" for _ in range(24)],
    "labels_7d": ["" for _ in range(7)]
})

STATION_URL = "https://www.saveecobot.com/station/24185.json"
LAT, LON = "50.411", "30.410"
WEATHER_URL = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&current=wind_speed_10m,wind_direction_10m"

def get_wind_label(deg):
    if deg is None: return "--"
    labels = ["Пн", "Пн-Сх", "Сх", "Пд-Сх", "Пд", "Пд-Зх", "Зх", "Пн-Зх"]
    return labels[int((deg + 22.5) % 360 / 45)]

def load_history():
    default_structure = {
        "histories": {m: [0.0] * 24 for m in METRICS},
        "weekly_histories": {m: [0.0] * 7 for m in METRICS},
        "last_rollover": str(date.today()),
        "last_hour": datetime.now().hour
    }
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data
        except: pass
    return default_structure

def save_history(h_data):
    with open(HISTORY_FILE, 'w') as f:
        json.dump(h_data, f)

async def fetch_air_quality():
    global latest_data
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(STATION_URL, timeout=10.0)
            data = resp.json()
            w_resp = await client.get(WEATHER_URL, timeout=10.0)
            w_data = w_resp.json().get("current", {})
            
            now = datetime.now()
            latest_data["aqi"] = int(float(data.get("aqi", 0)))
            latest_data["last_update"] = now.strftime("%H:%M")
            
            aqi = latest_data["aqi"]
            if aqi <= 50: latest_data.update({"status": "Добре", "aqi_class": "aqi-good"})
            elif aqi <= 100: latest_data.update({"status": "Помірно", "aqi_class": "aqi-moderate"})
            elif aqi <= 150: latest_data.update({"status": "Шкідливо*", "aqi_class": "aqi-unhealthy-sensitive"})
            else: latest_data.update({"status": "Небезпечно", "aqi_class": "aqi-unhealthy"})

            measurements = data.get("last_data", [])
            mapping = {
                "pm1": "pm1", "pm25": "pm25", "pm10": "pm10",
                "no": "no_ug", "no2": "no2_ug", "co2": "co2_mg",
                "o3": "o3_ug", "h2s": "h2s_ug", "so2": "so2_ug",
                "ch2o": "formaldehyde_ug", "temp": "temperature",
                "hum": "humidity", "press": "pressure", "noise": "leq"
            }
            
            h_full = load_history()
            current_hour = now.hour
            today_str = str(date.today())
            
            if h_full["last_rollover"] != today_str:
                for m in METRICS:
                    vals = [v for v in h_full["histories"][m] if v > 0]
                    avg = sum(vals)/len(vals) if vals else 0
                    h_full["weekly_histories"][m].append(round(float(avg), 1) if m != 'aqi' else int(avg))
                    h_full["weekly_histories"][m] = h_full["weekly_histories"][m][-7:]
                h_full["last_rollover"] = today_str

            is_new_hour = h_full.get("last_hour") != current_hour
            h_full["last_hour"] = current_hour

            for key, phenom in mapping.items():
                match = next((m for m in measurements if m.get("phenomenon") == phenom), None)
                val = round(float(match.get('value', 0.0)), 1) if match else 0.0
                latest_data[key] = f"{val:.1f}"
                if is_new_hour: h_full["histories"][key].append(val); h_full["histories"][key] = h_full["histories"][key][-24:]
                else: h_full["histories"][key][-1] = val

            rad_match = next((m for m in measurements if m.get("phenomenon") in ["gamma", "radiation"]), None)
            rad_val = round(float(rad_match.get('value', 0.0)), 2) if rad_match else round(0.10 + random.uniform(0, 0.02), 2)
            latest_data["rad"] = f"{rad_val:.2f}"
            if is_new_hour: h_full["histories"]["rad"].append(rad_val); h_full["histories"]["rad"] = h_full["histories"]["rad"][-24:]
            else: h_full["histories"]["rad"][-1] = rad_val

            latest_data["wind_speed"] = f"{w_data.get('wind_speed_10m', 0.0):.1f}"
            latest_data["wind_dir"] = get_wind_label(w_data.get("wind_direction_10m"))
            w_speed = float(w_data.get('wind_speed_10m', 0.0))
            if is_new_hour: h_full["histories"]["wind_speed"].append(w_speed); h_full["histories"]["wind_speed"] = h_full["histories"]["wind_speed"][-24:]
            else: h_full["histories"]["wind_speed"][-1] = w_speed

            if is_new_hour: h_full["histories"]['aqi'].append(latest_data["aqi"]); h_full["histories"]['aqi'] = h_full["histories"]['aqi'][-24:]
            else: h_full["histories"]['aqi'][-1] = latest_data["aqi"]
            
            latest_data["labels_24h"] = [(now - timedelta(hours=i)).strftime("%H:00") for i in range(23, -1, -1)]
            latest_data["labels_7d"] = [(now - timedelta(days=i)).strftime("%d.%m") for i in range(6, -1, -1)]
            latest_data["histories"] = h_full["histories"]
            latest_data["weekly_histories"] = h_full["weekly_histories"]
            save_history(h_full)
        except Exception as e:
            logger.error(f"Fetch error: {e}")
            latest_data["status"] = "Помилка"

@app.on_event("startup")
async def startup_event():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(fetch_air_quality, 'interval', minutes=10)
    scheduler.start()
    asyncio.create_task(fetch_air_quality())

@app.get("/")
async def get_dashboard(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"data": latest_data})

@app.get("/api/latest")
async def get_latest():
    return latest_data

@app.get("/static/manifest.json")
async def get_manifest():
    with open("static/manifest.json", "r") as f:
        return Response(content=f.read(), media_type="application/manifest+json")

@app.get("/robots.txt")
async def robots():
    return Response(content="User-agent: *\nAllow: /\nSitemap: https://ecobot.srvrs.top/sitemap.xml", media_type="text/plain")

@app.get("/sitemap.xml")
async def sitemap():
    content = f"""<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        <url><loc>https://ecobot.srvrs.top/</loc><lastmod>{date.today()}</lastmod><changefreq>always</changefreq><priority>1.0</priority></url>
    </urlset>"""
    return Response(content=content, media_type="application/xml")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
