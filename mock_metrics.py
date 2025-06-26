from http.server import BaseHTTPRequestHandler, HTTPServer
import json, random
from multiprocessing import Process


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/metrics":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            data = {
                "cpu": random.randint(10, 90),
                "mem": f"{random.randint(10, 80)}%",
                "disk": f"{random.randint(10, 70)}%",
                "uptime": f"{random.randint(0, 3)}d {random.randint(0, 23)}h {random.randint(0, 59)}m {random.randint(0, 59)}s"

            }
            self.wfile.write(json.dumps(data).encode())
        else:
            self.send_response(404)
            self.end_headers()


def run_server(port):
    print(f"Mock server running at http://127.0.0.1:{port}/metrics")
    HTTPServer(("127.0.0.1", port), Handler).serve_forever()


if __name__ == "__main__":
    processes = []
    for port in range(8001, 8031):
        p = Process(target=run_server, args=(port,))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
