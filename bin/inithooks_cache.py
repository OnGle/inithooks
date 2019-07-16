#!/usr/bin/python3
"""Interface to inithooks cache

Arguments:

    key                 key name (required)
    value               if specified, will set as key value
                        if omitted, will return the value of key if set

Environment:

    INITHOOKS_CACHE     path to cache (default: /var/lib/inithooks/cache)
"""

import os
import sys

def fatal(e):
    print("Error:", e, file=sys.stderr)
    sys.exit(1)

def usage(s=None):
    if s:
        print("Error:", s, file=sys.stderr)
    print("Syntax: %s <key> [value]" % sys.argv[0], file=sys.stderr)
    print(__doc__, file=sys.stderr)
    sys.exit(1)

class KeyStore:
    def __init__(self, path):
        self.path = path
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def read(self, key):
        keypath = os.path.join(self.path, key)

        if os.path.exists(keypath):
            with open(keypath, 'r') as fob:
                data = fob.read()
            return data

        return None

    def write(self, key, val):
        keypath = os.path.join(self.path, key)

        with open(keypath, 'w') as fob:
            fob.write(val)

#convenience functions
CACHE_DIR = os.environ.get('INITHOOKS_CACHE', '/var/lib/inithooks/cache')

def read(key):
    return KeyStore(CACHE_DIR).read(key)

def write(key, value):
    return KeyStore(CACHE_DIR).write(key, value)


if __name__ == "__main__":
    import getopt

    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "h", ["help"])
    except getopt.GetoptError as e:
        usage(e)

    for opt, val in opts:
        if opt in ("-h", "--help"):
            usage()

    if len(args) == 0:
        usage()

    if len(args) > 2:
        fatal("too many arguments")

    if len(args) == 1:
        val = read(args[0])
        if val:
            print(val)

    if len(args) == 2:
        write(args[0], args[1])

