#!/bin/bash

echo "Starting Offline GPS Tracking System..."

# Start tile server
echo "Starting tile server on port 8080..."
cd "/Users/dcinac/Documents/Map Server/maps"
"/Users/dcinac/Library/Application Support/Zed/node/node-v24.11.0-darwin-arm64/bin/tileserver-gl" maptiler-osm-2020-02-10-v3.11-planet.mbtiles > /tmp/tileserver.log 2>&1 &
TILE_PID=$!

sleep 3

# Start Traccar
echo "Starting Traccar on port 8082..."
cd "/Users/dcinac/Documents/Map Server/traccar-other-6.12.2"
export PATH="/opt/homebrew/opt/openjdk@21/bin:$PATH"
java -jar tracker-server.jar conf/traccar.xml > /tmp/traccar.log 2>&1 &
TRACCAR_PID=$!

sleep 5

# Open offline map in browser
echo "Opening offline map viewer..."
open "/Users/dcinac/Documents/Map Server/tracker.html"

echo ""
echo "✓ Tile server: http://localhost:8080 (PID: $TILE_PID)"
echo "✓ Traccar API: http://localhost:8082 (PID: $TRACCAR_PID)"
echo "✓ Offline Map: opened in browser"
echo ""
echo "Logs: /tmp/tileserver.log and /tmp/traccar.log"
echo "Press Ctrl+C to stop all services"

trap "kill $TILE_PID $TRACCAR_PID 2>/dev/null" EXIT

wait
