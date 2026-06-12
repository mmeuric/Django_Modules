import sys
import antigravity


def geohash(lat, lon, date, dow):
    """
    Calcule le géohash xkcd à partir de la latitude, longitude,
    date (YYYY-MM-DD) et cours d'ouverture du Dow Jones.
    Utilise antigravity.geohash(lat, lon, datedow_bytes).
    datedow_bytes = b'YYYY-MM-DD-dow'
    """
    datedow = f"{date}-{dow}".encode()
    antigravity.geohash(lat, lon, datedow)


def main():
    if len(sys.argv) != 5:
        print(
            "Usage: python3 geohashing.py <latitude> <longitude> "
            "<YYYY-MM-DD> <dow_jones>"
        )
        sys.exit(1)

    try:
        lat = float(sys.argv[1])
        lon = float(sys.argv[2])
        date = sys.argv[3]
        dow = sys.argv[4]
        # Validation basique de la date
        parts = date.split('-')
        if len(parts) != 3 or not all(p.isdigit() for p in parts):
            raise ValueError("Date must be in YYYY-MM-DD format")
        # Validation dow jones (doit être numérique)
        float(dow)
    except ValueError as e:
        print(f"Error: invalid parameter — {e}")
        sys.exit(1)

    geohash(lat, lon, date, dow)


if __name__ == '__main__':
    main()
