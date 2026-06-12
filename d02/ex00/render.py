import sys
import os
import re


def get_settings_variables():
    import settings
    return {k: v for k, v in vars(settings).items() if not k.startswith('_')}


def render(template_path):
    if not template_path.endswith('.template'):
        print("Error: file must have a .template extension")
        sys.exit(1)
    if not os.path.isfile(template_path):
        print("Error: file '{}' does not exist".format(template_path))
        sys.exit(1)

    variables = get_settings_variables()

    with open(template_path, 'r') as f:
        content = f.read()

    try:
        result = content.format_map(variables)
    except KeyError as e:
        print("Error: missing variable {} in settings.py".format(e))
        sys.exit(1)

    output_path = re.sub(r'\.template$', '.html', template_path)
    with open(output_path, 'w') as f:
        f.write(result)

    print("Rendered: {} -> {}".format(template_path, output_path))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 render.py <file.template>")
        sys.exit(1)
    render(sys.argv[1])
