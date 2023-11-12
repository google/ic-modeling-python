""" ModelTokenizer Class

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

import abc
from imp.base.writers import tokens

from imp.base.models import component
from typing import Callable, Iterator, Sequence

TokenizerFunctionType = Callable[[component.Component], Sequence[tokens.Token]]


class tokenizer_for:
  """Class based decorator for tokenzier functions.

  This library's approach to converting our models to source code
  involves the creation of fine-grained handlers. Given a component
  it will produce a sequence of tokens (including formatting tokens).

  For example, a tokenizer for a comment may look like this:

    @tokenizer_for(imp.base.models.comment.Comment)
    def tokenize_comments(comment: Comment):
      yield from Symbol("//") + Space() + Literal(comment.txt)

  The decorator makes it easy to create a dict mapping tokenizer functions
  to the component class when given a list of tokenizer functions;

    for fn in tokenizer_functions:
      target = fn.__dict__['tokenizer_for']
      self.handlers_by_token_cls[target] = fn
  """

  def __init__(self, component_cls):
    self.target = component_cls

  def __call__(self, tokenizer_fn):
    tokenizer_fn.__dict__['tokenizer_for'] = self.target
    return tokenizer_fn


class ModelTokenizer:
  """Produces tokens from components/containers."""

  @abc.abstractmethod
  def tokenize(self, item: component.Component) -> Iterator[tokens.Token]:
    """Given a component, yields its tokens.

    This abstract base class gives authors several options for implementing their tokenizer.

    The simplest of each approach is to create a list of TokenizerFunctionTypes and when given
    an item, explicitly look up the handler based on the class type.  Variations of similar
    tokenizers by including different fine-grained handlers into the list.  This list
    can be created by a class method, or defined as a module level constant and passed into
    the initializer of the target ModelTokenizer.

    It could be also implemented as a class that uses functools.multipledispatchmethod, with one
    method for each component type.
    """