#!/usr/bin/env python3
"""
Skript pro vyčištění Python cache a __pycache__ složek
Řeší problémy s přejmenováním modulů
"""

import os
import shutil
import sys

def find_and_remove_pycache(directory="."):
    """Najde a smaže všechny __pycache__ složky"""
    removed_count = 0
    
    for root, dirs, files in os.walk(directory):
        # Najít __pycache__ složky
        if "__pycache__" in dirs:
            pycache_path = os.path.join(root, "__pycache__")
            try:
                shutil.rmtree(pycache_path)
                print(f"✅ Smazána cache: {pycache_path}")
                removed_count += 1
            except Exception as e:
                print(f"❌ Chyba při mazání {pycache_path}: {e}")
        
        # Najít .pyc soubory
        for file in files:
            if file.endswith('.pyc'):
                pyc_path = os.path.join(root, file)
                try:
                    os.remove(pyc_path)
                    print(f"✅ Smazán .pyc soubor: {pyc_path}")
                    removed_count += 1
                except Exception as e:
                    print(f"❌ Chyba při mazání {pyc_path}: {e}")
    
    return removed_count

def clear_import_cache():
    """Vyčistí Python import cache v paměti"""
    # Smazání modulů z sys.modules které začínají na game_object nebo game_objects
    modules_to_remove = []
    
    for module_name in sys.modules.keys():
        if (module_name.startswith('game_object') or 
            module_name.startswith('ui') or 
            module_name.startswith('utils')):
            modules_to_remove.append(module_name)
    
    for module_name in modules_to_remove:
        try:
            del sys.modules[module_name]
            print(f"✅ Smazán z paměti: {module_name}")
        except KeyError:
            pass
    
    return len(modules_to_remove)

def check_directory_structure():
    """Zkontroluje aktuální strukturu adresářů"""
    print("\n📁 Aktuální struktura:")
    
    expected_dirs = ['game_objects', 'ui', 'utils']
    old_dirs = ['game_object']  # Původní název
    
    for dir_name in expected_dirs:
        if os.path.exists(dir_name):
            print(f"✅ {dir_name}/ - EXISTUJE")
            init_file = os.path.join(dir_name, '__init__.py')
            if os.path.exists(init_file):
                print(f"  ✅ {dir_name}/__init__.py - EXISTUJE")
            else:
                print(f"  ❌ {dir_name}/__init__.py - CHYBÍ")
        else:
            print(f"❌ {dir_name}/ - NEEXISTUJE")
    
    # Kontrola starých názvů
    for old_dir in old_dirs:
        if os.path.exists(old_dir):
            print(f"⚠️  {old_dir}/ - STARÝ NÁZEV STÁLE EXISTUJE! Smažte ho.")

def main():
    print("🧹 Čištění Python cache...")
    print(f"📍 Pracovní adresář: {os.getcwd()}")
    
    # 1. Vyčištění souborové cache
    print("\n1️⃣ Mazání __pycache__ složek a .pyc souborů...")
    removed_files = find_and_remove_pycache()
    
    if removed_files == 0:
        print("ℹ️  Žádné cache soubory nenalezeny")
    else:
        print(f"🗑️  Smazáno {removed_files} cache souborů/složek")
    
    # 2. Vyčištění import cache
    print("\n2️⃣ Mazání modulů z paměti...")
    removed_modules = clear_import_cache()
    
    if removed_modules == 0:
        print("ℹ️  Žádné moduly v paměti nenalezeny")
    else:
        print(f"🗑️  Smazáno {removed_modules} modulů z paměti")
    
    # 3. Kontrola struktury
    check_directory_structure()
    
    print("\n✨ Cache byla vyčištěna!")
    print("\n📋 Doporučené další kroky:")
    print("1. Ujistěte se, že složka 'game_object' (bez 's') neexistuje")
    print("2. Zkontrolujte, že máte složku 'game_objects' (s 's')")
    print("3. Restartujte Python interpreter / VS Code")
    print("4. Spusťte main.py znovu")

if __name__ == "__main__":
    main()