# Démarrage Rapide - Serveur SMTP Version 1

## En 3 commandes

### 1. Tester que tout fonctionne
```bash
./run_tests.sh
```

### 2. Démarrer le serveur
```bash
python3 main.py
```

### 3. Dans un autre terminal, tester
```bash
python3 test_client.py
```

## Résultat attendu

```
============================================================
Test du serveur SMTP - Version 1
============================================================

1. Connexion au serveur...
<< 220 Service ready

2. Test commande MAIL FROM...
<< 250 OK

3. Test commande RCPT TO...
<< 250 OK

...

✓ Test réussi!
```

## Voir les emails reçus

```bash
cat mailboxes/*.mbox
```

## C'est tout! 🎉

Pour plus de détails, consultez:
- **MANUEL.md** - Guide complet en français
- **README.md** - Documentation technique
- **STRUCTURE.md** - Architecture du projet
