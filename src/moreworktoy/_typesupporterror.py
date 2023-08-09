"""TypeSupportError is a custom exception intended to be raised by
functions invoked with arguments of unsupported types. """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from moreworktoy import Field


class TypeSupportError(Exception):
  """TypeSupportError is a custom exception intended to be raised by
  functions invoked with arguments of unsupported types. """

  def __init__(self, supportedType: type, arg: Any, varName: str) -> None:
    self._supportedType = Field()
