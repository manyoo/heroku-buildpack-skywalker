#!/usr/bin/env python

import ConfigParser
import io
import sys
import subprocess
import shutil

GIT = 'git'

def debug(line):
    verbose = True
    if verbose:
        print line

def normalize(content):
    lines = []
    for line in content.split('\n'):
        lines.append(line.strip('\t\r '))
    return '\n'.join(lines)

def get_submodules(content):
    content = normalize(content)
    parser = ConfigParser.RawConfigParser()
    parser.readfp(io.BytesIO(content))
    ret = {}
    for section in parser.sections():
        ret[section] = {}
        for option in parser.options(section):
            ret[section][option] = parser.get(section, option)
    return ret

def init():
    args = [GIT, "init"]
    subprocess.check_call(args)

def update(url, path):
    shutil.rmtree(path, ignore_errors=True)
    args = [GIT, "submodule", "add", url, path]
    subprocess.check_call(args)

def test():
    import unittest

    r = """[submodule "runtime"]
    path = runtime
    url = git://github.com/jonnor/imgflo.git"""
    print r
    e = {
        "submodule \"runtime\"": {
            "path": "runtime",
            "url": "git://github.com/jonnor/imgflo.git",
        }
    }
    class DummyCase(unittest.TestCase):
        def runTest(self):
            res = get_submodules(r)
            self.assertEqual(res, e)

    DummyCase().runTest()

if __name__ == '__main__':

    prog, args = sys.argv[0], sys.argv[1:]

    if len(args) == 1:
        content = open(args[0], 'r').read()
        submodules = get_submodules(content)
        print submodules
        init()
        for name, module in submodules.items():
            url = module.get('url')
            path = module.get('path')
            if not path and url:
                raise ValueError
            update(url, path)
    elif len(args) == 0:
        test()
    else:
        raise ValueError

