from http.server import BaseHTTPRequestHandler
import json
import statistics

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Set CORS headers
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        # Read request body
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        request_data = json.loads(post_data)
        
        # Extract parameters
        regions = request_data.get('regions', [])
        threshold_ms = request_data.get('threshold_ms', 180)
        
        # Telemetry data from your JSON file
        telemetry_data = [
            {"region": "apac", "latency_ms": 158.71, "uptime_pct": 99.325},
            {"region": "apac", "latency_ms": 177.71, "uptime_pct": 98.085},
            # ... add all other records from your file
        ]
        
        # Calculate metrics
        result = {}
        for region in regions:
            region_data = [r for r in telemetry_data if r['region'] == region]
            if region_data:
                latencies = [r['latency_ms'] for r in region_data]
                uptimes = [r['uptime_pct'] for r in region_data]
                
                latencies.sort()
                p95_index = int(0.95 * len(latencies)) - 1
                
                result[region] = {
                    "avg_latency": round(statistics.mean(latencies), 2),
                    "p95_latency": round(latencies[p95_index], 2),
                    "avg_uptime": round(statistics.mean(uptimes), 2),
                    "breaches": sum(1 for l in latencies if l > threshold_ms)
                }
        
        self.wfile.write(json.dumps(result).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
