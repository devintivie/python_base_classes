
import socket
import sys
from datetime import datetime
from time import sleep
import time
import enum


import ping

version = sys.version_info[0]


class socket_control:
    def __init__(self, iAddr, iPort = 5025):
        self.ip_address = iAddr
        self.port = iPort
        self.connection_status = connection_status.idle
        self.seq_num = 0
        
    def __del__(self):
        self.close()

    @property
    def is_connected(self):
        return self.connection_status == connection_status.connected
    
    @property
    def is_busy(self):
        return self.activity.is_alive()

    def connect(self):
        print('IP = {} and port = {}'.format(self.ip_address, self.port))
        try:
            self._socket = socket.create_connection([self.ip_address, self.port], timeout = 3)
            self.connection_status = connection_status.connected
            return self.connection_status.value
            # return connection_strings[self.connection_status]
        except socket.timeout :
            self.connection_status = connection_status.timeout
            return self.connection_status.value
            # return connection_strings[self.connection_status]
        except ConnectionRefusedError :
            self.connection_status = connection_status.refused
            return self.connection_status.value

        
    def close(self):
        try:
            self._socket.close()
        except AttributeError:
            pass
        finally:
            self.connection_status = connection_status.closed

    '''send bytes'''
    def send_bytes(self, byte_string, toLog = False, delay = 0, receive = True):
        if self.is_connected :
            if version == 3 :
                try:
                    self._socket.send(byte_string)
                except socket.timeout as stex:
                    self.close()
                    self.connection_status = connection_status.timeout
                    return stex.strerror
                except ConnectionResetError:
                    self.close()
                    self.connection_status = connection_status.connection_reset
                    return self.connection_status.value
                sleep(delay)
                
                if receive:
#                    print(f'[send debug] if receive = {receive}')
                    return self.receive_bytes()
                else:
                    return 'no receive'
            else:
                try:
                    self._socket.send(byte_string)
                except socket.timeout as stex:
                    self.close()
                    self.connection_status = connection_status.timeout
                    return stex.strerror
                sleep(delay)
                if receive:
                    return self.receive_bytes()
                else:
                    return b'Nothing to Receive'

        self.connection_status = connection_status.closed
        return self.connection_status.value
        
    '''send string'''
    def send(self, String, toLog = False, delay = 0, receive = True):
        byte_string = bytes(String, encoding = 'utf-8')
        response = self.send_bytes(byte_string, toLog=toLog, delay=delay, receive=receive)
        String = str(response, encoding='utf-8')
        String = String.replace('\r','').replace('\n', '')
        return String




#     def send(self, String, toLog = False, delay = 0, receive = True):
#         byte_string = bytes(String, encoding = 'utf-8')
# #        print(f'[send debug] command={String} : receive = {receive}')
#         if self.is_connected :
#             if version == 3 :
#                 try:
#                     self._socket.send(byte_string)
#                 except socket.timeout as stex:
#                     self.close()
#                     self.connection_status = connection_status.timeout
#                     return stex.strerror
#                 except ConnectionResetError:
#                     self.close()
#                     self.connection_status = connection_status.connection_reset
#                     return self.connection_status.value
#                 sleep(delay)
                
#                 if receive:
# #                    print(f'[send debug] if receive = {receive}')
#                     return self.receive()
#                 else:
#                     return 'no receive'
#             else:
#                 try:
#                     self._socket.send(String)
#                 except socket.timeout as stex:
#                     self.close()
#                     self.connection_status = connection_status.timeout
#                     return stex.strerror
#                 sleep(delay)
#                 if receive:
#                     return self.receive()
#                 else:
#                     return 'no receive'

