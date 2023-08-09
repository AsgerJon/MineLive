"""CoreWidget subclasses QWidget providing common and general
functionality."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QRectF, QRect, QPointF, QSizeF, QSize, Signal
from PySide6.QtGui import QResizeEvent
from PySide6.QtWidgets import QWidget
from icecream import ic

from workside.functional import parseParent
from workside.settings import Settings
from workside.styles import BaseStyle

ic.configureOutput(includeContext=True)


class CoreWidget(QWidget):
  """CoreWidget subclasses QWidget providing common and general
  functionality."""

  resized = Signal()
  newSize = Signal(QSize)

  def __init__(self, *args, **kwargs) -> None:
    parent = parseParent(*args, **kwargs)
    QWidget.__init__(self, parent)
    self._parent = parent
    self._style = None

  def update(self, *args, **kwargs) -> None:
    """Reimplementation emitting signals when update request is received
    and when it is completed"""
    QWidget.update(self, *args, **kwargs)

  def _setParent(self, parent: CoreWidget) -> None:
    """Setter-function for the parent widget. When using this method the
    parent argument is expected to be of type CoreWidget"""
    if isinstance(parent, CoreWidget):
      self._parent = parent
    else:
      raise TypeError

  def getParent(self) -> CoreWidget:
    """Getter-function for the parent. Using the explicit getter and
    setter for the parent widget requires them to be of type CoreWidget"""
    if isinstance(self._parent, CoreWidget):
      return self._parent
    e = """Expected parent to be of type CoreWidget, but received %s!"""
    raise TypeError(e % type(self._parent))

  def _createStyle(self) -> None:
    """Creator function for the default style"""
    self._style = BaseStyle('default', )

  def getStyle(self) -> BaseStyle:
    """Getter-function for the style"""
    if self._style is None:
      self._createStyle()
      return self.getStyle()
    if isinstance(self._style, BaseStyle):
      return self._style
    raise TypeError

  def setStyle(self, style: BaseStyle) -> None:
    """Setter-function for the style"""
    if isinstance(style, BaseStyle):
      self._style = style
    else:
      e = """Expected parent to be of type BaseStyle, but received %s!"""
      raise TypeError(e % type(self._parent))

  def show(self) -> None:
    """Reimplementation"""
    return QWidget.show(self)

  def __rmatmul__(self, other: BaseStyle) -> CoreWidget:
    """Applies given base style to self"""
    self.setStyle(other)
    return self

  def getViewPortF(self) -> QRectF:
    """Getter-function for viewport as floating points"""
    r = self.visibleRegion().boundingRect().toRectF()
    left, top, width, height = r.left(), r.top(), r.right(), r.bottom()
    width = max(width, Settings.minimumWidgetSize.width())
    height = max(height, Settings.minimumWidgetSize.height())
    leftTop, size = QPointF(left, top), QSizeF(width, height)
    return QRectF(leftTop, size)

  def getViewPort(self) -> QRect:
    """Getter-function for viewport as integers"""
    return self.getViewPortF().toRect()

  def minimumSizeHint(self) -> QSize:
    """Implementation of minimum size hint"""
    return Settings.minimumWidgetSize

  def resizeEvent(self, event: QResizeEvent) -> None:
    """Connects to signal"""
    self.resized.emit()
    self.newSize.emit(event.size())
    QWidget.resizeEvent(self, event)
