import json
import os
import shutil
import yaml
from core.configurations import (
    CATALOG_CONFIG_FILE,
    MKDOCS_TEMPLATE_FILE,
    BUILD_DESTINATION_PATH
)
from core.generator import FileGenerator


class Bundler:

    def __call__(self, *args, **kwargs):
        """Delete and recreate the build dir"""
        try:
            shutil.rmtree(BUILD_DESTINATION_PATH)
        except FileNotFoundError:
            pass

        os.mkdir(BUILD_DESTINATION_PATH)

        with open(CATALOG_CONFIG_FILE, 'r') as config_file:
            fg = FileGenerator(json.load(config_file))
            fg.generate()
            self._update_nav(fg.yaml_structure_data)
        self._copy_data()

    @staticmethod
    def _update_nav(yaml_structure_data: list):
        """Update nav structure"""
        with open(MKDOCS_TEMPLATE_FILE, 'r') as yaml_file:
            yaml_data = yaml_file.read()

        print(yaml_data)

        # edit nav structure
        nav = yaml.dump(yaml_structure_data, sort_keys=False)
        yaml_data = yaml_data.replace('{{nav}}', f'\n{nav}')
        print(yaml_data)

        # save nav structure
        with open(f'{BUILD_DESTINATION_PATH}/mkdocs.yml', 'w') as yaml_file:
            yaml_file.write(yaml_data)

    def _copy_data(self):
        """copy extra static data"""
        for source, destination in self.to_copy:
            try:
                shutil.copyfile(source, destination)
            except FileNotFoundError:
                continue
