#!/bin/bash

# Afficher la version de pip utilisée
pip --version

# Installer la version de développement de path.py depuis GitHub
# dans le dossier local_lib (--upgrade écrase une installation existante)
pip install --upgrade --target=./local_lib \
    git+https://github.com/jaraco/path.git \
    2>&1 | tee install.log
PIP_STATUS=${PIPESTATUS[0]}

# Si l'installation a réussi, exécuter le programme Python
if [ $PIP_STATUS -eq 0 ]; then
    python3 my_program.py
else
    echo "Error: installation of path.py failed. Check install.log for details."
    exit 1
fi
