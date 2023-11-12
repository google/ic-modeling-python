""" Base classes for Signals.

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

import component
import datatypes
import enum


class Signal(component.Component):
  """Base class for all signals.

  Signals are used to cary information from one block to another. Special language-specific signals include:
  - Nodes (Spice)
  - Vars/wires (Verilog)
  - Busses
  - Interfaces

  """
  def __init__(self, name, dtype: datatypes.DataType):
    super().__init__()
    self.name = name
    self.dtype = dtype


class Direction(enum.Enum):
  INPUT = "input"
  OUTPUT = "output"
  INOUT = "inout"
  REF = "ref"
  INTERNAL = ""


class Port(Signal):
  """Base class for SystemVerilog ports."""

  def __init__(self, name, dtype, direction):
    super().__init__(name, dtype=dtype)
    self.direction = direction
