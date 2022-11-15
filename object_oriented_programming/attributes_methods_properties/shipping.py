import iso6346


class ShippingContainer:

  HEIGHT_FT = 8.5
  WIDTH_FT = 8.0
  FRIDGE_VOLUME_FT3 = 100

  next_serial = 1337

  # @classmethod used for method with needs the class (cls) but not the instance (self)
  @classmethod
  def _generate_serial(cls):
    result = cls.next_serial
    cls.next_serial += 1
    return result

  # @staticmethod needs neither the class nor the instance (no cls or self)
  @staticmethod
  def _make_bic_code(owner_code, serial):
    return iso6346.create(
      owner_code=owner_code, 
      serial=str(serial).zfill(6)
    )
  
  @classmethod
  def create_empty(cls, owner_code, length_ft, **kwargs):
    return cls(owner_code, length_ft, contents=[], **kwargs)

  @classmethod
  def create_with_items(cls, owner_code, length_ft, items, **kwargs):
    return cls(owner_code, length_ft, contents=list(items), **kwargs)

  # To ensure polymorphic behaviour with the static _make_bic_code method, we must use self._make_bic_code to ensure it acts on the instance of the class object
  def __init__(self, owner_code, length_ft, contents, **kwargs):
    self.owner_code = owner_code
    self.length_ft = length_ft
    self.contents = contents
    self.bic = self._make_bic_code(
      owner_code=owner_code, 
      serial=ShippingContainer._generate_serial() 
    )
  
  # @property decorator instead of getters and setters functions
  @property
  def volume_ft3(self):
    return self._calc_volume()

  def _calc_volume(self):
    return ShippingContainer.HEIGHT_FT * ShippingContainer.WIDTH_FT * self.length_ft


class RefrigeratedShippingContainer(ShippingContainer):

  MAX_CELSIUS = 4.0

  def __init__(self, owner_code, length_ft, contents, *, celsius, **kwargs):
    super().__init__(owner_code, length_ft, contents, **kwargs)
    if celsius > RefrigeratedShippingContainer.MAX_CELSIUS:
      raise ValueError('Temperature too hot!')
    self.celsius = celsius
  
  @staticmethod
  def _c_to_f(celsius):
    return celsius * 9/5 + 32
  
  @staticmethod
  def _f_to_c(farenheit):
    return (farenheit - 32) * 5/9

  # With the celsius property, we use the template method to delegate to regular methods (_set_celsius) and use those methods to override properties instead
  @property
  def celsius(self):
    return self._celsius
    
  @celsius.setter
  def celsius(self, value):
    self._set_celsius(value)
  
  # Delegation means it's easier for the HeatedRefrigeratedShippingContainer class to inherit this value check of "Too hot" and can implement it's own instance check of "Too cold" without having to repeat code
  def _set_celsius(self, value):
    if value > RefrigeratedShippingContainer.MAX_CELSIUS:
      raise ValueError('Temperature too hot!')
    self._celsius = value

  @property
  def fahrenheit(self):
    return RefrigeratedShippingContainer._c_to_f(self.celsius)
  
  @fahrenheit.setter
  def fahrenheit(self, value):
    self.celsius = RefrigeratedShippingContainer._f_to_c(value)

  def _calc_volume(self):
    return (
      super()._calc_volume()
      - RefrigeratedShippingContainer.FRIDGE_VOLUME_FT3
    )

  @staticmethod
  def _make_bic_code(owner_code, serial):
    return iso6346.create(
      owner_code=owner_code,
      serial=str(serial).zfill(6),
      category='R'
    )

class HeatedRefrigeratedShippingContainer(RefrigeratedShippingContainer):

  MIN_CELSIUS = -20

  def _set_celsius(self, value):
    if value < HeatedRefrigeratedShippingContainer.MIN_CELSIUS:
      raise ValueError('Temperature too cold!')
    super()._set_celsius(value)