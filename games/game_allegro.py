#### Imports ####

from pdfrw.objects.pdfname import PdfName
from pdfrw.objects.pdfstring import PdfString
from pdfrw.objects.pdfdict import PdfDict
from pdfrw import PdfArray
from core.main_engine import create_widget, create_page, add_renderer
from core.config import IMAGES_DIR, load_js

#### Variables ####

PAGE_WIDTH = 612
PAGE_HEIGHT = 792
CANVAS_WIDTH = 612
CANVAS_HEIGHT = 400
CANVAS_BASE = PAGE_HEIGHT - CANVAS_HEIGHT
FARME_WORKER_WIDTH = 35
FARME_WORKER_HEIGHT = 35
APPLE_WIDTH = 35
APPLE_HEIGHT = 35


#### Functions ####

def build():

    # Dynamically builds a data dictionary from global constants, filtering primitive types for safe JavaScript injection.
    game_constants = {
        k: v for k, v in globals().items() 
        if k.isupper() and isinstance(v, (int, float, str))
    }

    fields = []

    # Character: Farmer Worker
    fields.append(create_widget(
        "farmer_worker", 
        x=(CANVAS_WIDTH - FARME_WORKER_WIDTH) / 4, 
        y=CANVAS_HEIGHT + 100,
        width=FARME_WORKER_WIDTH,
        height=FARME_WORKER_HEIGHT,
        field_type="button",
        icon_path=str(IMAGES_DIR / "worker.png")
    ))

    # Item: Apple
    fields.append(create_widget(
        "apple", 
        x=(CANVAS_WIDTH - FARME_WORKER_WIDTH) / 4, 
        y=CANVAS_HEIGHT + 100,
        width=APPLE_WIDTH,
        height=APPLE_HEIGHT,
        field_type="button",
        icon_path=str(IMAGES_DIR / "apple.png")
    ))

    # Keyboard Input Field
    fields.append(create_widget(
        "keyboard_input",
        x=(CANVAS_WIDTH - 100) / 2 - 7.5, 
        y=CANVAS_HEIGHT - 25,
        width=115, height=30, 
        r=0.8, g=0.8, b=0.2,
        value="Click here to play!",
        maxlen=0,
        font="Helv",
        size=14,
        text_color="0 0 0",
        on_key_stroke="handle_input(event);"
    ))
    
    # Score Field
    fields.append(create_widget(
        "score_field",
        x=85, y=PAGE_HEIGHT - 33,
        width=60, height=30,
        r=0, g=0, b=0,
        opaque=False,
        value="0",
        readonly=True,
        font="HeBo",
        size=20,
        text_color="1 1 1"
    ))
   
    # Renderer Field 
    add_renderer(fields, 0, 0, PAGE_WIDTH, PAGE_HEIGHT)
    
    # JavaScript loading and setup
    script_js = load_js('game_allegro.js')
    
    # Creates the page linking widgets to the JavaScript logic
    page = create_page(fields, script_js, constants=game_constants)

    # Rendering Configuration: background, score overlay, and dimensions
    config = {
        "background": str(IMAGES_DIR / "background_grass.jpg"),
        "width": PAGE_WIDTH,
        "height": PAGE_HEIGHT,
        "assets": [
            {
                "path": str(IMAGES_DIR / "score_label.png"),
                "width": 80, "height": 22, "x": 5, "y": 764
            },
            {
                "path": str(IMAGES_DIR / "keyboard_wasd.png"),
                "width": 125, "height": 83.9, "x": 243.5, "y": 250
            }
        ]
    }

    return page, config