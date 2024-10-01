#!./alatty/launcher/alatty +launch
# License: GPL v3 Copyright: 2016, Kovid Goyal <kovid at kovidgoyal.net>

import importlib


def main() -> None:
    m = importlib.import_module('alatty_tests.main')
    getattr(m, 'main')()


if __name__ == '__main__':
    main()
