from elem import Elem, Text


class Html(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__('html', attr, content, 'double')


class Head(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__('head', attr, content, 'double')


class Body(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__('body', attr, content, 'double')


class Title(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__('title', attr, content, 'double')


class Meta(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__('meta', attr, content, 'simple')


class Img(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__('img', attr, content, 'simple')


class Table(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__('table', attr, content, 'double')


class Th(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__('th', attr, content, 'double')


class Tr(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__('tr', attr, content, 'double')


class Td(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__('td', attr, content, 'double')


class Ul(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__('ul', attr, content, 'double')


class Ol(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__('ol', attr, content, 'double')


class Li(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__('li', attr, content, 'double')


class H1(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__('h1', attr, content, 'double')


class H2(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__('h2', attr, content, 'double')


class P(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__('p', attr, content, 'double')


class Div(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__('div', attr, content, 'double')


class Span(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__('span', attr, content, 'double')


class Hr(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__('hr', attr, content, 'simple')


class Br(Elem):
    def __init__(self, content=None, attr={}):
        super().__init__('br', attr, content, 'simple')


if __name__ == '__main__':
    # Test basique demandé par le sujet
    print(Html([Head(), Body()]))
    print()

    # Reproduction de la structure HTML de l'ex04
    page = Html([
        Head([Title(Text('Hello ground!'))]),
        Body([
            H1(Text('Oh no, not again!')),
            Img(attr={'src': 'http://i.imgur.com/pfp3T.jpg'})
        ])
    ])
    print(page)
    print()

    # Tests couvrant toutes les classes
    print("--- Tests de toutes les classes ---")
    print(Meta(attr={'charset': 'UTF-8'}))
    print(Hr())
    print(Br())
    print(P(Text('Un paragraphe.')))
    print(Span(Text('Un span.')))
    print(H2(Text('Titre niveau 2')))
    print(Div([P(Text('Dans un div.'))]))
    print(Ul([Li(Text('Item 1')), Li(Text('Item 2'))]))
    print(Ol([Li(Text('Premier')), Li(Text('Deuxième'))]))
    print(Table([
        Tr([Th(Text('Col 1')), Th(Text('Col 2'))]),
        Tr([Td(Text('Val 1')), Td(Text('Val 2'))])
    ]))
