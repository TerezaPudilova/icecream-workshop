#!/usr/bin/env python3
"""
Vyčištění projektu - odstranění nepotřebných souborů a zjednodušení
"""

import os
import shutil
from datetime import datetime

def cleanup_project():
    """Vyčistí projekt od diagnostických a modularizačních souborů"""
    
    print("🧹 VYČIŠTĚNÍ PROJEKTU")
    print("=" * 40)
    
    # Soubory ke smazání
    files_to_remove = [
        # Diagnostické soubory
        "icecream/diagnose_module.py",
        "icecream/diagnose.py",
        "icecream/fix_project.py", 
        "icecream/test_module_paths.py",
        "icecream/clear_cache.py",
        "run_icecream.py",
        "test_from_parent.py",
        
        # Modularizační soubory (pro jen přímé spuštění)
        "icecream/__init__.py",
        "icecream/utils/path_helper.py",
    ]
    
    # Smazání souborů
    removed_count = 0
    for file_path in files_to_remove:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"🗑️ Smazán: {file_path}")
                removed_count += 1
            except Exception as e:
                print(f"❌ Chyba při mazání {file_path}: {e}")
        else:
            print(f"⚪ Neexistuje: {file_path}")
    
    print(f"\n📊 Smazáno {removed_count} souborů")
    
    return removed_count > 0

