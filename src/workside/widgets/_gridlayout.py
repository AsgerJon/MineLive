"""GridLayout subclasses QGridLayout streamlining and simplifying layout
management at the cost of flexibility."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Signal, QEvent
from PySide6.QtWidgets import QGridLayout, QLayoutItem, QWidgetItem
from worktoy.parsing import maybeTypes

from workside.widgets import CoreWidget


class GridLayout(QGridLayout):
  """GridLayout subclasses QGridLayout streamlining and simplifying layout
  management at the cost of flexibility."""

  receivedPaintEvent = Signal()

  def __init__(self, *_) -> None:
    QGridLayout.__init__(self, )
    self._widgets = {}
    self._curInd = 0

  def _rowAt(self, index: int) -> int:
    """Returns the row matching the index. """
    rowCount = self.rowCount()
    if not rowCount:
      raise IndexError('Empty Layout!')
    return int(index % self.rowCount())

  def _colAt(self, index: int) -> int:
    """Returns the column matching the index."""
    rowCount = self.rowCount()
    if not rowCount:
      raise IndexError('Empty Layout!')
    return int(index // self.columnCount())

  def _rowColIndex(self, row: int, col: int) -> int:
    """Returns the index for the cell at given row and column"""
    return self.rowCount() * col + row

  def _getWidgets(self) -> dict[int, CoreWidget]:
    """Getter-function for list of widgets"""
    return self._widgets

  def addWidget(self, widget: CoreWidget, *args, **kwargs) -> None:
    """Reimplementation connecting paint event signals from each widget"""
    intArgs = maybeTypes(int, *args)
    row, col = intArgs[:2]
    self._getWidgets().update([(self._rowColIndex(row, col), widget)])
    QGridLayout.addWidget(self, widget, *args)

  def __iter__(self) -> GridLayout:
    """Implementation of iteration"""
    self._curInd = 0
    return self

  def __next__(self) -> CoreWidget:
    """Implementation of iteration"""
    out = None
    while out is None:
      self._curInd += 1
      if self._curInd > self.rowCount() * self.columnCount():
        raise StopIteration
      out = self._getWidgets().get(self._curInd - 1, None)
    return out
