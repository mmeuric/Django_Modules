#!/bin/bash

# Créer un virtualenv Python3 nommé django_venv
python3 -m venv django_venv

# Installer les dépendances listées dans requirement.txt dans le virtualenv
django_venv/bin/pip install -r requirement.txt

if [ $? -eq 0 ]; then
    echo "Installation successful."
else
    echo "Error: installation failed."
    exit 1
fi

# Activer le virtualenv
# Note : pour que l'activation persiste dans votre shell,
# lancez ce script avec : source my_script.sh
source django_venv/bin/activate
