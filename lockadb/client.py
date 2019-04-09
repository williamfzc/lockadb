import requests
from lockadb.config import SERVER_URL_PREFIX


def heartbeat() -> bool:
    return requests.get(SERVER_URL_PREFIX).ok


def get_devices() -> str:
    request_url = SERVER_URL_PREFIX + '/devices'
    return requests.get(request_url).text


if __name__ == '__main__':
    devices = get_devices()
    print(devices)
