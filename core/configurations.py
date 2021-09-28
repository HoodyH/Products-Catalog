# data section
DATA_CSV_SOURCE = 'data/database.csv'

# build section
BUILD_DESTINATION_PATH = 'build'
BUILD_ITEM_DESTINATION_PATH = f'{BUILD_DESTINATION_PATH}/files/'
BUILD_CATALOG_CONFIG_FILE = f'{BUILD_DESTINATION_PATH}/catalog.json'

# template section
MKDOCS_TEMPLATE_FILE = 'catalog/mkdocs.yml'
PRODUCT_TEMPLATE_FILENAME = 'catalog/templates/item.md'

FILES_TO_COPY = [
    # Nav-Webpage-Name, Source, Destination
    ('Home', 'catalog/index.md', f'{BUILD_DESTINATION_PATH}/index.md')
]
