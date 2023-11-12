"""Module builder mixin classes.

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
from imp.base.models import comments
from imp.system_verilog.models import parameters

from typing import Optional


"""
To bind builder methods:
meth = types.MethodType(fn, cls(), cls) # Bind fn to an instance of the class 'cls'.
"""


class ModuleBuilderMixin(container.NamespaceBuilderMixin):
  """Builder API for Modules and their child containers."""

  # Generic blocks and groups.
  def group(self) -> container.Group:
    """Creates and returns a group."""
    return self._add_item(container.Group())

  def block(self, name: Optional[str] = None) -> 'ModuleItemBlock':
    """Creates and returns a block."""
    item = self._add_item(container.Block(name=name))
    if name:
      self._add_named_item(name=name, item=item)
    return item

  # Comments
  def comment(self, txt: str) -> comments.Comment:
    item = comments.Comment(txt=txt)
    return self._add_item(item)

  def banner(self, txt: str) -> comments.Banner:
    item = comments.Banner(txt=txt)
    return self._add_item(item)

  def block_comment(self, txt: str) -> comments.BlockComment:
    item = comments.BlockComment(txt=txt)
    return self._add_item(item)

  def parameter(self, name, dtype, default=None, comment=None):
    """Create a ParameterDeclaration and returns a Parameter."""
    param = parameters.Parameter(name, dtype, default)
    self._add_named_item(name=name, item=param)

    param_declaration = parameters.ParameterDeclaration(
      names=[name], parameter=param)
    self._add_item(param_declaration)

    return param

  def localparam(self, name, dtype, value, comment=None) -> parameters.LocalParam:
    """Creates and returns a localparam."""
    param = parameters.LocalParam(
        name,
        dtype,
        value,
        comment=comment)
    self._add_named_item(name=name, item=param)

    declaration = parameters.LocalParamDeclaration(names=[name], localparam=param)
    self._add_item(declaration)
    return param
