# Serveur SMTP - Version 1

## Description

Serveur SMTP simple implémentant les commandes minimales pour la version 1 du projet.

## Architecture POO

Le projet est organisé en classes, chacune dans son propre fichier :

- **email_model.py** : Classe `Email` - Représente un email avec ses métadonnées (FROM, TO, DATA)
- **mailbox.py** : Classe `MailBox` - Gère le stockage des emails dans des fichiers
- **smtp_session.py** : Classe `SMTPSession` - Gère une session SMTP avec un client
- **smtp_server.py** : Classe `SMTPServer` - Serveur principal qui écoute les connexions
- **main.py** : Point d'entrée du programme

## Commandes SMTP supportées

### Version 1 (Commandes minimales)
- **MAIL FROM:** - Définit l'expéditeur
- **RCPT TO:** - Définit un destinataire (peut être appelé plusieurs fois)
- **DATA** - Commence la saisie du message (terminer par une ligne contenant uniquement un point)
- **QUIT** - Ferme la connexion
- **RSET** - Réinitialise la transaction en cours

## Installation

Aucune dépendance externe requise. Le projet utilise uniquement la bibliothèque standard Python.

```bash
# Python 3.10+ recommandé
python3 --version
```

## Utilisation

### Démarrer le serveur

```bash
cd /home/thibault/Bureau/Interop/projetEmail/ProjetEmail/ProjetEmail
python3 main.py
```

Le serveur démarre sur le port 2525 (port non privilégié).

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
Deuxième ligne du message.
.
250 OK
QUIT
221 Service closing transmission channel
Connection closed by foreign host.
```

## Stockage des emails

Les emails sont stockés dans le répertoire `mailboxes/` :
- Chaque destinataire a son propre fichier (boîte mail)
- Format : `destinataire_at_domaine.json`
- Exemple : `bob_at_example.com.json`

## Structure d'un email stocké

Chaque fichier JSON contient un tableau d'emails :

```json
[
  {
    "mail_from": "alice@example.com",
    "rcpt_to": ["bob@example.com"],
    "data": "Subject: Test Email\n\nCeci est un message de test.",
    "timestamp": "2024-11-05T16:30:00.000000"
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

## Notes

- Le serveur utilise le port 2525 pour éviter les problèmes de permissions (le port 25 nécessite sudo)
- Le serveur supporte plusieurs connexions simultanées grâce au threading
- Les emails sont stockés immédiatement après la commande DATA
- Le serveur affiche les commandes reçues et les réponses envoyées dans la console
