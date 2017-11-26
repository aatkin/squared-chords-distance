# -*- coding: utf-8 -*-

import sys
import json
import functools

from sqcd import sqcd

def read_in():
    lines = sys.stdin.readlines()
    return json.loads(lines[0])

def main():
    [training, test] = read_in()
    sqcd(training, test)
    # sqcd(None, None)

if __name__ == '__main__':
    main()
