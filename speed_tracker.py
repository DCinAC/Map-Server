#!/usr/bin/env python3
import json
import csv
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from datetime import datetime
import math

locations = []
speed_cameras = []

# Load cameras from CSV
try:
    with open('cameras.csv', 'r') as f:
        reader = csv.DictReader(f)
        speed_cameras = [{'lat': float(r['lat']), 'lon': float(r['lon']),
                         'limit': int(r['limit']), 'type': r['type']} for r in reader]
    print(f"Loaded {len(speed_cameras)} speed cameras")
except:
    print("No cameras.csv found - running without camera data")

def distance(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

class SpeedHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == '/log':
            params = parse_qs(parsed.query)
            data = {
                'lat': float(params.get('lat', [0])[0]),
                'lon': float(params.get('longitude', [0])[0]),
                'speed': float(params.get('s', [0])[0]),
                'time': params.get('time', [datetime.now().isoformat()])[0]
            }

            # Check nearby cameras
            nearby = [c for c in speed_cameras if distance(data['lat'], data['lon'], c['lat'], c['lon']) < 500]
            data['cameras'] = nearby
            data['warning'] = any(data['speed'] > c.get('limit', 999) for c in nearby)

            locations.append(data)
            if len(locations) > 100:
                locations.pop(0)

            print(f"Speed: {data['speed']} km/h at {data['lat']}, {data['lon']}")
            if data['warning']:
                print(f"⚠️  SPEED WARNING! Camera ahead")

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'OK')

        elif self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = '''<!DOCTYPE html>
<html>
<head>
    <title>Speed Tracker</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <style>
        body{margin:0;font-family:sans-serif;}
        #map{height:calc(100vh - 60px);}
        #info{height:60px;padding:10px;background:#333;color:#fff;font-size:20px;}
        .warning{background:#f00!important;animation:blink 1s infinite;}
        @keyframes blink{50%{opacity:0.5;}}
    </style>
</head>
<body>
    <div id="info">Speed: <span id="speed">--</span> km/h | Cameras nearby: <span id="cameras">0</span></div>
    <div id="map"></div>
    <script>
        const map = L.map('map').setView([51.5, -0.1], 13);
        L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
        let marker, cameraMarkers = [];

        setInterval(async () => {
            const res = await fetch('/api/location');
            const data = await res.json();
            if(data.lat && data.lon){
                if(!marker) marker = L.marker([data.lat, data.lon]).addTo(map);
                else marker.setLatLng([data.lat, data.lon]);
                map.setView([data.lat, data.lon], 15);

                document.getElementById('speed').textContent = data.speed || 0;
                document.getElementById('cameras').textContent = (data.cameras || []).length;
                document.getElementById('info').className = data.warning ? 'warning' : '';

                cameraMarkers.forEach(m => map.removeLayer(m));
                cameraMarkers = (data.cameras || []).map(c =>
                    L.circleMarker([c.lat, c.lon], {color:'red', radius:8}).addTo(map)
                );
            }
        }, 1000);
    </script>
</body>
</html>'''
            self.wfile.write(html.encode())

        elif self.path == '/api/location':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            loc = locations[-1] if locations else {}
            self.wfile.write(json.dumps(loc).encode())

if __name__ == '__main__':
    print('Speed Tracker running on http://0.0.0.0:8192')
    print('Configure GPSLogger: http://YOUR_IP:8192/log?lat=%LAT&longitude=%LON&time=%TIME&s=%SPD')
    HTTPServer(('0.0.0.0', 8192), SpeedHandler).serve_forever()