#         self.connection_status = connection_status.closed
#         return self.connection_status.value

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
                    self.close()
                    self.connection_status = connection_status.timeout
                    return stex.strerror
                sleep(delay)
                return self.receive()

            #python2.7
            else:
                try:
                    self._socket.send(msg_length + seq_num_bytes + String)
                except socket.timeout as stex:
                    self.close()
                    self.connection_status = connection_status.timeout
                    return stex.strerror
                sleep(delay)
                return self.receive()
        self.connection_status = connection_status.closed
        return self.connection_status.value
        # return 'Not Connected'

    '''receive string'''
    def receive(self, MaxBytes=2048):
        byte_string =  self.receive_bytes(MaxBytes)
        String = str(byte_string, encoding='utf-8')
        String = String.replace('\r','').replace('\n', '')
        return String

    def receive_bytes(self, MaxBytes=2048):
        if self.is_connected:
            if version == 3:
                try:
                    byte_string = self._socket.recv(MaxBytes)
                except socket.timeout as stex:
                    self.connection_status = connection_status.timeout
                    return self.connection_status.value
                    # byte_string = b'socket timeout'
                except ConnectionResetError:
                    self.close()
                    self.connection_status = connection_status.connection_reset
                    return self.connection_status.value
                    # byte_string = b'connection reset'
                return byte_string
            else:
                try:
                    byte_string = self._socket.recv(MaxBytes)
                except socket.timeout as stex:
                    self.connection_status = connection_status.timeout
                    return self.connection_status.value
                    # byte_string = b'socket timeout'
                except ConnectionResetError:
                    self.close()
                    self.connection_status = connection_status.connection_reset
                    return self.connection_status.value
                return byte_string
        self.connection_status = connection_status.closed
        return self.connection_status.value
        # return 'Not Connected'

    def receive_comm_layer(self, MaxBytes=2048):
        if self.is_connected:
            if version == 3:
                try:
                    message_len = int.from_bytes(self._sock.recv(4), 'little')
                    seq_num = int.from_bytes(self._sock.recv(4), 'little')
                    byte_string = self._socket.recv(message_len)
                except socket.timeout as stex:
                    self.connection_status = connection_status.timeout
                    return self.connection_status.value
                    # byte_string = b'socket timeout'
                except ConnectionResetError:
                    self.close()
                    self.connection_status = connection_status.connection_reset
                    return self.connection_status.value
                String = str(byte_string, encoding='utf-8')
                String = String.replace('\r','').replace('\n', '')
                return String
            else:
                try:
                    byte_string = self._socket.recv(MaxBytes)
                except socket.timeout as stex:
                    self.connection_status = connection_status.timeout
                    return self.connection_status
                except ConnectionResetError:
                    self.close()
                    self.connection_status = connection_status.connection_reset
                    return self.connection_status
                String = str(byte_string, encoding='utf-8')
                String = String.replace('\r','').replace('\n', '')
                return String
        self.connection_status = connection_status.closed
        return self.connection_status.value

    def print_hex(self, string):
        tempString = ":".join('{:02x}'.format(ord(c)) for c in string)
        print(tempString)     

    def ping_check(self):
        if ping.ping_check(self.ip_address):
            self.IsConnectionProblem = False
            self.connection_status = connection_status.connecting
            return 1
        else:
            self.IsConnectionProblem = True
            self.connection_status = connection_status.ping_failed
            return 0    


class connection_status(enum.Enum):
    idle = b'Idle'
    connecting = b'Connecting'
    connected = b'Connected'
    canceled = b'Canceled'
    closed = b'Closed'
    timeout = b'Timeout'
    socket_error = b'Socket Error'
    bad_port = b'Bad Port',
    connection_reset = b'Connection Reset'
    refused = b'Connection Refused'
    ping_failed = b'Ping Failed'
    

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
    # test = socket_control('169.254.208.101', 5025)
    # for i in range(500):
    test = socket_control('151.1.10.12', 9760)
    # test = socket_control('151.1.1.236', 9760)
    # test = socket_control('151.1.1.179', 9500)
    # test = socket_control('151.1.10.10', 10027)
    print(test.is_connected)

    try:
        test.connect()
        resp = test.send(':IDN?\n')
        print(resp)

        resp = test.send(':TEMP?\n')
        print(resp)
        # if 'Closed' not in resp:
        # while(True):
        #     if not test.is_connected:
        #         break
        #     # sleep(0.5)
        #     print(test.is_connected)
        #     # test.send('syst:ip 169.254.208.101')
        #     resp = test.send("$016\r", receive=True)#\x00\xa5\x01\x02\x03\x04\x05\x06\x07\x08\x09", receive=True)
        #     print(f'resp = {resp}')
        #     # print(test.send('STS?'))
        #     # sleep(3)
        #     sleep(0.5)

    finally:
        test.close()
        print(test.is_connected)






    