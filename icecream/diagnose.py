#!/usr/bin/env python3
"""
Podrobná diagnostika problému s importy
"""

import os
import sys

def diagnose_project():
    print("🔍 PODROBNÁ DIAGNOSTIKA PROJEKTU")
    print("=" * 50)
    
    # 1. Základní informace
    print(f"📁 Aktuální adresář: {os.getcwd()}")
    print(f"🐍 Python verze: {sys.version}")
    print(f"📍 Python cesta: {sys.executable}")
    
    # 2. Obsah aktuálního adresáře
    print(f"\n📂 Obsah aktuálního adresáře:")
    try:
        items = os.listdir('.')
        for item in sorted(items):
            if os.path.isdir(item):
                print(f"   📁 {item}/")
            else:
                print(f"   📄 {item}")
    except Exception as e:
        print(f"   ❌ Chyba při čtení adresáře: {e}")
    
    # 3. Kontrola struktury projektu
    print(f"\n🏗️ KONTROLA STRUKTURY PROJEKTU:")
    
    required_structure = {
        'main.py': 'file',
        'game_objects': 'dir',
        'game_objects/__init__.py': 'file',
        'game_objects/draggable_item.py': 'file',
        'game_objects/customer.py': 'file', 
        'game_objects/order.py': 'file',
        'game_objects/floating_icecream.py': 'file',
        'ui': 'dir',
        'ui/__init__.py': 'file',
        'ui/drawing.py': 'file',
        'ui/buttons.py': 'file',
        'utils': 'dir',
        'utils/__init__.py': 'file',
        'utils/asset_loader.py': 'file',
        'utils/game_logic.py': 'file',
        'utils/game_state.py': 'file'
    }
    
    missing_items = []
    
    for item, item_type in required_structure.items():
        if item_type == 'file':
            if os.path.isfile(item):
                print(f"   ✅ {item}")
            else:
                print(f"   ❌ {item} - CHYBÍ!")
                missing_items.append(item)
        elif item_type == 'dir':
            if os.path.isdir(item):
                print(f"   ✅ {item}/")
            else:
                print(f"   ❌ {item}/ - CHYBÍ!")
                missing_items.append(item)
    
    # 4. Kontrola obsahu __init__.py souborů
    print(f"\n📝 KONTROLA __init__.py SOUBORŮ:")
    
    init_files = [
        'game_objects/__init__.py',
        'ui/__init__.py', 
        'utils/__init__.py'
    ]
    
    for init_file in init_files:
        if os.path.exists(init_file):
            try:
                with open(init_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if content:
                        lines = content.count('\n') + 1
                        print(f"   ✅ {init_file} - {lines} řádků")
                    else:
                        print(f"   ⚠️ {init_file} - PRÁZDNÝ!")
            except Exception as e:
                print(f"   ❌ {init_file} - Chyba čtení: {e}")
        else:
            print(f"   ❌ {init_file} - NEEXISTUJE!")
    
    # 5. Kontrola sys.path
    print(f"\n🛤️ PYTHON SEARCH PATH:")
    current_dir = os.path.abspath('.')
    path_contains_current = current_dir in sys.path
    
    print(f"   📍 Aktuální adresář: {current_dir}")
    print(f"   📍 Je v sys.path: {'✅ ANO' if path_contains_current else '❌ NE'}")
    
    print(f"   📍 Prvních 5 cest v sys.path:")
    for i, path in enumerate(sys.path[:5]):
        marker = "👈" if path == current_dir else ""
        print(f"      {i+1}. {path} {marker}")
    
    # 6. Test importu s detailní chybou
    print(f"\n🧪 TEST IMPORTŮ:")
    
    # Přidání aktuálního adresáře do sys.path
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
        print(f"   📍 Přidán aktuální adresář do sys.path")
    
    # Test jednotlivých importů
    test_imports = [
        ('game_objects', 'import game_objects'),
        ('game_objects.draggable_item', 'from game_objects.draggable_item import DraggableItem'),
        ('ui', 'import ui'),
        ('ui.drawing', 'from ui.drawing import draw_gradient_background'),
        ('utils', 'import utils'),
        ('utils.game_state', 'from utils.game_state import GameState')
    ]
    
    for module_name, import_statement in test_imports:
        try:
            exec(import_statement)
            print(f"   ✅ {module_name} - OK")
        except ImportError as e:
            print(f"   ❌ {module_name} - ImportError: {e}")
        except Exception as e:
            print(f"   ❌ {module_name} - Jiná chyba: {e}")
    
    # 7. Kontrola starých názvů
    print(f"\n🕵️ KONTROLA STARÝCH NÁZVŮ:")
    old_names = ['game_object']  # bez 's'
    
    for old_name in old_names:
        if os.path.exists(old_name):
            print(f"   ⚠️ NALEZEN STARÝ NÁZEV: {old_name}/ - SMAŽTE HO!")
        else:
            print(f"   ✅ {old_name}/ - neexistuje (dobře)")
    
    # 8. Souhrn
    print(f"\n📊 SOUHRN:")
    if missing_items:
        print(f"   ❌ Chybí {len(missing_items)} položek: {missing_items}")
        print(f"   🛠️ Doporučení: Spusťte setup_project.py pro vytvoření chybějících souborů")
    else:
        print(f"   ✅ Všechny požadované soubory existují")
    
    if not path_contains_current:
        print(f"   ⚠️ Aktuální adresář není v sys.path")
        print(f"   🛠️ Doporučení: Spouštějte Python z adresáře s main.py")
    
    # 9. Doporučená řešení
    print(f"\n💡 DOPORUČENÁ ŘEŠENÍ:")
    print(f"   1. Ujistěte se, že jste v adresáři s main.py")
    print(f"   2. Smažte všechny složky s nesprávnými názvy")
    print(f"   3. Zkontrolujte, že všechny __init__.py soubory obsahují správné importy")
    print(f"   4. Restartujte Python prostředí")
    print(f"   5. Zkuste spustit: python -c 'import game_objects; print(\"OK\")'")

if __name__ == "__main__":
    diagnose_project()