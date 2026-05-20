#### Imports ####

from pdfrw import PdfWriter
from core.main_engine import insert_image


#### Functions ####

# Generates the game inside the PDF
def generate_game(game_builder, output_path):
    page, config = game_builder()    
    writer = PdfWriter()
    writer.addpage(page)
    writer.write(output_path)    

    # Adds Background Layer
    if "background" in config:
        insert_image(
            output_path, 
            config["background"], 
            config.get("width", 612), 
            config.get("height", 792),
            x=0, y=0
        )

    # Inserts any additional dynamic assets defined in the game configuration
    if "assets" in config:
        for asset in config["assets"]:
            insert_image(
                output_path,
                asset["path"],
                width=asset["width"],
                height=asset["height"],
                x=asset["x"],
                y=asset["y"]
            )