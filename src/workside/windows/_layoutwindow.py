"""LayoutWindow subclasses BaseWindow providing the visual widgets in the
window. While this class should not provide business logic, it should
implement methods for dynamic functionalities of the widgets."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QKeyEvent, QTextCursor
from PySide6.QtWidgets import QVBoxLayout, QGridLayout, QHBoxLayout
from PySide6.QtWidgets import QWidget
from icecream import ic

from workside.styles import headerStyle, labelStyle
from workside.widgets import CoreWidget, VSpacer, HSpacer
from workside.widgets import DoubleSpacer
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
    self._baseVerticalBoxLayout = None
    self._baseHorizontalBoxLayout = None
    self._horizontalSpacers = []
    self._verticalSpacers = []
    self._doubleSpacers = []

  def _createBaseVerticalLayout(self) -> None:
    """Creator-function for the vertical base layout"""
    self._baseVerticalBoxLayout = QVBoxLayout()

  def _getBaseVerticalBoxLayout(self) -> QVBoxLayout:
    """Getter-function for the vertical base layout"""
    if self._baseVerticalBoxLayout is None:
      self._createBaseVerticalLayout()
      return self._getBaseVerticalBoxLayout()
    if isinstance(self._baseVerticalBoxLayout, QVBoxLayout):
      return self._baseVerticalBoxLayout
    raise TypeError

  def _createHorizontalBoxLayout(self) -> None:
    """Creator function for the horizontal layout"""
    self._baseHorizontalBoxLayout = QHBoxLayout()

  def _getBaseHorizontalBoxLayout(self) -> QHBoxLayout:
    """Getter function for the horizontal layout"""
    if self._baseHorizontalBoxLayout is None:
      self._createHorizontalBoxLayout()
      return self._getBaseHorizontalBoxLayout()
    if isinstance(self._baseHorizontalBoxLayout, QHBoxLayout):
      return self._baseHorizontalBoxLayout
    raise TypeError

  def _createBaseLayout(self) -> None:
    """Creator-function for the base layout"""
    self._baseGridLayout = QGridLayout()

  def _getBaseLayout(self) -> QGridLayout:
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
    self._baseHeaderWidget.setText('Welcome to MineLive!')

  def _getBaseHeaderWidget(self) -> CoreWidget:
    """Getter-function for the header widget"""
    if self._baseHeaderWidget is None:
      self._createBaseHeaderWidget()
    if isinstance(self._baseHeaderWidget, CoreWidget):
      return self._baseHeaderWidget
    raise TypeError

  def _createBaseWidget(self) -> None:
    """Creator-function for the base widget"""
    self._baseWidget = CoreWidget()

  def _getBaseWidget(self) -> CoreWidget:
    """Getter-function for the base widget"""
    if self._baseWidget is None:
      self._createBaseWidget()
      return self._getBaseWidget()
    if isinstance(self._baseWidget, CoreWidget):
      return self._baseWidget

  def _createStructureLabel(self) -> None:
    """Creator-function for label indicating any present structure"""
    self._structureLabel = Label()
    labelStyle @ self._structureLabel
    self._baseHeaderWidget.setText('Welcome to MineLive!')

  def _getStructureLabel(self) -> CoreWidget:
    """Getter-function for the structure label"""

  def _getVSpacerList(self) -> list[VSpacer]:
    """Getter-function for the list of vertical spacers"""
    return self._verticalSpacers

  def _getVSpacer(self) -> VSpacer:
    """Getter-function for the vertical spacer"""
    spacer = VSpacer()
    self._getVSpacerList().append(spacer)
    return spacer

  def _getHSpacerList(self) -> list[HSpacer]:
    """Getter-function for the list of horizontal spacers"""
    return self._horizontalSpacers

  def _getHSpacer(self) -> HSpacer:
    """Getter function for horizontal spacers"""
    spacer = HSpacer()
    self._getHSpacerList().append(spacer)
    return spacer

  def _getDoubleSpacerList(self) -> list[DoubleSpacer]:
    """Getter-function for list of double spacers"""
    return self._doubleSpacers

  def _getDoubleSpacer(self) -> DoubleSpacer:
    """Getter-function for double spacer"""
    spacer = DoubleSpacer()
    self._getDoubleSpacerList().append(spacer)
    return spacer

  def setupWidgets(self) -> None:
    """Sets up the widgets"""
    self._getBaseLayout().addWidget(self._getBaseHeaderWidget(), 0, 0, 1, 1)
    self._getBaseLayout().addWidget(self._getStructureLabel(), 1, 0, 1, 1)
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
