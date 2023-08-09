"""LabelStyle instances specify particular styles used by instances of
Label. """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Never

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor

from moreworktoy import ReadOnlyError, ProtectedPropertyError
from workside.styles import Family


class LabelStyle:
  """LabelStyle instances specify particular styles used by instances of
  Label. """

  defaultValues = dict(
    fontFamily=Family.MODERN,
    fontSize=12,
    fontWeight=QFont.Weight.Normal,
    fontColor=QColor(0, 0, 0, 255),
    textAlign=Qt.AlignmentFlag.AlignCenter,
    padding=2,
    border=1,
    margin=2,
  )

  def __init__(self, name: str, data: str, **kwargs) -> None:
    self._data = data
    self._data |= dict(**kwargs)
    self._name = name

  def _getName(self) -> str:
    """Getter-function for name"""
    return self._name

  def _setName(self, *_) -> Never:
    """Setter-function for name"""
    raise ReadOnlyError('name')

  def _delName(self) -> Never:
    """Illegal deleter-function"""
    raise ProtectedPropertyError('name')

  name = property(_getName, _setName, _delName)
