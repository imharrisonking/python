class Base:
  def __init__(self):
    print('Base initialiser')
  
  def f(self):
    print('Base.f()')

class Sub(Base):
  def __init__(self):
    super().__init__()
    print('Sub initialiser')
  
  def f(self):
    print('Sub.f()')