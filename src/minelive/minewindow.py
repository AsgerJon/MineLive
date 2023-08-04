"""MineWindow subclasses BaseWindow"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from workside.windows import MainWindow


class MineWindow(MainWindow):
  """MineWindow subclasses BaseWindow"""

  def __init__(self) -> None:
    super().__init__()
