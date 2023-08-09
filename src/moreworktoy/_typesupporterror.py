"""TypeSupportError is a custom exception intended to be raised by
functions invoked with arguments of unsupported types. """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from types import TracebackType
from typing import Never, Self

from worktoy.parsing import extractArg
from worktoy.stringtools import stringList, monoSpace

from moreworktoy import PermissionLevel, ProtectedPropertyError
from moreworktoy import ReadOnlyError

readOnly = PermissionLevel.READ_ONLY


class TypeSupportError(Exception):
  """TypeSupportError is a custom exception intended to be raised by
  functions invoked with arguments of unsupported types. """

  def __init__(self, *args, **kwargs) -> None:
    typeKeys = stringList('type_, type, fieldType, supportType')
    self._type, a, kw = extractArg(type, typeKeys, *args, **kwargs)
    nameKeys = stringList('name, variableName, varName')
    self._name, args, kwargs = extractArg(str, nameKeys, *args, **kwargs)
    badKeys = stringList('badArg, badArgument, wrongArgument')
    self._badArg, args, kwargs = extractArg(self.type_, badKeys, *a, **kw)
    self._callMeMaybe = None
    self._instance = None
    self._className = None

  def with_traceback(self, traceBack: TracebackType | None) -> Self:
    """Reimplementation of the method extract context specific information
    presented by the particular exception instance. This information
    includes the name of the method or function invoking it, and if this
    be an instance method, the return value from the __str__ from that
    instance and well as the class name of the instance will be included
    as well."""
    frame = traceBack.tb_frame
    self._callMeMaybe = frame.f_code.co_name
    self._instance = frame.f_locals.get('self', None)
    if self._instance is not None:
      self._className = self._instance.__class__.__qualname__
    return Exception.with_traceback(self, traceBack)

  def _getType(self) -> type:
    """Getter-function for the type"""
    if isinstance(self._type, type):
      return self._type
    raise TypeError

  def _setType(self, *_) -> Never:
    """Illegal setter function"""
    raise ReadOnlyError('type')

  def _delType(self, ) -> Never:
    """Illegal deleter function"""
    raise ProtectedPropertyError('type')

  def _getName(self) -> str:
    """Getter-function for name"""
    if isinstance(self._name, str):
      return ''
    raise TypeError

  def _setName(self, *_) -> Never:
    """Illegal-setter function for name"""
    raise ReadOnlyError('name')

  def _delName(self, ) -> Never:
    """Illegal delete function for name"""
    raise ProtectedPropertyError('name')

  name = property(_getName, _setName, _delName)
  type_ = property(_getType, _setType, _delType)

  def __repr__(self, ) -> str:
    """Code Representation"""
    cls = self.__class__.__qualname__
    return '%s(%s, %s)' % (cls, self.type_, self._badArg)

  def __str__(self) -> str:
    """String Representation including inferred contextual information"""
    msg = """Expected argument to be of type: """
    if self.name:
      msg = """Expected argument named %s to be of type: """ % self.name

    msg = '%s%s, but received %s of type %s! <br>' % (
      msg, self.type_, self._badArg, type(self._badArg))
    if self._instance is None or self._className is None:
      msg = '%s This occurred during call to function: %s' % (
        msg, self._callMeMaybe)
      return monoSpace(msg)
    msg = """%s This occurred during call to method %s on instance %s of 
    class %s"""
    return monoSpace(msg)
