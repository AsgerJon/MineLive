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
    LayoutWindow.show(self)
    self.setupActions()

  def setupActions(self) -> None:
    """Sets up the actions"""
  #
  # def handleLeftPressHold(self) -> None:
  #   """Handles the left press hold signal"""
  #
  # def debugFunc01(self) -> None:
  #   """omg"""
  #   Sound.error.play()
  #
  # def debugFunc02(self) -> None:
  #   """omg"""
  #   Sound.ursodumbfr.play()
