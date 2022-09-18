import requests

def run(host, *args, **kwargs):
    if not args:
        print("[COMMAND-ERROR] Missing key (use get <key>)")
        return
    keys = args
    for key in keys:
        try:
            response = requests.get(f"{host}/{key}")
            if response.status_code == 200:
                value = response.json()["value"]
                print(f"- {key}: {value}")
            else:
                print(f"- [Failed] {key}: {response}")
        except requests.exceptions.ConnectionError:
            print("[ERROR] Failed to connect with host")
