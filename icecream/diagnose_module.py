#!/usr/bin/env python3
"""
Diagnostika problému s python -m icecream.main
"""

import os
import sys
import subprocess

def diagnose_module_problem():
    print("🔍 DIAGNOSTIKA PROBLÉMU S MODULEM")
    print("=" * 60)
    
    # Základní info
    print(f"📁 Aktuální adresář: {os.getcwd()}")
    print(f"🐍 Python: {sys.executable}")
    print(f"📍 Python verze: {sys.version.split()[0]}")
    
    # Kontrola struktury
    print(f"\n📂 KONTROLA STRUKTURY:")
    
    current_dir = os.getcwd()
    icecream_dir = os.path.join(current_dir, "icecream")
    
    if os.path.exists(icecream_dir):
        print(f"✅ icecream/ složka existuje")
        
        # Kontrola __init__.py v icecream/
        init_file = os.path.join(icecream_dir, "__init__.py")
        if os.path.exists(init_file):
            print(f"✅ icecream/__init__.py existuje")
        else:
            print(f"❌ icecream/__init__.py CHYBÍ! - Toto je pravděpodobně problém")
            
        # Kontrola main.py
        main_file = os.path.join(icecream_dir, "main.py")
        if os.path.exists(main_file):
            print(f"✅ icecream/main.py existuje")
        else:
            print(f"❌ icecream/main.py CHYBÍ!")
            
        # Kontrola modulů
        modules = ["game_objects", "ui", "utils"]
        for module in modules:
            module_dir = os.path.join(icecream_dir, module)
            module_init = os.path.join(module_dir, "__init__.py")
            
            if os.path.exists(module_dir):
                print(f"✅ icecream/{module}/ existuje")
                if os.path.exists(module_init):
                    print(f"✅ icecream/{module}/__init__.py existuje")
                else:
                    print(f"❌ icecream/{module}/__init__.py CHYBÍ!")
            else:
                print(f"❌ icecream/{module}/ CHYBÍ!")
    else:
        print(f"❌ icecream/ složka neexistuje v {current_dir}")
        return False
    
    # Test Python import
    print(f"\n🧪 TEST PYTHON IMPORTU:")
    
    # Test 1: Základní import icecream
    print(f"1️⃣ Test: import icecream")
    result = subprocess.run([
        sys.executable, "-c", "import icecream; print('✅ Import icecream úspěšný')"
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ {result.stdout.strip()}")
    else:
        print(f"❌ Chyba: {result.stderr.strip()}")
    
    # Test 2: Import icecream.main
    print(f"2️⃣ Test: import icecream.main")
    result = subprocess.run([
        sys.executable, "-c", "import icecream.main; print('✅ Import icecream.main úspěšný')"
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ {result.stdout.strip()}")
    else:
        print(f"❌ Chyba: {result.stderr.strip()}")
    
    # Test 3: Spuštění jako modul
    print(f"3️⃣ Test: python -m icecream.main")
    result = subprocess.run([
        sys.executable, "-m", "icecream.main"
    ], capture_output=True, text=True, timeout=5)
    
    if result.returncode == 0:
        print(f"✅ Modul se spustil úspěšně")
        print(f"📤 Stdout: {result.stdout[:200]}...")
    else:
        print(f"❌ Chyba při spuštění modulu:")
        print(f"📤 Stderr: {result.stderr}")
        print(f"📤 Stdout: {result.stdout}")
    
    # Test cest k assetům
    print(f"\n📦 TEST CEST K ASSETŮM:")
    result = subprocess.run([
        sys.executable, "-c", 
        """
import sys
sys.path.insert(0, './icecream')
try:
    from utils.path_helper import debug_paths
    debug_paths()
except Exception as e:
    print(f'❌ Chyba: {e}')
    import traceback
    traceback.print_exc()
"""
    ], capture_output=True, text=True)
    
    print(result.stdout)
    if result.stderr:
        print(f"❌ Chyby: {result.stderr}")

def create_missing_files():
    """Vytvoří chybějící __init__.py soubory"""
    print(f"\n🛠️ VYTVÁŘENÍ CHYBĚJÍCÍCH SOUBORŮ:")
    
    current_dir = os.getcwd()
    icecream_dir = os.path.join(current_dir, "icecream")
    
    # icecream/__init__.py
    init_file = os.path.join(icecream_dir, "__init__.py")
    if not os.path.exists(init_file):
        try:
            with open(init_file, 'w', encoding='utf-8') as f:
                f.write('"""\nIcecream Game Package\n"""\n\n__version__ = "1.0.0"\n')
            print(f"✅ Vytvořen: icecream/__init__.py")
        except Exception as e:
            print(f"❌ Chyba při vytváření icecream/__init__.py: {e}")
    else:
        print(f"✅ icecream/__init__.py již existuje")

def provide_solutions():
    """Poskytne řešení problémů"""
    print(f"\n💡 MOŽNÁ ŘEŠENÍ:")
    print("=" * 40)
    
    print("1️⃣ VYTVOŘENÍ __init__.py:")
    print("   Spusťte: create_missing_files() funkci")
    print()
    
    print("2️⃣ ALTERNATIVNÍ SPUŠTĚNÍ:")
    print("   cd icecream-workshop")
    print("   PYTHONPATH=./icecream python -m main")
    print()
    
    print("3️⃣ PŘÍMÉ SPUŠTĚNÍ:")
    print("   cd icecream")
    print("   python main.py")
    print()
    
    print("4️⃣ SCRIPT WRAPPER:")
    print("   Vytvořte run_icecream.py v icecream-workshop/")

def create_wrapper_script():
    """Vytvoří wrapper script pro snadné spuštění"""
    wrapper_content = '''#!/usr/bin/env python3
"""
Wrapper script pro spuštění icecream hry
Spusťte z icecream-workshop/ pomocí: python run_icecream.py
"""

import os
import sys

# Přidání icecream do Python path
icecream_path = os.path.join(os.path.dirname(__file__), "icecream")
if os.path.exists(icecream_path):
    sys.path.insert(0, icecream_path)
    
    # Změna pracovního adresáře na icecream
    os.chdir(icecream_path)
    
    # Import a spuštění main
    try:
        import main
        print("🎮 Spouštím Icecream Game...")
        main.main()
    except Exception as e:
        print(f"❌ Chyba při spuštění: {e}")
        import traceback
        traceback.print_exc()
else:
    print(f"❌ Icecream složka nenalezena: {icecream_path}")
'''
    
    wrapper_path = "run_icecream.py"
    try:
        with open(wrapper_path, 'w', encoding='utf-8') as f:
            f.write(wrapper_content)
        print(f"✅ Vytvořen wrapper script: {wrapper_path}")
        print(f"🚀 Spusťte pomocí: python {wrapper_path}")
    except Exception as e:
        print(f"❌ Chyba při vytváření wrapper scriptu: {e}")

if __name__ == "__main__":
    # Spuštění diagnostiky
    diagnose_module_problem()
    
    # Vytvoření chybějících souborů
    create_missing_files()
    
    # Vytvoření wrapper scriptu
    print(f"\n" + "="*60)
    create_wrapper_script()
    
    # Možná řešení
    provide_solutions()
    
    print(f"\n🎯 DOPORUČENÍ:")
    print("Nejjednodušší je použít vytvořený run_icecream.py script")
    print("nebo spouštět přímo: cd icecream && python main.py")