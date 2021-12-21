from prometheus_client import Gauge, start_http_server
from http.server import BaseHTTPRequestHandler
import socket
import time
import psutil


PORT_NUMBER = 4444
APP_PORT = 9005


class CustomCollector(BaseHTTPRequestHandler):
    def collect(self):
        host = socket.gethostname()
        ram_metrics = Gauge("memory_usage_bytes", "Memory usage in bytes.",
                            {'host': host})
        cpu_metrics = Gauge("cpu_usage", "CPU usage details",
                            {'host': host})
        counter = Gauge("access_counter", "access details")
        counter.set(0)

        while True:
            time.sleep(15)
            # Add ram metrics
            ram = psutil.virtual_memory()
            swap = psutil.swap_memory()
            ram_metrics.labels('ram_used').set(ram.used)
            print(ram.used)
            ram_metrics.labels('ram_cached').set(ram.cached)
            ram_metrics.labels('swap_memory_used').set(swap.used)
            counter.inc(1)
            for c, p in enumerate(psutil.cpu_percent(interval=1, percpu=True)):
                cpu_metrics.labels('cores').set(c)
                cpu_metrics.labels('percentage_use').set(p)


if __name__ == "__main__":
    try:
        start_http_server(PORT_NUMBER)
        x = CustomCollector
        x.collect(self=x)
    except KeyboardInterrupt:
        exit(0)
