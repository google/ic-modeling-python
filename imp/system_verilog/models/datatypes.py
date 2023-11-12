"""SystemVerilog Datatypes

Copyright 2023 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import abc
from imp.base.models import datatypes


class IntegerTypeBase(datatypes.DataType, abc.ABC):
  """Integral values."""

  def __init__(self, signed=None):
    self._signed = signed

  @abc.abstractmethod
  def default_signedness(self):
    raise NotImplementedError("Must be implemented by subclasses.")

  @property
  def signed(self):
    return self._signed if self._signed is not None else self.default_signedness


class IntegerAtomType(IntegerTypeBase):
  """Data types representing SV 'integer_atom_type' types."""
  type_name: str


class IntType(IntegerAtomType):
  """2-state data type, 32-bit signed (by default) integer."""
  type_name = "int"
  signed = True

  @property
  def default_signedness(self):
    return True


class LogicType(datatypes.IntegerTypeBase):
  """4-state data type, user-defined vector size, unsigned."""

  def __init__(self, msb:int, lsb:int):
    self.msb = msb
    self.lsb = lsb

  @property
  def default_signedness(self):
    return False
