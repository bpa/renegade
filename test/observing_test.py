import unittest
import observing

class ObservableClass(observing.Observable):
  def __init__(self):
    self.one = 1
    self.two = 2

class BaseClass:
  def __init__(self):
    self.zero = 'zero'

class ObsSubClassOne(ObservableClass):
  def __init__(self):
    self.classone = 'one'

class ObsSubClassTwo(ObsSubClassOne):
  def __init__(self):
    self.classtwo = 'two'
  
class ObservingTest(unittest.TestCase):
  def setUp(self):
    self.object  = None
    self.field   = None
    self.old_val = None
    self.new_val = None

  def handle_observation(self, object, field, old_val, new_val):
    self.object  = object
    self.field   = field
    self.old_val = old_val
    self.new_val = new_val

  def test_assign(self):
    oc = ObservableClass()
    oc.add_observer(self)
    oc.one = 2
    self.assertEqual( oc,   self.object)
    self.assertEqual('one', self.field)
    self.assertEqual( 1,    self.old_val)
    self.assertEqual( 2,    self.new_val)

  def test_assign_new_field(self):
    oc = ObservableClass()
    oc.add_observer(self)
    oc.new = "hi"
    self.assertEqual( oc,   self.object)
    self.assertEqual('new', self.field)
    self.assertEqual( None, self.old_val)
    self.assertEqual( "hi", self.new_val)

  def test_field_mask(self):
    oc = ObservableClass()
    oc.add_observer(self,['one','new'])
    oc.two = "hi"
    self.assertEqual(None,  self.field)
    oc.one = "One"
    self.assertEqual('one', self.field)
    oc.new = "New"
    self.assertEqual(None,  self.old_val)
    self.assertEqual("New", self.new_val)

  def test_inheritance(self):
    one = ObsSubClassOne()
    two = ObsSubClassTwo()
    one.add_observer(self)
    two.add_observer(self)
    one.zero = 0
    self.assertEqual( 0, self.new_val)
    one.classone = 1
    self.assertEqual( 1, self.new_val)
    two.classone = 2
    self.assertEqual( 2, self.new_val)
    two.classtwo = 3
    self.assertEqual( 3, self.new_val)
