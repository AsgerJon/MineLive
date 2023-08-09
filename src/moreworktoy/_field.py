"""Field quickly provides a property to a class. Specify default value,
permission levels and name at creation time."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Never, Any
from warnings import warn

from worktoy.core import maybe
from worktoy.parsing import maybeType, extractArg
from worktoy.stringtools import monoSpace, stringList

from moreworktoy import ProtectedPropertyError, ReadOnlyError, \
  SecretPropertyError

from moreworktoy import PermissionLevel as PermLvl


class Field:
  """Field quickly provides a property to a class. Specify default value,
  permission levels and name at creation time."""

  def __init__(self, *args, **kwargs) -> None:
    self._defaultValue = None
    typeKeys = stringList('type_, type, fieldType, supportType')
    self._type, args, kwargs = extractArg(type, typeKeys, *args, **kwargs)
    nameKeys = stringList('name, variableName, varName')
    self._name, args, kwargs = extractArg(str, nameKeys, *args, **kwargs)
    self._name = maybe(self._name, '%s' % self._type)
    permKeys = stringList('PermissionLevel, permLevel, permissions')
    self._perm, args, kwargs = extractArg(PermLvl, permKeys, *args, **kwargs)
    defaultKeys = stringList('defaultValue, defVal, val0, initialValue')
    self._defVal = None
    if isinstance(self._type, type):
      self._defVal, args, kwargs = extractArg(
        self._type, defaultKeys, *args, **kwargs)
    self._root = kwargs.get('_root', None)
    if self._root is not None:
      w = """Created rooted instance of class Field. This allows this 
      instance to change its permission level at runtime. <br> You can 
      suppress this warning by setting keyword argument to 'noWarn'."""
      if not isinstance(self._root, str):
        self._root = 'warn'
      if self._root != 'noWarn':
        warn(monoSpace(w))

  def _getPermission(self, ) -> PermLvl:
    """Getter-function for permissions"""
    if isinstance(self._perm, PermLvl):
      return self._PermLvl
    raise TypeError

  def _setPermission(self, *args, ) -> None:
    """Setter-function for permissions"""
    if self._root is None:
      e = """Unauthorized attempt at changing permission level!"""
      raise PermissionError(e)
    pLevel = maybeType(PermLvl, *args)
    pValue = maybeType(int, *args)
    pAccess = maybeType(str, *args)
    if pLevel is None:
      if pValue is None:
        if not isinstance(pAccess, str):
          raise TypeError
        if pAccess not in ['none', 'getter', 'setter', 'delete']:
          self._PermLvl = PermLvl.SECRET
        else:
          self._PermLvl = PermLvl.getFromAccess(pAccess)
      if isinstance(pValue, int):
        self._PermLvl = PermLvl.getFromValue(pValue)
      else:
        raise TypeError
    elif isinstance(pLevel, PermLvl):
      self._PermLvl = pLevel
    else:
      raise TypeError

  def _delPermission(self) -> Never:
    """Illegal delete function"""
    e = """LOL, you tried to delete the delete permission level on 
    Field %s LMAO!""" % self.name
    raise ProtectedPropertyError(monoSpace(e))

  def _getName(self) -> str:
    """Getter-function for name"""
    if isinstance(self._name, str):
      return self._name
    raise TypeError

  def _setName(self, *_) -> Never:
    """Illegal-setter function for name"""
    raise ReadOnlyError('name')

  def _delName(self, ) -> Never:
    """Illegal delete function for name"""
    raise ProtectedPropertyError('name')

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

  permLevel = property(_getPermission, _setPermission, _delPermission)
  name = property(_getName, _setName, _delName)
  type_ = property(_getType, _setType, _delType)

  def __get__(self, instance, owner) -> Any:
    if self.permLevel.canGet:
      value = maybe(self._value, self._defVal)
      if value is None:
        e = """When accessing the value of this Field both value and 
        default value were None!"""
        raise ValueError(monoSpace(e))
      return self._value
    raise SecretPropertyError('value')

  def __set__(self, instance, value) -> None:
    if not self.permLevel.canSet:
      raise ReadOnlyError('value')
    if not isinstance(value, self.type_):
      raise TypeError
    self._value = value

  def __delete__(self, instance) -> None:
    if self.permLevel.canDel:
      self._value = None
    else:
      raise ProtectedPropertyError('value')
