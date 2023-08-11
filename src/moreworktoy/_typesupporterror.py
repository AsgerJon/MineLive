"""TypeSupportError is a custom exception intended to be raised by
functions invoked with arguments of unsupported types. """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from types import TracebackType
from typing import Self, Any

from worktoy.core import plenty
from worktoy.stringtools import monoSpace
from icecream import ic

from moreworktoy import PermissionLevel, Field

ic.configureOutput(includeContext=True)
readOnly = PermissionLevel.READ_ONLY


class TypeSupportError(Exception):
  """TypeSupportError is a custom exception intended to be raised by
  functions invoked with arguments of unsupported types. """

  badArg = Field()
  actualType = Field()
  expectedType = Field()
  argName = Field()
  instance = Field()
  callMeMaybe = Field()
  className = Field()

  def __init__(self, badArg: Any, type_: type, argName: str) -> None:
    self.badArg = badArg
    self.actualType = type(badArg)
    self.expectedType = type_
    self.argName = argName

  def with_traceback(self, traceBack: TracebackType | None) -> Self:
    """Reimplementation of the method extract context specific information
    presented by the particular exception instance. This information
    includes the name of the method or function invoking it, and if this
    be an instance method, the return value from the __str__ from that
    instance and well as the class name of the instance will be included
    as well."""
    frame = traceBack.tb_frame
    self.callMeMaybe = frame.f_code.co_name
    self.instance = frame.f_locals.get('self', None)
    if self.instance is not None:
      self.className = self.instance.__class__.__qualname__
    return Exception.with_traceback(self, traceBack)

  def _getContext(self) -> str:
    """Getter-function for the context in which the error was raised."""

  def _getInstanceMethod(self) -> str:
    """Getter-function for the context, if it was an instance method"""
    instance = self.instance
    method = self.callMeMaybe
    cls = self.className
    if not plenty(instance, method, cls):
      return ''
    msg = """This error was raised by object: (%s.__str__(...)): <br>
    %s <br>during execution of method: %s!"""

  def __repr__(self, ) -> str:
    """Code Representation"""
    cls = self.__class__.__qualname__
    bad = self.badArg
    name = self.argName
    type_ = self.expectedType
    return '%s(%s, %s, %s)' % (cls, bad, name, type_)

  def __str__(self) -> str:
    """String Representation including inferred contextual information"""
    title = self.__class__.__qualname__
    msg = """Expected argument %s to be of type %s, but received: !"""
    header = msg % (self.argName, self.expectedType)
    msg = """>>> %s""" % (self.badArg)
    badArg = msg % self.badArg
    msg = """of type %s!"""
    badType = msg % self.actualType
    msg = """This error occurred during"""
    msg = """Expected argument to be of type: """
    if self.argName:
      msg = """Expected argument named %s to be of type: """ % self.argName
    msg = '%s%s, but received %s of type %s! <br>' % (
      msg, self.type_, self._badArg, type(self._badArg))
    if self._instance is None or self._className is None:
      msg = '%s This occurred during call to function: %s' % (
        msg, self._callMeMaybe)
      return monoSpace(msg)
    msg = """%s This occurred during call to method %s on instance %s of 
    class %s"""
    return monoSpace(msg)
