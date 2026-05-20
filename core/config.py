#### Imports ####

import sys
from pathlib import Path


#### Variables ####

BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
WEB_DIR    = BASE_DIR / "web"
OUTPUT_DIR = BASE_DIR / "output" / "games"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
BROWSER_PATH = r"C:\Users\Wilson\AppData\Local\Programs\Opera GX\opera.exe"


#### Functions ####

# Allow imports from 'core' and 'games' modules
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

# Loading utilities
def load_js(filename): 
    core_path = WEB_DIR / "main_engine.js"
    game_path = WEB_DIR / filename
    
    try:       
        with open(core_path, 'r', encoding='utf-8') as f:
            core_code = f.read()
        with open(game_path, 'r', encoding='utf-8') as f:
            game_code = f.read()
            
        return core_code + "\n" + game_code
    except FileNotFoundError as e:
        print(f"❌ ERROR: JS file not found: {e.filename}")
        return ""
    