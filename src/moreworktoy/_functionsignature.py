"""FunctionSignature instances specify a combination of positional
arguments. The instances are used by the Overloader class in support of
the WorkType metaclass. """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from moreworktoy import Args, Field


class FunctionSignature:
  """FunctionSignature instances specify a combination of positional
  arguments. The instances are used by the Overloader class in support of
  the WorkType metaclass. """

  sig = Field(list)

  @staticmethod
  def _getSig(*args) -> list[type]:
    """Getter-function for the types of the given positional arguments"""
    return [type(arg) for arg in args]

  def __init__(self, *args, **kwargs) -> None:
    args = Args(*args)
    self.sig << (args @ type)
