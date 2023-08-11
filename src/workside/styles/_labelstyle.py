"""LabelStyle instances specify particular styles used by instances of
Label. """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Never

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor

from moreworktoy import (ReadOnlyError, ProtectedPropertyError,
                         AbstractField, \
  PermissionLevel)
from workside.styles import Family

readOnly = PermissionLevel.READ_ONLY


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

  def __init__(self, name: str, **kwargs) -> None:
    self._data = LabelStyle.defaultValues | kwargs
    self._name = AbstractField(name, readOnly, name=name)
