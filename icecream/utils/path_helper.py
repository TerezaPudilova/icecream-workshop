"""
Pomocné funkce pro správné cesty k assetům
"""

import os
import sys

def get_project_root():
    """
    Najde kořenový adresář projektu (kde je main.py a assets/)
    Funguje bez ohledu na to, odkud se spouští
    """
    # Získání adresáře tohoto souboru (utils/)
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Pokud jsme v utils/, jdeme o úroveň výš do icecream/
    project_root = os.path.dirname(current_file_dir)
    
    # Kontrola zda máme správný adresář (hledáme main.py a assets/)
    main_py_path = os.path.join(project_root, "main.py")
    assets_path = os.path.join(project_root, "assets")
    
    if os.path.exists(main_py_path) and os.path.exists(assets_path):
        return project_root
    
    # Pokud nejsme ve správném adresáři, zkusíme najít icecream/ složku
    # Toto pomůže když spouštíme python -m icecream.main
    current_working_dir = os.getcwd()
    
    # Možné cesty kde hledat icecream/ složku
    possible_paths = [
        current_working_dir,  # aktuální adresář
        os.path.join(current_working_dir, "icecream"),  # ./icecream/
        os.path.dirname(current_working_dir),  # ../
    ]
    
    for path in possible_paths:
        icecream_path = os.path.join(path, "icecream") if not path.endswith("icecream") else path
        
        if os.path.exists(icecream_path):
            main_py = os.path.join(icecream_path, "main.py")
            assets_dir = os.path.join(icecream_path, "assets")
            
            if os.path.exists(main_py) and os.path.exists(assets_dir):
                return icecream_path
    
    # Fallback - vrátíme původní project_root
    print(f"⚠️ Nelze najít kořenový adresář projektu, používám: {project_root}")
    return project_root

def get_asset_path(relative_path):
    """
    Vrátí správnou cestu k assetu relativně k hlavnímu adresáři projektu
    
    Args:
        relative_path (str): Relativní cesta od assets/ složky
        
    Returns:
        str: Plná cesta k souboru
        
    Example:
        get_asset_path("Icecream/download.png") -> "/path/to/icecream/assets/Icecream/download.png"
    """
    project_root = get_project_root()
    full_path = os.path.join(project_root, "assets", relative_path)
    return full_path

def check_asset_exists(relative_path):
    """
    Zkontroluje zda asset existuje
    
    Args:
        relative_path (str): Relativní cesta od assets/ složky
        
    Returns:
        bool: True pokud soubor existuje
    """
    full_path = get_asset_path(relative_path)
    exists = os.path.exists(full_path)
    
    # Debug informace
    if not exists:
        print(f"🔍 Asset nenalezen: {relative_path}")
        print(f"   Hledaná cesta: {full_path}")
        print(f"   Projekt root: {get_project_root()}")
        print(f"   Pracovní adresář: {os.getcwd()}")
    
    return exists

def list_assets_in_directory(directory):
    """
    Vypíše všechny assety v daném adresáři
    
    Args:
        directory (str): Adresář relativně k assets/
        
    Returns:
        list: Seznam souborů v adresáři
    """
    full_path = get_asset_path(directory)
    if os.path.exists(full_path):
        return os.listdir(full_path)
    else:
        return []

# Debug funkce
def debug_paths():
    """Vypíše debug informace o cestách"""
    print("🔍 DEBUG INFORMACE O CESTÁCH:")
    print(f"   📁 Pracovní adresář: {os.getcwd()}")
    print(f"   📄 Tento soubor: {__file__}")
    print(f"   📂 Adresář tohoto souboru: {os.path.dirname(os.path.abspath(__file__))}")
    print(f"   🎯 Projekt root: {get_project_root()}")
    print(f"   📦 Assets adresář: {os.path.join(get_project_root(), 'assets')}")
    
    # Test některých assetů
    test_assets = ["Icecream/download.png", "Customers/Customer1FF.png"]
    for asset in test_assets:
        path = get_asset_path(asset)
        exists = os.path.exists(path)
        status = "✅" if exists else "❌"
        print(f"   {status} {asset} -> {path}")

# Test funkce
if __name__ == "__main__":
    debug_paths()