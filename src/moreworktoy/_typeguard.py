"""TypeGuard is a class ensuring that a given argument belongs to the
proper class or type. The baseclass may be used as it is, but can also be
subclassed to include type casting explicitly. """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from worktoy.parsing import extractArg
from worktoy.stringtools import stringList

from moreworktoy import Field, PermissionLevel

readOnly = PermissionLevel.READ_ONLY


class TypeGuard:
  """TypeGuard is a class ensuring that a given argument belongs to the
  proper class or type. The baseclass may be used as it is, but can also be
  subclassed to include type casting explicitly. """

  def __init__(self, *args, **kwargs) -> None:
    typeKeys = stringList('type_, type, fieldType, supportType')
    self._type, args, kwargs = extractArg(type, typeKeys, *args, **kwargs)

  def __call__(self, arg: Any) -> bool:
    """Testing guard against given argument"""

  def _typeCast(self, arg: Any) -> Any:
    """Casts the given argument as the type given by the expectedType
    property"""
