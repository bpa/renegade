import unittest
import map
from pygame import Rect

class MapTest(unittest.TestCase):
  def test_calculate_tile_coverage(self):
    v = Rect(0,0,11,11)
    m = map.MapBase(50,50)
    c = m.map_tile_coverage
    e = map.MapEntity(1)

    #Not enough map on up and left
    m.place_character(e,(1,1))
    v.center = (6,6)
    m.calculate_tile_coverage(v)
    self.assertEqual(0,c.left)
    self.assertEqual(0,c.top)

    #Not enough map on down and right
    e.move_to((49,49))
    v.center = e.pos
    m.calculate_tile_coverage(v)
    self.assertEqual(32,c.left)
    self.assertEqual(32,c.top)

    #Top
    e.move_to((25,21))
    v.center = (25,25)
    m.calculate_tile_coverage(v)
    self.assertEqual(16,c.left)
    self.assertEqual(12,c.top)
