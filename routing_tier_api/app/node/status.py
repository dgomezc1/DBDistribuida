import requests

def health_check(base_url):
    try:
        response = requests.get(f"{base_url}/db/PING")
        if response.status_code != 200:
            return False

        _json = response.json()
        if _json["value"] != "PONG":
            return False
        return True
    except requests.exceptions.ConnectionError:
        return False
