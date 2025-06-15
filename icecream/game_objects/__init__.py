# game_objects/__init__.py
"""
Herní objekty - třídy pro všechny herní entity
"""

from .draggable_item import DraggableItem
from .customer import Customer
from .order import Order
from .floating_icecream import FloatingIcecream

__all__ = ['DraggableItem', 'Customer', 'Order', 'FloatingIcecream']

# ===================================