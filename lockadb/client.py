import requests
import json
import subprocess
import sys
import contextlib
import requests.exceptions
from lockadb.config import SERVER_URL_PREFIX


def heartbeat() -> bool:
    try:
        resp = requests.get(SERVER_URL_PREFIX)
    except requests.exceptions.ConnectionError:
        return False

    return resp.ok


def get_devices() -> str:
    request_url = SERVER_URL_PREFIX + '/devices'
    return json.loads(requests.get(request_url).text)


def acquire_device(device_id: str) -> bool:
    request_url = SERVER_URL_PREFIX + '/devices/acquire?device_id=' + device_id
    response = json.loads(requests.post(request_url).text)
    return 'error' not in response


def release_device(device_id: str) -> bool:
    request_url = SERVER_URL_PREFIX + '/devices/release?device_id=' + device_id
    response = json.loads(requests.post(request_url).text)
    return 'error' not in response


@contextlib.contextmanager
def lock_device(device_id: str):
    assert acquire_device(device_id), 'device {} is busy'.format(device_id)
    yield
    assert release_device(device_id)


class LockAdbRunner(object):
    @classmethod
    def is_device_specific(cls, command: list) -> bool:
        # too few
        if len(command) < 3:
            return False
        # no device id
        if command[1] != '-s':
            return False
        return True

    @classmethod
    def run(cls, command: list):
        full_command = ['adb'] + command
        if not cls.is_device_specific(full_command):
            subprocess.call(full_command, stderr=subprocess.DEVNULL)
            return

        # device requirement
        device_id = full_command[2]
        with lock_device(device_id):
            subprocess.call(full_command, stderr=subprocess.DEVNULL)


def main():
    is_server_online = heartbeat()
    if not is_server_online:
        print('ladb offline. Start your ladb server with `ladb.start-server` firstly.')
        return

    command = sys.argv[1:]
    LockAdbRunner.run(command)


if __name__ == '__main__':
    main()
