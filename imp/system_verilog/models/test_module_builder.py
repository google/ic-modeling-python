"""

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


from imp.system_verilog.models import datatypes
from imp.system_verilog.models import modules


def test_module_param_builder():
  m = modules.Module(module_name="example")
  m.localparam(name="p1", dtype=datatypes.IntType(), value=30)

  assert len(m.items) == 1
  assert m.p1.value == 30
  assert isinstance(m.p1.dtype, datatypes.IntType)
