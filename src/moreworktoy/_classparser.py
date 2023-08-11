"""NameSpace is a custom class implementing mutable and immutable
mappings. This makes it a convenient mapping for use in the metaclass
__prepare__."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any, Never

from worktoy.core import maybe
from worktoy.stringtools import monoSpace

from moreworktoy import (Field, ReadOnlyError,
                         ProtectedPropertyError, \
                         Args, \
                         Constant)


class ClassParser:
  """NameSpace is a custom class implementing mutable and immutable
  mappings. This makes it a convenient mapping for use in the metaclass
  __prepare__"""

  className = Constant(str)
  baseClasses = Constant(list)
  temp = Field(list)
  ownerName = Constant(str)
  owner = Constant(type)

  def __init__(self, *args, **kwargs) -> None:
    args = Args(*args)
    self._className = args * str
    self._baseClasses = args @ type
    self._temp = [(k, [v]) for (k, v) in kwargs.items()]
    self._fieldNames = []
    self._fields = []
    self._curInd = 0
    self._ownerName = args * str
    self._owner = args * type

  def _getClassName(self) -> str:
    """Getter-function for the class name."""
    if isinstance(self._className, str):
      return self._className
    raise TypeError

  def _getFieldNames(self) -> list[str]:
    """Getter-function for the list of Field instances encountered by this
    instance of NameSpace"""
    return self._fieldNames

  def _setFieldNames(self, *_) -> Never:
    """Illegal Setter function"""
    raise ReadOnlyError('fieldNames')

  def _delFieldNames(self, ) -> Never:
    """Illegal deleter function"""
    raise ProtectedPropertyError('fieldNames')

  def _getOwnerName(self) -> str:
    """Getter-function for the name of the owner class. Please note that
    this property ensures that the __prepare__ method can provide the
    intended name of the class to be created before it is created. This
    name is returned by this getter. Later, the getter function for the
    owner class attempts to find 'type' in globals and locals at the key
    given by this variable."""
    if isinstance(self._ownerName, str):
      return self._ownerName
    raise TypeError

  def _setOwnerName(self, name: str) -> None:
    """Setter-function permitted only when the name owner name is None"""
    if self._ownerName is not None:
      raise ReadOnlyError('ownerName')
    self._ownerName = name

  def _delOwnerName(self) -> Never:
    """Illegal deleter-function"""
    raise ProtectedPropertyError('ownerName')

  def _getOwner(self) -> type:
    """Getter-function for the owner class"""
    globalOwner = globals().get(self.ownerName, None)
    localOwner = locals().get(self.ownerName, None)
    owner = maybe(self._owner, globalOwner, localOwner)
    if isinstance(owner, type):
      return owner
    raise TypeError

  def _setOwner(self, owner: type) -> None:
    """Setter-function for the owner class"""
    if self._owner is not None:
      raise ReadOnlyError('owner')
    self._owner = owner

  def _delOwner(self) -> Never:
    """Illegal deleter function"""
    raise ProtectedPropertyError('owner')

  def items(self) -> list[tuple[str, list[Any]]]:
    """Implementation of the 'items' method."""
    return [item for item in self._temp]

  def keys(self) -> list[str]:
    """Implementation of keys method. Please note, that the object
    returned provides a snapshot of the keys as they were. The object will
    not update itself to reflect changes."""
    return [key for key in self]

  def values(self) -> list[list[Any]]:
    """Implementation of values method."""
    return [val for (_, val) in self.items()]

  def __iter__(self, ) -> NameSpace:
    """Implementation of iteration"""
    self._curInd = 0
    return self

  def __next__(self, ) -> str:
    """Implementation of iteration"""
    self._curInd += 1
    if self._curInd > len(self._temp):
      raise StopIteration
    return self._temp[self._curInd - 1][0]

  def _getValuesAt(self, key) -> tuple[str, list[Any]]:
    """Returns the entire contents of the data structure at given key"""
    for (k, v) in self.items():
      if k == key:
        return v
    self._temp.append((key, []))
    return self[key]

  def __getitem__(self, key: str) -> Any:
    """Implementation of the dictionary interface. It returns the first
    entry defined at given key."""
    out = [*self._getValuesAt(key)[1], None][0]
    if out is None:
      return self.__missing__(key)

  def __setitem__(self, key: str, value: Any, **kwargs) -> None:
    """Implementation of the dictionary interface"""
    if key in self.fieldNames:
      e = """Variable name %s already assigned to a Field!"""
      raise NameError(e)
    if isinstance(value, Field):
      value.name = key
      self.fieldNames.append(key)
      self.fields.append(value)
    self[key][1].append(value)

  def __delitem__(self, key: str) -> None:
    """Implementation of the dictionary interface. Please note, that this
    'delete' method sets the entry at key in data to an empty list. """
    self[key][1].clear()

  def __missing__(self, key: str) -> Never:
    """Implementation of dictionary interfaces"""
    raise KeyError(key)

  def __contains__(self, key: str) -> bool:
    """Implementation of membership test"""
    for k in self:
      if k == key:
        return True
    return False

  def __bool__(self, ) -> bool:
    """Implementation of empty test"""
    return True if self._temp else False

  def __str__(self, ) -> str:
    """String Representation"""
    title = '\n**Instance of NameSpace**'
    subTitle = ' - a subclass of %s - ' % dict().__class__.__name__
    header = monoSpace(r"""This instance of NameSpace provides the 
      following key, value pairs:""")
    body = '\n'.join(['%s: %s' % (k, str(v)) for (k, v) in self.items()])
    return '\n'.join([title, subTitle, header, body])

  def _getFields(self) -> list[Field]:
    """Getter-function for the list of fields set on the owner class"""
    return self._fields

  def _setFields(self, *_) -> Never:
    """Illegal setter function"""
    raise ReadOnlyError('fields')

  def _delFields(self) -> Never:
    """Illegal deleter function"""
    raise ProtectedPropertyError('fields')

  fields = property(_getFields, _setFields, _delFields)
  fieldNames = property(_getFieldNames, _setFieldNames, _delFieldNames)
