import os
import mkdocs.__main__
from core.configurations import BUILD_DESTINATION_PATH
from core.bundler import Bundler


if __name__ == '__main__':
    
    Bundler()(auto_numerate=os.environ.get('AUTO_NUMERATE', False))
    mkdocs.__main__.build_command(['--clean', '-f', f'{BUILD_DESTINATION_PATH}/mkdocs.yml'])
