import requests
import json

DEFAULT_HOST = 'mc.vimemc.net'


# TODO: Add JSON parsing for API
class ServerStatusHelper:
    def __init__(self, host: str = None):
        if host is None:
            host = DEFAULT_HOST
        self.host = host

    def _raw(self):
        r = requests.get(f'https://api.mcsrvstat.us/2/{self.host}')
        return json.loads(r.text)

    def update(self):
        return self._raw()


if __name__ == '__main__':
    test = ServerStatusHelper()
    print(test.update())
