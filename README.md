# Serveur SMTP/POP3 - Version 3

## Description

Serveur SMTP simple (versions 1 et 2) + ajout d'un serveur POP3 minimal (version 3).
Lien vers la vidéo youtube de démonstration : https://youtu.be/xWrajwIOm_M

## Architecture POO

Le projet est organisé en classes, chacune dans son propre fichier :

- **email_model.py** : Classe `Email` - Représente un email avec ses métadonnées
- **mailbox.py** : Classe `MailBox` - Gère le stockage des emails dans des fichiers json
- **smtp_session.py** : Classe `SMTPSession` - Gère une session SMTP avec un client
- **smtp_server.py** : Classe `SMTPServer` - Serveur principal qui écoute les connexions
- **pop3_session.py** : Classe `POP3Session` - Gère une session POP3 avec un client
- **pop3_server.py** : Classe `POP3Server` - Serveur POP3 qui écoute les connexions
- **main.py** : Fichier controlleur

## Commandes SMTP

### Version 1
- **MAIL FROM:** - Expéditeur
- **RCPT TO:** - Destinataire(s)
- **DATA** - Message (se termine par un "." seul)
- **QUIT** - Ferme la connexion
- **RSET** - Réinitialise la connexion

### Version 2
- **EHLO** - Version étendue non supportée (répond "502 Command not implemented")
- **HELO** - Version basique (répond "250 OK")

## Commandes POP3 (Version 3)

Pour rester au plus simple, le serveur POP3 accepte la séquence :
- **USER** - Sélectionne la boîte (ex: `USER bob@example.com`)
- **PASS** - Mot de passe non vérifié (accepté)

Commandes POP3 supportées :
- **STAT**
- **LIST**
- **RETR**
- **QUIT**

## Utilisation

### Démarrer le serveur

```bash
python3 main.py
```

Le serveur démarre sur le port 2525

Le serveur POP3 démarre sur le port 2110

### Tester avec Thunderbird

Configurer Thunderbird :

Serveur Entrant (POP3)
```bash
Protocole : POP3
Nom du serveur : localhost
Port : 2110
Sécurité de la connexion : Aucune
Méthode d’authentification : Mot de passe simple
Nom d’utilisateur : Adresse mail voulu
```

Serveur sortant (SMTP)
```bash
Nom du serveur : localhost
Port : 2525
Sécurité de la connexion : Aucune
Méthode d’authentification : Aucune
Nom d’utilisateur : adresse mail voulu
```
Aller dans Paramètres -> Parmètres des comptes -> Paramètres serveur (sur l'adresse mail qui reçoit) -> Décocher "laisser les messages sur le serveur"

La conservation des messages sur le serveur demande l'utilisation de commandes non implémentées

Envoyer un mail de manière classique

Actualiser la boîte mail de réception


### Tester avec telnet

Ouvrir un nouveau terminal et se connecter au serveur :

```bash
telnet localhost 2525
```

### Exemple de session SMTP

```
$ telnet localhost 2525
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
220 Service ready
MAIL FROM:<alice@example.com>
250 OK
RCPT TO:<bob@example.com>
250 OK
DATA
354 Start mail input; end with <CRLF>.<CRLF>
Subject: Test Email

Ceci est un message de test.
.
250 OK
QUIT
221 Service closing transmission channel
Connection closed by foreign host.
```

Ouvrir un nouveau terminal et se connecter a POP3 :

```bash
telnet localhost 2110
```

### Exemple de session POP3

```
$ telnet localhost 2110
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
+OK POP3 server ready
USER bob@example.com
+OK
PASS test
+OK
STAT
+OK 1 148
LIST
+OK 1 messages
1 148
.
RETR 1
+OK 148 octets
From: alice@example.com
To: bob@example.com
Date: 2025-11-07T16:30:00.000000

Subject: Test Email

Ceci est un message de test.
.
QUIT
+OK Goodbye
Connection closed by foreign host.
```

## Stockage des emails

Les emails sont stockés dans le répertoire `mailboxes/` :
- Chaque destinataire a son propre fichier
- Exemple : `bob_at_example.com.json`

## Structure d'un email stocké

Chaque fichier JSON contient un tableau d'emails :

```json
[
  {
    "mail_from": "alice@example.com",
    "rcpt_to": ["bob@example.com"],
    "data": "Subject: Test Email\n\nCeci est un message de test.",
    "timestamp": "2025-11-07T16:30:00.000000"
  }
]
```

## Codes de réponse SMTP

- **220** - Service ready
- **221** - Service closing transmission channel
- **250** - OK
- **354** - Start mail input
- **500** - Syntax error, command unrecognized
- **503** - Bad sequence of commands
