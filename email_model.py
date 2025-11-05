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
    
    def to_string(self) -> str:
        """
        Convertit l'email en format texte pour stockage
        
        Returns:
            Représentation textuelle de l'email
        """
        result = f"From: {self.mail_from}\n"
        result += f"Date: {self.timestamp.strftime('%a, %d %b %Y %H:%M:%S')}\n"
        for recipient in self.rcpt_to:
            result += f"To: {recipient}\n"
        result += "\n"
        result += self.data
        result += "\n"
        return result
