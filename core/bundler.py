import json
import os
import shutil
import yaml
from core.configurations import (
    DATA_CSV_SOURCE,
    CATALOG_CONFIG_FILE,
    MKDOCS_TEMPLATE_FILE,
    BUILD_DESTINATION_PATH,
    FILES_TO_COPY
)
from core.generator import FileGenerator
from core.reader import CsvReader


class Bundler:

    def __call__(self, *args, **kwargs):
        """Delete and recreate the build dir"""

        cr = CsvReader()
        with open(DATA_CSV_SOURCE, 'r', encoding='latin') as file:
            cr.read(file)
        
        # Save catalog.json file just in case
        with open(CATALOG_CONFIG_FILE, 'w') as file:
            file.write(json.dumps(cr.catalog, indent=4))
        
        # Remove and recreate build destination
        try:
            shutil.rmtree(BUILD_DESTINATION_PATH)
        except FileNotFoundError:
            pass

        os.mkdir(BUILD_DESTINATION_PATH)

        # generate docs
        fg = FileGenerator(cr.catalog)
        fg.generate()
        self._update_nav(fg.yaml_structure_data)
        self._copy_data()

    @staticmethod
    def _update_nav(yaml_structure_data: list):
        """Update nav structure"""
        with open(MKDOCS_TEMPLATE_FILE, 'r') as yaml_file:
            yaml_data = yaml_file.read()

        # edit nav structure
        nav = yaml.dump(yaml_structure_data, sort_keys=False)
        yaml_data = yaml_data.replace('{{nav}}', f'\n{nav}')

        # save nav structure
        with open(f'{BUILD_DESTINATION_PATH}/mkdocs.yml', 'w') as yaml_file:
            yaml_file.write(yaml_data)

    @staticmethod
    def _copy_data():
        """copy extra static data"""
        for source, destination in FILES_TO_COPY:
            try:
                shutil.copyfile(source, destination)
            except FileNotFoundError:
                continue
