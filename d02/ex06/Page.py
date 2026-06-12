from elem import Elem, Text
from elements import (Html, Head, Body, Title, Meta, Img, Table, Th, Tr, Td,
                      Ul, Ol, Li, H1, H2, P, Div, Span, Hr, Br)


class Page:

    def __init__(self, elem):
        self.elem = elem

    def __str__(self):
        if isinstance(self.elem, Html):
            return '<!DOCTYPE html>\n' + str(self.elem)
        return str(self.elem)

    def write_to_file(self, filename):
        with open(filename, 'w') as f:
            f.write(str(self))

    def is_valid(self):
        try:
            return self._validate(self.elem)
        except Exception:
            return False

    def _validate(self, elem):
        allowed_types = (Html, Head, Body, Title, Meta, Img, Table, Th, Tr, Td,
                         Ul, Ol, Li, H1, H2, P, Div, Span, Hr, Br, Text)

        if not isinstance(elem, allowed_types):
            return False

        # Les Text sont des feuilles : toujours valides
        if isinstance(elem, Text):
            return True

        content = elem.content

        if isinstance(elem, Html):
            # Exactement [Head, Body] dans cet ordre
            if len(content) != 2:
                return False
            if not isinstance(content[0], Head) or not isinstance(content[1], Body):
                return False

        elif isinstance(elem, Head):
            # Exactement un Title, rien d'autre
            if len(content) != 1 or not isinstance(content[0], Title):
                return False

        elif isinstance(elem, (Body, Div)):
            # H1, H2, Div, Table, Ul, Ol, Span, Text uniquement
            allowed = (H1, H2, Div, Table, Ul, Ol, Span, Text)
            if not all(isinstance(c, allowed) for c in content):
                return False

        elif isinstance(elem, (Title, H1, H2, Li, Th, Td)):
            # Exactement un Text
            if len(content) != 1 or not isinstance(content[0], Text):
                return False

        elif isinstance(elem, P):
            # Uniquement des Text
            if not all(isinstance(c, Text) for c in content):
                return False

        elif isinstance(elem, Span):
            # Text ou P uniquement
            if not all(isinstance(c, (Text, P)) for c in content):
                return False

        elif isinstance(elem, (Ul, Ol)):
            # Au moins un Li, uniquement des Li
            if len(content) == 0 or not all(isinstance(c, Li) for c in content):
                return False

        elif isinstance(elem, Tr):
            # Au moins un Th ou Td, mutuellement exclusifs
            if len(content) == 0:
                return False
            has_th = any(isinstance(c, Th) for c in content)
            has_td = any(isinstance(c, Td) for c in content)
            if has_th and has_td:
                return False
            if not all(isinstance(c, (Th, Td)) for c in content):
                return False

        elif isinstance(elem, Table):
            # Uniquement des Tr
            if not all(isinstance(c, Tr) for c in content):
                return False

        # Validation récursive de tous les enfants
        return all(self._validate(child) for child in content)


if __name__ == '__main__':
    # --- Pages valides ---

    # Page HTML complète valide
    page_valide = Page(Html([
        Head([Title(Text('Mon super CV'))]),
        Body([
            H1(Text('Jean Dupont')),
            H2(Text('Développeur Python')),
            Div([
                Span(Text('Compétences : Python, Django, Git')),
                Ul([Li(Text('Python')), Li(Text('Django')), Li(Text('Git'))]),
            ]),
            Table([
                Tr([Th(Text('Compétence')), Th(Text('Niveau'))]),
                Tr([Td(Text('Python')), Td(Text('Expert'))]),
                Tr([Td(Text('Django')), Td(Text('Avancé'))]),
            ])
        ])
    ]))
    print("=== Page valide ===")
    print("is_valid():", page_valide.is_valid())
    print(page_valide)
    page_valide.write_to_file('cv.html')
    print("Fichier cv.html écrit.")
    print()

    # Fragment Span en racine : pas de DOCTYPE
    fragment = Page(Span([Text('Juste un fragment.')]))
    print("=== Fragment Span (pas de DOCTYPE) ===")
    print("is_valid():", fragment.is_valid())
    print(fragment)
    print()

    # --- Pages invalides ---

    # Head avec deux Title
    inv1 = Page(Html([
        Head([Title(Text('A')), Title(Text('B'))]),
        Body([H1(Text('Titre'))])
    ]))
    print("=== Invalide : Head avec deux Title ===")
    print("is_valid():", inv1.is_valid())
    print()

    # Body contient un P directement (interdit selon les règles)
    inv2 = Page(Html([
        Head([Title(Text('Test'))]),
        Body([P(Text('Interdit dans body'))])
    ]))
    print("=== Invalide : P directement dans Body ===")
    print("is_valid():", inv2.is_valid())
    print()

    # Tr avec mix Th et Td
    inv3 = Page(Html([
        Head([Title(Text('Test'))]),
        Body([
            Table([Tr([Th(Text('Header')), Td(Text('Data'))])])
        ])
    ]))
    print("=== Invalide : Tr avec Th ET Td ===")
    print("is_valid():", inv3.is_valid())
    print()

    # Ul vide
    inv4 = Page(Html([
        Head([Title(Text('Test'))]),
        Body([Ul([])])
    ]))
    print("=== Invalide : Ul vide ===")
    print("is_valid():", inv4.is_valid())
    print()

    # Html avec mauvais ordre (Body avant Head)
    inv5 = Page(Html([
        Body([H1(Text('Titre'))]),
        Head([Title(Text('Test'))])
    ]))
    print("=== Invalide : Body avant Head ===")
    print("is_valid():", inv5.is_valid())
    print()

    # H1 avec deux Text
    inv6 = Page(Html([
        Head([Title(Text('Test'))]),
        Body([H1([Text('A'), Text('B')])])
    ]))
    print("=== Invalide : H1 avec deux Text ===")
    print("is_valid():", inv6.is_valid())
