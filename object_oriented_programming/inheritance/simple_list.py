class SimpleList:
  def __init__(self, items):
    self._items = list(items)
  
  def add(self, item):
    self._items.append(item)
  
  def __getitem__(self, index):
    return self._items[index]
  
  def sort(self):
    self._items.sort()

  def __len__(self):
    return len(self._items)
  
  def __repr__(self):
    return f'{type(self).__name__}({self._items!r})'

class SortedList(SimpleList):
  def __init__(self, items=()):
    super().__init__(items)
    self.sort()
  
  def add(self, item):
    super().add(item)
    self.sort()

class IntList(SortedList):
  def __init__(self, items=()):
    for x in items: self._validate(x)
    s = super()
    print(s)
    s.__init__(items)
    print(s.__init__)
  
  # isinstance(x, int) returns True if x is an int, otherwise returns False
  @staticmethod
  def _validate(x):
    if not isinstance(x, int):
      raise TypeError('IntList only supports integer values')
    
  def add(self, item):
    self._validate(item)
    super().add(item)

# We can create a class that uses multiple inheritance by specifying the base classes it should inherit as a tuple list
class SortedIntList(IntList, SortedList):
  pass