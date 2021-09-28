from typing import TextIO
import csv
import re


class CsvReader:
    """Read the excel csw file and build the catalog structure"""
    def __init__(self):
        self.catalog: dict = {}
    
    @staticmethod
    def _clean_text(text):
        return re.sub(r"[-()_\"#/@;:<>{}=~|.?,]", " ", text)
    
    def _build_single_product(self, identifier, line_number,  title, content, link):
        """clean upo the text and build the product object"""
        title = self._clean_text(title)
        return {
            "id": identifier,
            "row": line_number,
            "title": title,
            "content": content,
            "link": link
          }
    
    def _append_to_catalog_structure(self, first_key: str, second_key: str, third_key: str, product: dict):
        try:
            self.catalog[first_key]
        except KeyError:
            self.catalog[first_key] = {}
            
        try:
            self.catalog[first_key][second_key]
        except KeyError:
            self.catalog[first_key][second_key] = {}
            
        try:
            self.catalog[first_key][second_key][third_key].append(product)
        except KeyError or ValueError:
            self.catalog[first_key][second_key][third_key] = [product]
    
    def read(self, csv_file: TextIO):
        """read the data from the csv, and """
        csv_data = csv.reader(csv_file, delimiter=';')

        for idx, row in enumerate(csv_data):
            # skip first, line
            if idx == 0:
                continue

            line_number = row[0]
            # unpack ids
            first_id, first_key = row[1].lstrip("0"), row[2]
            second_id, second_key = row[3].lstrip("0"), row[4]
            third_id, third_key = row[5].lstrip("0"), row[6]
            fourth_id, fourth_key = row[7], row[9]
            fifth_id, fifth_key = row[10], row[12]
            
            # main content
            link = row[14]
            web_name = row[15]  # WEB
            title = row[17]  # PDF
            content = row[19]
            
            if link and title:
                product = self._build_single_product(web_name, line_number, title, content, link)
                self._append_to_catalog_structure(
                    f'{first_id}. {first_key}',
                    f'{second_id}. {second_key}',
                    f'{third_id}. {third_key}',
                    product
                )

                
if __name__ == '__main__':
    cr = CsvReader()
    with open('Database.csv', 'r', encoding='latin') as file:
        cr.read(file)
    
    import json
    with open('catalog.json', 'w') as file:
        file.write(json.dumps(cr.catalog, indent=4))
