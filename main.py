import json
import mkdocs.__main__
import yaml
from core.configurations import (
    CATALOG_CONFIG_FILE,
    MKDOCS_TEMPLATE_FILE,
    MKDOCS_CONFIG_FILE
)
from core.generator import FileGenerator


def update_nav(yaml_structure_data: list):
    """Update nav structure"""
    with open(MKDOCS_TEMPLATE_FILE, 'r') as yaml_file:
        yaml_data = yaml_file.read()

    print(yaml_data)

    # edit nav structure
    nav = yaml.dump(yaml_structure_data, sort_keys=False)
    yaml_data = yaml_data.replace('{{nav}}', f'\n{nav}')
    print(yaml_data)

    # save nav structure
    with open(MKDOCS_CONFIG_FILE, 'w') as yaml_file:
        yaml_file.write(yaml_data)


def generate():
    with open(CATALOG_CONFIG_FILE, 'r') as config_file:
        fg = FileGenerator(json.load(config_file))
        fg.generate()
        update_nav(fg.yaml_structure_data)


if __name__ == '__main__':
    generate()
    mkdocs.__main__.build_command(['--clean', '-f', MKDOCS_CONFIG_FILE])
