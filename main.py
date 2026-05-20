#### Imports ####

import sys
import pkgutil
import importlib
import games
from core.generator import generate_game
from core.config import BROWSER_PATH # Nome atualizado
from core.main_engine import open_PDF_in_browser


#### Variables ####

# Dictionary {'game': 'path_game'} from the /games directory
GAMES = {
    name: f"games.{name}"
    for _, name, _ in pkgutil.iter_modules(games.__path__)
}
print("✅ DEBUG: Available games:", list(GAMES.keys()))


#### Main Function ####

def main():

    game_key = sys.argv[1].lower()  # Retrieves the game name typed in the terminal

    if game_key not in GAMES:
        print(f"❌ ERROR: The game '{game_key}' was not found.")
        return

    module = importlib.import_module(GAMES[game_key])  # Dynamically loads only the requested game module
    pdf_path = f"output/games/{game_key}.pdf"

    generate_game(module.build, pdf_path)
    print(f"✅ SUCCESS: {game_key.capitalize()} generated at: {pdf_path}")

    # Opens the PDF in the configured browser (or the system default if not specified)
    open_PDF_in_browser(pdf_path, BROWSER_PATH)
    print("✅ Game opened in the browser!")

if __name__ == "__main__":
    main() # Runs main() only when the file is executed directly (not when imported)