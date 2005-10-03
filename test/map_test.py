import unittest
import map
from pygame import Rect

class MapTest(unittest.TestCase):
  def test_calculate_tile_coverage(self):
    r = Rect(0,0,11,11)
    m = map.MapBase(50,50)
    c = m.map_tile_coverage
    e = map.MapEntity(1)

    #Not enough map on up and left
    m.place_character(e,(0,0))
    m.calculate_tile_coverage(r)
    self.assertEqual(0,c.left)
    self.assertEqual(0,c.top)

    #Not enough map on down and right
    e.move_to((49,49))
    m.calculate_tile_coverage(r)
    self.assertEqual(34,c.left)
    self.assertEqual(34,c.top)

    #Top left boundary
    #Bottom right boundary
