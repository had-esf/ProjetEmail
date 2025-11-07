# Manuel d'Utilisation - Serveur SMTP Version 1

## Démarrage rapide

### 1. Lancer le serveur

```bash
cd /home/thibault/Bureau/Interop/projetEmail/ProjetEmail/ProjetEmail
python3 main.py
```

Le serveur démarre sur le port **2525** et affiche:
```
============================================================
Serveur SMTP - Version 1
Commandes supportées: MAIL, RCPT, DATA, QUIT, RSET
============================================================
Serveur SMTP démarré sur *:2525
En attente de connexions...
```

### 2. Tester avec le client Python

Ouvrir un **nouveau terminal** et lancer:

```bash
python3 test_client.py
```

Ce script teste automatiquement toutes les commandes et affiche le résultat.

### 3. Tester avec telnet (manuel)

Ouvrir un **nouveau terminal** et se connecter:

```bash
telnet localhost 2525
```

Puis taper les commandes suivantes:

```
MAIL FROM:<alice@example.com>
RCPT TO:<bob@example.com>
DATA
Subject: Test

Ceci est un message de test.
.
QUIT
```

> **Note**: La ligne contenant uniquement un point (`.`) termine le message.

### 4. Tester avec le script shell

```bash
chmod +x test_smtp.sh
./test_smtp.sh
```

## Vérification des emails reçus

Les emails sont stockés dans le répertoire `mailboxes/`:

```bash
ls -l mailboxes/
cat mailboxes/bob_at_example.com.json
```

## Commandes SMTP supportées

| Commande | Syntaxe | Description |
|----------|---------|-------------|
| MAIL | `MAIL FROM:<expediteur@domain.com>` | Définit l'expéditeur |
| RCPT | `RCPT TO:<destinataire@domain.com>` | Ajoute un destinataire (répétable) |
| DATA | `DATA` | Démarre la saisie du message |
| QUIT | `QUIT` | Ferme la connexion |
| RSET | `RSET` | Annule la transaction en cours |

## Codes de réponse

| Code | Signification |
|------|---------------|
| 220 | Service ready (bienvenue) |
| 250 | OK (commande acceptée) |
| 354 | Start mail input (entrer le message) |
| 221 | Service closing (fermeture) |
| 500 | Syntax error (erreur de syntaxe) |
| 503 | Bad sequence (mauvais ordre de commandes) |

## Ordre des commandes

Pour envoyer un email, les commandes doivent être dans cet ordre:

1. **MAIL FROM** (obligatoire) - Définit l'expéditeur
2. **RCPT TO** (obligatoire, répétable) - Définit le(s) destinataire(s)
3. **DATA** (obligatoire) - Envoie le contenu
4. **QUIT** (optionnel) - Ferme proprement la connexion

## Exemples d'utilisation

### Exemple 1: Email simple

```
MAIL FROM:<alice@example.com>
RCPT TO:<bob@example.com>
DATA
Subject: Hello

Bonjour Bob!
.
QUIT
```

### Exemple 2: Email avec plusieurs destinataires

```
MAIL FROM:<alice@example.com>
RCPT TO:<bob@example.com>
RCPT TO:<charlie@example.com>
RCPT TO:<dave@example.com>
DATA
Subject: Réunion

Bonjour à tous,

La réunion est prévue demain à 10h.

Cordialement,
Alice
.
QUIT
```

### Exemple 3: Plusieurs emails dans une session

```
MAIL FROM:<alice@example.com>
RCPT TO:<bob@example.com>
DATA
Subject: Premier email

Contenu du premier email.
.
RSET
MAIL FROM:<alice@example.com>
RCPT TO:<charlie@example.com>
DATA
Subject: Deuxième email

Contenu du deuxième email.
.
QUIT
```

## Arrêter le serveur

Dans le terminal où le serveur s'exécute, appuyer sur **Ctrl+C**.

Le serveur affichera:
```
Arrêt du serveur demandé...
Serveur SMTP arrêté
```

## Dépannage

### Le port 2525 est déjà utilisé

Arrêter tous les processus Python:
```bash
pkill -f "python3 main.py"
```

Ou changer le port dans `main.py`:
```python
server = SMTPServer(host='', port=3000)  # Nouveau port
```

### Permission refusée

Si vous voulez utiliser le port 25 (port SMTP standard), vous devez lancer avec sudo:
```bash
sudo python3 main.py
```

Mais il est recommandé d'utiliser le port 2525 pour éviter les problèmes de permissions.

### Les emails ne sont pas stockés

Vérifier que:
1. Le répertoire `mailboxes/` existe
2. Vous avez les droits d'écriture
3. La séquence de commandes est correcte (MAIL → RCPT → DATA)

## Architecture du code

Le projet utilise une **architecture orientée objet** avec un fichier par classe:

- `email_model.py` - Classe Email
- `mailbox.py` - Classe MailBox
- `smtp_session.py` - Classe SMTPSession
- `smtp_server.py` - Classe SMTPServer
- `main.py` - Point d'entrée

Pour plus de détails, voir `STRUCTURE.md`.

## Prochaines versions

**Version 2** ajoutera:
- Support de HELO et EHLO
- Compatibilité avec Thunderbird

**Version 3** ajoutera:
- Protocole POP3
- Consultation des emails

## Support

Pour toute question, consulter:
- `README.md` - Documentation technique
- `STRUCTURE.md` - Architecture du projet
- `ProjetEMail.txt` - Spécifications complètes
