"""Constant subclasses Field to provide a simplified version when fields
of constant value are intended. The constructor expects the first
positional argument to hold the value to be retained throughout the
existence of the instance. The type is inferred automatically."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from moreworktoy import Field


class Constant(Field):
  """Constant subclasses Field to provide a simplified version when fields
  of constant value are intended."""

  def __init__(self, value: Any) -> None:
    type_ = type(value)
