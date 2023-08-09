"""Family represents font families"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from enum import Enum

from PySide6.QtGui import QFont, QPainter
from PySide6.QtCore import QObject
from PySide6.QtWidgets import QWidget
from icecream import ic
from worktoy.core import maybe

ic.configureOutput(includeContext=True)


class Family(Enum):
  """Enum specifying font families"""
  ARIAL = 'Arial'
  TIMESNEWROMAN = 'Times New Roman'
  COURIERNEW = 'Courier New'
  VERDANA = 'Verdana'
  CAMBRIA = 'Cambria'
  TAHOMA = 'Tahoma'
  CALIBRI = 'Calibri'
  COMICSANSMS = 'Comic Sans MS'
  HELVETICA = 'Helvetica'
  GENEVA = 'Geneva'
  LUCIDAGRANDE = 'Lucida Grande'
  DEJAVUSANS = 'DejaVu Sans'
  DEJAVUSERIF = 'DejaVu Serif'
  DEJAVUSANSMONO = 'DejaVu Sans Mono'
  LIBERATIONSANS = 'Liberation Sans'
  LIBERATIONSERIF = 'Liberation Serif'
  LIBERATIONMONO = 'Liberation Mono'
  UBUNTU = 'Ubuntu'
  CANTARELL = 'Cantarell'
  DROIDSANS = 'Droid Sans'
  DROIDSERIF = 'Droid Serif'
  ROBOTO = 'Roboto'
  ROBOTOCONDENSED = 'Roboto Condensed'
  ROBOTOMONO = 'Roboto Mono'
  NOTOSANS = 'Noto Sans'
  NOTOSERIF = 'Noto Serif'
  NOTOSANSMONO = 'Noto Sans Mono'
  SOURCESANSPRO = 'Source Sans Pro'
  SOURCESERIFPRO = 'Source Serif Pro'
  SOURCECODEPRO = 'Source Code Pro'
  MODERN = 'Modern No. 20'

  def asQFont(self, size: int = None) -> QFont:
    """Creates a QFont version of self at font size given"""
    font = QFont()
    font.setFamily(self.value)
    font.setPointSize(maybe(size, 12))
    return font

  def __repr__(self) -> str:
    """Code representation"""
    return 'Family.%s' % self.name

  def __str__(self) -> str:
    """String representation"""
    return self.value

  def __rmatmul__(self, other: QObject) -> QObject | QPainter:
    """Applies font family to other"""
    if isinstance(other, QFont):
      other.setFamily(self.value)
      return other
    if isinstance(other, QWidget) or isinstance(other, QPainter):
      font = other.font()
      font.setFamily(self.value)
      other.setFont(font)
      if isinstance(other, QWidget) or isinstance(other, QPainter):
        return other
      raise TypeError
    return NotImplemented