def simplify_main_py():
    """Zjednoduší main.py - odstraní setup funkci"""
    
    print(f"\n🔧 ZJEDNODUŠENÍ MAIN.PY")
    print("-" * 30)
    
    main_file = "icecream/main.py"
    
    if not os.path.exists(main_file):
        print("❌ main.py nenalezen")
        return False
    
    # Záloha
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"icecream/main_before_cleanup_{timestamp}.py"
    
    try:
        shutil.copy(main_file, backup_file)
        print(f"💾 Záloha: {backup_file}")
        
        # Načtení obsahu
        with open(main_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Odstranění setup funkce a jejího volání
        lines = content.split('\n')
        new_lines = []
        skip_until_empty = False
        
        for line in lines:
            # Přeskočit definici setup funkce
            if line.strip().startswith('def setup_module_paths():'):
                skip_until_empty = True
                continue
            
            # Přeskočit tělo funkce až do prázdné řádky
            if skip_until_empty:
                if line.strip() == '' and not line.startswith('    '):
                    skip_until_empty = False
                continue
            
            # Přeskočit volání setup funkce
            if 'setup_module_paths()' in line:
                continue
            
            # Přeskočit komentář o setup funkci
            if '# DŮLEŽITÉ: Nastavení cest PŘED' in line:
                continue
                
            new_lines.append(line)
        
        # Zápis zpět
        simplified_content = '\n'.join(new_lines)
        
        with open(main_file, 'w', encoding='utf-8') as f:
            f.write(simplified_content)
        
        print("✅ main.py zjednodušen")
        return True
        
    except Exception as e:
        print(f"❌ Chyba při zjednodušování main.py: {e}")
        return False

def fix_asset_loader():
    """Opraví asset_loader.py - vrátí jednoduché cesty"""
    
    print(f"\n🔧 OPRAVA ASSET_LOADER.PY")
    print("-" * 30)
    
    asset_file = "icecream/utils/asset_loader.py"
    
    if not os.path.exists(asset_file):
        print("❌ asset_loader.py nenalezen")
        return False
    
    try:
        # Záloha
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"icecream/utils/asset_loader_backup_{timestamp}.py"
        shutil.copy(asset_file, backup_file)
        print(f"💾 Záloha: {backup_file}")
        
        # Načtení a úprava
        with open(asset_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Nahrazení složitých cest jednoduchými
        replacements = [
            # Odstranění importu path_helper
            ('from .path_helper import get_asset_path, check_asset_exists', ''),
            
            # Nahrazení get_asset_path jednoduchými cestami
            ('image_path = get_asset_path("Icecream/icecream_uvod_2.png")\n        icecream_sheet = pygame.image.load(image_path).convert_alpha()', 
             'icecream_sheet = pygame.image.load("assets/Icecream/icecream_uvod_2.png").convert_alpha()'),
            
            ('image_path = get_asset_path("Icecream/download.png")\n        spritesheet = pygame.image.load(image_path).convert_alpha()', 
             'spritesheet = pygame.image.load("assets/Icecream/download.png").convert_alpha()'),
            
            ('image_path = get_asset_path("Icecream/cones.png")\n        spritesheet = pygame.image.load(image_path).convert_alpha()', 
             'spritesheet = pygame.image.load("assets/Icecream/cones.png").convert_alpha()'),
            
            # Ostatní get_asset_path
            ('pygame.image.load(get_asset_path("Icecream/cokoladova.png")).convert_alpha()', 
             'pygame.image.load("assets/Icecream/cokoladova.png").convert_alpha()'),
            
            ('pygame.image.load(get_asset_path("Icecream/smoulova.png")).convert_alpha()', 
             'pygame.image.load("assets/Icecream/smoulova.png").convert_alpha()'),
            
            ('pygame.image.load(get_asset_path("Icecream/kornout.png")).convert_alpha()', 
             'pygame.image.load("assets/Icecream/kornout.png").convert_alpha()'),
        ]
        
        for old, new in replacements:
            content = content.replace(old, new)
        
        # Zápis zpět
        with open(asset_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ asset_loader.py opraven")
        return True
        
    except Exception as e:
        print(f"❌ Chyba při opravě asset_loader.py: {e}")
        return False

def fix_customer_py():
    """Opraví customer.py - vrátí jednoduchou cestu"""
    
    print(f"\n🔧 OPRAVA CUSTOMER.PY")
    print("-" * 25)
    
    customer_file = "icecream/game_objects/customer.py"
    
    if not os.path.exists(customer_file):
        print("❌ customer.py nenalezen")
        return False
    
    try:
        with open(customer_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Jednoduché nahrazení složité cesty
        old_code = '''import os

def get_customer_asset_path(relative_path):
    """Helper pro získání cesty k customer assetům"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    return os.path.join(project_root, "assets", relative_path)'''
        
        new_code = ''
        
        content = content.replace(old_code, new_code)
        
        # Nahrazení složité cesty jednoduchou
        content = content.replace(
            'image_path = get_customer_asset_path("Customers/Customer1FF.png")',
            'image_path = "assets/Customers/Customer1FF.png"'
        )
        
        with open(customer_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ customer.py opraven")
        return True
        
    except Exception as e:
        print(f"❌ Chyba při opravě customer.py: {e}")
        return False

def update_utils_init():
    """Aktualizuje utils/__init__.py - odstraní path_helper"""
    
    print(f"\n🔧 AKTUALIZACE UTILS/__INIT__.PY")
    print("-" * 35)
    
    init_file = "icecream/utils/__init__.py"
    
    if not os.path.exists(init_file):
        print("❌ utils/__init__.py nenalezen")
        return False
    
    try:
        with open(init_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Odstranění path_helper importů
        lines = content.split('\n')
        new_lines = []
        
        for line in lines:
            # Přeskočit řádky s path_helper
            if 'path_helper' in line:
                continue
            new_lines.append(line)
        
        new_content = '\n'.join(new_lines)
        
        with open(init_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("✅ utils/__init__.py aktualizován")
        return True
        
    except Exception as e:
        print(f"❌ Chyba při aktualizaci utils/__init__.py: {e}")
        return False

def create_readme():
    """Vytvoří README.md s instrukcemi"""
    
    readme_content = """# Icecream Game 🍦

Jednoduchá hra na obsluhu zmrzlinárny vytvořená v Pygame.

## 🚀 Spuštění hry

```bash
cd icecream/
python main.py
```

## 🎮 Ovládání

- **Enter** - Spustit hru / Dokončit objednávku
- **Mezerník** - Reset sestavování
- **Escape** - Návrat do menu / Ukončit hru
- **Myš** - Přetahování ingrediencí

## 📁 Struktura projektu

```
icecream/
├── main.py              # Hlavní soubor hry
├── assets/              # Grafické assety
├── game_objects/        # Herní objekty (zákazníci, předměty, objednávky)
├── ui/                  # Uživatelské rozhraní
└── utils/               # Pomocné funkce
```

## 🎯 Cíl hry

Obsluhujte zákazníky ve zmrzlinárně! Sestavte správné objednávky podle požadavků zákazníků v časovém limitu.

---
*Projekt vytvořen jako vzdělávací ukázka programování v Pygame*
"""
    
    try:
        with open("README.md", 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print("✅ README.md vytvořen")
        return True
    except Exception as e:
        print(f"❌ Chyba při vytváření README.md: {e}")
        return False

def show_final_structure():
    """Ukáže finální strukturu projektu"""
    
    print(f"\n📁 FINÁLNÍ STRUKTURA:")
    print("=" * 30)
    print("""
icecream-workshop/
├── README.md               # 📖 Instrukce
├── requirements.txt        # 📦 Závislosti  
└── icecream/              # 🎮 Hlavní hra
    ├── main.py            # 🚀 Spuštění
    ├── assets/            # 🎨 Obrázky
    ├── game_objects/      # 👥 Herní objekty
    ├── ui/                # 🖼️ Rozhraní
    └── utils/             # 🔧 Nástroje

🚀 Spuštění: cd icecream && python main.py
""")

if __name__ == "__main__":
    print("🧹 VYČIŠTĚNÍ PROJEKTU PRO JEDNODUCHÉ SPUŠTĚNÍ")
    print("=" * 60)
    
    # Postupné vyčištění
    cleanup_project()
    simplify_main_py()
    fix_asset_loader()
    fix_customer_py()
    update_utils_init()
    create_readme()
    
    # Finální struktura
    show_final_structure()
    
    print(f"\n🎉 VYČIŠTĚNÍ DOKONČENO!")
    print("=" * 30)
    print("✅ Projekt je nyní jednoduchý a přehledný")
    print("🚀 Spusťte: cd icecream && python main.py")
    print("📖 Přečtěte si README.md pro více informací")