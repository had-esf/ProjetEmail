#!/usr/bin/env python3
"""
Point d'entrée du serveur SMTP - Version 1
Gère les commandes MAIL, RCPT et DATA
"""

from smtp_server import SMTPServer


def main():
    """Fonction principale pour démarrer le serveur SMTP"""
    print("=" * 60)
    print("Serveur SMTP - Version 1")
    print("Commandes supportées: MAIL, RCPT, DATA, QUIT, RSET")
    print("=" * 60)
    
    # Crée et démarre le serveur sur le port 2525
    # (port non privilégié, pas besoin de sudo)
    server = SMTPServer(host='', port=2525)
    
    try:
        server.start()
    except KeyboardInterrupt:
        print("\nArrêt du serveur...")
    finally:
        server.stop()


if __name__ == '__main__':
    main()
