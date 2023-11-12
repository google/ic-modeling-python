"""Writer class.

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

from imp.base.writers.formatter import Formatter
from imp.base.writers import tokens
from typing import Iterator, Union

TokenizerType = Iterator[Union[tokens.Token, tokens.TokenStream]]


class Writer:
  """Given a tokenizer function and a formatter, converts the tokens to text."""
  def __init__(self, tokenizer, formatter: Formatter):
    self.tokenizer = tokenizer
    self.formatter = formatter

  def process(self, item):
    self.formatter.process_tokens(self.tokenizer.tokenize(item))

  def get_text_for(self, item):
    self.formatter.reset()
    self.process(item)
    return self.formatter.text

