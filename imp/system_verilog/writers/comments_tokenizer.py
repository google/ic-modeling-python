"""Translate Comments to SystemVerilog code.

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
from imp.base.models import comments
from imp.base.writers.model_tokenizer import tokenizer_for

SP = tokens.Space
Symbol = tokens.Symbol
Literal = tokens.Literal
CR = tokens.NewLine


@tokenizer_for(comments.Comment)
def comment_tokenizer(target: comments.Comment, tokenize):
  yield from Symbol("//") + SP() + Literal(target.txt)


@tokenizer_for(comments.Banner)
def banner_tokenizer(target: comments.Banner, tokenize):
  banner_txt = target.border_char * target.num
  yield from Symbol("//") + SP() + Literal(banner_txt) + CR()
  yield from Symbol("//") + SP() + Literal(target.txt) + CR()
  yield from Symbol("//") + SP() + Literal(banner_txt) + CR()


@tokenizer_for(comments.BlockComment)
def block_comment_tokenizer(target: comments.BlockComment, tokenize):
  yield from Symbol("/*") + SP() + Literal(target.txt) + SP() + Symbol("*/")