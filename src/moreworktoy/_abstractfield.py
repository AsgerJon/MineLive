"""Field quickly provides a property to a class. Specify default value,
permission levels and name at creation time."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import Never, Any
from warnings import warn

from icecream import ic
from worktoy.parsing import maybeType
from worktoy.stringtools import monoSpace
from worktoy.typetools import CallMeMaybe

from moreworktoy import ProtectedPropertyError, ReadOnlyError, \
  SecretPropertyError, Args
from moreworktoy import PermissionLevel as PermLvl

ic.configureOutput(includeContext=True)


class AbstractField:
  """Field quickly provides a property to a class. Specify default value,
  permission levels and name at creation time."""

  @classmethod
  def _getBaseInstance(cls, type_: type) -> Any:
    """Getter-function for base instance of a given type"""
    if type_ is list:
      return []
    if type_ in [float, int, complex]:
      return 0 if type_ is int else 0.0
    if type_ is str:
      return ''
    try:
      constructor = getattr(type_, '__call__', lambda: None)
    except TypeError as e:
      msg = """When attempting to find a base instance of the given type %s, 
      the following error was encountered: %s""" % (type_, e)
      raise TypeError(msg)
    if isinstance(constructor, CallMeMaybe):
      return constructor()
    raise TypeError('constructor')

  @classmethod
  @abstractmethod
  def _getPermissionLevel(cls) -> PermLvl:
    """Getter-function for the permission level. This is an abstract
    method that should be implemented by subclasses."""

  def __init__(self, *args, **kwargs) -> None:
    self._value = None
    self._type = None
    self._name = None
    self._permLvl = self._getPermissionLevel()
    args = Args(*args)
    if len(args) == 1:
      if isinstance(args[0], type):
        self._type = args[0]
      else:
        self._value = args[0]
    if len(args) == 2:
      self._value = args[0]
      if isinstance(args[1], str):
        self._name = args[1]
      elif isinstance(args[1], type):
        if isinstance(self._value, args[1]):
          self._type = args[1]
        else:
          raise TypeError
      warn('Ignoring second positional argument: %s' % args[1])
    if len(args) > 2:
      self._value = args.pop(0)
      self._name = args * str
      self._type = args * type
      if self._type:
        if not isinstance(self._value, self._type):
          raise TypeError
      else:
        self._type = type(self._value)
    try:
      self._root = kwargs['_root']
    except KeyError:
      self._root = None
    if self._root is not None:
      w = """Created rooted instance of class Field. This allows this 
      instance to change its permission level at runtime. """
      warn(monoSpace(w))

  def _getPermission(self, ) -> PermLvl:
    """Getter-function for permissions"""
    if isinstance(self._permLvl, PermLvl):
      return self._permLvl
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
          self._permLvl = PermLvl.SECRET
        else:
          self._permLvl = PermLvl.getFromAccess(pAccess)
      if isinstance(pValue, int):
        self._permLvl = PermLvl.getFromValue(pValue)
      else:
        raise TypeError
    elif isinstance(pLevel, PermLvl):
      self._permLvl = pLevel
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

  def _setName(self, name: str) -> None:
    """Illegal-setter function for name"""
    if self._name is not None:
      raise ReadOnlyError('name')
    if not isinstance(name, str):
      raise TypeError
    self._name = name

  def _delName(self, ) -> Never:
    """Illegal delete function for name"""
    raise ProtectedPropertyError('name')

  def _getType(self) -> type:
    """Getter-function for the type"""
    if isinstance(self._type, type):
      return self._type
    raise TypeError

  def _setType(self, type_: type) -> None:
    """Illegal setter function"""
    if self._type is not None:
      raise ReadOnlyError('type')
    if not isinstance(type_, type):
      raise TypeError
    self._type = type_

  def _delType(self, ) -> Never:
    """Illegal deleter function"""
    raise ProtectedPropertyError('type')

  permLevel = property(_getPermission, _setPermission, _delPermission)
  name = property(_getName, _setName, _delName)
  type_ = property(_getType, _setType, _delType)

  def __get__(self, instance, owner) -> Any:
    if self.permLevel.canGet:
      if self._value is None and self._type is None:
        raise TypeError('Both value is None and type is None!')
      if self._value is None and isinstance(self._type, type):
        self._value = self._getBaseInstance(self._type)
      if self._type is None:
        self._type = type(self._value)
        return self._value
      if isinstance(self._value, self._type):
        return self._value
      raise TypeError
    raise SecretPropertyError('value')

  def __set__(self, instance, value) -> None:
    if not self.permLevel.canSet and self._value is not None:
      raise ReadOnlyError('value')
    if self._type is None:
      self._type = type(value)
    if not isinstance(value, self._type):
      raise TypeError
    self._value = value

  def __delete__(self, instance) -> None:
    if self.permLevel.canDel:
      self._value = None
    else:
      raise ProtectedPropertyError('value')
