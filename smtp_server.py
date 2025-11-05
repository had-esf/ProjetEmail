#!/usr/bin/env python3
"""
Classe SMTPServer - Serveur SMTP principal
"""

import socket
import threading
from smtp_session import SMTPSession
from mailbox import MailBox


class SMTPServer:
    """
    Serveur SMTP qui écoute les connexions et crée des sessions
    """
    
    def __init__(self, host: str = '', port: int = 2525):
        """
        Initialise le serveur SMTP
        
        Args:
            host: Adresse d'écoute ('' pour toutes les interfaces)
            port: Port d'écoute (2525 par défaut, port non privilégié)
        """
        self.host = host
        self.port = port
        self.mailbox = MailBox()
        self.running = False
        self.server_socket = None
    
    def start(self) -> None:
        """Démarre le serveur SMTP"""
        try:
            # Crée la socket d'écoute
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Permet de réutiliser l'adresse immédiatement après fermeture
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # Lie la socket au port
            self.server_socket.bind((self.host, self.port))
            # Met en écoute
            self.server_socket.listen(5)
            self.running = True
            
            print(f"Serveur SMTP démarré sur {self.host if self.host else '*'}:{self.port}")
            print("En attente de connexions...")
            
            # Boucle d'acceptation des connexions
            while self.running:
                try:
                    # Accepte une nouvelle connexion
                    client_socket, client_address = self.server_socket.accept()
                    print(f"\nNouvelle connexion de {client_address}")
                    
                    # Crée un thread pour gérer la session
                    session = SMTPSession(client_socket, self.mailbox)
                    thread = threading.Thread(target=session.handle_connection)
                    thread.daemon = True  # Le thread se termine avec le programme
                    thread.start()
                    
                except KeyboardInterrupt:
                    print("\nArrêt du serveur demandé...")
                    break
                except Exception as e:
                    if self.running:
                        print(f"Erreur lors de l'acceptation d'une connexion: {e}")
        
        except Exception as e:
            print(f"Erreur lors du démarrage du serveur: {e}")
        
        finally:
            self.stop()
    
    def stop(self) -> None:
        """Arrête le serveur SMTP"""
        self.running = False
        if self.server_socket:
            try:
                self.server_socket.close()
                print("Serveur SMTP arrêté")
            except Exception as e:
                print(f"Erreur lors de la fermeture du serveur: {e}")
