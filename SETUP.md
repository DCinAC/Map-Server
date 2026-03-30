# GPS Tracking Setup Guide

## Step 1: Start Traccar Server

```bash
cd "/Users/dcinac/Documents/Map Server/traccar-other-6.12.2"
export PATH="/opt/homebrew/opt/openjdk@21/bin:$PATH"
java -jar tracker-server.jar conf/traccar.xml
```

Keep this terminal open. Traccar will run on port 8082.

## Step 2: Access Traccar Web Interface

Open browser: `http://localhost:8082`

- Default login: **admin** / **admin**
- Change password after first login

## Step 3: Add Your Phone as a Device

1. Click the **+** button (top right)
2. Select "Device"
3. Enter:
   - Name: `My Phone`
   - Identifier: `phone123` (remember this!)
4. Click Save

## Step 4: Install Phone App

### Android: GPSLogger
- Install from Play Store
- Open app → Settings
- **Logging details** → Log to custom URL
- URL: `http://YOUR_MACBOOK_IP:5055/?id=phone123&lat=%LAT&lon=%LON&speed=%SPD&timestamp=%TIMESTAMP`
- Method: GET

### iOS: Traccar Client
- Install from App Store
- Server URL: `http://YOUR_MACBOOK_IP:5055`
- Device identifier: `phone123`

## Step 5: Find Your MacBook IP

```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
```

Use the IP that starts with `192.168.x.x` or `10.x.x.x`

## Step 6: Test

1. Start sending location from phone app
2. Refresh Traccar web interface
3. You should see your phone's location on the map

## Offline Maps (Optional)

Install **Organic Maps** from Mac App Store:
- Free, no tracking
- Download regions while online
- Works 100% offline after download
