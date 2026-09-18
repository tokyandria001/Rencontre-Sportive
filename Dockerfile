FROM alpine:3.20
WORKDIR /app
COPY . .
# Aucune stack connue détectée automatiquement.
# Adaptez l'image de base, l'installation des dépendances et la commande de démarrage.
CMD ["true"]
