import unittest
import window_manager, core

class WMTest(unittest.TestCase):
  def test_window_group_membership(self):
    wm = window_manager.Minimal()
    win = wm.window()
    win.show()
    self.assertTrue

  def test_z_order(self):
    wm = window_manager.Minimal()
    front  = wm.window(z=0)
    middle = wm.window(z=2)
    back   = wm.window(z=1)
    list = wm.zorder
    self.assertEqual(front,  list[0])
    self.assertEqual(middle, list[2])
    self.assertEqual(back,   list[1])

  def test_window_show(self):
    wm = window_manager.Minimal()
    win = wm.window()
    win.hide()
    win.show()
    self.assertTrue(wm.spritedict.has_key(win))
    self.assertTrue(wm.windows.spritedict.has_key(win))
    self.assertEqual(1,len(wm.zorder))

  def test_window_hide(self):
    wm = window_manager.Minimal()
    win = wm.window()
    self.assertTrue(wm.spritedict.has_key(win))
    self.assertTrue(wm.windows.spritedict.has_key(win))
    win.hide()
    self.assertFalse(wm.spritedict.has_key(win))
    self.assertTrue(wm.windows.spritedict.has_key(win))
    self.assertEqual(0,len(wm.zorder))

  def test_window_create(self):
    wm = window_manager.Minimal()
    win = wm.window()
    self.assertTrue(wm.spritedict.has_key(win))
    self.assertTrue(wm.windows.spritedict.has_key(win))

  def test_z_draw_order(self):
    wm = window_manager.Minimal()
    front  = wm.window(z=0)
    back   = wm.window(z=1)
    front.image = front
    back.image = back
    list = []
    real = core.screen.blit
    core.screen.blit = lambda img, rect: list.append(img)
    wm.draw()
    core.screen.blit = real
    self.assertEqual(front,  list[0])
    self.assertEqual(back,   list[1])

  def test_window_create_size(self):
    wm = window_manager.Minimal()
    win = wm.window(30,40)
    self.assertEqual(40,win.image.get_height())
    self.assertEqual(30,win.image.get_width())

  def test_window_draw_location(self):
    wm = window_manager.Minimal()
    win = wm.window(30,40)
    rect = []
    real = core.screen.blit
    core.screen.blit = lambda img, r: rect.append(r)
    wm.draw()
    core.screen.blit = real
    rect = rect[0]
    self.assertNotEqual(None,rect)
    self.assertEquals( 0, rect.top)
    self.assertEquals( 0, rect.left)
    self.assertEquals(30, rect.width)
    self.assertEquals(40, rect.height)
