import sys
import http.client

def check_health():
    try:
        conn = http.client.HTTPConnection("localhost", 8000)
        conn.request("GET", "/health/")
        response = conn.getresponse()
        if response.status == 200:
            sys.exit(0)  # Healthy
        else:
            sys.exit(1)  # Unhealthy
    except Exception as e:
        sys.exit(1)  # Unhealthy

if __name__ == "__main__":
    check_health()
