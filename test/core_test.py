import unittest
import core
import sys

class CoreTest(unittest.TestCase):
  def get_cores(self):
    mock = sys.modules.pop('core')
    real = __import__('core')
    sys.modules['core'] = mock
    return (real, mock)

  def test_can_switch_core(self):
    self.assertNotEquals(-1,sys.modules['core'].__file__.find('mocks'))
    mock = sys.modules.pop('core')
    c = __import__('core')
    self.assertEquals(-1,sys.modules['core'].__file__.find('mocks'))
    sys.modules['core'] = mock
    self.assertNotEquals(-1,sys.modules['core'].__file__.find('mocks'))

  def test_get_cores(self):
    (real, mock) = self.get_cores()
    self.assertNotEquals(-1,mock.__file__.find('mocks'))
    self.assertEquals(-1,real.__file__.find('mocks'))
    self.assertNotEqual(real,mock)

  def test_mock_has_all_core_elements(self):
    (real, mock) = self.get_cores()
    for k in real.__dict__.keys():
        if not k.startswith('__'):
            self.assertTrue(mock.__dict__.has_key(k), "Mock missing %s" % k)

  def test_real_has_all_mock_elements(self):
    (real, mock) = self.get_cores()
    for k in mock.__dict__.keys():
        if not k.startswith('__'):
            self.assertTrue(real.__dict__.has_key(k), "Real missing %s" % k)
