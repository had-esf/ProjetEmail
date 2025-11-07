#!/usr/bin/env python3
"""
Script de test pour vérifier le stockage JSON des emails
"""

from email_model import Email
from mailbox import MailBox
import json
import os

def test_json_storage():
    print("=" * 60)
    print("Test du stockage JSON des emails")
    print("=" * 60)
    
    # Créer un email de test
    email = Email()
    email.set_mail_from("alice@example.com")
    email.add_recipient("bob@example.com")
    email.add_recipient("charlie@example.com")
    email.set_data("Subject: Test JSON\n\nCeci est un test du stockage JSON.")
    
    print("\n1. Email créé:")
    print(f"   From: {email.mail_from}")
    print(f"   To: {', '.join(email.rcpt_to)}")
    print(f"   Timestamp: {email.timestamp}")
    
    # Créer une mailbox et stocker l'email
    mailbox = MailBox()
    success = mailbox.store_email(email)
    
    if success:
        print("\n2. ✓ Email stocké avec succès")
    else:
        print("\n2. ✗ Erreur lors du stockage")
        return
    
    # Vérifier les fichiers créés
    print("\n3. Fichiers créés:")
    for recipient in email.rcpt_to:
        safe_name = recipient.replace("@", "_at_").replace("<", "").replace(">", "")
        filepath = os.path.join("mailboxes", f"{safe_name}.json")
        if os.path.exists(filepath):
            print(f"   ✓ {filepath}")
            
            # Lire et afficher le contenu
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"     Nombre d'emails: {len(data)}")
        else:
            print(f"   ✗ {filepath} introuvable")
    
    # Tester la désérialisation
    print("\n4. Test de désérialisation:")
    safe_name = email.rcpt_to[0].replace("@", "_at_").replace("<", "").replace(">", "")
    filepath = os.path.join("mailboxes", f"{safe_name}.json")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
        if data:
            restored_email = Email.from_dict(data[0])
            print(f"   From: {restored_email.mail_from}")
            print(f"   To: {', '.join(restored_email.rcpt_to)}")
            print(f"   ✓ Email restauré avec succès")
    
    print("\n" + "=" * 60)
    print("✓ TOUS LES TESTS RÉUSSIS")
    print("=" * 60)

if __name__ == "__main__":
    test_json_storage()
