#!/usr/bin/env python3
"""
Classe Email - Représente un email avec ses informations de base
"""

from datetime import datetime
from typing import Optional


class Email:
    """
    Classe représentant un email avec ses métadonnées
    """
    
    def __init__(self):
        """Initialise un email vide"""
        self.mail_from: Optional[str] = None
        self.rcpt_to: list[str] = []
        self.data: Optional[str] = None
        self.timestamp: datetime = datetime.now()
    
    def set_mail_from(self, sender: str) -> None:
        """
        Définit l'expéditeur de l'email
        
        Args:
            sender: Adresse email de l'expéditeur
        """
        self.mail_from = sender
    
    def add_recipient(self, recipient: str) -> None:
        """
        Ajoute un destinataire à l'email
        
        Args:
            recipient: Adresse email du destinataire
        """
        if recipient not in self.rcpt_to:
            self.rcpt_to.append(recipient)
    
    def set_data(self, content: str) -> None:
        """
        Définit le contenu de l'email
        
        Args:
            content: Contenu du message
        """
        self.data = content
    
    def is_valid(self) -> bool:
        """
        Vérifie si l'email est valide (a un expéditeur, au moins un destinataire et du contenu)
        
        Returns:
            True si l'email est valide, False sinon
        """
        return (self.mail_from is not None and 
                len(self.rcpt_to) > 0 and 
                self.data is not None)
    
    def to_dict(self) -> dict:
        """
        Convertit l'email en dictionnaire pour sérialisation JSON
        
        Returns:
            Dictionnaire contenant les données de l'email
        """
        return {
            "mail_from": self.mail_from,
            "rcpt_to": self.rcpt_to,
            "data": self.data,
            "timestamp": self.timestamp.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Email':
        """
        Crée un email à partir d'un dictionnaire
        
        Args:
            data: Dictionnaire contenant les données de l'email
            
        Returns:
            Instance d'Email
        """
        email = cls()
        email.mail_from = data.get("mail_from")
        email.rcpt_to = data.get("rcpt_to", [])
        email.data = data.get("data")
        if "timestamp" in data:
            email.timestamp = datetime.fromisoformat(data["timestamp"])
        return email
