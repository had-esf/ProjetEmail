#!/usr/bin/env python3
# Modèle de données pour un email

from datetime import datetime
from typing import Optional


class Email:
    
    def __init__(self):
        self.mail_from: Optional[str] = None
        self.rcpt_to: list[str] = []
        self.data: Optional[str] = None
        self.timestamp: datetime = datetime.now()
    
    # Définit l'expéditeur
    def set_mail_from(self, sender: str) -> None:  
        self.mail_from = sender
    
    # Ajoute un destinataire
    def add_recipient(self, recipient: str) -> None:
        if recipient not in self.rcpt_to:
            self.rcpt_to.append(recipient)
    
    # Définit le contenu
    def set_data(self, content: str) -> None:
        self.data = content
    
    # Vérifie la validité de l'email
    def is_valid(self) -> bool:
        return (self.mail_from is not None and 
                len(self.rcpt_to) > 0 and 
                self.data is not None)
    
    # Convertit l'email en dictionnaire
    def to_dict(self) -> dict:
        return {
            "mail_from": self.mail_from,
            "rcpt_to": self.rcpt_to,
            "data": self.data,
            "timestamp": self.timestamp.isoformat()
        }
    
    # Crée un email à partir d'un dictionnaire
    @classmethod
    def from_dict(cls, data: dict) -> 'Email':
        email = cls()
        email.mail_from = data.get("mail_from")
        email.rcpt_to = data.get("rcpt_to", [])
        email.data = data.get("data")
        if "timestamp" in data:
            email.timestamp = datetime.fromisoformat(data["timestamp"])
        return email

