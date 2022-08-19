import json
import sys

from createTopoObj import createObjList
from verifyTopo import verify, fail


def read_topology(filename):
    try:
        with open(filename) as fin:
            d = json.load(fin)
        verify(d)  # Проверка топологии на корректность
        return createObjList(d)

    except (FileNotFoundError, IsADirectoryError):
        fail("Файл", filename, "не найден")
    except json.decoder.JSONDecodeError as e:
        fail(e)


if __name__ == "__main__":
    read_topology(sys.args[-1], None)
