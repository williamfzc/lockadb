from fastapi import FastAPI
from whenconnect import when_connect, when_disconnect
from loguru import logger


class Device(object):
    class DeviceStatus(object):
        FREE = 0
        BUSY = 1

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


when_connect(device='any', do=DeviceManager.add)
when_disconnect(device='any', do=DeviceManager.remove)

app = FastAPI()


@app.get("/")
def hello():
    return {"hello": "from lockadb server"}


@app.get("/devices")
def all_devices():
    device_id_list = [i.device_id for i in DeviceManager.DEVICE_DICT.values()]
    return {"devices": device_id_list}


# start server with:
#   uvicorn server:app --reload
