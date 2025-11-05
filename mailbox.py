#!/usr/bin/env python3
"""
Classe MailBox - Gère le stockage des emails dans des fichiers
"""

import os
from email_model import Email


class MailBox:
    """
    Classe pour gérer le stockage des emails dans des fichiers
    Chaque destinataire a sa propre boîte mail (fichier)
    """
    
    def __init__(self, mailbox_dir: str = "mailboxes"):
        """
        Initialise le gestionnaire de boîtes mail
        
        Args:
            mailbox_dir: Répertoire où stocker les boîtes mail
        """
        self.mailbox_dir = mailbox_dir
        self._ensure_mailbox_dir()
    
    def _ensure_mailbox_dir(self) -> None:
        """Crée le répertoire des boîtes mail s'il n'existe pas"""
        if not os.path.exists(self.mailbox_dir):
            os.makedirs(self.mailbox_dir)
    
    def _get_mailbox_path(self, recipient: str) -> str:
        """
        Obtient le chemin du fichier de boîte mail pour un destinataire
        
        Args:
            recipient: Adresse email du destinataire
            
        Returns:
            Chemin complet du fichier de boîte mail
        """
        # Nettoie l'adresse email pour créer un nom de fichier valide
        safe_name = recipient.replace("@", "_at_").replace("<", "").replace(">", "")
        return os.path.join(self.mailbox_dir, f"{safe_name}.mbox")
    
    def store_email(self, email: Email) -> bool:
        """
        Stocke un email dans les boîtes mail de tous ses destinataires
        
        Args:
            email: Email à stocker
            
        Returns:
            True si le stockage a réussi, False sinon
        """
        if not email.is_valid():
            print("Email invalide, impossible de stocker")
            return False
        
        try:
            # Stocke l'email dans la boîte mail de chaque destinataire
            for recipient in email.rcpt_to:
                mailbox_path = self._get_mailbox_path(recipient)
                with open(mailbox_path, 'a', encoding='utf-8') as f:
                    f.write("=" * 80 + "\n")
                    f.write(email.to_string())
                    f.write("=" * 80 + "\n\n")
                print(f"Email stocké dans {mailbox_path}")
            return True
        except Exception as e:
            print(f"Erreur lors du stockage de l'email: {e}")
            return False
    
    def list_mailboxes(self) -> list[str]:
        """
        Liste toutes les boîtes mail existantes
        
        Returns:
            Liste des noms de boîtes mail
        """
        if not os.path.exists(self.mailbox_dir):
            return []
        
        return [f for f in os.listdir(self.mailbox_dir) if f.endswith('.mbox')]
