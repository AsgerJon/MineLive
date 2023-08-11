"""MetaField provides metaclass shared by the Field classes"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from icecream import ic

from moreworktoy import Field
from moreworktoy import WorkTypeMeta

ic.configureOutput(includeContext=True)

ic(Field)


class WorkType(metaclass=WorkTypeMeta):
  """This interim class should be inherited from. """


ic(Field)
