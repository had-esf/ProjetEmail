# Structure du Projet - Serveur SMTP Version 1

## Architecture Orientée Objet

Le projet est organisé selon une architecture POO avec **un fichier par classe**.

### Fichiers créés

#### Classes principales

1. **email_model.py**
   - Classe: `Email`
   - Rôle: Représente un email avec ses métadonnées
   - Attributs: `mail_from`, `rcpt_to`, `data`, `timestamp`
   - Méthodes: `set_mail_from()`, `add_recipient()`, `set_data()`, `is_valid()`, `to_string()`

2. **mailbox.py**
   - Classe: `MailBox`
   - Rôle: Gère le stockage des emails dans des fichiers
   - Méthodes: `store_email()`, `list_mailboxes()`
   - Stockage: Crée un fichier `.mbox` par destinataire dans le répertoire `mailboxes/`

3. **smtp_session.py**
   - Classe: `SMTPSession`
   - Rôle: Gère une session SMTP complète avec un client
   - Commandes implémentées:
     - `MAIL FROM:` - Définit l'expéditeur
     - `RCPT TO:` - Définit un destinataire (supporté multiple fois)
     - `DATA` - Réception du contenu de l'email
     - `QUIT` - Ferme la connexion
     - `RSET` - Réinitialise la transaction
   - Codes de réponse SMTP standard: 220, 221, 250, 354, 500, 503

4. **smtp_server.py**
   - Classe: `SMTPServer`
   - Rôle: Serveur principal qui écoute les connexions
   - Fonctionnalités:
     - Écoute sur le port 2525 (configurable)
     - Gestion multi-clients avec threading
     - Création automatique d'une session par client

#### Point d'entrée

5. **main.py**
   - Point d'entrée du programme
   - Démarre le serveur SMTP sur le port 2525
   - Gestion propre des interruptions (Ctrl+C)

#### Fichiers de test et documentation

6. **test_client.py**
   - Client de test automatique en Python
   - Teste toutes les commandes SMTP
   - Vérifie la conformité du serveur

7. **test_smtp.sh**
   - Script shell pour tester avec `nc` (netcat)
   - Envoi automatique d'un email de test

8. **README.md**
   - Documentation complète du projet
   - Instructions d'installation et d'utilisation
   - Exemples de sessions SMTP

9. **STRUCTURE.md** (ce fichier)
   - Description de l'architecture du projet

## Diagramme de classes simplifié

```
┌─────────────────┐
│   SMTPServer    │
│                 │
│ - host          │
│ - port          │
│ - mailbox       │
│                 │
│ + start()       │
│ + stop()        │
└────────┬────────┘
         │ crée
         ▼
┌─────────────────┐         ┌──────────────┐
│  SMTPSession    │ utilise │   MailBox    │
│                 │────────▶│              │
│ - client_socket │         │ - mailbox_dir│
│ - current_email │         │              │
│                 │         │ + store()    │
│ + handle_conn() │         └──────────────┘
│ + handle_mail() │
│ + handle_rcpt() │
│ + handle_data() │
└────────┬────────┘
         │ utilise
         ▼
    ┌─────────┐
    │  Email  │
    │         │
    │ - from  │
    │ - to[]  │
    │ - data  │
    └─────────┘
```

## Flux d'exécution

1. **Démarrage**: `main.py` crée une instance de `SMTPServer`
2. **Écoute**: Le serveur attend les connexions sur le port 2525
3. **Connexion**: À chaque nouvelle connexion, création d'une `SMTPSession` dans un thread
4. **Session SMTP**:
   - Envoi du message de bienvenue (220)
   - Réception et traitement des commandes SMTP
   - Création d'un objet `Email`
   - Stockage via `MailBox` à la fin de DATA
5. **Stockage**: Un fichier `.mbox` est créé/mis à jour pour chaque destinataire

## Tests effectués

✓ Connexion au serveur (code 220)
✓ Commande MAIL FROM (code 250)
✓ Commande RCPT TO simple (code 250)
✓ Commande RCPT TO multiple (code 250)
✓ Commande DATA (code 354)
✓ Stockage du contenu de l'email
✓ Commande QUIT (code 221)
✓ Création des fichiers .mbox
✓ Stockage correct des emails

## Conformité Version 1

Le serveur implémente toutes les fonctionnalités requises pour la **Version 1** du projet:

- ✓ Commande MAIL FROM
- ✓ Commande RCPT TO
- ✓ Commande DATA
- ✓ Stockage dans des fichiers nommés selon le destinataire
- ✓ Architecture POO avec un fichier par classe
- ✓ Code commenté et documenté

## Pour aller plus loin (Versions futures)

**Version 2** - À implémenter:
- Gestion des commandes HELO et EHLO
- Identification de la version du protocole
- Compatibilité avec clients standards (Thunderbird)

**Version 3** - À implémenter:
- Protocole POP3 pour la consultation des emails
- Commandes: QUIT, STAT, LIST, RETR
