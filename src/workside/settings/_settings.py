"""Settings provides a centrally defined collection of settings"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QSize, QMargins
from PySide6.QtGui import QFont
from icecream import ic

ic.configureOutput(includeContext=True)


class Settings:
  """Settings provides a centrally defined collection of settings
  #  Copyright (c) 2023 Asger Jon Vistisen
  #  MIT Licence"""

  headerLabelWidth = 60
  soundName = 'razer'

  movingDelayTime = 200
  releaseDeadLineTime = 350
  pressHoldTime = 500
  singleClickLockoutTime = 300
  doubleClickLockoutTime = 200
  releaseClickDelayTime = 100

  minimumWidgetSize = QSize(32, 32)
  minimumFontSize = 10

  #  Label
  labelMargins = QMargins(4, 4, 4, 4)
  labelPadding = QMargins(2, 2, 2, 2)

  defaultFont = QFont()
  from workside.styles import Family
  defaultFont @ Family.COURIERNEW
  defaultFont.setWeight(QFont.Weight.Normal)
  defaultFont.setPointSize(12)

  DEBUGGING = True
