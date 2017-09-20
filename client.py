from ParamikoServer import Server
from paramiko import Transport
from paramiko import  RSAKey

host_key = RSAKey(filename='./rsa.key')

class Client():

    def __init__(self, sock, addr):
        self.socket = sock
        self.address = addr
        self.closed = False
        try:
            self.transport = Transport(sock)
        except Exception:
            pass
        self.chan = None

    def connect(self):
        try:
            self.transport.load_server_moduli()
            self.transport.add_server_key(host_key)
            server = Server()
            self.transport.start_server(server=server)
            self.chan = self.transport.accept(100)
        except Exception:
            pass

    def get_channel(self):
        return self.chan

    def getAddr(self):
        return self.address[0]

    def isclosed(self):
        return self.closed
    def getScock(self):
        return self.socket

    def close(self):
        try:
            self.closed = True
            self.socket.close()
        except Exception:
            pass

    def toclose(self):
        self.closed = True
