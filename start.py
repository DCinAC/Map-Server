#!/usr/bin/env python3
import subprocess
import time
import signal
import sys
import os

processes = []

def cleanup(sig, frame):
    print("\nStopping services...")
    for p in processes:
        p.terminate()
    sys.exit(0)

signal.signal(signal.SIGINT, cleanup)

base_dir = "/Users/dcinac/Documents/Map Server"
print("Starting Offline GPS Tracking System...")

# Start tile server
print("Starting tile server on port 8080...")
tile_log = open(os.path.join(base_dir, "logs/tileserver.log"), "w")
tile_proc = subprocess.Popen([
    "/Users/dcinac/Library/Application Support/Zed/node/node-v24.11.0-darwin-arm64/bin/tileserver-gl",
    os.path.join(base_dir, "maps/maptiler-osm-2020-02-10-v3.11-planet.mbtiles")
], stdout=tile_log, stderr=tile_log, cwd=base_dir)
processes.append(tile_proc)

time.sleep(3)

# Start Traccar
print("Starting Traccar on port 8082...")
traccar_log = open(os.path.join(base_dir, "logs/traccar.log"), "w")
os.environ["PATH"] = "/opt/homebrew/opt/openjdk@21/bin:" + os.environ.get("PATH", "")
traccar_proc = subprocess.Popen([
    "java", "-jar", "tracker-server.jar", "conf/traccar.xml"
], stdout=traccar_log, stderr=traccar_log, cwd=os.path.join(base_dir, "traccar-other-6.12.2"))
processes.append(traccar_proc)

time.sleep(5)

# Open browser
print("Opening tracker in browser...")
subprocess.Popen(["open", "tracker.html"])

print("\n✓ Tile server: http://localhost:8080 (PID: {})".format(tile_proc.pid))
print("✓ Traccar API: http://localhost:8082 (PID: {})".format(traccar_proc.pid))
print("✓ Tracker opened in browser")
print("\nLogs: logs/tileserver.log and logs/traccar.log")
print("Press Ctrl+C to stop all services\n")

# Keep running
while True:
    time.sleep(1)

