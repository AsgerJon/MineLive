"""MainWindow"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from icecream import ic

from workside.windows import LayoutWindow

ic.configureOutput(includeContext=True)


class MainWindow(LayoutWindow):
  """MainWindow
  #  Copyright (c) 2023 Asger Jon Vistisen
  #  MIT Licence"""

  def __init__(self, ) -> None:
    LayoutWindow.__init__(self)
    self.setMinimumWidth(480)
    self.setMinimumHeight(640)
    self.setWindowTitle('Welcome to WorkSide!')

  def show(self) -> None:
    """Reimplementation of show method"""
    self.setupActions()
    LayoutWindow.show(self)
    for widget in self._getBaseLayout():
      widget.update()
      print(widget)
    self._getBaseLayout().parentWidget().repaint()

  def setupActions(self) -> None:
    """Sets up the actions"""

  def _paintMe(self) -> None:
    """Announces having received a paint event."""
    print('paint event received')

  def _receivedUpdate(self) -> None:
    """DEBUGGER"""
    print('update requested')

  def _completeUpdate(self) -> None:
    """DEBUGGER"""
    print('update completed')

  def debugFunc01(self) -> None:
    """LOL"""
    print(self._getBaseLayout().parentWidget())

  def debugFunc02(self) -> None:
    """LOL"""
    print(self._getBaseLayout().parentWidget().update())
