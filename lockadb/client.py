import requests
import json
from lockadb.config import SERVER_URL_PREFIX


def heartbeat() -> bool:
    return requests.get(SERVER_URL_PREFIX).ok


def get_devices() -> str:
    request_url = SERVER_URL_PREFIX + '/devices'
    return json.loads(requests.get(request_url).text)


def acquire_device(device_id: str):
    request_url = SERVER_URL_PREFIX + '/devices/acquire?device_id=' + device_id
    return json.loads(requests.post(request_url).text)


def release_device(device_id: str):
    request_url = SERVER_URL_PREFIX + '/devices/release?device_id=' + device_id
    return json.loads(requests.post(request_url).text)


if __name__ == '__main__':
    TEST_DEVICE_ID = '123456F'

    devices = get_devices()
    print(devices)

    result = acquire_device(TEST_DEVICE_ID)
    print(result)

    result = release_device(TEST_DEVICE_ID)
    print(result)
