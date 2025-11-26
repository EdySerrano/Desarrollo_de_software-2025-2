import requests
import sys

def run_tests():
    print("Running E2E Tests...")
    
    # 1. Frontend Raiz
    try:
        print("Testing Frontend Raiz (http://localhost:8080/)...")
        resp = requests.get("http://localhost:8080/")
        if resp.status_code == 200:
            print("PASS: Frontend Raiz returned 200")
        else:
            print(f"FAIL: Frontend Raiz returned {resp.status_code}")
            sys.exit(1)
    except Exception as e:
        print(f"FAIL: Frontend Raiz exception: {e}")
        sys.exit(1)

    # 2. Backend Directo (Aislamiento)
    try:
        print("Testing Backend Isolation (http://localhost:5000/api/status)...")
        requests.get("http://localhost:5000/api/status", timeout=2)
        print("FAIL: Backend was reachable directly!")
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("PASS: Backend is isolated (ConnectionError)")
    except Exception as e:
        print(f"PASS: Backend is isolated ({type(e).__name__})")

    # 3. Frontend -> Backend
    try:
        print("Testing Frontend -> Backend Proxy (http://localhost:8080/api/data)...")
        resp = requests.get("http://localhost:8080/api/data")
        if resp.status_code == 200:
            data = resp.json()
            if data == {"data": "from_backend"}:
                print("PASS: Got correct JSON from backend via frontend")
            else:
                print(f"FAIL: Incorrect JSON: {data}")
                sys.exit(1)
        else:
            print(f"FAIL: Proxy returned {resp.status_code}")
            sys.exit(1)
    except Exception as e:
        print(f"FAIL: Proxy exception: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_tests()
