import core
import dialog
import pygame
from pygame import color, font
from pygame.locals import RLEACCEL
from window_manager import StaticWindow

class HUD(StaticWindow):
    def __init__(self, hero):
        self.fg = color.Color('white')
        self.bg = color.Color('blue')
        self.tr = color.Color('black')

        self.bgwin = core.wm.window(-8,24,4,-28,z=7,name="HUD Background")
        self.bgwin.image.fill(self.bg)
        self.bgwin.image.set_alpha(128)

        self.borderwin = core.wm.window(height=32,y=-32,z=6,name="HUD Border")
        self.borderwin.image.fill(self.tr)
        dialog.draw_round_border(self.borderwin.image,color=self.fg)
        self.borderwin.image.set_colorkey(self.tr, RLEACCEL)

        rect = core.wm.make_rect_from_relative(8,-28,-16,25)
        StaticWindow.__init__(self,rect,z=5)
        self.update = self.real_update
        self.set_hero(hero)
        self.font = font.Font(None, 20)
        self.rows = 2
        self.image.set_colorkey(self.tr, RLEACCEL)

    def set_hero(self, hero):
        self.hero = hero
        hero.add_observer(self,['max_hp','hp','exp','level', \
                                'gold','weapon','armor'])
        self.update = self.real_update

    def handle_observation(self, hero, field, old, new):
        self.update = self.real_update

    def nop(self): pass
    def real_update(self):
        self.image.fill(self.tr)
        hero = self.hero
        text = "HP: %d/%d  Exp: %d  Level: %d" % \
                (hero.get_hp(), hero.get_max_hp(), hero.get_exp(), hero.get_level())
        self.draw_text(text, 1)
        text = "Gold: %d  Weapon: %s  Armor: %s" % \
            (hero.get_gold(), hero.weapon.get_name(), hero.armor.get_name())
        self.draw_text(text, 0)
        self.update = self.nop

    def draw_text(self, text, row):
        font_height = self.font.get_height()
        top = row * (font_height - 6) - 3
        rendered = self.font.render(text, True, self.fg).convert_alpha()
        base = self.image.get_rect().height
        self.image.blit(rendered, (0, top))
