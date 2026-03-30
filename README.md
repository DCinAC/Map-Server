# Map Server

Offline GPS navigation system that uses your phone as a GPS source and displays on your laptop's bigger screen. Perfect for family trips or areas without internet.

## Prerequisites

1. **Download Traccar** (v6.12.2 or later)
   - Get it from https://github.com/traccar/traccar/releases
   - Extract to `traccar-other-6.12.2/` in this directory

2. **Download offline maps** (.mbtiles format)
   - Place map files in the `maps/` folder
   - Get maps from sources like OpenMapTiles or Protomaps

## Quick Start

1. **Start the server:**
   ```bash
   python3 gps_server.py
   ```

2. **View map:** Open `http://YOUR_MACBOOK_IP:8080` in browser

3. **Phone setup:** Install GPSLogger app and configure

## Phone Apps

### Android: GPSLogger
- Install from Play Store
- Settings → Logging details → Log to custom URL
- URL: `http://YOUR_MACBOOK_IP:8080/?lat=%LAT&lon=%LON`
- Method: POST

### iOS: OwnTracks (HTTP mode)
- Install from App Store
- Mode: HTTP
- URL: `http://YOUR_MACBOOK_IP:8080`
- Device ID: phone

## Find Your MacBook IP
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
```

## Offline Maps

Install Organic Maps from App Store for offline viewing.
