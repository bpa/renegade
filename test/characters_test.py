import unittest
import types
from characters import *
import pickle

class CharacterTest(unittest.TestCase):

  def test_monster_create(self):
    chuckie = Monster()
    self.assertTrue(isinstance(chuckie.gold,types.IntType))

  def test_kill_monster(self):
    monster = Monster()
    hero = Hero()
    gold = monster.get_gold()
    self.assertTrue(isinstance(gold,types.IntType))

    exp = monster.get_exp_value()
    self.assertTrue(isinstance(exp,types.IntType))
    oldexp = hero.get_exp()
    self.assertTrue(isinstance(oldexp,types.IntType))
    hero.gain_exp(exp)
    self.assertEqual(oldexp + exp, hero.get_exp())

    hgold = hero.get_gold()
    self.assertTrue(isinstance(hgold,types.IntType))
    hero.add_gold(gold)
    self.assertEqual(hgold + gold, hero.get_gold())

  def test_pickle_hero(self):
    hero = Hero()
    hero.add_gold(12)

    p = pickle.dumps(hero)
    h2 = pickle.loads(p)

    expected = hero.__dict__
    actual = h2.__dict__
    keys = expected.keys()
    keys.remove('armor')
    keys.remove('weapon')
    for i in keys:
      self.assertEqual(expected[i], actual[i])
    self.assertTrue(actual.has_key('armor'))
    self.assertTrue(actual.has_key('weapon'))
