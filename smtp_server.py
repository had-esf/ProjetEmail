#!/usr/bin/env python3
# Serveur SMTP principal

import socket
import threading
from smtp_session import SMTPSession
from mailbox import MailBox


class SMTPServer:
    
    def __init__(self, host: str = '', port: int = 2525):
        self.host = host
        self.port = port
        self.mailbox = MailBox()
        self.running = False
        self.server_socket = None
    
    # Démarre le serveur
    def start(self) -> None:
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.running = True
            
            print(f"Serveur SMTP démarré sur {self.host if self.host else '*'}:{self.port}")
            print("En attente de connexions...")
            
            while self.running:
                try:
                    client_socket, client_address = self.server_socket.accept()
                    print(f"\nNouvelle connexion de {client_address}")
                    
                    session = SMTPSession(client_socket, self.mailbox)
                    thread = threading.Thread(target=session.handle_connection)
                    thread.daemon = True
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
    
    # Arrête le serveur
    def stop(self) -> None:
        self.running = False
        if self.server_socket:
            try:
                self.server_socket.close()
                print("Serveur SMTP arrêté")
            except Exception as e:
                print(f"Erreur lors de la fermeture du serveur: {e}")

