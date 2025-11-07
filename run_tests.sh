#!/bin/bash
# Script de test complet pour le serveur SMTP Version 1

echo "=========================================="
echo "Tests du Serveur SMTP - Version 1"
echo "=========================================="
echo ""

# Vérification que le serveur n'est pas déjà lancé
if lsof -Pi :2525 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "⚠ Le port 2525 est déjà utilisé"
    echo "Arrêt du processus existant..."
    pkill -f "python3 main.py"
    sleep 1
fi

# Nettoyage des anciennes boîtes mail
echo "1. Nettoyage des anciennes boîtes mail..."
rm -rf mailboxes/
echo "✓ Nettoyé"
echo ""

# Compilation des fichiers Python
echo "2. Vérification de la syntaxe Python..."
python3 -m py_compile email_model.py mailbox.py smtp_session.py smtp_server.py main.py test_client.py 2>&1
if [ $? -eq 0 ]; then
    echo "✓ Tous les fichiers Python sont valides"
else
    echo "✗ Erreur de syntaxe détectée"
    exit 1
fi
echo ""

# Démarrage du serveur en arrière-plan
echo "3. Démarrage du serveur SMTP..."
python3 main.py > /tmp/smtp_server.log 2>&1 &
SERVER_PID=$!
sleep 2

# Vérification que le serveur est bien démarré
if ! ps -p $SERVER_PID > /dev/null 2>&1; then
    echo "✗ Le serveur n'a pas démarré correctement"
    cat /tmp/smtp_server.log
    exit 1
fi
echo "✓ Serveur démarré (PID: $SERVER_PID)"
echo ""

# Exécution du client de test
echo "4. Exécution des tests..."
echo ""
python3 test_client.py
TEST_RESULT=$?
echo ""

# Vérification des boîtes mail créées
echo "5. Vérification des boîtes mail..."
if [ -d "mailboxes" ] && [ "$(ls -A mailboxes)" ]; then
    echo "✓ Boîtes mail créées:"
    ls -lh mailboxes/
    echo ""
    echo "Contenu de la première boîte mail:"
    echo "-----------------------------------"
    cat mailboxes/*.json | head -20
    echo "-----------------------------------"
else
    echo "✗ Aucune boîte mail créée"
    TEST_RESULT=1
fi
echo ""

# Arrêt du serveur
echo "6. Arrêt du serveur..."
kill $SERVER_PID 2>/dev/null
wait $SERVER_PID 2>/dev/null
echo "✓ Serveur arrêté"
echo ""

# Résultat final
echo "=========================================="
if [ $TEST_RESULT -eq 0 ]; then
    echo "✓ TOUS LES TESTS RÉUSSIS"
    echo "Le serveur SMTP Version 1 est fonctionnel!"
else
    echo "✗ CERTAINS TESTS ONT ÉCHOUÉ"
    echo "Consultez les logs pour plus de détails"
fi
echo "=========================================="

exit $TEST_RESULT
