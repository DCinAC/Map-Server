# GPS Location Streaming Setup

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
