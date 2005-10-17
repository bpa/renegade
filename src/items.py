import core, os
import shelve
import dice

__item_shelf = {}
__name_index = {}

class Item(object):
    def __init__(self,id,name,value):
        self.id = id
        self.name = name
        self.value = int(value)
        self.image = None
        self.image_name = None

    def get_name(self):
        return self.name

    def get_value(self):
        return self.value

    def __getstate__(self):
        dict = self.__dict__.copy()
        dict.pop('image')
        return dict

    def __setstate__(self,dict):
        self.__dict__ = dict
        self.image = None

class Weapon(Item):
    def __init__(self, id, name, value=0, damage='1d1'):
        Item.__init__(self, id, name, value)
        self.damage = damage

    def get_damage(self):
        return dice.roll(self.damage)
    
class Armor(Item):
    def __init__(self, id, name, value=0, rating=0):
        Item.__init__(self, id, name, value)
        self.rating = int(rating)

    def get_rating(self):
        return self.rating

def init(basedir):
    '''Loads items file found in games directory'''
    global __item_shelf, __name_index
    csv = os.path.join(basedir,'items.csv')
    db = os.path.join(basedir,'items')
    idx = os.path.join(basedir,'item_index')
    try:
        db_st_mtime = os.stat(db).st_mtime
    except:
        db_st_mtime = 0
    if os.stat(csv).st_mtime > db_st_mtime:
        __write_items_db(csv,db,idx)
    else:
        __item_shelf = shelve.open(db)
        __name_index = shelve.open(idx)

def get_item(name):
    '''Looks up item by name or id and returns the item or None if not found'''
    global __item_shelf, __name_index
    if __item_shelf.has_key(name):
      return __item_shelf[name]
    if __name_index.has_key(name):
      return __item_shelf[__name_index[name]]
    return None

def get_items(*list):
    '''Returns a list of items passed in by name or id.
If an item in the list does not exist, it is not returned.  This means it is
possible to get an empty list back'''
    ret = []
    for name in list:
      item = get_item(name)
      if item != None: ret.append(item)
    return ret

def __write_items_db(csv_file, db_file, idx_file):
    global __item_shelf, __name_index
    csv = open(csv_file,'r')
    __item_shelf = shelve.open(db_file)
    __name_index = shelve.open(idx_file)
    reading = True
    while reading:
      line = csv.readline()
      if line == '': break
      line = line.split('#',1)[0] #strip comments and sp
      info = line.split(',')
      if len(info) > 1:
          info = map(lambda s: s.strip(), info)
          id = info[0]
          if id.startswith('A'):
              __item_shelf[id] = Armor(*info)
              __name_index[info[1]] = id
          if id.startswith('W'):
              __item_shelf[id] = Weapon(*info)
              __name_index[info[1]] = id
