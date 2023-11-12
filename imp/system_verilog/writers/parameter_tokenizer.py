"""Tokenizers to Parameters to SystemVerilog code.

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
from imp.system_verilog.models import parameters

SP = tokens.Space
Symbol = tokens.Symbol
Keyword = tokens.Keyword
Literal = tokens.Literal
CR = tokens.NewLine


@tokenizer_for(parameters.LocalParamDeclaration)
def localparam_declaration_tokenizer(target: parameters.LocalParamDeclaration, tokenize):
  identifiers = [tokens.Identifier(name) for name in target.names]
  yield from Keyword('localparam') + SP()
  yield from tokenize(target.localparam.dtype) + SP()
  yield from tokens.CommaSeperated(identifiers, tokenize)
  if value := target.localparam.value:
    yield from SP() + Symbol("=") + SP() + Literal(value)
  yield from Symbol(";") + CR()
