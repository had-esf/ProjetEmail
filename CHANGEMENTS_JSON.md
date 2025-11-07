# Migration du format .mbox vers .json

## Résumé

Le système de stockage des emails a été migré du format texte `.mbox` vers le format structuré `.json`.

---

## Modifications du code

### 1. `email_model.py`

**Supprimé :**
- Méthode `to_string()` - convertissait l'email en format texte

**Ajouté :**
- Méthode `to_dict()` - convertit l'email en dictionnaire pour JSON
- Méthode classique `from_dict()` - crée un email à partir d'un dictionnaire JSON

### 2. `mailbox.py`

**Modifié :**
- Import ajouté : `import json`
- Extension de fichier : `.mbox` → `.json`
- Méthode `_get_mailbox_path()` : retourne maintenant un chemin `.json`
- Méthode `store_email()` : 
  - Charge les emails existants depuis le JSON
  - Ajoute le nouvel email au tableau
  - Sauvegarde avec `json.dump()` avec indentation
- Méthode `list_mailboxes()` : filtre maintenant les fichiers `.json`

---

## Modifications de la documentation

### Fichiers mis à jour :
1. **MANUEL.md** - Références aux fichiers `.mbox` → `.json`
2. **STRUCTURE.md** - Description du stockage et méthodes
3. **LIVRABLE_V1.md** - Format, exemples et références
4. **README.md** - Format de stockage et structure d'email
5. **FICHIERS.md** - Commandes de consultation
6. **QUICKSTART.md** - Commandes d'affichage
7. **run_tests.sh** - Script de test

### Exemples de fichiers stockés mis à jour

Ancien format (.mbox) :
```
================================================================================
From: alice@example.com
Date: Wed, 05 Nov 2025 17:04:16
To: bob@example.com

Subject: Test
...
================================================================================
```

Nouveau format (.json) :
```json
[
  {
    "mail_from": "alice@example.com",
    "rcpt_to": ["bob@example.com"],
    "data": "Subject: Test\n...",
    "timestamp": "2025-11-05T17:04:16.123456"
  }
]
```

---

## Fichiers supprimés

**Fichiers .mbox obsolètes :**
- `mailboxes/bob_at_example.com.mbox`
- `mailboxes/charlie_at_example.com.mbox`

---

## Avantages du format JSON

1. **Structure** - Format structuré et standardisé
2. **Lisibilité** - Plus facile à lire et à parser
3. **Extensibilité** - Facile d'ajouter de nouveaux champs
4. **Interopérabilité** - Compatible avec de nombreux outils
5. **Type-safe** - Validation de structure possible
6. **Multi-emails** - Tableau d'emails dans un seul fichier

---

## Tests effectués

✓ Compilation Python sans erreurs
✓ Stockage JSON fonctionnel
✓ Désérialisation JSON fonctionnelle
✓ Création de fichiers avec extension `.json`
✓ Format JSON valide avec indentation

### Script de test créé
- `test_json_storage.py` - Vérifie le stockage et la désérialisation JSON

---

## Compatibilité

Le nouveau système est **entièrement fonctionnel** et remplace complètement l'ancien format .mbox.

**Note :** Les anciens fichiers .mbox ne sont **pas compatibles** avec le nouveau système et ont été supprimés.

---

## Date de migration
7 Novembre 2025
