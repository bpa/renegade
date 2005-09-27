#! /usr/bin/env python
import unittest
import os, sys, types

#getopt to find options
#find specific test suites/tests

def all():
  tests = []
  sys.path.append(os.path.realpath('../src'))
  for root, dirs, files in os.walk('.'):
    sys.path.append(root)
    if dirs.count('.svn'):
      dirs.remove('.svn')
    for f in files:
      if f.lower().endswith('test.py'):
        test = __import__(f[:-3])
        for name in dir(test):
            obj = getattr(test, name)
            if (isinstance(obj, (type, types.ClassType)) and
                issubclass(obj, unittest.TestCase)):
              tests.append(unittest.makeSuite(obj))
    sys.path.pop()
  os.chdir('../src')
  return unittest.TestSuite(tests)

os.sys.path.insert(0,'../src')
os.sys.path.insert(0,'mocks')
import core
core.init()
os.sys.path.remove('mocks')
os.sys.path.remove('../src')
unittest.main(defaultTest='all')
