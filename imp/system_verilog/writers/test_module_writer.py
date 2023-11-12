"""End to end test of SystemVerilog model creation and code generation.

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
from imp.system_verilog.writers import systemverilog_writer


def test_empty_module_to_text():
  """Test converting an empty module to text."""

  writer = systemverilog_writer.SystemVerilogWriter()
  target = modules.Module(module_name="example")

  text = writer.get_text_for(target)
  expected = "\n".join([
      "module example(",
      ");",
      "endmodule",
    ]
  )
  assert text == expected


def test_convert_comprehensive_module_to_text():
  """A test case covering every component usage."""

  writer = systemverilog_writer.SystemVerilogWriter()

  target = modules.Module(module_name="example")
  target.localparam(name="p1", dtype=datatypes.IntType(), value=30)

  text = writer.get_text_for(target)
  expected = "\n".join([
      "module example(",
      ");",
      "",
      "  localparam int p1 = 30;",
      "endmodule",
    ]
  )
  assert text == expected
