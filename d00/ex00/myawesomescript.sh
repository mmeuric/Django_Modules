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

# Alternative si un retour chariot \r parasite l'affichage et que tr est interdit :
# curl -sL -o /dev/null -w '%{url_effective}\n' "$1"
# (resout toute la chaine de redirection et n'imprime que l'URL finale, sans \r)
