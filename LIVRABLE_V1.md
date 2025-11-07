# Livrable Version 1 - Serveur SMTP Simple

**Projet:** Déploiement de Services et Interopérabilité - E-Mail  
**Version:** 1 - SMTP Simple  
**Date:** 5 Novembre 2025  
**Fonctionnalités:** Commandes MAIL, RCPT et DATA

---

## ✅ Validation des Exigences Version 1

### Exigences Fonctionnelles

- ✅ **Commande MAIL** - Gestion de l'expéditeur
- ✅ **Commande RCPT** - Gestion d'un ou plusieurs destinataires
- ✅ **Commande DATA** - Réception du contenu de l'email
- ✅ **Stockage** - Un fichier par destinataire nommé selon RCPT
- ✅ **Format** - Stockage dans des fichiers .json

### Exigences Techniques

- ✅ **Architecture POO** - Un fichier par classe
- ✅ **Python 3** - Utilise uniquement la bibliothèque standard
- ✅ **Code commenté** - Docstrings et commentaires
- ✅ **Tests** - Client de test automatique fourni

---

## 📁 Structure du Projet

### Classes (Architecture POO)

```
email_model.py    → Classe Email      (modèle de données)
mailbox.py        → Classe MailBox    (stockage)
smtp_session.py   → Classe SMTPSession (protocole SMTP)
smtp_server.py    → Classe SMTPServer (serveur réseau)
main.py           → Point d'entrée
```

### Fichiers de Test

```
test_client.py    → Client de test Python automatique
test_smtp.sh      → Script de test shell
run_tests.sh      → Suite de tests complète
```

### Documentation

```
README.md         → Documentation technique (anglais)
MANUEL.md         → Manuel d'utilisation (français)
STRUCTURE.md      → Architecture détaillée
FICHIERS.md       → Liste des fichiers
QUICKSTART.md     → Démarrage rapide
LIVRABLE_V1.md    → Ce fichier
```

---

## 🚀 Utilisation

### Démarrage Simple

```bash
# Tester que tout fonctionne
./run_tests.sh

# Démarrer le serveur
python3 main.py
```

### Test avec telnet

```bash
telnet localhost 2525

MAIL FROM:<alice@example.com>
RCPT TO:<bob@example.com>
DATA
Subject: Test

Message de test.
.
QUIT
```

### Consultation des Emails

```bash
ls mailboxes/
cat mailboxes/bob_at_example.com.json
```

---

## 🧪 Tests Effectués

### ✅ Tests Réussis

- [x] Connexion au serveur (code 220)
- [x] Commande MAIL FROM (code 250)
- [x] Commande RCPT TO simple (code 250)
- [x] Commande RCPT TO multiple (code 250)
- [x] Commande DATA (code 354)
- [x] Fin de DATA avec point (code 250)
- [x] Commande QUIT (code 221)
- [x] Commande RSET (code 250)
- [x] Stockage dans fichiers .json
- [x] Gestion multi-clients (threading)

### Résultat des Tests

```
==========================================
✓ TOUS LES TESTS RÉUSSIS
Le serveur SMTP Version 1 est fonctionnel!
==========================================
```

---

## 📊 Protocole SMTP Implémenté

### Codes de Réponse

| Code | Description |
|------|-------------|
| 220 | Service ready |
| 221 | Service closing transmission channel |
| 250 | OK |
| 354 | Start mail input; end with <CRLF>.<CRLF> |
| 500 | Syntax error, command unrecognized |
| 503 | Bad sequence of commands |

### Commandes Supportées

| Commande | Description | Exemple |
|----------|-------------|---------|
| MAIL FROM | Définit l'expéditeur | `MAIL FROM:<user@domain.com>` |
| RCPT TO | Ajoute un destinataire | `RCPT TO:<user@domain.com>` |
| DATA | Démarre la saisie du message | `DATA` |
| QUIT | Ferme la connexion | `QUIT` |
| RSET | Réinitialise la transaction | `RSET` |

### Séquence Standard

```
Client                  Serveur
  |                        |
  |------ connexion ------>|
  |<----- 220 Ready -------|
  |                        |
  |-- MAIL FROM:<...> ---->|
  |<----- 250 OK ----------|
  |                        |
  |-- RCPT TO:<...> ------>|
  |<----- 250 OK ----------|
  |                        |
  |------ DATA ----------->|
  |<----- 354 Input -------|
  |-- contenu + "." ------>|
  |<----- 250 OK ----------|
  |                        |
  |------ QUIT ----------->|
  |<----- 221 Closing -----|
  |                        |
```

---

## 📦 Stockage des Emails

### Format des Fichiers

- **Répertoire:** `mailboxes/`
- **Format:** Un fichier `.json` par destinataire
- **Nommage:** `destinataire_at_domaine.json`
- **Encodage:** UTF-8

### Exemple de Fichier Stocké

```json
[
  {
    "mail_from": "alice@example.com",
    "rcpt_to": [
      "bob@example.com",
      "charlie@example.com"
    ],
    "data": "Subject: Test Email\nFrom: Alice <alice@example.com>\nTo: Bob <bob@example.com>\n\nBonjour Bob,\n\nCeci est un message de test.\n\nCordialement,\nAlice",
    "timestamp": "2025-11-05T17:04:16.123456"
  }
]
```

---

## 🔧 Configuration

### Port par Défaut

- **Port:** 2525 (non privilégié)
- **Raison:** Évite les problèmes de permissions (le port 25 nécessite sudo)
- **Modifiable dans:** `main.py`

### Dépendances

- **Python:** 3.10+ recommandé
- **Bibliothèques:** Bibliothèque standard uniquement
- **Système:** Linux/Unix (testé sur Ubuntu)

---

## 🎓 Conformité Pédagogique

### Respect du Sujet

- ✅ Version 1 complète
- ✅ Commandes minimales SMTP (MAIL, RCPT, DATA)
- ✅ Stockage selon paramètre RCPT
- ✅ Architecture POO

### Code

- ✅ Commenté et documenté
- ✅ Docstrings sur toutes les méthodes
- ✅ Noms de variables explicites
- ✅ Pas de plagiat - Code original

### Tests

- ✅ Client de test fourni
- ✅ Script de test automatique
- ✅ Tests manuels documentés

---

## 📝 Prochaines Étapes

### Version 2 (à venir)

- [ ] Commande HELO
- [ ] Commande EHLO avec réponse 502
- [ ] Compatibilité Thunderbird

### Version 3 (à venir)

- [ ] Protocole POP3
- [ ] Commandes QUIT, STAT, LIST, RETR
- [ ] Consultation des emails

---

## 📖 Documentation Complète

Pour plus de détails, consultez:

- **QUICKSTART.md** - Démarrage en 3 commandes
- **MANUEL.md** - Guide complet en français
- **README.md** - Documentation technique
- **STRUCTURE.md** - Diagrammes et architecture
- **FICHIERS.md** - Liste complète des fichiers

---

## ✨ Résumé

Le **serveur SMTP Version 1** est **fonctionnel et validé**.

Toutes les exigences de la Version 1 sont remplies:
- ✅ Commandes MAIL, RCPT, DATA opérationnelles
- ✅ Stockage dans des fichiers selon RCPT
- ✅ Architecture POO propre
- ✅ Code commenté et testé
- ✅ Documentation complète

**Le projet est prêt pour la livraison.**

---

*Généré le 5 Novembre 2025*
