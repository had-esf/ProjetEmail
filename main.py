#!/usr/bin/env python3
# Point d'entrée du serveur SMTP

from smtp_server import SMTPServer


# Lance le serveur
def main():
    print("=" * 60)
    print("Serveur SMTP - Version 1")
    print("Commandes supportées: MAIL, RCPT, DATA, QUIT, RSET")
    print("=" * 60)
    
    server = SMTPServer(host='', port=2525)
    
    try:
        server.start()
    except KeyboardInterrupt:
        print("\nArrêt du serveur...")
    finally:
        server.stop()


if __name__ == '__main__':
    main()
