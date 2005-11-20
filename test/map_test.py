import unittest
import map, core
from testgame import TestGame
from map import NORTH, SOUTH, EAST, WEST
from pygame import Rect
import gc, sys, pickle
gc.set_debug(gc.DEBUG_UNCOLLECTABLE)

class MapTest(unittest.TestCase):
  def setUp(self):
    core.screen.rect.width = 352
    core.screen.rect.height = 352

  def tearDown(self):
    core.screen.rect.width = 32
    core.screen.rect.height = 32

  def test_init(self):
    m = map.MapBase(50,50)
    v = m.viewport
    c = m.map_tile_coverage
    d = m.dimentions

    #Dimensions should be a rect with the map size
    self.assertEqual(0, d.top)
    self.assertEqual(0, d.left)
    self.assertEqual(50,d.width)
    self.assertEqual(50,d.height)

    #Viewport should be as wide as the screen: 352 / 32 = 11
    self.assertEqual(11,v.width)
    self.assertEqual(11,v.height)

    #Cache size should be 5 more than viewport
    self.assertEqual(16,c.width)
    self.assertEqual(16,c.height)

  def test_calculate_tile_coverage(self):
    v = Rect(0,0,11,11)
    m = map.MapBase(50,50)
    e = map.MapEntity(1)
    m.place_character(e,(25,25))
    c = m.map_tile_coverage

    #Normal centered
    e.move_to((25,25))
    v.center = (25,25)
    m.calculate_tile_coverage(v)
    self.assertEqual(16,c.width)
    self.assertEqual(16,c.height)
    self.assertEqual((25,25),c.center)

    #Not enough map on up and left
    e.move_to((1,1))
    v.center = (6,6)
    m.calculate_tile_coverage(v)
    self.assertEqual(0,c.left)
    self.assertEqual(0,c.top)

    #Not enough map on down and right
    e.move_to((48,48))
    v.right = 50
    v.bottom = 50
    m.calculate_tile_coverage(v)
    self.assertEqual(50,c.right)
    self.assertEqual(50,c.bottom)

    #Refresh while walking north
    e.move_to((25,21))
    v.center = (25,25)
    m.calculate_tile_coverage(v)
    self.assertEqual(v.bottom + 1,c.bottom)
    self.assertEqual(25,c.centerx)

    #Refresh while walking south
    e.move_to((25,29))
    v.center = (25,25)
    m.calculate_tile_coverage(v)
    self.assertEqual(v.top - 1,c.top)
    self.assertEqual(25,c.centerx)

    #Refresh while walking east
    e.move_to((29,25))
    v.center = (25,25)
    m.calculate_tile_coverage(v)
    self.assertEqual(v.left - 1,c.left)
    self.assertEqual(25,c.centery)

    #Refresh while walking west
    e.move_to((21,25))
    v.center = (25,25)
    m.calculate_tile_coverage(v)
    self.assertEqual(v.right + 1,c.right)
    self.assertEqual(25,c.centery)

  def test_ref_count(self):
    game = TestGame()

    self.assertTrue(sys.getrefcount(game.save_data.map) > 1)
    game.save_data.map.dispose()
    self.assertEqual(2, sys.getrefcount(game.save_data.map))

  def test_pickle_map(self):
    game = TestGame()

    p = pickle.dumps(game.save_data.map)
    loaded = pickle.loads(p)

    expected = game.save_data.map.__dict__
    actual = loaded.__dict__
    keys = expected.keys()
    special = ['is_left','is_right','is_up','is_down','character','entities','tiles','non_passable_entities','tile_manager','offset','map_frames','sound','save_data']
    for k in special:
      keys.remove(k)
      self.assertTrue(actual.has_key(k))
    for i in keys:
      self.assertEqual(expected[i], actual[i])

  def test_pickle_map_entity(self):
    game = TestGame()

    p = pickle.dumps(game.save_data.character)
    loaded = pickle.loads(p)

    expected = game.save_data.character.__dict__
    actual = loaded.__dict__
    keys = expected.keys()
    keys.remove('map')
    special = ['_Sprite__g','image']
    for k in special:
      keys.remove(k)
      self.assertTrue(actual.has_key(k))
    for i in keys:
      self.assertEqual(expected[i], actual[i])
