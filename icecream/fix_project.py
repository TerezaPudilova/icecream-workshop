#!/usr/bin/env python3
"""
Skript pro opravu projektu - vyčistí cache a nahradí main.py
"""

import os
import shutil

def fix_project():
    print("🔧 Opravuji projekt...")
    
    # 1. Smazání cache
    if os.path.exists("__pycache__"):
        shutil.rmtree("__pycache__")
        print("✅ Smazána __pycache__")
    
    # 2. Záloha starého main.py
    if os.path.exists("main.py"):
        shutil.copy("main.py", "main_old.py")
        print("✅ Záloha main.py -> main_old.py")
    
    # 3. Test importu
    print("🧪 Testování importů...")
    
    try:
        import game_objects.draggable_item
        import ui.drawing
        import utils.game_state
        print("✅ Importy fungují správně")
        
        print("\n🎯 Doporučení:")
        print("1. Nahraďte main.py souborem main_working.py")
        print("2. Nebo spusťte: python main_working.py")
        print("3. Pokud vše funguje, přejmenujte main_working.py na main.py")
        
    except ImportError as e:
        print(f"❌ Import stále nefunguje: {e}")
        print("🛠️ Problém je hlubší - možná chybí některé soubory")

if __name__ == "__main__":
    fix_project()