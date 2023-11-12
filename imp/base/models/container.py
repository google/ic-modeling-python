"""Base class for all Containers.

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
import typing

from imp.base.models import component
from typing import Any, Iterator, List, Mapping, Optional


class ContainerBuilderMixin(abc.ABC):
  """Abstract base class for Container subclasses."""

  @abc.abstractmethod
  def _add_item(self, item: component.Component):
    """Adds an item to a container"""


class NamespaceBuilderMixin(ContainerBuilderMixin):
  """Abstract base class for namespaced containers."""

  @abc.abstractmethod
  def _add_named_item(self, name: str, item: component.Component):
    """Adds a named item to a component's namespace."""


class Container(ContainerBuilderMixin, component.Component):
  """Base class for SV constructs that contain other components."""

  parent: 'Container'

  def __init__(self):
    self._items = []

  @property
  def items(self) -> List[Iterator[component.Component]]:
    """Returns all child items of the container."""
    return list(self.iter_items(expand=True))

  def _add_item(self, item: component.Component) -> component.Component:
    """Adds an item to the container and sets its parent."""
    self._items.append(item)
    item.set_parent(self)
    return item

  def __contains__(self, item: component.Component):
    """Returns True if the item is part of this container."""
    return item in self.items

  def __iter__(self) -> Iterator[component.Component]:
    """Iterate over the items stored in this container."""
    for item in self._items:
      if isinstance(item, Container):
        yield from item
      else:
        yield item

  def iter_items(self, expand=True, filter_fn=lambda i: True) -> Iterator[component.Component]:
    """Iterates over the container's items, filtering them if needed."""
    for item in self._items:
      if filter_fn(item):
        yield item

      if isinstance(item, Container) and expand:
        yield from item.iter_items(expand=expand, filter_fn=filter_fn)


class NamespacedContainer(Container):
  """Adds support for namespaced components within a Container."""
  _named_items: Mapping[str, component.Component]

  def __init__(self):
    super().__init__()
    self._named_items = {}

  def _add_named_item(self, name: str, item: component.Component) -> component.Component:
    if name in self._named_items:
      raise KeyError(f"An item named {name} already exists in {self}")
    self._named_items[name] = item
    return item

  def __getattr__(self, name: str) -> Any:
    if name == "_named_items":
      object.__getattribute__(self, name)
    if name in self._named_items:
      return self._named_items[name]
    object.__getattribute__(self, name)

  def _validate_item(self):
    """Raises a ValueError if the item isn't allowed in the container."""


class Block(NamespacedContainer):
  parent: NamespacedContainer

  def __init__(self, name: Optional[str] = None):
    super().__init__()
    self.name = name


class Group(Container):
  """Logically groups a sequence of Components together."""
  parent: NamespacedContainer

  def _add_named_item(self, name: str, item: component.Component):
    parent = typing.cast(NamespacedContainer, self.parent)
    parent._add_named_item(name=name, item=item)
