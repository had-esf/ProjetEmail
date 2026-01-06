#!/usr/bin/env python3
# Gestion du stockage des emails

import os
import json
from email_model import Email


class MailBox:
    
    # Initialise le gestionnaire de boîtes
    def __init__(self, mailbox_dir: str = "mailboxes"):
        self.mailbox_dir = mailbox_dir
        self._ensure_mailbox_dir()
    
    # Crée le répertoire des boîtes s'il n'existe pas
    def _ensure_mailbox_dir(self) -> None:
        if not os.path.exists(self.mailbox_dir):
            os.makedirs(self.mailbox_dir)
    
    # Chemin du fichier de boîte pour un destinataire
    def _get_mailbox_path(self, recipient: str) -> str:
        safe_name = recipient.replace("@", "_at_").replace("<", "").replace(">", "")
        return os.path.join(self.mailbox_dir, f"{safe_name}.json")
    
    # Stocke l'email pour chaque destinataire
    def store_email(self, email: Email) -> bool:
        if not email.is_valid():
            print("Email invalide, impossible de stocker")
            return False
        
        try:
            for recipient in email.rcpt_to:
                mailbox_path = self._get_mailbox_path(recipient)
                
                emails = []
                if os.path.exists(mailbox_path):
                    with open(mailbox_path, 'r', encoding='utf-8') as f:
                        emails = json.load(f)
                
                emails.append(email.to_dict())
                
                with open(mailbox_path, 'w', encoding='utf-8') as f:
                    json.dump(emails, f, ensure_ascii=False, indent=2)
                
                print(f"Email stocké dans {mailbox_path}")
            return True
        except Exception as e:
            print(f"Erreur lors du stockage de l'email: {e}")
            return False

    # Charge les emails d'un destinataire
    def load_emails(self, recipient: str) -> list[dict]:
        mailbox_path = self._get_mailbox_path(recipient)
        if not os.path.exists(mailbox_path):
            return []

        try:
            with open(mailbox_path, 'r', encoding='utf-8') as f:
                emails = json.load(f)
                if isinstance(emails, list):
                    return emails
        except Exception as e:
            print(f"Erreur lors du chargement de la boîte {mailbox_path}: {e}")

        return []
    
    # Liste les boîtes mail existantes
    def list_mailboxes(self) -> list[str]:
        if not os.path.exists(self.mailbox_dir):
            return []
        
        return [f for f in os.listdir(self.mailbox_dir) if f.endswith('.json')]

