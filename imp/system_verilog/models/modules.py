""" Module class definition.

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

from imp.base.models import container
from imp.system_verilog.models import module_builder_mixin


class ModuleHeader(container.Group):
  pass


class ModuleHeader(container.Block):
  """Module Header"""
  def __init__(self):
    super().__init__()
    self._ports = container.Block()
    self._parameters = container.Block()


class Module(container.NamespacedContainer, module_builder_mixin.ModuleBuilderMixin):
  """Class to represent SystemVerilog module definitions."""

  def __init__(self, module_name=None):
    super().__init__()
    self._module_name = module_name

  @property
  def module_name(self) -> str:
    return self._module_name


  @property
  def name(self) -> str:
    return self._module_name


if __name__ == '__main__':
  from imp.system_verilog.models import datatypes
  m = Module(module_name="example")
  print(m)
  p = m.parameter(name="p1", dtype=datatypes.IntType(), default=30)
  p2 = m.parameter(name="p2", dtype=datatypes.LogicType(msb=2, lsb=0), default=p*2)
  print(p.default, p.name)
  print(m.p1.default)