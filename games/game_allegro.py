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
    keyboard_input = create_widget(
        "keyboard_input",
        x=(CANVAS_WIDTH - 100) / 2 - 7.5, 
        y=CANVAS_HEIGHT - 25,
        width=115, height=30, 
        r=0.8, g=0.8, b=0.2,
        field_type="text",
        value="Click here to play!", # (WASD)",
        maxlen=0 # Allows unlimited typing
    )
    keyboard_input.DA = PdfString.encode("/Helv 14 Tf 0 0 0 rg")
    keyboard_input.AA = PdfDict(K=PdfDict(S=PdfName.JavaScript, JS=PdfString.encode("handle_input(event);"))) # Binds JavaScript key event handler
    fields.append(keyboard_input)

    # Score Field
    score_field = create_widget(
        "score_field",
        x=85, y=PAGE_HEIGHT - 33,
        width=60, height=30,
        r=0, g=0, b=0,
        opaque=False,
        field_type="text",
        value="0"
    )
    score_field.Ff = 1 # ReadOnly
    score_field.DA = PdfString.encode("/HeBo 20 Tf 1 1 1 rg")
    fields.append(score_field)
 
    # Renderer Field 
    add_renderer(fields, 0, 0, PAGE_WIDTH, PAGE_HEIGHT)
    
    # JavaScript loading and setup
    script_js = load_js('game_allegro.js')    
    js_template = """
    var PAGE_WIDTH = %(PAGE_WIDTH)s;
    var PAGE_HEIGHT = %(PAGE_HEIGHT)s;
    var CANVAS_WIDTH = %(CANVAS_WIDTH)s;
    var CANVAS_HEIGHT = %(CANVAS_HEIGHT)s;
    var CANVAS_BASE = %(CANVAS_BASE)s;
    var FARME_WORKER_WIDTH = %(FARME_WORKER_WIDTH)s;
    var FARME_WORKER_HEIGHT = %(FARME_WORKER_HEIGHT)s;
    var APPLE_WIDTH = %(APPLE_WIDTH)s;
    var APPLE_HEIGHT = %(APPLE_HEIGHT)s;
    %(script_js)s
    """ % {
        "PAGE_WIDTH": PAGE_WIDTH, "PAGE_HEIGHT": PAGE_HEIGHT,
        "CANVAS_WIDTH": CANVAS_WIDTH, "CANVAS_HEIGHT": CANVAS_HEIGHT,
        "CANVAS_BASE": CANVAS_BASE, "FARME_WORKER_WIDTH": FARME_WORKER_WIDTH,
        "FARME_WORKER_HEIGHT": FARME_WORKER_HEIGHT, "APPLE_WIDTH": APPLE_WIDTH,
        "APPLE_HEIGHT": APPLE_HEIGHT, "script_js": script_js
    }

    # Creates the page linking widgets to the JavaScript logic
    page = create_page(fields, js_template)

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