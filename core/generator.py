import os
from core.configurations import PRODUCT_TEMPLATE_FILENAME, BUILD_ITEM_DESTINATION_PATH


class FileGenerator:

    def __init__(self, data: dict):
        self.data: dict = data
        self.yaml_structure_data: list = []

    @staticmethod
    def _generate_product_file(filename, data):
        """fill the template with the data"""
        product_data = ''

        with open(PRODUCT_TEMPLATE_FILENAME, 'r') as fr:
            # fill the template
            for el in data:
                template = fr.read()
                product_data += template \
                    .replace('{{id}}', el.get('id', '')) \
                    .replace('{{title}}', el.get('title', '')) \
                    .replace('{{content}}', el.get('content', '')) \
                    .replace('{{link}}', el.get('link', ''))
                fr.seek(0)

        with open(BUILD_ITEM_DESTINATION_PATH + filename, 'w') as fw:
            fw.write(product_data)

    def generate(self, auto_numerate=False):
        """
        Generate all the files in place
        :param auto_numerate: auto numerate the index, or numerate basing on csv order definition
        """

        os.mkdir(BUILD_ITEM_DESTINATION_PATH)

        for first_id, first_key in enumerate(self.data.keys()):
            yaml_first_key = f'{first_id + 1}. {first_key}' if auto_numerate else first_key
            yaml_first_structure_data = {yaml_first_key: []}

            for second_id, second_key in enumerate(self.data[first_key].keys()):
                yaml_second_key = f'{second_id + 1}. {second_key}' if auto_numerate else second_key
                yaml_second_structure_data = {yaml_second_key: []}

                for third_id, third_key in enumerate(self.data[first_key][second_key].keys()):
                    # get item data
                    data = self.data[first_key][second_key][third_key]
                    
                    # get the file name vit generate numeration from csv or auto-generate it
                    filename = data.get('filename')
                    if auto_numerate:
                        filename = f'{first_id + 1}-{second_id + 1}-{third_id + 1}.md'
                    yaml_third_key = f'{third_id + 1}. {third_key}' if auto_numerate else third_key

                    # Generate the file in the filesystem from the template
                    self._generate_product_file(filename, data.get('data', []))
                    
                    # fill yaml structure
                    yaml_second_structure_data[yaml_second_key].append({
                        yaml_third_key: f'files/{filename}'
                    })

                yaml_first_structure_data[yaml_first_key].append(yaml_second_structure_data)

            self.yaml_structure_data.append(yaml_first_structure_data)
