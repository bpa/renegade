
import unittest
import types
import items
import os

class ItemsTest(unittest.TestCase):
    def setUp(self):
        items.init(os.path.join(os.path.dirname(__file__),"testgame"))

    def tearDown(self):
        dir = os.path.dirname(__file__)
        try:
          os.unlink(os.path.join(dir,"testgame","items.db"))
          os.unlink(os.path.join(dir,"testgame","item_index.db"))
        except:
          pass

    def test_shelf_name(self):
        dir = os.path.dirname(__file__)
        try:
          f = open(os.path.join(dir,"testgame","items.db"),"r")
          f.close()
        except:
          raise
          self.fail("Database name wrong")
        try:
          f = open(os.path.join(dir,"testgame","item_index.db"),"r")
          f.close()
        except:
          self.fail("Index name wrong")

    def test_get_item(self):
        w = items.get_item("W01")
        self.assertTrue(isinstance(w,items.Weapon))
        self.assertEqual("W01",         w.id)
        self.assertEqual("Empty Hands", w.name)
        self.assertEqual(10,            w.value)
        self.assertEqual("1d4",         w.damage)
      
        a = items.get_item("A01")
        self.assertTrue(isinstance(a,items.Armor))
        self.assertEqual("A01",       a.id)
        self.assertEqual("Iron Skin", a.name)
        self.assertEqual(39,          a.value)
        self.assertEqual(3,           a.rating)
  
        a2 = items.get_item("Headband")
        self.assertTrue(isinstance(a2,items.Armor))
        self.assertEqual("A02",      a2.id)
        self.assertEqual("Headband", a2.name)
        self.assertEqual(3,          a2.value)
        self.assertEqual(0,          a2.rating)

    def test_get_items(self):
        i = items.get_items("W01","Iron Skin","A02")
        self.assertTrue(isinstance(i[0],items.Weapon))
        self.assertEqual("Empty Hands", i[0].name)
        self.assertTrue(isinstance(i[1],items.Armor))
        self.assertEqual("Iron Skin", i[1].name)
        self.assertTrue(isinstance(i[2],items.Armor))
        self.assertEqual("Headband", i[2].name)

    def test_weapon(self):
        i = items.get_item('W01')
        d = i.get_damage()
        self.assertNotEqual(0,d)
