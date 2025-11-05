#!/usr/bin/env python3
"""
Classe SMTPSession - Gère une session SMTP avec un client
"""

import socket
from email_model import Email
from mailbox import MailBox


class SMTPSession:
    """
    Gère une session SMTP avec un client
    Implémente les commandes MAIL, RCPT et DATA pour la version 1
    """
    
    # Codes de réponse SMTP
    READY = "220 Service ready\r\n"
    OK = "250 OK\r\n"
    START_MAIL_INPUT = "354 Start mail input; end with <CRLF>.<CRLF>\r\n"
    CLOSING = "221 Service closing transmission channel\r\n"
    SYNTAX_ERROR = "500 Syntax error, command unrecognized\r\n"
    BAD_SEQUENCE = "503 Bad sequence of commands\r\n"
    
    def __init__(self, client_socket: socket.socket, mailbox: MailBox):
        """
        Initialise une session SMTP
        
        Args:
            client_socket: Socket de connexion avec le client
            mailbox: Gestionnaire de boîtes mail
        """
        self.client_socket = client_socket
        self.mailbox = mailbox
        self.current_email: Email = Email()
        self.in_data_mode = False
        self.mail_from_received = False
        self.rcpt_to_received = False
    
    def send_response(self, response: str) -> None:
        """
        Envoie une réponse au client
        
        Args:
            response: Réponse à envoyer
        """
        self.client_socket.sendall(response.encode('utf-8'))
        print(f">> {response.strip()}")
    
    def handle_connection(self) -> None:
        """Gère la connexion avec le client"""
        try:
            # Envoie le message de bienvenue
            self.send_response(self.READY)
            
            buffer = ""
            while True:
                # Réception des données
                data = self.client_socket.recv(1024).decode('utf-8', errors='ignore')
                if not data:
                    break
                
                buffer += data
                
                # Traite les commandes ligne par ligne
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    line = line.rstrip('\r')
                    
                    if not self.in_data_mode:
                        # Mode commande
                        print(f"<< {line}")
                        if not self.process_command(line):
                            break
                    else:
                        # Mode DATA
                        if line == '.':
                            # Fin du message
                            self.in_data_mode = False
                            # Stocke l'email
                            if self.mailbox.store_email(self.current_email):
                                self.send_response(self.OK)
                            else:
                                self.send_response("554 Transaction failed\r\n")
                            # Réinitialise pour un nouvel email
                            self.reset_email()
                        else:
                            # Ajoute la ligne au contenu de l'email
                            if self.current_email.data is None:
                                self.current_email.data = line + "\n"
                            else:
                                self.current_email.data += line + "\n"
                
        except Exception as e:
            print(f"Erreur dans la session: {e}")
        finally:
            self.client_socket.close()
            print("Connexion fermée")
    
    def process_command(self, command: str) -> bool:
        """
        Traite une commande SMTP
        
        Args:
            command: Commande reçue du client
            
        Returns:
            True pour continuer, False pour fermer la connexion
        """
        if not command:
            return True
        
        # Sépare la commande de ses arguments
        parts = command.split(None, 1)
        cmd = parts[0].upper() if parts else ""
        args = parts[1] if len(parts) > 1 else ""
        
        # Traitement des commandes
        if cmd == "MAIL":
            return self.handle_mail(args)
        elif cmd == "RCPT":
            return self.handle_rcpt(args)
        elif cmd == "DATA":
            return self.handle_data()
        elif cmd == "QUIT":
            return self.handle_quit()
        elif cmd == "RSET":
            return self.handle_rset()
        else:
            self.send_response(self.SYNTAX_ERROR)
            return True
    
    def handle_mail(self, args: str) -> bool:
        """
        Gère la commande MAIL FROM
        
        Args:
            args: Arguments de la commande
            
        Returns:
            True pour continuer
        """
        if not args.upper().startswith("FROM:"):
            self.send_response(self.SYNTAX_ERROR)
            return True
        
        # Extrait l'adresse email
        sender = args[5:].strip()
        # Supprime les < > si présents
        sender = sender.strip('<>')
        
        self.current_email.set_mail_from(sender)
        self.mail_from_received = True
        self.send_response(self.OK)
        return True
    
    def handle_rcpt(self, args: str) -> bool:
        """
        Gère la commande RCPT TO
        
        Args:
            args: Arguments de la commande
            
        Returns:
            True pour continuer
        """
        if not self.mail_from_received:
            self.send_response(self.BAD_SEQUENCE)
            return True
        
        if not args.upper().startswith("TO:"):
            self.send_response(self.SYNTAX_ERROR)
            return True
        
        # Extrait l'adresse email
        recipient = args[3:].strip()
        # Supprime les < > si présents
        recipient = recipient.strip('<>')
        
        self.current_email.add_recipient(recipient)
        self.rcpt_to_received = True
        self.send_response(self.OK)
        return True
    
    def handle_data(self) -> bool:
        """
        Gère la commande DATA
        
        Returns:
            True pour continuer
        """
        if not self.mail_from_received or not self.rcpt_to_received:
            self.send_response(self.BAD_SEQUENCE)
            return True
        
        self.in_data_mode = True
        self.send_response(self.START_MAIL_INPUT)
        return True
    
    def handle_quit(self) -> bool:
        """
        Gère la commande QUIT
        
        Returns:
            False pour fermer la connexion
        """
        self.send_response(self.CLOSING)
        return False
    
    def handle_rset(self) -> bool:
        """
        Gère la commande RSET (réinitialisation)
        
        Returns:
            True pour continuer
        """
        self.reset_email()
        self.send_response(self.OK)
        return True
    
    def reset_email(self) -> None:
        """Réinitialise l'état pour un nouvel email"""
        self.current_email = Email()
        self.mail_from_received = False
        self.rcpt_to_received = False
        self.in_data_mode = False
