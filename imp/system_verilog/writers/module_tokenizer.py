"""Tokenizers to translate module definitions to SystemVerilog code.

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

from imp.base.writers import tokens
from imp.base.writers.model_tokenizer import tokenizer_for
from imp.system_verilog.models import modules


# For brevity.
Identifier = tokens.Identifier
Keyword = tokens.Keyword
Symbol = tokens.Symbol
SP = tokens.Space
CR = tokens.NewLine


@tokenizer_for(modules.Module)
def module_tokenizer(module: modules.Module, tokenize):

  yield from Keyword('module') + SP() + Identifier(module.module_name)
  yield from Symbol('(') + CR()
  yield from Symbol(')') + Symbol(';') + CR()

  yield tokens.Indent()

  # If the module is not empty, insert a  new line before additional items.
  if len(module.items):
    yield CR()

  for item in module.items:
    yield from tokenize(item)

  yield tokens.Dedent()
  yield from Keyword('endmodule') + CR()