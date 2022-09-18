import requests

def run(host, *args, **kwargs):
    if not args or len(args) != 2:
        print("[COMMAND-ERROR] Missing key (use set <key> <value>)")
        return
    key = args[0]
    value = args[1]

    try:
        response = requests.post(f"{host}/", json={"key": key, "value": value})
        if response.status_code == 201:
            print(f"- {key}: {value}")
        else:
            print(f"- [Failed] {key}: {response}")
    except requests.exceptions.ConnectionError:
        print("[ERROR] Failed to connect with host")

