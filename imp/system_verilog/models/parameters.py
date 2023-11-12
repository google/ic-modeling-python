"""Parameter Classes

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

from imp.base.models import component


class Parameter(component.Component):
  """Parameters."""
  def __init__(self, name, dtype, default=None):
    self.name = name
    self.dtype = dtype
    self.default = default

  @property
  def is_constant(self):
    return True


class ParameterDeclaration(component.Component):
  def __init__(self, names, parameter: Parameter):
    self.names = names
    self.parameter = parameter


class LocalParam(component.Component):
  """Local parameters"""
  def __init__(self, name, dtype, value, comment=None):
    super().__init__()
    self.name = name
    self.dtype = dtype
    self.value = value
    self.comment = comment

  @property
  def is_constant(self):
    return True


class LocalParamDeclaration(component.Component):
  def __init__(self, names, localparam):
    self.names = names
    self.localparam = localparam