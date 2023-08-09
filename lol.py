
class LegitClass:
  pass


class TrollClass:
  """LMAO"""

  def __init__(self, *args, **kwargs) -> None:
    pass

  def __getattribute__(self, name) -> Any:
    """YEET!"""
    if name == '__class__':
      return 'LegitClass'
    return object.__getattribute__(self, name)
