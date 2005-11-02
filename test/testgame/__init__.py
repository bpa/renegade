import game, map
import characters

class TestGame(game.Game):
  def new_game(self):
    self.save_data.hero = characters.Hero()
    self.save_data.hero.add_gold(150)
    self.load_map('small.Small')
    self.save_data.character = map.MapEntity()
    self.save_data.character.init('stolen-01',2,0,-1)
    self.save_data.map.place_character(self.save_data.character, (9,4) )
