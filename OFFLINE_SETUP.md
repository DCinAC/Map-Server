# Offline GPS Tracking Setup

## What You Need

1. Download map tiles for your region from: https://openmaptiles.com/downloads/
   - Choose your region (e.g., Hong Kong, UK)
   - Download the `.mbtiles` file
   - Place it in `/Users/dcinac/Documents/Map Server/maps/`

## Setup Steps

### 1. Create maps directory
```bash
mkdir -p "/Users/dcinac/Documents/Map Server/maps"
```

### 2. Start tile server (after downloading .mbtiles)
```bash
cd "/Users/dcinac/Documents/Map Server/maps"
tileserver-gl-light your-region.mbtiles
```
This runs on `http://localhost:8080`

### 3. Configure Traccar for offline tiles
Edit: `/Users/dcinac/Documents/Map Server/traccar-other-6.12.2/conf/traccar.xml`

Add before `</properties>`:
```xml
<entry key='web.url'>http://localhost:8082</entry>
<entry key='web.path'>./web</entry>
```

### 4. Start Traccar
```bash
cd "/Users/dcinac/Documents/Map Server/traccar-other-6.12.2"
export PATH="/opt/homebrew/opt/openjdk@21/bin:$PATH"
java -jar tracker-server.jar conf/traccar.xml
```

### 5. Configure in Traccar web UI
- Login: `http://localhost:8082` (admin/admin)
- Settings → Server → Map
- Change map URL to: `http://localhost:8080/styles/basic-preview/{z}/{x}/{y}.png`

## Phone Setup (Works Offline via LAN)

Your phone and MacBook must be on same WiFi network.

**Android - GPSLogger:**
- URL: `http://YOUR_MAC_IP:5055/?id=phone123&lat=%LAT&lon=%LON&speed=%SPD`

**iOS - Traccar Client:**
- Server: `http://YOUR_MAC_IP:5055`
- Device ID: `phone123`

Find Mac IP: `ifconfig | grep "inet " | grep -v 127.0.0.1`

## How It Works Offline

- Phone → WiFi → MacBook (no internet needed)
- Traccar uses local tile server for maps
- Everything runs on your LAN
