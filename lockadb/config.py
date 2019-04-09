import pathlib


ROOT_PATH = pathlib.Path(__file__).parent.resolve()

CHARSET = 'utf-8'

SERVER_PORT = 29410
SERVER_URL_PREFIX = 'http://127.0.0.1:{}'.format(SERVER_PORT)
