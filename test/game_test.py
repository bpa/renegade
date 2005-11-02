import unittest
import game
import pickle
import sys, os
import testgame

class GameTest(unittest.TestCase):
  def setUp(self):
    dir = os.path.dirname(testgame.__file__)
    for file in os.listdir(dir):
      if file.startswith('save'):
        os.unlink(os.path.join(dir,file))
    
  def test_save_game(self):
    tg = testgame.TestGame()
    tg.save()
