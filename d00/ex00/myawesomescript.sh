#!/bin/sh
# ex00 - Affiche l'URL reelle vers laquelle pointe un lien bit.ly.
# Commandes autorisees uniquement : curl, grep, cut
#
# Usage : ./myawesomescript.sh bit.ly/1O72s3U
#
# bit.ly renvoie une redirection HTTP (3xx) avec un en-tete "Location:".
# curl -sI    : requete HEAD, en-tetes seulement, mode silencieux.
# grep -i     : isole la ligne location (insensible a la casse).
# cut -d ' '  : extrait l'URL (2e champ apres "location: ").
curl -sI "$1" | grep -i '^location:' | cut -d ' ' -f 2


