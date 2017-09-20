from threading import Event
from paramiko import  ServerInterface
from paramiko import  OPEN_SUCCEEDED
from paramiko import  OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
from paramiko import  AUTH_SUCCESSFUL
from paramiko import  AUTH_FAILED
class Server(ServerInterface):
    def __init__(self):
        self.event = Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return OPEN_SUCCEEDED
        return OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        if (username == 'root') and (password == 'thetoorpassword'):
            return AUTH_SUCCESSFUL
        return AUTH_FAILED