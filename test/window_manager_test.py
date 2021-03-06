import unittest
import window_manager, core
from pygame import Rect
import gc

class WMTest(unittest.TestCase):
  def test_window_group_membership(self):
    wm = window_manager.Minimal()
    win = wm.window()
    win.show()
    self.assertTrue

  def test_center(self):
    wm = window_manager.Minimal()
    win  = wm.window(16,8,'center','center')
    self.assertEqual(8, win.rect.left)
    self.assertEqual(12,win.rect.top) 

  def test_percent(self):
    wm = window_manager.Minimal()
    win  = wm.window('50%','25%')
    self.assertEqual(16, win.rect.width)
    self.assertEqual(8,  win.rect.height) 

  def test_percent_and_center(self):
    wm = window_manager.Minimal()
    win  = wm.window('75%',x='center')
    self.assertEqual(24, win.rect.width)
    self.assertEqual(32, win.rect.height) 

  def test_z_order(self):
    wm = window_manager.Minimal()
    front  = wm.window(z=0)
    back   = wm.window(z=2)
    middle = wm.window(z=1)
    list = wm.current_screen.zorder
    map(lambda s: s.z, list)
    self.assertEqual(front,  list[2])
    self.assertEqual(middle, list[1])
    self.assertEqual(back,   list[0])

  def test_window_show(self):
    wm = window_manager.Minimal()
    win = wm.window()
    win.hide()
    win.show()
    self.assertTrue(wm.current_screen.spritedict.has_key(win))
    self.assertEqual(1,len(wm.current_screen.zorder))

  def test_window_hide(self):
    wm = window_manager.Minimal()
    win = wm.window()
    self.assertTrue(wm.current_screen.spritedict.has_key(win))
    win.hide()
    self.assertFalse(wm.current_screen.spritedict.has_key(win))
    self.assertEqual(0,len(wm.current_screen.zorder))

  def test_window_create(self):
    wm = window_manager.Minimal()
    win = wm.window()
    self.assertTrue(wm.current_screen.spritedict.has_key(win))

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
    self.assertEqual(front,  list[1])
    self.assertEqual(back,   list[0])

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

  def test_create_window_with_offsets(self):
    wm = window_manager.Minimal()
    win = wm.window()
    self.assertEqual(32,win.image.get_width())
    self.assertEqual(32,win.image.get_height())
    win2 = wm.window(-2,-16)
    self.assertEqual(30,win2.image.get_width())
    self.assertEqual(16,win2.image.get_height())
    win3 = wm.window(x=-2,y=-16)
    self.assertEqual(30,win3.rect.left)
    self.assertEqual(16,win3.rect.top)

  def test_create_with_rect(self):
    wm = window_manager.Minimal()
    r = Rect(5,10,15,20)
    win = wm.window(r)
    wir = win.image.get_rect()
    wr = win.rect
    self.assertEqual(15,wir.width)
    self.assertEqual(20,wir.height)
    self.assertEqual(5, wr.left)
    self.assertEqual(10,wr.top)
    self.assertEqual(15,wr.width)
    self.assertEqual(20,wr.height)

  def test_screen(self):
    list = []
    core.screen.blit = lambda img, rect: list.append(rect)
    wm = window_manager.Minimal()

    r = Rect(0,0,5,5)
    one = wm.window(r)
    self.assertEqual(1,len(wm.current_screen.zorder))

    wm.set_screen("second")
    r = Rect(5,5,5,5)
    two = wm.window(r)
    self.assertEqual(1,len(wm.current_screen.zorder))

    wm.draw()
    self.assertEqual(1,len(list))
    self.assertEquals( 5, list[0].top)

    list = []
    wm.set_screen("main")
    self.assertEqual(1,len(wm.current_screen.zorder))
    wm.draw()
    self.assertEqual(1,len(list))
    self.assertEquals( 0, list[0].top)

  def test_destroy(self):
    wm = window_manager.Minimal()
    one = wm.window()
    one.focus()
    
    self.assertEqual(1,len(wm.current_screen.zorder))
    self.assertEqual(1,len(wm.current_screen.spritedict))
    self.assertEqual(one,wm.active_window)
    one.destroy()

    self.assertEqual(0,len(wm.current_screen.zorder))
    self.assertEqual(0,len(wm.current_screen.spritedict))
    self.assertNotEqual(one,wm.active_window)
