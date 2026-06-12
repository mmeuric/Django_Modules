import sys
import requests
import dewiki


def fetch_wikipedia(query):
    """
    Interroge l'API Wikipedia (française) pour la requête donnée.
    Suit les redirections automatiquement.
    Retourne le JSON brut de la réponse.
    """
    url = "https://fr.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "prop": "revisions",
        "rvprop": "content",
        "rvslots": "*",
        "format": "json",
        "titles": query,
        "redirects": 1,
    }
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def extract_content(data):
    """
    Extrait le contenu Wiki Markup depuis la réponse JSON de l'API.
    Retourne None si la page n'existe pas.
    """
    pages = data.get("query", {}).get("pages", {})
    for page_id, page in pages.items():
        if page_id == "-1":
            return None
        revisions = page.get("revisions", [])
        if revisions:
            # Nouvelle structure API (slots)
            slots = revisions[0].get("slots", {})
            if slots:
                return slots.get("main", {}).get("*", "")
            # Ancienne structure (fallback)
            return revisions[0].get("*", "")
    return None


def save_result(query, content):
    """
    Nettoie le Wiki Markup via dewiki et écrit le résultat dans un fichier .wiki.
    Le nom du fichier ne contient aucun espace.
    """
    clean = dewiki.from_string(content)
    filename = query.replace(" ", "_") + ".wiki"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(clean)
    return filename


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 request_wikipedia.py \"<search term>\"")
        sys.exit(1)

    query = sys.argv[1].strip()
    if not query:
        print("Error: search term cannot be empty.")
        sys.exit(1)

    try:
        data = fetch_wikipedia(query)
        content = extract_content(data)
        if content is None:
            print(f"Error: no Wikipedia article found for '{query}'.")
            sys.exit(1)
        filename = save_result(query, content)
        print(f"Result saved in {filename}")
    except requests.exceptions.ConnectionError:
        print("Error: unable to connect to Wikipedia. Check your internet connection.")
        sys.exit(1)
    except requests.exceptions.Timeout:
        print("Error: the request to Wikipedia timed out.")
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        print(f"Error: HTTP error — {e}")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Error: network error — {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
