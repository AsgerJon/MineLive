"""The 'functional' package provides convenient utility functions for use
in the WorkSide framework"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QWidget
from worktoy.parsing import extractArg
from worktoy.stringtools import stringList


def parseParent(*args, **kwargs) -> QWidget:
  """Parses arguments to parent"""
  parentKeys = stringList('parent, main, mainWindow, window')
  parent, args, kwargs = extractArg(QWidget, parentKeys, *args, **kwargs)
  if isinstance(parent, QWidget):
    return parent
 