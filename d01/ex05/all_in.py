import sys


def all_in():
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
    expressions = sys.argv[1].split(',')
    # Two successive commas produce an empty element -> display nothing
    for expr in expressions:
        if expr.strip() == '':
            return
    for expr in expressions:
        # Normalize multiple spaces
        expr_clean = ' '.join(expr.split())
        # Case-insensitive search in states
        found_state = None
        for s in states:
            if s.lower() == expr_clean.lower():
                found_state = s
                break
        if found_state:
            code = states[found_state]
            capital = capital_cities[code]
            print(f"{capital} is the capital of {found_state}")
            continue
        # Case-insensitive search in capital cities
        found_capital = None
        found_state_name = None
        for code, cap in capital_cities.items():
            if cap.lower() == expr_clean.lower():
                found_capital = cap  # official casing
                for s, c in states.items():
                    if c == code:
                        found_state_name = s
                        break
                break
        if found_state_name:
            print(f"{found_capital} is the capital of {found_state_name}")
        else:
            print(f"{expr_clean} is neither a capital city nor a state")


if __name__ == '__main__':
    all_in()
