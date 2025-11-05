# Liste des Fichiers du Projet

## Fichiers créés pour la Version 1

### Classes Python (Architecture POO)

| Fichier | Classe | Description |
|---------|--------|-------------|
| `email_model.py` | `Email` | Représente un email avec FROM, TO, DATA |
| `mailbox.py` | `MailBox` | Gère le stockage des emails dans des fichiers |
| `smtp_session.py` | `SMTPSession` | Gère une session SMTP avec un client |
| `smtp_server.py` | `SMTPServer` | Serveur principal qui écoute les connexions |

### Point d'entrée

| Fichier | Description |
|---------|-------------|
| `main.py` | Lance le serveur SMTP sur le port 2525 |

### Tests

| Fichier | Description |
|---------|-------------|
| `test_client.py` | Client de test automatique en Python |
| `test_smtp.sh` | Script shell pour tester avec netcat |

### Documentation

| Fichier | Description |
|---------|-------------|
| `README.md` | Documentation technique complète (anglais) |
| `MANUEL.md` | Manuel d'utilisation en français |
| `STRUCTURE.md` | Description de l'architecture du projet |
| `FICHIERS.md` | Ce fichier - Liste de tous les fichiers |

### Fichiers existants (non modifiés)

| Fichier | Description |
|---------|-------------|
| `ProjetEMail.txt` | Spécifications du projet |
| `serveur.py` | Ancien fichier serveur socket (non utilisé) |
| `.gitignore` | Configuration git (mis à jour) |

## Répertoires

| Répertoire | Description |
|------------|-------------|
| `mailboxes/` | Stockage des emails reçus (créé automatiquement) |

## Comment utiliser ces fichiers

### 1. Démarrer le serveur
```bash
python3 main.py
```

### 2. Tester le serveur
```bash
# Option 1: Client Python automatique
python3 test_client.py

# Option 2: Script shell
./test_smtp.sh

# Option 3: Telnet manuel
telnet localhost 2525
```

### 3. Consulter les emails reçus
```bash
ls mailboxes/
cat mailboxes/destinataire_at_domain.mbox
```

## Commandes utiles

### Arrêter le serveur
```bash
# Dans le terminal du serveur
Ctrl+C

# Ou forcer l'arrêt
pkill -f "python3 main.py"
```

### Nettoyer les boîtes mail
```bash
rm -rf mailboxes/
```

### Vérifier les processus
```bash
ps aux | grep main.py
netstat -tulpn | grep 2525
```

## Validation de la Version 1

✓ Toutes les classes nécessaires créées
✓ Un fichier par classe (architecture POO)
✓ Commandes MAIL, RCPT, DATA implémentées
✓ Stockage dans des fichiers selon RCPT
✓ Tests fonctionnels réussis
✓ Documentation complète

Le projet est **prêt pour la livraison de la Version 1**.
