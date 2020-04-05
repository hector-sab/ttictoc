from .tictoc import Timer,tic,toc

def __get_version():
  import json
  with open('ttictoc/version.json') as f:
    version = json.load(f)['version']
  return version

__version__ = __get_version()
