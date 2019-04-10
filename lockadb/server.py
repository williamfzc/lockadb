from fastapi import FastAPI
from whenconnect import when_connect, when_disconnect
from loguru import logger
import uvicorn

from lockadb.config import SERVER_PORT


class Device(object):
    class DeviceStatus(object):
        FREE = r'FREE'
        BUSY = r'BUSY'

    def __init__(self, device_id):
        self.device_id = device_id
        self.status = self.DeviceStatus.FREE

    def is_free(self):
        return self.status == self.DeviceStatus.FREE

    def acquire(self):
        self.status = self.DeviceStatus.BUSY

    def release(self):
        self.status = self.DeviceStatus.FREE

    def __hash__(self):
        return hash(self.device_id)


class DeviceManager(object):
    DEVICE_DICT = dict()

    @classmethod
    def add(cls, device_id: str) -> bool:
        if device_id in cls.DEVICE_DICT:
            logger.warning('device {} already existed'.format(device_id))
            return False
        device = Device(device_id)
        cls.DEVICE_DICT[device_id] = device
        return True

    @classmethod
    def remove(cls, device_id: str) -> bool:
        if device_id not in cls.DEVICE_DICT:
            logger.warning('device {} not existed'.format(device_id))
            return False
        del cls.DEVICE_DICT[device_id]
        return True

    @classmethod
    def is_device_existed(cls, device_id: str) -> bool:
        return device_id in cls.DEVICE_DICT

    @classmethod
    def is_device_busy(cls, device_id: str) -> bool:
        device = DeviceManager.DEVICE_DICT[device_id]
        return device.is_free()

    @classmethod
    def is_device_available(cls, device_id: str) -> bool:
        return cls.is_device_existed(device_id) and cls.is_device_busy(device_id)

    @classmethod
    def acquire(cls, device_id: str):
        device = cls.DEVICE_DICT[device_id]
        device.acquire()

    @classmethod
    def release(cls, device_id: str):
        device = cls.DEVICE_DICT[device_id]
        device.release()


when_connect(device='any', do=DeviceManager.add)
when_disconnect(device='any', do=DeviceManager.remove)


# --- API below ---

app = FastAPI()


@app.get("/")
def hello():
    return {"hello": "from lockadb server"}


@app.get("/devices")
def all_devices():
    device_list = [i.__dict__ for i in DeviceManager.DEVICE_DICT.values()]
    return {"devices": device_list}


@app.post("/devices/acquire")
def acquire_device(device_id: str):
    # existed, and free
    if not DeviceManager.is_device_available(device_id):
        return {"error": "device {} not available".format(device_id)}

    DeviceManager.acquire(device_id)
    return all_devices()


@app.post("/devices/release")
def release_device(device_id: str):
    # existed
    if not DeviceManager.is_device_existed(device_id):
        return {"error": "device {} not existed".format(device_id)}

    DeviceManager.release(device_id)
    return all_devices()


def main():
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=SERVER_PORT,
        log_level="info"
    )


if __name__ == '__main__':
    main()
