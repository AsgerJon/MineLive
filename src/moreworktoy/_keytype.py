"""The keyType function takes a string as argument and returns the class
matching this string. If the key is missing a KeyError is raised. This can
be suppressed by setting keyword 'allowMissing'."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import builtins

from worktoy.core import maybe


def keyType(key, **kwargs) -> type:
  """The keyType function takes a string as argument and returns the class
  matching this string. If the key is missing a KeyError is raised. This can
  be suppressed by setting keyword 'allowMissing'."""
  fromBuiltins = builtins.__dict__.get(key, None)
  fromGlobals = globals().get(key, None)
  fromLocals = locals().get(key, None)
  cls = maybe(fromBuiltins, fromGlobals, fromLocals)
  if cls is not None:
    if isinstance(cls, type):
      return cls
  if kwargs.get('allowMissing', None) is not None:
    raise KeyError(key)
