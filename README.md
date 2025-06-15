# 🍦 Ice Cream Game

Jednoduchá 2D hra vytvořená v Pythonu pomocí knihovny Pygame. Otevře se jako samostatné desktopové okno.

## 🧰 Požadavky

- Python 3.11+
- Pygame
- NumPy

## 🛠️ Instalace

1. Naklonuj repozitář:

```bash
git clone https://github.com/tvoje-uzivatelske-jmeno/icecream-game.git
cd icecream-game

```

## 🛠️ Aktivace .venv a spuštění hry

1. Vytvoř a aktivuj virtuální prostředí

```bash
python -m venv .venv
source .venv/bin/activate   # na Windows: .venv\Scripts\activate
```

2. Nainstaluj závilosti

```bash
pip install -r requirements.txt
```

3. spusť hru

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
