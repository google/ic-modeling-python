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

import pathlib


class Token:
  """Class that represents a token of text."""

  type: str = "TOKEN"

  def __init__(self, value: str = None, line_num: int = None, char_num: int = None, file: pathlib.Path = None):
    self.value = value
    self.line_num = line_num
    self.char_num = char_num
    self.file = file

  def __repr__(self):
    text = f'{self.__class__.__name__}({self.type!r}, {self.value!r}'

    if self.line_num:
      text += f', {self.line_num}, {self.char_num})'

    return text

  def __add__(self, other):
    return TokenStream([self, other])

  def __radd__(self, other):
    return TokenStream([other, self])

  def __iter__(self):
    yield self

  def __str__(self):
    return self.value


class TokenStream:
  def __init__(self, tokens):
    self.tokens = tokens

  def __add__(self, other):
    self.tokens.append(other)
    return self

  def __radd__(self, other):
    return TokenStream([other, self])

  def __iter__(self):
    for item in self.tokens:
      yield from item


class FormattingToken(Token):
  """Tokens used to format or align text."""


class WhiteSpace(FormattingToken):
  """Represents an ignored token."""
  type: str = "WHITESPACE"


class Space(WhiteSpace):
  """Indicates a number of space characters."""
  type: str = "SPACE"

  def __init__(self, n: int = 1):
    self.n = n
    self.value = ' ' * n


class Indent(WhiteSpace):
  """Indicates an indentation."""
  type: str = "INDENT"


class Dedent(WhiteSpace):
  """Indicates an indentation."""
  type: str = "INDENT"


class NewLine(FormattingToken):
  """Represents a return (new line) token."""
  type: str = "NewLine"


class Null(Token):
  """Represents an ignored line token."""
  type: str = "NULL"


class Symbol(Token):
  """Tokens used to represent symbols."""
  type: str = "SYMBOL"


class Identifier(Token):
  """Used to represent the names of variables, signals, etc.."""


class Keyword(Token):
  """Token used to represent keywords."""
  type: str = "KEYWORD"


class Literal(Token):
  """Used to denote literal values."""
  def __init__(self, value):
    super().__init__(value)


class Name(Token):
  """Token used to represent named constructs."""
  type: str = "NAME"


class Number(Token):
  """Token used to represent numbers."""
  type: str = "NUMBER"


class Type(Token):
  """Token used to represent data types."""
  type: str = "TYPE"


class LineComment(Token):
  """Token used to represent a line comment."""
  type: str = "LINE_COMMENT"


class BlockComment(Token):
  """Token used to represent a block comment."""
  type: str = "BLOCK_COMMENT"


class EndOfFile(Token):
  """Token used to denote the end of source code."""
  type = "END_OF_FILE"

  def __init__(self, line_num, char_num):
    self.line_num = line_num
    self.char_num = char_num

  def __repr__(self):
    return (f'{self.__class__.__name__}( '
            f'{self.line_num}, {self.char_num})')


class SymbolSeperated:
  """Helper class to emit tokens delimited by symbol characters."""
  def __init__(self, items, separator, tokenize):
    self.items = items
    self.seperator = separator
    self.tokenize = tokenize

  def __iter__(self):
    for i, item in enumerate(self.items, start=1):
      yield from self.tokenize(item)
      if i < len(self.items):
        yield from self.seperator


class CommaSeperated(SymbolSeperated):
  def __init__(self, items, tokenize):
    super().__init__(items=items, separator=Symbol(",") + Space(), tokenize=tokenize)


class SemicolonSeperated(SymbolSeperated):
  def __init__(self, items):
    super().__init__(items=items, separator=Symbol(";") + Space())


class DelimitedList:
  """A group of tokens, with delimiters."""

  def __init__(self, items, start, stop, delimiter):
    self._start = start
    self._stop = stop
    self._delimiter = delimiter
    self.items = items

  def start(self):
    yield Space()
    yield self._start
    yield NewLine(trace="DL:StartDone")

  def stop(self):
    yield self._stop

  def delimiter(self):
    yield Null()
    while True:
      yield self._delimiter

  # def each(self, item):
  #   yield from self.tokenize(item)

  def tokenize(self):
    if not len(self.items):
      return

    yield from self.start()
    delimiter = self.delimiter()
    yield Indent(trace="DL:StartItems")
    for item in self.items:
      d = next(delimiter)
      yield d
      if not isinstance(d, Null):
        yield Return(trace="DL:ItemDone")
      yield from self.each(item)
    yield Return(trace="DL:StopItems")
    yield Dedent(trace="DL:StopItems")

    yield from self.stop()

  def __iter__(self):
    yield from self.tokenize()


class ParensWithComma(DelimitedList):

  def __init__(self, items):
    super().__init__(start=Symbol("("),
                     stop=Symbol(")"),
                     delimiter=Symbol(','),
                     items=items)