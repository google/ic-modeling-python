"""Converts a TokenStream to source code.

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

import functools

from imp.base.writers import tokens
from imp.base.writers.tokens import Token, Null, Name, Indent, Dedent, Space, NewLine, Keyword


class Formatter:
  """Class to convert a token stream to formatted text."""

  def __init__(self, tab: str = "  ", debug=False):
    self._lines = []
    self._current_line = []
    self._prefix = []
    self._tab = tab
    self._debug = debug

  def reset(self):
    self._lines = []
    self._current_line = []
    self._prefix = []

  @property
  def text(self):
    txt = "\n".join(list(self._lines))
    txt += "".join(self._current_line)
    return txt


  def print(self):
    print(self.text)

  def process_tokens(self, token_generator, debug=False):
    """Main token processing method."""

    self._debug = debug

    for token in token_generator:
      if debug:
        trace = f"({token.trace})" if token.trace else ''
        print(f"Token:{str(token):30} {trace:20} prefix:{str(self._prefix):12}  line:{self._current_line}")
        if isinstance(token, NewLine):
          print("\n")

      if isinstance(token, tokens.TokenStream):
        raise ValueError(f"Found a TokenStream instead of a Token. "
                         " The tokenizer should use 'yield from'.")

      if not isinstance(token, Token):
        raise ValueError(f"Unexpected token type: {token} {type(token)}")

      self.handle(token)


  def add_word(self, word):
    self._current_line.append(word)

  # ----------------------------------------
  # Handlers
  # ----------------------------------------
  @functools.singledispatchmethod
  def handle(self, token: Token):
    ...

  @handle.register
  def handle_null(self, token: Null):
    pass

  @handle.register
  def handle_token(self, token: Token):
    value = str(token.value)
    self.add_word(value)

  @handle.register
  def handle_identifier(self, token: Name):
    value = str(token.value)
    self.add_word(value)

  @handle.register
  def handle_keyword(self, token: Keyword):
    value = str(token.value)
    self.add_word(value)

  @handle.register
  def handle_indent(self, token: Indent):
    self._prefix.append(self._tab)

  @handle.register
  def handle_dedent(self, token: Dedent):
    self._prefix.pop()

  @handle.register
  def handle_space(self, token: Space):
    self.add_word(' ' * token.n)

  @handle.register
  def handle_return(self, token: NewLine):
    # Only add white space if something follows it.
    if self._current_line:
      self._lines.append("".join(list(self._prefix) + self._current_line))
    else:
      self._lines.append("")
    self._current_line = []

