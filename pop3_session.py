#!/usr/bin/env python3
# Gestion d'une session POP3 client

import socket
from mailbox import MailBox


class POP3Session:

    READY = "+OK POP3 server ready\r\n"
    OK = "+OK\r\n"
    ERR = "-ERR\r\n"

    def __init__(self, client_socket: socket.socket, mailbox: MailBox):
        self.client_socket = client_socket
        self.mailbox = mailbox
        self.current_user: str | None = None
        self.authenticated = False

    # Envoie une réponse au client
    def send_response(self, response: str) -> None:
        self.client_socket.sendall(response.encode('utf-8'))
        print(f">> {response.strip()}")

    # Envoie une réponse multi-lignes (terminée par un ".")
    def send_multiline(self, lines: list[str]) -> None:
        for line in lines:
            if line.startswith('.'):
                line = '.' + line
            self.send_response(line + "\r\n")
        self.send_response(".\r\n")

    # Charge la liste des emails pour l'utilisateur courant
    def _load_messages(self) -> list[dict]:
        if self.current_user is None:
            return []
        return self.mailbox.load_emails(self.current_user)

    # Calcule la taille d'un message POP3 (en octets) à partir d'un dict
    def _message_bytes(self, msg: dict) -> bytes:
        mail_from = msg.get("mail_from", "")
        rcpt_to = msg.get("rcpt_to", [])
        timestamp = msg.get("timestamp", "")
        data = msg.get("data", "")

        headers = []
        if mail_from:
            headers.append(f"From: {mail_from}")
        if rcpt_to:
            if isinstance(rcpt_to, list):
                headers.append("To: " + ", ".join(rcpt_to))
            else:
                headers.append(f"To: {rcpt_to}")
        if timestamp:
            headers.append(f"Date: {timestamp}")

        content = "\r\n".join(headers) + "\r\n\r\n" + str(data)
        return content.encode('utf-8', errors='ignore')

    # Récupère la taille d'un message par index (1..N)
    def _get_message_size(self, messages: list[dict], index: int) -> int | None:
        if index < 1 or index > len(messages):
            return None
        return len(self._message_bytes(messages[index - 1]))

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
                    if not line:
                        continue

                    print(f"<< {line}")
                    if not self.process_command(line):
                        return

        except Exception as e:
            print(f"Erreur dans la session POP3: {e}")
        finally:
            self.client_socket.close()
            print("Connexion POP3 fermée")

    # Traite une commande POP3
    def process_command(self, command: str) -> bool:
        parts = command.split(None, 1)
        cmd = parts[0].upper() if parts else ""
        args = parts[1] if len(parts) > 1 else ""

        if cmd == "USER":
            return self.handle_user(args)
        elif cmd == "PASS":
            return self.handle_pass(args)
        elif cmd == "STAT":
            return self.handle_stat()
        elif cmd == "LIST":
            return self.handle_list(args)
        elif cmd == "RETR":
            return self.handle_retr(args)
        elif cmd == "QUIT":
            return self.handle_quit()
        else:
            self.send_response("-ERR Command not implemented\r\n")
            return True

    def _require_auth(self) -> bool:
        if not self.authenticated or self.current_user is None:
            self.send_response("-ERR Use USER/PASS first\r\n")
            return False
        return True

    # USER <mail>
    def handle_user(self, args: str) -> bool:
        user = args.strip().strip('<>').strip()
        if not user:
            self.send_response("-ERR Missing user\r\n")
            return True

        self.current_user = user
        self.authenticated = False
        self.send_response("+OK\r\n")
        return True

    # PASS <anything> (pas de vérification)
    def handle_pass(self, args: str) -> bool:
        if self.current_user is None:
            self.send_response("-ERR Use USER first\r\n")
            return True

        self.authenticated = True
        self.send_response("+OK\r\n")
        return True

    # STAT
    def handle_stat(self) -> bool:
        if not self._require_auth():
            return True

        messages = self._load_messages()
        sizes = [len(self._message_bytes(m)) for m in messages]
        self.send_response(f"+OK {len(messages)} {sum(sizes)}\r\n")
        return True

    # LIST [msg]
    def handle_list(self, args: str) -> bool:
        if not self._require_auth():
            return True

        messages = self._load_messages()

        arg = args.strip()
        if not arg:
            sizes = [len(self._message_bytes(m)) for m in messages]
            self.send_response(f"+OK {len(messages)} messages\r\n")
            lines = [f"{i + 1} {sizes[i]}" for i in range(len(messages))]
            self.send_multiline(lines)
            return True

        try:
            index = int(arg)
        except ValueError:
            self.send_response("-ERR Invalid message number\r\n")
            return True

        size = self._get_message_size(messages, index)
        if size is None:
            self.send_response("-ERR No such message\r\n")
            return True

        self.send_response(f"+OK {index} {size}\r\n")
        return True

    # RETR <msg>
    def handle_retr(self, args: str) -> bool:
        if not self._require_auth():
            return True

        arg = args.strip()
        if not arg:
            self.send_response("-ERR Missing message number\r\n")
            return True

        try:
            index = int(arg)
        except ValueError:
            self.send_response("-ERR Invalid message number\r\n")
            return True

        messages = self._load_messages()
        if index < 1 or index > len(messages):
            self.send_response("-ERR No such message\r\n")
            return True

        msg_bytes = self._message_bytes(messages[index - 1])
        msg_text = msg_bytes.decode('utf-8', errors='ignore')

        self.send_response(f"+OK {len(msg_bytes)} octets\r\n")
        self.send_multiline(msg_text.splitlines())
        return True

    # QUIT
    def handle_quit(self) -> bool:
        self.send_response("+OK Goodbye\r\n")
        return False
