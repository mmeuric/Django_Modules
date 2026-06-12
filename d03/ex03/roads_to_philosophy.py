import sys
import requests
from bs4 import BeautifulSoup


def get_page(url):
    """Récupère le contenu HTML d'une page Wikipedia."""
    headers = {"User-Agent": "Mozilla/5.0 (roads-to-philosophy bot)"}
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    return response.text


def get_title(soup):
    """Retourne le titre principal de la page (h1#firstHeading)."""
    heading = soup.find(id="firstHeading")
    return heading.get_text().strip() if heading else None


def is_valid_link(tag, excluded_prefixes):
    """
    Vérifie qu'un tag <a> est un lien vers un article Wikipedia valide :
    - href commence par /wiki/
    - pas de préfixe exclu (Help:, Wikipedia:, File:, etc.)
    - pas dans une balise italique (<i> ou <em>)
    """
    href = tag.get("href", "")
    if not href.startswith("/wiki/"):
        return False
    for prefix in excluded_prefixes:
        if href.startswith(prefix):
            return False
    for parent in tag.parents:
        if parent.name in ("i", "em"):
            return False
        if parent.name in ("p", "div", "td", "body"):
            break
    return True


def get_links_outside_parentheses(paragraph):
    """
    Parcourt les enfants directs d'un paragraphe et retourne les balises <a>
    qui ne sont pas à l'intérieur de parenthèses dans le texte.
    """
    result = []
    depth = 0
    for element in paragraph.children:
        if hasattr(element, 'string') and element.string and element.name is None:
            depth += element.string.count('(') - element.string.count(')')
        elif hasattr(element, 'name') and element.name == 'a':
            if depth == 0:
                result.append(element)
        elif hasattr(element, 'children'):
            for child in element.children:
                if hasattr(child, 'string') and child.string and child.name is None:
                    depth += child.string.count('(') - child.string.count(')')
                elif hasattr(child, 'name') and child.name == 'a':
                    if depth == 0:
                        result.append(child)
    return result


def find_first_valid_link(soup, base_url, excluded_prefixes):
    """
    Trouve le premier lien valide dans les paragraphes d'introduction
    de l'article Wikipedia.
    """
    content = soup.find(id="mw-content-text")
    if not content:
        return None

    body_content = content.find(class_="mw-parser-output")
    if not body_content:
        body_content = content

    for p in body_content.find_all("p", recursive=False):
        if not p.get_text().strip():
            continue
        candidates = get_links_outside_parentheses(p)
        for link in candidates:
            if is_valid_link(link, excluded_prefixes):
                return base_url + link["href"]
    return None


def roads_to_philosophy(query):
    """
    Suit la chaîne de liens Wikipedia depuis query jusqu'à Philosophy.
    Affiche chaque article visité et le résultat final.
    """
    base_url = "https://en.wikipedia.org"
    excluded_prefixes = [
        "/wiki/Help:",
        "/wiki/Wikipedia:",
        "/wiki/File:",
        "/wiki/Special:",
        "/wiki/Talk:",
        "/wiki/Portal:",
        "/wiki/Category:",
        "/wiki/Template:",
        "/wiki/Template_talk:",
        "/wiki/Wikipedia_talk:",
    ]

    url = base_url + "/wiki/" + query.replace(" ", "_")
    visited = []

    while True:
        try:
            html = get_page(url)
        except requests.exceptions.ConnectionError:
            print("Error: unable to connect to Wikipedia.")
            sys.exit(1)
        except requests.exceptions.Timeout:
            print("Error: connection timed out.")
            sys.exit(1)
        except requests.exceptions.HTTPError as e:
            print(f"Error: HTTP error — {e}")
            sys.exit(1)
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            sys.exit(1)

        soup = BeautifulSoup(html, "lxml")
        title = get_title(soup)

        if title is None:
            print("Error: could not parse the page title.")
            sys.exit(1)

        print(title)

        if title.lower() == "philosophy":
            visited.append(title)
            count = len(visited)
            print(f"{count} roads from {query} to philosophy !")
            sys.exit(0)

        if title in visited:
            print("It leads to an infinite loop !")
            sys.exit(0)

        visited.append(title)

        next_url = find_first_valid_link(soup, base_url, excluded_prefixes)

        if next_url is None:
            print("It leads to a dead end !")
            sys.exit(0)

        url = next_url


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 roads_to_philosophy.py \"<search term>\"")
        sys.exit(1)

    query = sys.argv[1].strip()
    if not query:
        print("Error: search term cannot be empty.")
        sys.exit(1)

    roads_to_philosophy(query)


if __name__ == '__main__':
    main()
