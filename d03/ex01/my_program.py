import sys


def main():
    sys.path.insert(0, './local_lib')
    from path import Path

    # Créer un dossier
    d = Path('my_directory')
    d.mkdir_p()

    # Créer un fichier dans ce dossier et écrire dedans
    f = d / 'my_file.txt'
    f.write_text('Hello from path.py!\nThis file was created using the path library.\n')

    # Lire et afficher le contenu du fichier
    content = f.read_text()
    print(content)


if __name__ == '__main__':
    main()
