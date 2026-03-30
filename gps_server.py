#!/usr/bin/env python3
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime

locations = []

class GPSHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers['Content-Length'])
        data = json.loads(self.rfile.read(length))
        data['timestamp'] = datetime.now().isoformat()
        locations.append(data)
        if len(locations) > 100:
            locations.pop(0)
        self.send_response(200)
        self.end_headers()
        print(f"Location: {data.get('lat')}, {data.get('lon')}")

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = f'''<!DOCTYPE html>
<html>
<head>
    <title>GPS Tracker</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <style>body{{margin:0;}}#map{{height:100vh;}}</style>
</head>
<body>
    <div id="map"></div>
    <script>
        const map = L.map('map').setView([0, 0], 2);
        L.tileLayer('https://tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png').addTo(map);
        let marker;
        setInterval(async () => {{
            const res = await fetch('/api/location');
            const data = await res.json();
            if(data.lat && data.lon){{
                if(!marker) marker = L.marker([data.lat, data.lon]).addTo(map);
                else marker.setLatLng([data.lat, data.lon]);
                map.setView([data.lat, data.lon], 15);
            }}
        }}, 2000);
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
    print('GPS Server running on http://0.0.0.0:8080')
    HTTPServer(('0.0.0.0', 8080), GPSHandler).serve_forever()
