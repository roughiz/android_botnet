# Installer la bonneversion de paramiko en utilsant la commande suivante :
```
$ pip install -r requirements.txt
```

# Configuration du serveur sftp sur un système unix

## Installation du serveur SSH :

Pour installer le serveur SSH rien de plus simple :
```
$ apt-get install openssh-server
```

## Sécurisation du serveur SSH

#### Modifier le port d'écoute :

La première chose à faire lors de l'installation d'un serveur SSH, est de changer le port d'écoute du serveur. Localisez la ligne suivant dans le fichier **etc/ssh/sshd_config** (icij'utilise le port 222 pour éviter les attaques par défaut :
```
Port 222
```

## Interdire les connexions root

Une sécurisation supplémentaire est d'interdire les connexions directes pour l'utilisateur root.

Cela se passe dans le même fichier que précédemment à l'aide de la ligne suivante :
```
PermitRootLogin yes
```

## Redémarrer votre serveur ssh

#### Configuration du serveur SFTP :

Editez à nouveau le fichier **/etc/ssh/sshd_config** et rajoutez à la fin de celui-ci les lignes suivantes :
```
Subsystem sftp internal-sftp
       Match group ftp
       ChrootDirectory /home/ftp/
       AllowTCPForwarding yes
```
	
##### Explication :

+  Subsystem sftp internal-sftp : permet de spécifier que l'on veut utiliser SFTP
+  Match group ftp : autorise l'accès qu'aux utilisateurs appartenant au groupe ftp
+  ChrootDirectory /home/ftp/ : spécifie la racine du FTP
+  AllowTCPForwarding yes : autorise la redirection des ports TCP

## Création du répertoire racine du FTP :

Nous allons maintenant créer le répertoire racine du FTP.
```
$ sudo mkdir -p /home/ftp
```

#### Appliquer les droits addéquats :
```
$ sudo chmod -R 705 /home/ftp/
```

#### Ajout du groupe ftp:
```
$ sudo groupadd ftp
```

#### Création du répertoire racine pour l'utilisateur bot
```
$ sudo mkdir -p /home/bot
```

#### Ajout de l'utilisateur bot, ce dernier n'aurapas de shell, il saura ainsi ajouter au groupe ftp
```
$ sudo useradd -s /bin/false -d /home/bot -g ftp bot
```

#### Création d'un mot de passe pour l'utlisateur bot
```
$ sudo passwd bot
```

### Création de dossier racine dans lequel se fera, la lecture des bots connectés
```
$ sudo mkdir -p /home/ftp/bot
```

### Création de dossier dans lequel se fera, l'écriture des bots connectés
```
$ sudo mkdir -p /home/ftp/bot/dump
```

#### Passage de droit à l'utilisateur bot
```
$ sudo chown -R  bot /home/ftp/bot/dump/
```

#### Création des clés pour l'authentification sftp
En tant que utilisateur bot 
```
$  mkdir /home/bot/.ssh
$  ssh-keygen 

```
##### Note : N'oubliez pas d'ajouter la clès publique de votre bot dans le ficheir **/home/bot/.ssh/authorized_keys**, cette dernière doit correspondre  à la clés privée du bot qui se trouve dans le dossier bot_keys. (pensez à crée votre propre paire!!)

#### Redémarer votre serveur ssh
```
sudo service ssh restart
```

#### Lancement du serveur :
```
$ sudo python malware.py
```

#### Lancement d'un bot en lign de commande : 
```
$ sudo python bot.py
```



