"""Base class for all data types.

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


class DataType:
  """Base class for all data types."""


class IntegerTypeBase(DataType, abc.ABC):
  """Used to describe signals carrying integer."""

  def __init__(self, signed=None):
    self._signed = signed

  @abc.abstractmethod
  def default_signedness(self):
    raise NotImplementedError("Must be implemented by subclasses.")

  @property
  def signed(self):
    return self._signed if self._signed is not None else self.default_signedness
