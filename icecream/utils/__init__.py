# utils/__init__.py
"""
Pomocné funkce - načítání assetů, herní logika a správa stavu
"""

from .asset_loader import load_scoop_spritesheet, load_cone_spritesheet, load_icecream_decoration
from .game_logic import *
from .game_state import GameState
from .path_helper import get_asset_path, check_asset_exists, list_assets_in_directory

__all__ = [
    # Asset loader
    'load_scoop_spritesheet', 'load_cone_spritesheet', 'load_icecream_decoration',
    # Game logic
    'check_order_correctness', 'reset_assembly', 'complete_order', 
    'add_new_customer', 'return_to_menu', 'reset_game_completely',
    'initialize_game', 'get_time_left', 'get_assembled_items_global', 'set_assembled_items_global',
    # Game state
    'GameState',
    # Path helper
    'get_asset_path', 'check_asset_exists', 'list_assets_in_directory'
]