# Catalog
Product catalog of a Sonepar branch company: Elettroveneta

A simple project to organize multiple excel product files in a single page application.

## How to build
- edit `catalof/catalog.json` with new products
- run main.py

Everything is auto-generated, 
if you want to add more files to the bundle edit the `FILES_TO_COPY` inside `core/configurations.py`

## How to edit mkdocs.yml
the nav inside the yml is auto-generated inside `build` folder, 
if you want to change mkdocs behavior edit the `catalog/mkdocs.yml` leaving the `nav: {{nav}}` line as it is.
