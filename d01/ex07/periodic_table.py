import sys


def parse_element(line):
    """Parse a line from periodic_table.txt and return (name, attrs_dict)."""
    name, attrs_str = line.strip().split(' = ')
    attrs = {}
    for attr in attrs_str.split(', '):
        key, val = attr.split(':', 1)
        attrs[key.strip()] = val.strip()
    return name.strip(), attrs


def get_period(number):
    """Return the period (row) of an element based on its atomic number."""
    n = int(number)
    if n <= 2:
        return 1
    elif n <= 10:
        return 2
    elif n <= 18:
        return 3
    elif n <= 36:
        return 4
    elif n <= 54:
        return 5
    elif n <= 56 or (72 <= n <= 86):
        return 6
    else:
        return 7


def element_to_html(name, attrs):
    """Generate the HTML for a single element table cell."""
    electron_str = attrs['electron']
    return (
        '        <td style="border: 1px solid black; padding:10px">\n'
        f'          <h4>{name}</h4>\n'
        '          <ul>\n'
        f'            <li>No {attrs["number"]}</li>\n'
        f'            <li>{attrs["small"]}</li>\n'
        f'            <li>{attrs["molar"]}</li>\n'
        f'            <li>{electron_str} electron</li>\n'
        '          </ul>\n'
        '        </td>'
    )


def generate_table():
    """Read periodic_table.txt and write periodic_table.html."""
    with open('periodic_table.txt', 'r') as f:
        lines = f.readlines()

    # Parse all elements
    elements = []
    for line in lines:
        line = line.strip()
        if '=' in line:
            name, attrs = parse_element(line)
            elements.append((name, attrs))

    # Organise by period (row) and position (column)
    table = {}
    for name, attrs in elements:
        period = get_period(attrs['number'])
        pos = int(attrs['position'])
        if period not in table:
            table[period] = {}
        table[period][pos] = (name, attrs)

    # Build HTML
    html_lines = [
        '<!DOCTYPE html>',
        '<html lang="en">',
        '<head>',
        '  <meta charset="UTF-8">',
        '  <title>Periodic Table of the Elements</title>',
        '  <style>',
        '    body { font-family: Arial, sans-serif; }',
        '    table { border-collapse: collapse; }',
        '    td { vertical-align: top; min-width: 80px; }',
        '    h4 { margin: 0 0 4px 0; }',
        '    ul { margin: 0; padding-left: 16px; font-size: 0.85em; }',
        '  </style>',
        '</head>',
        '<body>',
        '  <h1>Periodic Table of the Elements</h1>',
        '  <table>',
    ]

    for period in sorted(table.keys()):
        html_lines.append('    <tr>')
        row = table[period]
        for col in range(18):
            if col in row:
                name, attrs = row[col]
                html_lines.append(element_to_html(name, attrs))
            else:
                html_lines.append('        <td></td>')
        html_lines.append('    </tr>')

    html_lines += [
        '  </table>',
        '</body>',
        '</html>',
    ]

    with open('periodic_table.html', 'w') as f:
        f.write('\n'.join(html_lines) + '\n')

    print("periodic_table.html generated successfully.")


if __name__ == '__main__':
    generate_table()
