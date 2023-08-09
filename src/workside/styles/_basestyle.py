"""BaseStyle"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import Qt, QRectF, QMargins
from PySide6.QtGui import QBrush, QFont, QPen, QColor, QPainter, \
  QFontMetricsF
from icecream import ic
from worktoy.core import maybe
from worktoy.typetools import TypeBag

from workside.settings import Settings
from workside.styles import Family

if TYPE_CHECKING:
  from workside.widgets import CoreWidget

  Graphic = TypeBag(QPainter, CoreWidget)

ic.configureOutput(includeContext=True)


class BaseStyle:
  """Instances must contain settings applied to QPainters"""

  _baseValues = dict(
    fillColor=QColor(0, 0, 0, 0),
    fillStyle=Qt.BrushStyle.SolidPattern,
    lineColor=QColor(0, 0, 0, 0),
    lineStyle=Qt.PenStyle.SolidLine,
    lineWidth=1,
    fontFamily=Family.COURIERNEW,
    fontWeight=QFont.Weight.Normal,
    fontSize=12,
    margins=Settings.labelMargins,
  )

  def __init__(self, name: str, data: dict = None) -> None:
    data = maybe(data, {})
    if not isinstance(data, dict):
      raise TypeError
    self._viewPort = None
    self._name = name
    self._data = {}
    for (key, val) in BaseStyle._baseValues.items():
      self._data |= {key: data.get(key, val)}
    self._fontMetrics = None
    self._margins = None

  def createMargins(self) -> None:
    """Creator-function for the margins"""

  def getMargins(self) -> QMargins:
    """Getter-function for the margins"""
    return self.getData().get('margins')

  def getData(self) -> dict:
    """Getter-function for data"""
    return self._data

  def getFont(self, ) -> QFont:
    """Getter-function for QFont"""
    font = self._data.get('fontFamily').asQFont()
    weight = self._data.get('fontWeight')
    font.setWeight(weight)
    fontSize = self._data.get('fontSize')
    font.setPointSize(max(fontSize, Settings.minimumFontSize))
    return font

  def _createFontMetrics(self) -> None:
    """Creator-function for font metrics"""
    self._fontMetrics = QFontMetricsF(self.getFont())

  def getFontMetrics(self) -> QFontMetricsF:
    """Getter-function for font metrics"""
    if self._fontMetrics is None:
      self._createFontMetrics()
      return self.getFontMetrics()
    if isinstance(self._fontMetrics, QFontMetricsF):
      return self._fontMetrics
    msg = """Expected front metrics to be of type %s, but received: %s!"""
    raise TypeError(msg % (QFontMetricsF, type(self._fontMetrics)))

  def getBoundingRect(self, text: str) -> QRectF:
    """Getter-function for bounding rect"""
    return self.getFontMetrics().boundingRect(text)

  def getBrush(self) -> QBrush:
    """Getter-function for QBrush"""
    brush = QBrush()
    brush.setStyle(self._data.get('fillStyle'))
    brush.setColor(self._data.get('fillColor'))
    return brush

  def getPen(self) -> QPen:
    """Getter-function for QPen"""
    pen = QPen()
    pen.setStyle(self._data.get('lineStyle'))
    pen.setColor(self._data.get('lineColor'))
    pen.setWidth(self._data.get('lineWidth'))
    return pen

  def __matmul__(self, other: Graphic) -> Graphic:
    """Applies these settings to the given painter"""
    if isinstance(other, QPainter):
      other.setPen(self.getPen())
      other.setFont(self.getFont())
      other.setBrush(self.getBrush())
      return other
    return NotImplemented

  def __str__(self) -> str:
    """String representation"""
    out = 'BaseStyle instance: %s' % (self._name)
    return out

  def __repr__(self, ) -> str:
    """Code Representation"""
    out = 'BaseStyle: %s\n' % self._name
    for (key, val) in self._data.items():
      entry = '  %s: %s\n' % (key, val)
      out += entry
    return out
