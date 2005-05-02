from map import *
import dice
import combat

class Cave(MapBase):
    def __init__(self):
        MapBase.__init__(self,55,44)
        self.set_regen_rate(5)
        self.get_tiles_from_ascii(self.__ascii_art(), {
            ' ': ('stone',), '.': ('floor',), '+': ('cave',),'@': ('grass',),
            '0': ('dirt',),
            'walkable': '.+@0' })
        self.add_entry_listener(5,9, self.exit_cave)
        self.add_entry_listener(5,41, self.win_game)
        self.add_movement_listener(self.movement)
        self.monster_level = 1

        # Add markers to increment/decrement the monster level as you pass through caves
        self.add_entry_listener(10,3, self.check_level(EAST))
        self.add_entry_listener(21,7, self.check_level(EAST))
        self.add_entry_listener(31,10, self.check_level(SOUTH))
        self.add_entry_listener(32,18, self.check_level(EAST))
        self.add_entry_listener(36,11, self.check_level(NORTH))
        self.add_entry_listener(43,5, self.check_level(EAST))
        self.add_entry_listener(49,10, self.check_level(SOUTH))
        self.add_entry_listener(53,21, self.check_level(SOUTH))
        self.add_entry_listener(50,32, self.check_level(SOUTH))
        self.add_entry_listener(44,40, self.check_level(WEST))
        self.add_entry_listener(37,33, self.check_level(NORTH))
        self.add_entry_listener(33,24, self.check_level(WEST))
        self.add_entry_listener(25,32, self.check_level(SOUTH))
        self.add_entry_listener(22,42, self.check_level(WEST))
        self.add_entry_listener(17,33, self.check_level(NORTH))
        self.add_entry_listener(15,22, self.check_level(NORTH))
        self.add_entry_listener(11,15, self.check_level(WEST))
        self.add_entry_listener(1,21, self.check_level(SOUTH))
        self.add_entry_listener(4,32, self.check_level(SOUTH))

    def check_level(self, direction):
        def temp():
            if self.character.facing == direction:
                self.monster_level = self.monster_level + 1
            else: self.monster_level = self.monster_level - 1
        return temp
           
    def movement(self):
        print "Currently at (%d, %d)" % self.character.pos
        print "Monster level: %d" % self.monster_level
        if dice.roll('2d6') >= 10:
            self.random_fight()
    
    def exit_cave(self):
        core.game.teleport(None, (8,1), None, 'overworld.Overworld')
        
    def win_game(self):
        print "You have defeated the evil Minotaur and won!"

    def random_fight(self):
        monster = combat.gallery.generate_monster(self.monster_level)
        hero = core.game.save_data.hero
        combat.Combat(hero, monster, pygame.display.get_surface())

    def __ascii_art(self):
        """This is just an xpm with the header stripped"""
        return (
        "                                                       ",
        "              .......    ....                          ",
        "    ......  ..... ..    ......                         ",
        "   ......+00+...  .     ..   ...         ..  ...       ",
        "  ........  ...   ..    .. ....        ....  ......    ",
        "  ........  ..    ...  ... .          ....+00+..  ..   ",
        " .........        ...  ... ..        ......  ...   ..  ",
        " ... . ...        ..+00+.. ...      ......   ......... ",
        " ..  .  ..        ...  ...  ....   .....     ......... ",
        " .   +   .          .  ..    ..+  ..+..      ....+.... ",
        "                               0    0            0     ",
        "                               0    0            0     ",
        " .....   .  ...    ..  ..  ....+  ..+..         .+..   ",
        " ..... ...  ...   ...  ..  .. ..  .....         ....   ",
        " .  .. ...  ....  ...  ..  .. ..  ......        ....   ",
        " ..  . ..+00+....  ..  .. ...  .  .......      .....   ",
        " ...   ...  .....  ..  . .. .         ...     ... ..   ",
        " .........  .....  ..  . .. ....  ...  ..    ....  ..  ",
        " ..  ...     ....  ..  . .   ..+00+... ..    ....  ... ",
        " ...         ....  ..  ...   ...  .......    ...   ... ",
        " +...         .+.....  ...   ...  ......     ..     .+ ",
        " 0             0                                     0 ",
        " 0             0                                     0 ",
        " +.          ..+..     ..... ...  .... ....        ..+ ",
        " ..          .....     ..    ..+00+... ..          ... ",
        " ...         .....     .    ....  ...  ...    ........ ",
        " ....         .....    .   .....  ...   ..    ...  ... ",
        " .....        .....    .  ....    ....  ..        .... ",
        "  .. .        .....    . .....     .... .       ...... ",
        "  ....         .....   ......      ......     .......  ",
        "   ....        .....   .....        ....     ... ....  ",
        "   .+...       ..+...  ..+.         .+..     ..  .+.   ",
        "    0            0       0           0            0    ",
        "    0            0       0           0            0    ",
        " ...+.....     ..+..    .+..        .+...    .....+. . ",
        " .........     .....    ...         ....     ..  ... . ",
        "  .......      .....    ...        ....      .   ..  . ",
        "  .......      ......   ...        ....   .    ....  . ",
        "  .......      ......   ..          .... ..   ..  .  . ",
        "  .......       .....   ..          .......  ... ..... ",
        " ... . ...       ....  ....          .....+00+. ...    ",
        " ..  @  ..       ....  ....           .....  .....     ",
        " .       .        ..+00+...              ..  ....      ",
        "                                                       ")
