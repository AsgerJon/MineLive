"""LayoutWindow subclasses BaseWindow providing the visual widgets in the
window. While this class should not provide business logic, it should
implement methods for dynamic functionalities of the widgets."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QKeyEvent, QTextCursor, QPaintEvent
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QWidget
from icecream import ic

from workside.styles import headerStyle, labelStyle
from workside.widgets import CoreWidget, LayoutBackground, GridLayout
from workside.widgets import Label
from workside.windows import BaseWindow

wordStart = QTextCursor.MoveOperation.StartOfWord
wordEnd = QTextCursor.MoveOperation.EndOfWord
move = QTextCursor.MoveMode.MoveAnchor
mark = QTextCursor.MoveMode.KeepAnchor

ic.configureOutput(includeContext=True)


class LayoutWindow(BaseWindow):
  """LayoutWindow subclasses BaseWindow providing the visual widgets in the
  window. While this class should not provide business logic, it should
  implement methods for dynamic functionalities of the widgets."""

  def __init__(self, parent: QWidget = None) -> None:
    BaseWindow.__init__(self, parent)
    self._baseHeaderWidget = None
    self._debugButton = None
    self._debugButton2 = None
    self._baseWidget = None
    self._structureLabel = None
    self._centralWidget = None
    self._baseGridLayout = None
    self._horizontalSpacers = []
    self._verticalSpacers = []
    self._doubleSpacers = []

  def _createBaseLayout(self) -> None:
    """Creator-function for the base layout"""
    self._baseGridLayout = GridLayout()

  def _getBaseLayout(self) -> GridLayout:
    """Getter-function for the base layout"""
    if self._baseGridLayout is None:
      self._createBaseLayout()
      return self._getBaseLayout()
    if isinstance(self._baseGridLayout, QGridLayout):
      return self._baseGridLayout

  def _createBaseHeaderWidget(self) -> None:
    """Creator-function for the header widget"""
    self._baseHeaderWidget = Label()
    headerStyle @ self._baseHeaderWidget
    self._baseHeaderWidget.setText('Hardcore!')

  def _getBaseHeaderWidget(self) -> CoreWidget:
    """Getter-function for the header widget"""
    if self._baseHeaderWidget is None:
      self._createBaseHeaderWidget()
    if isinstance(self._baseHeaderWidget, CoreWidget):
      return self._baseHeaderWidget
    raise TypeError

  def _createBaseWidget(self) -> None:
    """Creator-function for the base widget"""
    self._baseWidget = LayoutBackground()

  def _getBaseWidget(self) -> LayoutBackground:
    """Getter-function for the base widget"""
    if self._baseWidget is None:
      self._createBaseWidget()
      return self._getBaseWidget()
    if isinstance(self._baseWidget, LayoutBackground):
      return self._baseWidget

  def _createStructureLabel(self) -> None:
    """Creator-function for label indicating any present structure"""
    self._structureLabel = Label()
    labelStyle @ self._structureLabel
    self._structureLabel.setText('TechWorld!')

  def _getStructureLabel(self) -> CoreWidget:
    """Getter-function for the structure label"""
    if self._structureLabel is None:
      self._createStructureLabel()
      return self._getStructureLabel()
    if isinstance(self._structureLabel, CoreWidget):
      return self._structureLabel

  def setupWidgets(self) -> None:
    """Sets up the widgets"""
    self._getBaseLayout().addWidget(self._getBaseHeaderWidget(), 0, 0, 1, 1)
    self._getBaseLayout().addWidget(self._getStructureLabel(), 1, 1, 1, 1)
    self._getBaseWidget().setLayout(self._getBaseLayout())
    self.setCentralWidget(self._getBaseWidget())

  def show(self) -> None:
    """Sets up the widgets before invoking the show super call"""
    self.setupWidgets()
    BaseWindow.show(self)

  def keyReleaseEvent(self, event: QKeyEvent) -> None:
    """Triggers spell checking"""
    BaseWindow.keyReleaseEvent(self, event)

  def keyPressEvent(self, event: QKeyEvent) -> None:
    """Triggers spell checking"""
    BaseWindow.keyPressEvent(self, event)
