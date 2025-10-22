"""Grouping functionality allows nesting of one item within another item
(parent item). This is useful in several use cases.

- artifact deployed within a node
- a class within a package, or a component
- composite structures (i.e. component within a node)

The grouping adapters has to implement three methods, see `AbstractGroup`
class.

It is important to note, that grouping adapters can be queried before
instance of an item to be grouped is created. This happens when item
is about to be created. Therefore, `AbstractGroup.can_contain` has
to be aware `AbstractGroup.item` can be null.
"""

from __future__ import annotations

import abc

from generic.multidispatch import FunctionDispatcher, multidispatch

from gaphor.core.modeling import Presentation


class AbstractGroup(metaclass=abc.ABCMeta):
    """Base class for grouping model elements.

    :param parent: Parent item, which groups other items.
    :type parent: Presentation
    :param item: Item to be grouped.
    :type item: Presentation
    """

    def __init__(self, parent: Presentation, item: Presentation) -> None:
        self.parent = parent
        self.item = item

    def can_contain(self) -> bool:
        """Determine if parent can contain item."""
        return True

    @abc.abstractmethod
    def group(self) -> None:
        """Perform grouping of items."""

    @abc.abstractmethod
    def ungroup(self) -> None:
        """Perform ungrouping of items."""


# Work around issue https://github.com/python/mypy/issues/3135 (Class decorators are not type checked)
# This definition, along with the the ignore below, seems to fix the behaviour for mypy at least.


class NoGrouping(AbstractGroup):
    def can_contain(self) -> bool:
        return False

    def group(self) -> None:
        pass

    def ungroup(self) -> None:
        pass


Group: FunctionDispatcher[type[AbstractGroup]] = multidispatch(object, object)(
    NoGrouping
)

# Until we can deal with types (esp. typing.Any) we use this as a workaround:
Group.register(None, object)(NoGrouping)
