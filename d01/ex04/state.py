import sys


def state():
    states = {
        "Oregon"     : "OR",
        "Alabama"    : "AL",
        "New Jersey" : "NJ",
        "Colorado"   : "CO"
    }
    capital_cities = {
        "OR": "Salem",
        "AL": "Montgomery",
        "NJ": "Trenton",
        "CO": "Denver"
    }
    if len(sys.argv) != 2:
        return
    city = sys.argv[1]
    code = None
    for c, cap in capital_cities.items():
        if cap == city:
            code = c
            break
    if code is None:
        print("Unknown capital city")
        return
    for s, c in states.items():
        if c == code:
            print(s)
            return


if __name__ == '__main__':
    state()
