#!/usr/bin/env python3
# Gestion d'une session SMTP client

import socket
from email_model import Email
from mailbox import MailBox


class SMTPSession:
    
    READY = "220 Service ready\r\n"
    OK = "250 OK\r\n"
    START_MAIL_INPUT = "354 Start mail input; end with <CRLF>.<CRLF>\r\n"
    CLOSING = "221 Service closing transmission channel\r\n"
    SYNTAX_ERROR = "500 Syntax error, command unrecognized\r\n"
    BAD_SEQUENCE = "503 Bad sequence of commands\r\n"
    COMMAND_NOT_IMPLEMENTED = "502 Command not implemented\r\n"
    
    def __init__(self, client_socket: socket.socket, mailbox: MailBox):
        self.client_socket = client_socket
        self.mailbox = mailbox
        self.current_email: Email = Email()
        self.in_data_mode = False
        self.mail_from_received = False
        self.rcpt_to_received = False
        self.helo_received = False
    
    # Envoie une réponse au client
    def send_response(self, response: str) -> None:
        self.client_socket.sendall(response.encode('utf-8'))
        print(f">> {response.strip()}")
    
    # Gère la connexion
    def handle_connection(self) -> None:
        try:
            self.send_response(self.READY)
            
            buffer = ""
            while True:
                data = self.client_socket.recv(1024).decode('utf-8', errors='ignore')
                if not data:
                    break
                
                buffer += data
                
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    line = line.rstrip('\r')
                    
                    if not self.in_data_mode:
                        print(f"<< {line}")
                        if not self.process_command(line):
                            break
                    else:
                        if line == '.':
                            self.in_data_mode = False
                            if self.mailbox.store_email(self.current_email):
                                self.send_response(self.OK)
                            else:
                                self.send_response("554 Transaction failed\r\n")
                            self.reset_email()
                        else:
                            if self.current_email.data is None:
                                self.current_email.data = line + "\n"
                            else:
                                self.current_email.data += line + "\n"
                
        except Exception as e:
            print(f"Erreur dans la session: {e}")
        finally:
            self.client_socket.close()
            print("Connexion fermée")
    
    # Traite une commande SMTP
    def process_command(self, command: str) -> bool:
        if not command:
            return True
        
        parts = command.split(None, 1)
        cmd = parts[0].upper() if parts else ""
        args = parts[1] if len(parts) > 1 else ""
        
        if cmd == "EHLO":
            return self.handle_ehlo(args)
        elif cmd == "HELO":
            return self.handle_helo(args)
        elif cmd == "MAIL":
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
    
    # Commande EHLO (version étendue non supportée)
    def handle_ehlo(self, args: str) -> bool:
        self.send_response(self.COMMAND_NOT_IMPLEMENTED)
        return True
    
    # Commande HELO
    def handle_helo(self, args: str) -> bool:
        self.helo_received = True
        self.send_response(self.OK)
        return True
    
    # Commande MAIL FROM
    def handle_mail(self, args: str) -> bool:
        if not args.upper().startswith("FROM:"):
            self.send_response(self.SYNTAX_ERROR)
            return True
        
        sender = args[5:].strip()
        sender = sender.strip('<>')
        
        self.current_email.set_mail_from(sender)
        self.mail_from_received = True
        self.send_response(self.OK)
        return True
    
    # Commande RCPT TO
    def handle_rcpt(self, args: str) -> bool:
        if not self.mail_from_received:
            self.send_response(self.BAD_SEQUENCE)
            return True
        
        if not args.upper().startswith("TO:"):
            self.send_response(self.SYNTAX_ERROR)
            return True
        
        recipient = args[3:].strip()
        recipient = recipient.strip('<>')
        
        self.current_email.add_recipient(recipient)
        self.rcpt_to_received = True
        self.send_response(self.OK)
        return True
    
    # Commande DATA
    def handle_data(self) -> bool:
        if not self.mail_from_received or not self.rcpt_to_received:
            self.send_response(self.BAD_SEQUENCE)
            return True
        
        self.in_data_mode = True
        self.send_response(self.START_MAIL_INPUT)
        return True
    
    # Commande QUIT
    def handle_quit(self) -> bool:
        self.send_response(self.CLOSING)
        return False
    
    # Commande RSET
    def handle_rset(self) -> bool:
        self.reset_email()
        self.send_response(self.OK)
        return True
    
    # Réinitialise l'état
    def reset_email(self) -> None:
        self.current_email = Email()
        self.mail_from_received = False
        self.rcpt_to_received = False
        self.in_data_mode = False

