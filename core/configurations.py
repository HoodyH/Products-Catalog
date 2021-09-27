# build section
BUILD_DESTINATION_PATH = 'build'
BUILD_ITEM_DESTINATION_PATH = f'{BUILD_DESTINATION_PATH}/files/'

# template section
CATALOG_CONFIG_FILE = 'catalog/catalog.json'
MKDOCS_TEMPLATE_FILE = 'catalog/mkdocs.yml'
PRODUCT_TEMPLATE_FILENAME = 'catalog/templates/item.md'

FILES_TO_COPY = [
    ('catalog/index.md', f'{BUILD_DESTINATION_PATH}/index.md')
]
