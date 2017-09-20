from time import sleep

def receiveFromChannel(channel):
    lengdatawait = -1
    data = ""
    while channel.get_transport().is_active():
        if channel.recv_ready():
            if lengdatawait < 0:
                a = channel.recv(4096)
                a= a.split('\0',1)
                lengdatawait = int(a[0])
                data = a[1]
            if lengdatawait == len(data):
                return data
            data += channel.recv(lengdatawait-len(data))
            if lengdatawait == len(data):
                return data
        else:
            sleep(0.2)


def sendToChannel(data,channel):
    datatosend = str(len(data)) + '\0' + data
    channel.sendall(datatosend)

def closeChannel(channel):
    channel.close()