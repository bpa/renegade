import unittest
import window_manager

class WMTest(unittest.TestCase):
  def test_window_group_membership(self):
    wm = window_manager.Minimal()
    win = wm.window()
    win.show()
    self.assertTrue
