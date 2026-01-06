#!/usr/bin/env python3
# Point d'entrée du serveur SMTP

import threading
from smtp_server import SMTPServer
from pop3_server import POP3Server


# Lance le serveur
def main():
    print("=" * 60)
    print("Serveur SMTP/POP3 - Version 3")
    print("SMTP: MAIL, RCPT, DATA, QUIT, RSET, EHLO, HELO")
    print("POP3: USER, PASS, STAT, LIST, RETR, QUIT")
    print("=" * 60)
    
    server = SMTPServer(host='', port=2525)
    pop3_server = POP3Server(host='', port=2110)
    pop3_thread = threading.Thread(target=pop3_server.start)
    pop3_thread.daemon = True
    pop3_thread.start()
    
    try:
        server.start()
    except KeyboardInterrupt:
        print("\nArrêt du serveur...")
    finally:
        server.stop()
        pop3_server.stop()


if __name__ == '__main__':
    main()
