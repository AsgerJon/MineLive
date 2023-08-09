"""PaintWidget subclasses the CoreWidget and implements the paintEvent. """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QColor

from workside.widgets import CoreWidget


class PaintWidget(CoreWidget):
  """PaintWidget subclasses the CoreWidget and implements the paintEvent. """

  def __init__(self, *args, **kwargs) -> None:
    CoreWidget.__init__(self, *args, **kwargs)
    self._backgroundColor = None

  def _createBackgroundColor(self) -> None:
    """Creator-function for the background color"""

  def _getBackgroundColor(self) -> QColor:
    """Getter-function for background color"""
