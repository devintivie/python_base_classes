from websocket import create_connection
import time
import json

class web_socket_client:
    def __init__(self, uri, port):
        self._uri = uri
        self._port = port
        self._ws = None

    def __del__(self):
        self.close()

    @property
    def is_connected(self):
        return self._ws.connected
    
    @property
    def _connection_string(self):
        return f'{self._uri}:{self._port}'

    def connect(self):
        try:
            self._ws = create_connection(self._connection_string)
        except Exception as ex:
            print(ex)

    def close(self, reason=1000):
        if self._ws:
            self._ws.close(status=reason)

    def send_quick_string(self, message, delay = 0, receive = True):
            self._ws.send(message)

            if delay > 0:
                time.sleep(delay)
            
            if receive:
                return self._ws.recv()
            else:
                return 'no receive'
            