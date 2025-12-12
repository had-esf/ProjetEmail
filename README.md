# Serveur SMTP - Version 1

## Description

Serveur SMTP simple implémentant les commandes minimales pour la version 1 du projet.
Lien vers la vidéo youtube de démonstration : https://youtu.be/xWrajwIOm_M

## Architecture POO

Le projet est organisé en classes, chacune dans son propre fichier :

- **email_model.py** : Classe `Email` - Représente un email avec ses métadonnées
- **mailbox.py** : Classe `MailBox` - Gère le stockage des emails dans des fichiers json
- **smtp_session.py** : Classe `SMTPSession` - Gère une session SMTP avec un client
- **smtp_server.py** : Classe `SMTPServer` - Serveur principal qui écoute les connexions
- **main.py** : Fichier controlleur

## Commandes SMTP

### Version 1
- **MAIL FROM:** - Expéditeur
- **RCPT TO:** - Destinataire(s)
- **DATA** - Message (se termine par un "." seul)
- **QUIT** - Ferme la connexion
- **RSET** - Réinitialise la connexion

## Utilisation

### Démarrer le serveur

```bash
python3 main.py
```

Le serveur démarre sur le port 2525

### Tester avec Thunderbird

Configurer Thunderbird :

Serveur sortant (SMTP)
```bash
Nom du serveur : localhost
Port : 2525
Sécurité de la connexion : Aucune
Méthode d’authentification : Aucune
Nom d’utilisateur : (vide)
```

Envoyer un mail de manière classique

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
