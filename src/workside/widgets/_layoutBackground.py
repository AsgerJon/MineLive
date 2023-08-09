"""LayoutBackground is a subclass of CoreWidget useful for providing a
background on which to hold layouts."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPen, QColor, QBrush, QPaintEvent, QPainter
from PySide6.QtWidgets import QGridLayout, QSizePolicy
from worktoy.waitaminute import ProceduralError

from workside.widgets import CoreWidget, GridLayout


class LayoutBackground(CoreWidget):
  """LayoutBackground is a subclass of CoreWidget useful for providing a
  background on which to hold layouts."""

  @staticmethod
  def _getPen() -> QPen:
    """Getter-function for the pen"""
    pen = QPen()
    pen.setStyle(Qt.PenStyle.SolidLine)
    pen.setColor(QColor(0, 0, 0, 255))
    pen.setWidth(2)
    return pen

  @staticmethod
  def _getBrush() -> QBrush:
    """Getter-function for the pen"""
    brush = QBrush()
    brush.setStyle(Qt.BrushStyle.SolidPattern)
    brush.setColor(QColor(223, 223, 223, 255))
    return brush

  def setLayout(self, layout: GridLayout) -> None:
    """Setter-function for the grid layout. Please note that only
    GridLayout instances are supported."""
    maxPolicy = QSizePolicy.Policy.Maximum
    minPolicy = QSizePolicy.Policy.MinimumExpanding
    self.setSizePolicy(maxPolicy, maxPolicy)
    if isinstance(layout, GridLayout):
      CoreWidget.setLayout(self, layout)
      for widget in layout:
        widget.setSizePolicy(minPolicy, minPolicy)
        widget.resized.connect(self._updateSlot)
        widget.adjustSize()
    else:
      e = """Expected layout to be of type %s, but received %s!"""
      raise TypeError(e % (GridLayout, type(layout)))

  def _updateSlot(self, *_) -> None:
    """Receives the update notification"""
    self.update()

  def paintEvent(self, event: QPaintEvent) -> None:
    """Implementation of the paint event."""
    layout = self.layout()
    if layout is None:
      raise ProceduralError(name=layout, type_=QGridLayout, )
    if not isinstance(layout, QGridLayout):
      e = """Expected layout to be of type %s, but received %s!"""
      raise TypeError(e % (QGridLayout, type(layout)))
    painter = QPainter()
    painter.begin(self)
    painter.setPen(self._getPen())
    painter.setBrush(self._getBrush())
    for row in range(layout.rowCount()):
      for col in range(layout.columnCount()):
        painter.drawRect(layout.cellRect(row, col))
    blankBrush = QBrush()
    blankBrush.setStyle(Qt.BrushStyle.NoBrush)
    bluePen = QPen()
    bluePen.setStyle(Qt.PenStyle.SolidLine)
    bluePen.setWidth(3)
    bluePen.setColor(QColor(0, 0, 255, 255))
    painter.setPen(bluePen)
    painter.setBrush(blankBrush)
    painter.drawRect(self.layout().contentsRect())
    painter.end()

  def __repr__(self) -> str:
    """Code representation"""
    return 'LayoutBackground()'

  def __str__(self) -> str:
    """String representation"""
    return 'LayoutBackground'
