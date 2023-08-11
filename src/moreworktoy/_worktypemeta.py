"""MetaField provides metaclass shared by the Field classes"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any, Self, Type, MutableMapping

from worktoy.typetools import CallMeMaybe

from moreworktoy import NameSpace, InvalidNameSpaceError

Bases = tuple[type]
Map = MutableMapping[str, Any]


class WorkTypeMeta(type):
  """MetaField provides metaclass shared by the Field classes"""

  @staticmethod
  def createNameSpace(name: str, bases: Bases, **kwargs) -> Map:
    """Creator-function for the nameSpace used by the __prepare__ method.
    By default, an instance of 'dict' is returned containing:
      nameSpace = dict(
      __prepare_data__=dict(name=name, bases=bases, **kwargs))
    To use an instance of a custom class instead of the builtin dict,
    it is sufficient to reimplement this method as the __prepare__ method
    is already implemented to call this method."""
    return dict(__prepare_data__=dict(name=name, bases=bases, **kwargs))

  @staticmethod
  def isValidNamespace(obj: Map) -> int:
    """Check if the given object can be used as a namespace in a
    metaclass."""

    # Check for presence of methods
    requiredMethods = ['__getitem__', '__setitem__', '__contains__']
    if not all(hasattr(obj, method) for method in requiredMethods):
      return 1

    # Test functionality of methods
    try:
      testKey, testValue = "testKey", "testValue"

      # Test __setitem__
      obj[testKey] = testValue

      # Test __getitem__
      try:
        retrievedValue = obj[testKey]
        if retrievedValue != testValue:
          return 2
      except KeyError:
        # If KeyError is raised during retrieval, return False
        return 3

      # Test __contains__
      if testKey not in obj:
        return 4

      # Test for KeyError on unsupported key
      counter = 69420
      baseUnsupportedKey = lambda x: 'LMAO%d' % x
      while baseUnsupportedKey(counter) in obj:
        counter += 1
      _ = obj[baseUnsupportedKey(counter)]  # This should raise a KeyError

    except Exception as e:
      # This is expected for the unsupported key test
      if isinstance(e, KeyError):
        return 0
      raise InvalidNameSpaceError(5, obj) from e

    return 6

  @classmethod
  def __prepare__(mcls, name: str, bases: Bases, **kwargs) -> Map:
    """The default implementation receives an appropriate object from the
    createNameSpace method and returns it. Subclasses can adjust this
    behaviour as needed. Please note that the base implementation includes
    a call to the validateNameSpace method, which ensures that the object
    intended for use as namespace does in fact support the necessary
    operations."""
    testNameSpace = mcls.createNameSpace(name, bases, **kwargs)
    nameSpace = mcls.createNameSpace(name, bases, **kwargs)
    exitCode = mcls.isValidNamespace(testNameSpace)
    if exitCode:
      raise InvalidNameSpaceError(exitCode, nameSpace)
    return nameSpace

  @staticmethod
  def __pre_init__(self: Any, *args, **kwargs) -> None:
    """During instance creation, this method is invoked after the __new__
    on the class, but before the __init__ on the class. By default,
    this method does nothing, but it is invoked by the default instance
    creation allowing subclasses to simply implement this method."""

  @staticmethod
  def __post_init__(self: Any, *args, **kwargs) -> None:
    """Similar to above except called after the __init__ on the class"""

  def enhanceMethod(cls, methodKey: str, factory: CallMeMaybe) -> type:
    """This method is used to augment a method on the given class. Provide
    a key to the method to be enhanced and a factory function which
    receives as argument the existing method and which returns the
    enhanced version. This enhanced version then overwrites the existing
    one before returning the class. Please note, that the given factory
    are expected to be comprehensively type annotated. The factory should
    also explicitly set type annotations on the returned method. If not,
    this method will explicitly set those annotations found on the legacy
    method."""
    legacy = getattr(cls, methodKey, None)
    if legacy is None:
      e = """The given key: %s does not match any implemented method on 
      the given class: %s!""" % (methodKey, cls.__qualname__)
      raise KeyError(e)
    if not isinstance(legacy, CallMeMaybe):
      e = """Expected given key: %s to point to a callable function, 
      but received type: %s""" % (methodKey, type(legacy))
      raise TypeError(e)
    enhancedMethod = factory(legacy)
    if not enhancedMethod.get('__annotations__', None):
      legacyAnnotations = legacy.get('__annotations__', None)
      setattr(enhancedMethod, '__annotations__', legacyAnnotations)
    setattr(cls, methodKey, enhancedMethod)
    return cls

  def __new__(mcls,
              name: str,
              bases: Bases,
              nameSpace: NameSpace,
              **kwargs) -> type:
    """Implementation of class creation logic"""
    cls = super().__new__(mcls, name, bases, nameSpace, **kwargs)
    setattr(cls, '__pre_init__', mcls.__pre_init__)
    setattr(cls, '__post_init__', mcls.__post_init__)
    return cls

  def __init__(cls,
               name: str,
               bases: Bases,
               nameSpace: NameSpace,
               **kwargs) -> None:
    """Implementation of class initialization"""
    type.__init__(cls, name, bases, nameSpace, **kwargs)

  def __call__(cls: Type[Self], *args, **kwargs) -> Any:
    """Instance creation and initialization"""
    self = object.__new__(cls)
    cls.__pre_init__(self, *args, **kwargs)
    cls.__init__(self, *args, **kwargs)
    cls.__post_init__(self, *args, **kwargs)
    return self
