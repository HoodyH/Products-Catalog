import mkdocs.__main__
from core.configurations import BUILD_DESTINATION_PATH
from core.bundler import Bundler


if __name__ == '__main__':
    Bundler()()
    mkdocs.__main__.build_command(['--clean', '-f', f'{BUILD_DESTINATION_PATH}/mkdocs.yml'])
