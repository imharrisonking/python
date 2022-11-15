'''
Script demonstrates how developers can override __repr__, __str__ and __format__ 
to return a more useful object representation of a string, which is ideally formatted as
source code for a constructor call
'''

class Position:

    def __init__(self, latitude, longitude):
        if not (-90 <= latitude <= +90):
            raise ValueError(f"Latitude {latitude} out of range")

        if not (-180 <= longitude <= +180):
            raise ValueError(f"Longitude {longitude} out of range")

        self._latitude = latitude
        self._longitude = longitude

    @property
    def latitude(self):
        return self._latitude

    @property
    def longitude(self):
        return self._longitude

    @property
    def latitude_hemisphere(self):
      return 'N' if self.latitude >= 0 else 'S'
    
    @property
    def longitude_hemisphere(self):
      return 'E' if self.longitude >= 0 else 'W'

    # __repr__ is designed for use for the developer. Convetions are to 1. Include necessary state, but be prepared to compromise 2. Format as constructor invocation source code
    def __repr__(self):
        return f'{typename(self)}(latitude={self.latitude}, longitude={self.longitude})'

    # __str__ delegates to __format__ with the default argument of 2 decimal places
    def __str__(self):
      return format(self)
    
    # __format__ gives represenation for users but gives more control than __str__ as it is interpreted by format strings
    def __format__(self, format_spec):
      component_format_spec = '.2f'
      prefix, dot, suffix = format_spec.partition('.')
      if dot:
        num_decimals = int(suffix)
        component_format_spec = f'.{num_decimals}f'

      latitude = format(abs(self.latitude), component_format_spec)
      longitude = format(abs(self.longitude), component_format_spec)
      return (
        f'{latitude}° {self.latitude_hemisphere}, '
        f'{longitude}° {self.longitude_hemisphere}'
      )

class EarthPosition(Position):
  pass

class MarsPosition(Position):
  pass

# Utility class using dunder name and type(object) to get the name of an object
def typename(obj):
    return type(obj).__name__