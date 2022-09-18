import requests

def run(host, *args, **kwargs):
    if not args:
        print("[COMMAND-ERROR] Missing key (use set <key>)")
        return
    keys = args

    for key in keys:
        try:
            response = requests.delete(f"{host}/{key}")
            if response.status_code == 204:
                print(f"- {key} was removed")
            else:
                print(f"- [Failed] {key}: {response}")
        except requests.exceptions.ConnectionError:
            print("[ERROR] Failed to connect with host")
