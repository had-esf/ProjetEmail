#!/usr/bin/env python3
"""
Client de test pour le serveur SMTP
"""

import socket
import time


def test_smtp_server():
    """Test le serveur SMTP avec une session complète"""
    print("=" * 60)
    print("Test du serveur SMTP - Version 1")
    print("=" * 60)
    
    try:
        # Connexion au serveur
        print("\n1. Connexion au serveur...")
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', 2525))
        
        # Lecture du message de bienvenue
        response = client.recv(1024).decode('utf-8')
        print(f"<< {response.strip()}")
        
        # Test MAIL FROM
        print("\n2. Test commande MAIL FROM...")
        client.sendall(b"MAIL FROM:<alice@example.com>\r\n")
        response = client.recv(1024).decode('utf-8')
        print(f"<< {response.strip()}")
        
        # Test RCPT TO
        print("\n3. Test commande RCPT TO...")
        client.sendall(b"RCPT TO:<bob@example.com>\r\n")
        response = client.recv(1024).decode('utf-8')
        print(f"<< {response.strip()}")
        
        # Test RCPT TO multiple
        print("\n4. Test second RCPT TO...")
        client.sendall(b"RCPT TO:<charlie@example.com>\r\n")
        response = client.recv(1024).decode('utf-8')
        print(f"<< {response.strip()}")
        
        # Test DATA
        print("\n5. Test commande DATA...")
        client.sendall(b"DATA\r\n")
        response = client.recv(1024).decode('utf-8')
        print(f"<< {response.strip()}")
        
        # Envoi du contenu
        print("\n6. Envoi du contenu de l'email...")
        email_content = """Subject: Test Email
From: Alice <alice@example.com>
To: Bob <bob@example.com>

Bonjour Bob,

Ceci est un email de test pour le serveur SMTP.

Cordialement,
Alice
.\r
"""
        client.sendall(email_content.encode('utf-8'))
        response = client.recv(1024).decode('utf-8')
        print(f"<< {response.strip()}")
        
        # Test QUIT
        print("\n7. Test commande QUIT...")
        client.sendall(b"QUIT\r\n")
        response = client.recv(1024).decode('utf-8')
        print(f"<< {response.strip()}")
        
        # Fermeture
        client.close()
        
        print("\n" + "=" * 60)
        print("✓ Test réussi!")
        print("Vérifiez le répertoire mailboxes/ pour voir les emails stockés")
        print("=" * 60)
        
        return True
        
    except ConnectionRefusedError:
        print("\n✗ Erreur: Impossible de se connecter au serveur")
        print("Assurez-vous que le serveur est démarré sur le port 2525")
        return False
        
    except Exception as e:
        print(f"\n✗ Erreur lors du test: {e}")
        return False


if __name__ == '__main__':
    test_smtp_server()
