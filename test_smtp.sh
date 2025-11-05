#!/bin/bash
# Script de test pour le serveur SMTP
# Ce script envoie un email de test au serveur SMTP

echo "=========================================="
echo "Test du serveur SMTP - Version 1"
echo "=========================================="
echo ""
echo "Assurez-vous que le serveur est démarré sur le port 2525"
echo "Envoi d'un email de test..."
echo ""

# Envoie les commandes SMTP au serveur
(
echo "MAIL FROM:<test@example.com>"
sleep 0.1
echo "RCPT TO:<user1@example.com>"
sleep 0.1
echo "DATA"
sleep 0.1
echo "Subject: Test Email"
echo ""
echo "Ceci est un message de test automatique."
echo "Ligne 2 du message."
echo "."
sleep 0.1
echo "QUIT"
) | nc localhost 2525

echo ""
echo "=========================================="
echo "Test terminé"
echo "Vérifiez le répertoire mailboxes/ pour voir l'email stocké"
echo "=========================================="
