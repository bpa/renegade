import core
from pygame import color, Rect, font, draw
from window_manager import Window
from dialog import draw_round_border
from locals import *
from items import Weapon, Armor

class InventoryScreen(Window):
  def __init__(self):
    core.wm.set_screen("inventory")
    Window.__init__(self,core.screen.get_rect())
    core.wm.set_screen("main")
    self.fg = color.Color('white')
    self.bg = color.Color('Blue')
    self.font = font.Font(None, 20)
    self.equipped_icon = self.font.render("E", True, self.fg)
    self.character_fields = \
        ['level','hp','max_hp','strength','agility','vitality','thaco','ac','gold','exp']

  def handle_observation(self, obj, field, old, new):
    self.cache_stats()

  def run(self):
    self.hero = core.game.save_data.hero
    core.wm.set_screen("inventory")
    self.focus()
    core.screen.fill(self.bg)
    draw_round_border(core.screen, bounds=Rect(2,2,317,476))
    draw_round_border(core.screen, bounds=Rect(321,2,317,476))
    self.hero.add_observer(self,self.character_fields)
    self.inventory = self.hero.inventory
    self.cache_stats()
    self.cache_inventory()
    if len(self.inventory) > 0:
        self.selection = 0
    else:
        self.selection = -1
    self.draw_cursor()

  def draw_cursor(self):
    if self.selection != -1:
        draw.circle(core.screen, self.fg, (350,58+self.selection*25), 3)

  def handle_event(self, event):
    if event.type == PUSH_ARROW_EVENT or \
         event.type == REPEAT_ARROW_EVENT:
        if core.event_bag.is_up():
            self.selection_up()
        elif core.event_bag.is_down():
            self.selection_down()
    elif event.type == PUSH_ACTION_EVENT:
        self.activate_selection()
    elif event.type == QUIT_EVENT:
        self.blur()
        core.wm.set_screen("main")
        core.game.save_data.map.focus()
        core.game.save_data.hero.add_observer(self,[])
        del self.stats_text

  def cache_stats(self):
    self.stats_text = []
    add = self.stats_text.append
    text = self.render_text
    hero = core.game.save_data.hero.get
    label = Rect( 30,50,120,0)
    value = Rect(160,50,  0,0)
    for s in self.character_fields:
        add(text(s.capitalize(),label,align='right'))
        add(text(str(hero(s)),value))
        label.move_ip(0,25)
        value.move_ip(0,25)

  def cache_inventory(self):
    '''Making the assumption that we won't really have that many items'''
    self.inventory_text = []
    add = self.inventory_text.append
    text = self.render_text
    loc = Rect(375,50,0,0)
    for i in self.inventory:
        add(text(i.get_name(),loc))
        loc.move_ip(0,25)
    if len(self.inventory_text) == 0:
        add(text("Your inventory is empty",loc.move(30,0)))

  def nop(self, blit): pass
  def draw_character(self, blit):
    for t in self.stats_text:
        t(blit)

  def draw_items(self, blit):
    for i in self.inventory_text:
        i(blit)

  def draw(self, blit):
    draw.rect(core.screen, self.bg, Rect( 10, 10, 300, 440), 0)
    draw.rect(core.screen, self.bg, Rect(330, 10, 300, 440), 0)
    self.draw_character(blit)
    self.draw_items(blit)
    self.draw_cursor()
    if self.hero.weapon_loc != -1:
        blit(self.equipped_icon, (360, 50+self.hero.weapon_loc*25))
    if self.hero.armor_loc != -1:
        blit(self.equipped_icon, (360, 50+self.hero.armor_loc*25))

  def render_text(self,text,rect,align='left'):
    text_image = self.font.render(text, True, self.fg)
    if align == 'right':
        screen_loc = (rect.right - text_image.get_width(), rect.top)
    else:
        screen_loc = rect.topleft
    return lambda b: b(text_image, screen_loc)

  def selection_up(self):
    num_items = len(self.inventory)
    if num_items == 0: return
    if self.selection == 0:
        self.selection = num_items - 1
    else:
        self.selection = self.selection - 1

  def selection_down(self):
    num_items = len(self.inventory)
    if num_items == 0: return
    if self.selection < num_items - 1:
        self.selection = self.selection + 1
    else:
        self.selection = 0

  def activate_selection(self):
    if self.selection == -1: return
    item = self.inventory[self.selection]
    if isinstance(item, Weapon):
        if self.hero.weapon_loc == self.selection:
            self.hero.remove_weapon()
        else:
            self.hero.equip_weapon(self.selection)
    elif isinstance(item, Armor):
        if self.hero.armor_loc == self.selection:
            self.hero.remove_armor()
        else:
            self.hero.equip_armor(self.selection)
