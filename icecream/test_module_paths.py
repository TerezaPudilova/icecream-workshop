#!/usr/bin/env python3
"""
Test spouštění jako modul z různých adresářů
"""

import os
import sys
import subprocess

def test_module_import():
    """Test různých způsobů spouštění"""
    
    print("🧪 TEST SPOUŠTĚNÍ JAKO MODUL")
    print("=" * 50)
    print(f"📁 Aktuální adresář: {os.getcwd()}")
    
    # Test 1: Přímé spuštění z icecream/
    print(f"\n1️⃣ Test přímého spuštění z icecream/:")
    if os.path.exists("main.py"):
        print("✅ Jsme v icecream/ adresáři")
        try:
            # Test jen importů, ne celé hry
            result = subprocess.run([
                sys.executable, "-c",
                "from utils.path_helper import debug_paths; debug_paths()"
            ], capture_output=True, text=True, cwd=".")
            print("📤 Výstup:")
            print(result.stdout)
            if result.stderr:
                print("❌ Chyby:")
                print(result.stderr)
        except Exception as e:
            print(f"❌ Chyba: {e}")
    else:
        print("❌ Nejsme v icecream/ adresáři")
    
    # Test 2: Spuštění jako modul z nadřazeného adresáře
    print(f"\n2️⃣ Test spuštění jako modul:")
    parent_dir = os.path.dirname(os.getcwd())
    if os.path.exists(os.path.join(parent_dir, "icecream")):
        print("✅ Nalezen nadřazený adresář s icecream/")
        try:
            result = subprocess.run([
                sys.executable, "-c",
                "from icecream.utils.path_helper import debug_paths; debug_paths()"
            ], capture_output=True, text=True, cwd=parent_dir)
            print("📤 Výstup:")
            print(result.stdout)
            if result.stderr:
                print("❌ Chyby:")
                print(result.stderr)
        except Exception as e:
            print(f"❌ Chyba: {e}")
    else:
        print("❌ Nenalezen nadřazený adresář s icecream/")
    
    # Test 3: Simulace různých pracovních adresářů
    print(f"\n3️⃣ Test path_helper z různých míst:")
    
    # Přidání icecream do sys.path
    icecream_path = os.path.abspath(".")
    if icecream_path not in sys.path:
        sys.path.insert(0, icecream_path)
    
    try:
        from utils.path_helper import get_project_root, debug_paths
        
        print(f"📍 Aktuální projekt root: {get_project_root()}")
        
        # Změna pracovního adresáře a test
        original_cwd = os.getcwd()
        
        test_dirs = [
            ".",  # aktuální
            "..",  # nadřazený
            os.path.join("..", ".."),  # o dva výš
        ]
        
        for test_dir in test_dirs:
            if os.path.exists(test_dir):
                abs_test_dir = os.path.abspath(test_dir)
                print(f"\n   🔄 Změna na: {abs_test_dir}")
                try:
                    os.chdir(abs_test_dir)
                    print(f"   📁 Nový pracovní adresář: {os.getcwd()}")
                    print(f"   🎯 Projekt root: {get_project_root()}")
                    
                    # Test existence assets
                    assets_path = os.path.join(get_project_root(), "assets")
                    if os.path.exists(assets_path):
                        print(f"   ✅ Assets nalezeny: {assets_path}")
                    else:
                        print(f"   ❌ Assets nenalezeny: {assets_path}")
                        
                except Exception as e:
                    print(f"   ❌ Chyba: {e}")
                finally:
                    os.chdir(original_cwd)
        
    except ImportError as e:
        print(f"❌ Import selhal: {e}")
    
    print(f"\n📊 SOUHRN:")
    print("✅ Opravený path_helper by měl fungovat z jakéhokoliv adresáře")
    print("🎯 Automaticky najde icecream/ složku a assets/")

def create_test_script():
    """Vytvoří test script pro spuštění z nadřazeného adresáře"""
    
    test_content = '''#!/usr/bin/env python3
"""
Test script pro spuštění icecream modulu z nadřazeného adresáře
Spusťte z icecream-workshop/ pomocí: python test_from_parent.py
"""

import sys
import os

# Přidání icecream do Python path
icecream_path = os.path.join(os.getcwd(), "icecream")
if os.path.exists(icecream_path):
    sys.path.insert(0, icecream_path)
    print(f"✅ Přidána cesta: {icecream_path}")
else:
    print(f"❌ Icecream složka nenalezena: {icecream_path}")
    sys.exit(1)

# Test importu
try:
    from utils.path_helper import debug_paths
    print("✅ Import úspěšný")
    
    # Debug info
    debug_paths()
    
    # Test spuštění hry (jen import, ne spuštění)
    print("\\n🎮 Test importu hlavních modulů:")
    from game_objects.customer import Customer
    from utils.asset_loader import load_scoop_spritesheet
    print("✅ Všechny importy úspěšné")
    
    print("\\n🚀 Nyní můžete spustit: python -m icecream.main")
    
except ImportError as e:
    print(f"❌ Import selhal: {e}")
    import traceback
    traceback.print_exc()
'''
    
    parent_dir = os.path.dirname(os.getcwd())
    test_file_path = os.path.join(parent_dir, "test_from_parent.py")
    
    try:
        with open(test_file_path, 'w', encoding='utf-8') as f:
            f.write(test_content)
        print(f"✅ Vytvořen test script: {test_file_path}")
        print(f"📝 Spusťte z {parent_dir}/: python test_from_parent.py")
    except Exception as e:
        print(f"❌ Chyba při vytváření test scriptu: {e}")

if __name__ == "__main__":
    test_module_import()
    print(f"\n" + "="*50)
    create_test_script()