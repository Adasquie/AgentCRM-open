#!/bin/bash

echo "🔁 Chargement des variables d’environnement depuis .env"
export $(grep -v '^#' .env | xargs)

echo "🧼 Arrêt des processus MCP précédents s'ils existent"
pkill -f "python src/server/server.py" 2>/dev/null || true

echo "⚙️ Démarrage du MCP Server (en arrière-plan)"
python3 src/server/server.py &

echo "💬 Démarrage du bot Telegram"
python3 main.py