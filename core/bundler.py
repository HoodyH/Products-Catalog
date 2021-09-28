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
    
    def __init__(self):
        self.nav_structure: list = []

    def __call__(self, auto_numerate=False, *args, **kwargs):
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
        fg.generate(auto_numerate=auto_numerate)
        self.nav_structure = fg.yaml_structure_data
        self._copy_data()
        self._update_nav()

    def _copy_data(self):
        """copy extra static data"""
        for nav_name, source, destination in FILES_TO_COPY:
            try:
                shutil.copyfile(source, destination)
            
                # append extra files to the structure
                self.nav_structure.insert(0, {nav_name: destination[len(BUILD_DESTINATION_PATH)+1:]})
        
            except FileNotFoundError:
                continue

    def _update_nav(self):
        """Update nav structure"""
        with open(MKDOCS_TEMPLATE_FILE, 'r') as yaml_file:
            yaml_data = yaml_file.read()

        # edit nav structure
        nav = yaml.dump(self.nav_structure, sort_keys=False)
        yaml_data = yaml_data.replace('{{nav}}', f'\n{nav}')

        # save nav structure
        with open(f'{BUILD_DESTINATION_PATH}/mkdocs.yml', 'w') as yaml_file:
            yaml_file.write(yaml_data)
