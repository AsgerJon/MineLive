"""Keys is a class used to extract values from dictionaries or from
keyword arguments. """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from icecream import ic
from worktoy.core import maybe
from worktoy.stringtools import stringList

from moreworktoy import Args

ic.configureOutput(includeContext=True)


class Keys(list):
  """cunts"""

  def __init__(self, *args) -> None:
    args = Args(*args)
    posArgs = args @ str
    list.__init__(self, )
    for arg in posArgs:
      for key in stringList(arg):
        self.append(key)

  def prepend(self, element: Any) -> None:
    """Appends at the beginning"""
    self.insert(element, 0)

  def __rshift__(self, other: dict) -> Any:
    for key in self:
      val = other.get(key, None)
      if val is not None:
        return val
      val = other.get(key.lower(), None)
      if val is not None:
        return val
    return None

  def __rrshift__(self, other: str) -> Keys:
    """Inserts another key into the list of keys"""
    self.prepend(other)
    return self

  def _stringJoin(self, separator: str = None) -> str:
    """Returns a string of the current elements with the given separator.
    This separator defaults to an empty string."""
    s = maybe(separator, '')
    if isinstance(s, str):
      return s.join([str(arg) for arg in self])
    raise TypeError

  def __repr__(self, ) -> str:
    """Code Representation"""
    return 'Keys(%s)' % (self._stringJoin(', '))

  def __str__(self) -> str:
    """String Representation"""
    title = """Instance of \'Keys\'"""
    subtitle = 'Providing the following keys:'
    keys = self._stringJoin('\n')
    return '\n'.join([title, subtitle, keys])
