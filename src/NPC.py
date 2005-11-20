from map import *
import dialog, random
import core, items

class Merchant(MapEntity):
    def __init__(self,image=None):
        MapEntity.__init__(self,image)
        self.intro = 'INTRO'
        self.item_list = []
        self.item_names = []
        self.sell_factor = 0.6

    def set_intro(self, text):
        self.intro = text

    def set_item_list(self, *list):
        self.item_list = items.get_items(*list)
        self.item_names = map(lambda i: "%5i %s"%(i.value,i.name), self.item_list)
        self.item_names.append('Never mind')

    def set_sell_factor(self, sell_factor):
        self.sell_factor = sell_factor

    def activate(self):
        action = dialog.question(self.intro,
            ('I have an item to sell', 'I would like to make a purchase', 'Never mind'))
        if action == 0:
            self.do_sell()
        elif action == 1:
            choice = dialog.question('Select the item your heart desires:', self.item_names)
            if choice >= len(self.item_names)-1:
                dialog.message("Come back when you are ready to order!")
                return
            item = self.item_list[choice]
            hero = core.game.save_data.hero
            if item.value <= hero.get_gold():
                hero.add_gold( -item.get_value() )
                self.purchased(item)
            else:
                dialog.message('Come back when you have accumulated enough gold!')

    def do_sell(self):
        all_items = core.game.save_data.hero.get_inventory()[:]
        items = filter(lambda x: x.get_value()>0, all_items)
        item_names = map(self.sell_text, items)
        item_names.append('Never mind')
        choice = dialog.question('Select the item you are interested in selling:', item_names)
        if choice == len(items):
            return
        else:
            item = items[choice]
            hero = core.game.save_data.hero
            hero.get_inventory().remove(item)
            hero.add_gold( int(item.get_value()*self.sell_factor) )
            dialog.message('A bargain at twice the price!')
            
    def sell_text(self, item):
        return '%d - %s' % ( int(item.get_value()*self.sell_factor), item.get_name() )

    def item_text(self, item):
        return '%d - %s' % (item.get_value(), item.get_name())

    def purchased(self, item):
        core.game.save_data.hero.give_item(item)

class Townsperson(MapEntity):
    "A normal MapEntity that talks when activated and moves around on its own"
    
    def __init__(self,image=None):
        MapEntity.__init__(self,image)
        self.__next_move = 30

    def set_dialog(self, messages):
        """set_dialog(Tuple or Array)
           The strings in the array will be spoken in a loop"""
        self.dialog_text = messages
        self.current_dialog = 0

    def activate(self):
        dialog.message(self.dialog_text[self.current_dialog])
        self.current_dialog = self.current_dialog + 1
        if self.current_dialog >= len(self.dialog_text):
            self.current_dialog = 0

    def move_to(self, pos):
        MapEntity.move_to(self, pos)
        self.base_pos = pos

#TODO Make the Townsperson stay home.  I.E. make the random direction
#TODO     statistically keep the townsperson stay within a certain range
#TODO     from where they were last moved to
    def update(self):
        if not self.moving:
            if self.__next_move < 1:
                self.__next_move = random.randint(10,75)
                direction = random.randint(0,3)
                self.move(direction)
            self.__next_move = self.__next_move - 1
        MapEntity.update(self)
