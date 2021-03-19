
import socket
import sys
from datetime import datetime
from time import sleep
import time
import enum

version = sys.version_info[0]


class socket_control:
    def __init__(self, iAddr, iPort = 5025):
        self.ip_addr = iAddr
        self.port = iPort
        self.status = connection_status.idle
        self.seq_num = 0
        
    def __del__(self):
        self.close()

    @property
    def is_connected(self):
        return self.status == connection_status.connected

    def connect(self):
        print('IP = {} and port = {}'.format(self.ip_addr, self.port))
        try:
            self._socket = socket.create_connection([self.ip_addr, self.port], timeout = 3)
            self.status = connection_status.connected
            return self.status
            # return connection_strings[self.status]
        except socket.timeout :
            self.status = connection_status.timeout
            return self.status
            # return connection_strings[self.status]

        
    def close(self):
        try:
            self._socket.close()
        except AttributeError:
            pass
        finally:
            self.status = connection_status.closed
        
        
    def send(self, String, toLog = False, delay = 0):
        byte_string = bytes(String, encoding = 'utf-8')

        if self.is_connected :
            if version == 3 :
                try:
                    self._socket.send(byte_string)
                except socket.timeout as stex:
                    self.status = connection_status.timeout
                    return stex.strerror
                sleep(delay)
                return self.receive()
            else:
                try:
                    self._socket.send(String)
                except socket.timeout as stex:
                    self.close()
                    return stex.strerror
                sleep(delay)
                return self.receive()
        return 'Not Connected'

    def send_comm_layer(self, String, toLog = False, delay = 0):
        byte_string = bytes(String, encoding = 'utf-8')

        msg_length = len(byte_string).to_bytes(4, 'little')
        self.seq_num += 1
        seq_num_bytes = self.seq_num.to_bytes(4, 'little')
        
        if self.is_connected :
            if version == 3 :
                try:
                    temp_string = msg_length + seq_num_bytes + byte_string
                    self._socket.send(temp_string)
                except socket.timeout as stex:
                    self.status = connection_status.timeout
                    return stex.strerror
                sleep(delay)
                return self.receive()

            #python2.7
            else:
                try:
                    self._socket.send(msg_length + seq_num_bytes + String)
                except socket.timeout as stex:
                    self.close()
                    return stex.strerror
                sleep(delay)
                return self.receive()
        return 'Not Connected'

    def receive(self, MaxBytes=2048):
        if self.is_connected:
            if version == 3:
                try:
                    byte_string = self._socket.recv(MaxBytes)
                except socket.timeout as stex:
                    self.status = connection_status.timeout
                    return self.status
                    # byte_string = b'socket timeout'
                except ConnectionResetError:
                    self.close()
                    self.status = connection_status.connection_reset
                    return self.status
                    # byte_string = b'connection reset'
                String = str(byte_string, encoding='utf-8')
                String = String.replace('\r','').replace('\n', '')
                return String
            else:
                try:
                    byte_string = self._socket.recv(MaxBytes)
                except socket.timeout as stex:
                    self.status = connection_status.timeout
                    return self.status
                    # byte_string = b'socket timeout'
                except ConnectionResetError:
                    self.close()
                    self.status = connection_status.connection_reset
                    return self.status
                    # byte_string = b'connection reset'
                String = str(byte_string, encoding='utf-8')
                String = String.replace('\r','').replace('\n', '')
                return String
        self.status = connection_status.closed
        return self.status
        # return 'Not Connected'

    def receive_comm_layer(self, MaxBytes=2048):
        if self.is_connected:
            if version == 3:
                try:
                    message_len = int.from_bytes(self._sock.recv(4), 'little')
                    seq_num = int.from_bytes(self._sock.recv(4), 'little')
                    byte_string = self._socket.recv(message_len)
                except socket.timeout as stex:
                    self.status = connection_status.timeout
                    return self.status
                    # byte_string = b'socket timeout'
                except ConnectionResetError:
                    self.close()
                    self.status = connection_status.connection_reset
                    return self.status
                String = str(byte_string, encoding='utf-8')
                String = String.replace('\r','').replace('\n', '')
                return String
            else:
                try:
                    byte_string = self._socket.recv(MaxBytes)
                except socket.timeout as stex:
                    self.status = connection_status.timeout
                    return self.status
                except ConnectionResetError:
                    self.close()
                    self.status = connection_status.connection_reset
                    return self.status
                String = str(byte_string, encoding='utf-8')
                String = String.replace('\r','').replace('\n', '')
                return String
        self.status = connection_status.closed
        return self.status

    def print_hex(self, string):
        tempString = ":".join('{:02x}'.format(ord(c)) for c in string)
        print(tempString)        


class connection_status(enum.Enum):
    idle = 'Idle'
    connecting = 'Connecting'
    connected = 'Connected'
    canceled = 'Canceled'
    closed = 'Closed'
    timeout = 'Timeout'
    socket_error = 'Socket Error'
    bad_port = 'Bad Port',
    connection_reset = 'Connection Reset'

# connection_strings = dict(
#     1 = "Idle",
#     2 = 'Connecting',
#     3 = 'Connected',
#     4 = 'Canceled',
#     5 = 'Closed',
#     6 = 'Socket Timeout',
#     7 = 'Socket Error',
#     8 = 'Bad Port'
# )





if __name__ == "__main__":
    # test = socket_control('169.254.208.100', 5025)
    test = socket_control('169.254.208.100', 5025)
    print(test.is_connected)

    try:
        test.connect()
        sleep(0.5)
        print(test.is_connected)
        print(test.send('*idn?'))
        sleep(1)

    finally:
        test.close()
        print(test.is_connected)






    