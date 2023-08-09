"""Label provides an alternative to QLabel"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import string
from random import choices

from PySide6.QtCore import Qt, QRectF, QMargins
from PySide6.QtGui import QPaintEvent, QPainter, QFontMetrics, QFont, QColor
from icecream import ic
from worktoy.core import maybe

from workside.styles import BaseStyle
from workside.widgets import CoreWidget
from workside.settings import Settings

ic.configureOutput(includeContext=True)


class Label(CoreWidget):
  """Label provides an alternative to QLabel
  #  Copyright (c) 2023 Asger Jon Vistisen
  #  MIT Licence"""

  _maxLength = None

  @classmethod
  def _getMaxLength(cls) -> int:
    """Getter-function for the width in number of characters."""
    out = maybe(cls._maxLength, Settings.headerLabelWidth)
    if isinstance(out, int):
      return out
    raise TypeError

  def __init__(self, *args, **kwargs) -> None:
    CoreWidget.__init__(self, *args, **kwargs)
    self._words = None
    self._styleSettings = None
    self._fontMetrics = None
    self._font = None
    self._margins = None

  def _getMargins(self) -> QMargins:
    """Getter-function for margins"""
    return self.getStyle().getMargins()

  def _getPadding(self) -> QMargins:
    """Getter-function for padding"""
    return self.getStyle().getMargins()

  def _getBorderWidth(self) -> QMargins:
    """Getter-function for border width"""
    return self.getStyle().getBorderWidth()

  def _createFont(self, font: QFont = None) -> None:
    """Creator-function for font"""
    if font is None:
      self._font = Settings.defaultFont
    elif isinstance(font, QFont):
      self._font = font
    else:
      raise TypeError

  def _getFont(self) -> QFont:
    """Getter-function for the font"""
    if self._style is None:
      self._createStyle()
      return self._getFont()
    font = self.getStyle().getFont()
    self._createFontMetrics(font)
    return font

  def setFont(self, font: QFont) -> None:
    """Setter-function for the font"""
    self._createFont(font)
    self._createFontMetrics(font)

  def _createFontMetrics(self, font: QFont = None) -> None:
    """Creator-function for the font metrics"""
    if font is None:
      font = self._getFont()
    if isinstance(font, QFont):
      self._fontMetrics = QFontMetrics(font)

  def _getFontMetrics(self, ) -> QFontMetrics:
    """Getter-function for the font metrics"""
    if self._fontMetrics is None:
      self._createFontMetrics()
      return self._getFontMetrics()
    if isinstance(self._fontMetrics, QFontMetrics):
      return self._fontMetrics
    raise TypeError

  def _getBoundingRect(self, text: str = None) -> QRectF:
    """Getter-function for the QRectF that would be required to bound the
    given text by the given font."""
    letters = [*string.ascii_lowercase, *string.ascii_uppercase]
    text = maybe(text, ''.join(choices(letters, k=self._getMaxLength())))
    if isinstance(text, str):
      return self._getFontMetrics().boundingRect(text).toRectF()
    raise TypeError

  def setStyle(self, style: BaseStyle) -> None:
    """Reimplementation of the style setter such as to create the font
    metrics immediately"""
    self.setFont(style.getFont())
    CoreWidget.setStyle(self, style)

  def setText(self, text: str) -> None:
    """Setter-function for the text"""
    for word in text.split(' '):
      self._getWords().append(word)
    self.setMinimumSize(self._getBoundingRect(text).size().toSize())
    self.update()

  def getText(self, ) -> str:
    """Getter-function for the text"""
    words = []
    for word in reversed(self._getWords()):
      if len(words) + len(word) + 1 > self._getMaxLength():
        words.append('...')
        break
      else:
        words.append(word)
    text = ' '.join(reversed(words))
    fontMetrics = self._getFontMetrics()
    boundingRect = fontMetrics.boundingRect(text) + self._getMargins()
    boundingSize = boundingRect.size()
    self.setMinimumSize(boundingSize)
    return text

  def _getWords(self, ) -> list[str]:
    """Getter-function for the list of strings to be used construct the
    text."""
    if self._words is None:
      self._words = []
      return self._getWords()
    if isinstance(self._words, list):
      return self._words
    raise TypeError

  def show(self) -> None:
    """Reimplementation inserting a measure of the bounding rectangle
    setting the size"""
    self.setMinimumSize(self._getBoundingRect().size())
    CoreWidget.show(self)

  def paintEvent(self, event: QPaintEvent) -> None:
    """Implementation of paint event"""
    CoreWidget.paintEvent(self, event)
    alignFlag = Qt.AlignmentFlag.AlignCenter
    painter = QPainter()
    painter.begin(self)
    self.getStyle() @ painter
    text = self.getText()
    viewRectF = painter.viewport().toRectF()
    viewCenter = viewRectF.center()
    textRectF = viewRectF - self._getMargins()
    textRectF.moveCenter(viewCenter)
    boundingRect = QRectF(painter.boundingRect(textRectF, alignFlag, text))
    boundingRect.moveCenter(viewCenter)
    painter.fillRect(viewRectF, QColor(255, 0, 0, 63))
    painter.eraseRect(boundingRect, )
    painter.fillRect(boundingRect, QColor(223, 223, 223, 255))
    painter.drawText(boundingRect, alignFlag, text)
    painter.end()
