"""Top level SystemVerilog tokenizer.

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
from imp.base.writers import tokens
from imp.system_verilog.writers import comments_tokenizer
from imp.system_verilog.writers import datatype_tokenizer
from imp.system_verilog.writers import module_tokenizer
from imp.system_verilog.writers import parameter_tokenizer

from typing import Callable, Sequence

# A specific SystemVerilog tokenizer is defined by importing the component tokenizers
# and passing them as arguments to the SystemVerilogTokenizer class below.
#
# These are defined in reverse priority order: Tokenizers included later in the sequence
# take precedence over those defined earlier.
_DEFAULT_TOKENIZER_FUNCTIONS = (

  # Comments
  comments_tokenizer.comment_tokenizer,
  comments_tokenizer.banner_tokenizer,
  comments_tokenizer.block_comment_tokenizer,

  # Datatypes
  datatype_tokenizer.inttype_tokenizer,

  # Parameters
  parameter_tokenizer.localparam_declaration_tokenizer,

  # Signals
  # signal_tokenizer.var_declaration_tokenizer,
  # signal_tokenizer.port_declaration_tokenizer_ansi,

  # Modules
  module_tokenizer.module_tokenizer,
)

TokenizerFunctionType = Callable[[component.Component], Sequence[tokens.Token]]


class SystemVerilogTokenizer:
  """Produces SystemVerilog tokens from components."""

  _base_tokens_classes = (
    tokens.Keyword,
    tokens.Identifier,
    tokens.Symbol,
    tokens.Number
  )

  def __init__(self,
               tokenizer_functions=_DEFAULT_TOKENIZER_FUNCTIONS):
    self.handlers_by_token_cls = {}
    # Using reversed to allow later tokenizers to get priority.
    for fn in reversed(tokenizer_functions):
      target = fn.__dict__['tokenizer_for']
      self.handlers_by_token_cls[target] = fn


  def tokenize(self, item):
    # Dispatch on the component type.
    if isinstance(item, self._base_tokens_classes):
      yield item
    else:
      for token_cls, handler in self.handlers_by_token_cls.items():
        if isinstance(item, token_cls):
          yield from handler(item, tokenize=self.tokenize)
          break
      else:
        raise ValueError(f"Could not find a tokenizer for {item} ({type(item)}")
