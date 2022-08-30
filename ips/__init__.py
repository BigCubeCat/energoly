import json
import urllib.request
from .structures import *

__version__ = "1.0.2021"
__all__ = ["init", "init_test", "from_json", "from_file", "Powerstand"]


def get_library_path():
    import os
    path = os.path.abspath(__file__)
    return os.path.dirname(path)


def init() -> Powerstand:
    request = urllib.request.urlopen("http://localhost:26000/powerstand")
    if request.getcode() != 200:
        raise ConnectionRefusedError("Couldn't receive data from server")
    data = json.load(request)
    return Powerstand(data)


def init_test() -> Powerstand:
    from .test import stub_input
    return from_json(stub_input)


def from_json(string) -> Powerstand:
    data = json.loads(string)
    return Powerstand(data)


def from_file(filename) -> Powerstand:
    with open(filename, "r") as fin:
        raw_data = fin.read()
    return from_json(raw_data)

    
def from_log(filename, step) -> Powerstand:
    with open(filename, "r") as fin:
        raw_data = json.load(fin)
    return Powerstand(raw_data[step]['powerstand'])

