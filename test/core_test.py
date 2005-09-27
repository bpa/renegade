import unittest
import core

class CoreTest(unittest.TestCase):
  def test_mock_has_all_members(self):
    c = __import__('core')
    self.assertTrue(c.__dict__.has_key('test_element'))
