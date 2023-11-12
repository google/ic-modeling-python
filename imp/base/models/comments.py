"""Base class for all Comments.

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


class Comment(component.Component):
  """Represents a single line comment."""
  def __init__(self, txt: str):
    super().__init__()
    self.txt = txt


class Banner(Comment):
  """Represents a single line comment, bordered with additional text."""
  def __init__(self, txt, border_char="-", num=40):
    super().__init__(txt=txt)
    self.border_char = border_char
    self.num = num


class BlockComment(Comment):
  """Represents a block (multi-line) comment."""
  def __init__(self, txt: str):
    super().__init__(txt=txt)


class HasComments:
  """Mix-in class for adding a comments builder to a Container."""

  def comment(self, txt: str) -> Comment:
    item = comments.Comment(txt=txt)
    return self._add_item(item)


  def block_comment(self, txt: str) -> BlockComment:
    item = comments.BlockComment(txt=txt)
    return self._add_item(item)