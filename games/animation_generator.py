#### Imports ####

from pdfrw.objects.pdfname import PdfName
from pdfrw.objects.pdfdict import PdfDict
from core.main_engine import create_widget, create_page, add_renderer, create_mouse_tracker
from core.config import IMAGES_DIR, load_js


#### Variables ####

PAGE_WIDTH = 612
PAGE_HEIGHT = 792
CANVAS_WIDTH = 224
CANVAS_HEIGHT = 225
CANVAS_BASE = PAGE_HEIGHT - CANVAS_HEIGHT
BAR_WIDTH = 70 / 1.5
BAR_HEIGHT = 10 / 3
BAR_BASE_DISTANCE = CANVAS_BASE - 70 
BALL_WIDTH = 70 / 5
BALL_HEIGHT = 70 / 5


#### Functions ####

def build():

    # Dynamically builds a data dictionary from global constants, filtering primitive types for safe JavaScript injection.
    game_constants = {
        k: v for k, v in globals().items() 
        if k.isupper() and isinstance(v, (int, float, str))
    }

    fields = []

    # Character: Player Bar
    fields.append(create_widget(
        'bar',
        x=(CANVAS_WIDTH - BAR_WIDTH)/2, y=BAR_BASE_DISTANCE,
        width=BAR_WIDTH, height=BAR_HEIGHT,
        r=0.7, g=0.1, b=0, field_type="text"
    ))

    # Character: Enemy Ball
    fields.append(create_widget(
        'ball',
        x=(CANVAS_WIDTH - BAR_WIDTH) / 2, y=CANVAS_BASE + 30 / 4,
        width=BALL_WIDTH, height=BALL_HEIGHT,
        r=0.8, g=0, b=0.8, field_type="text"
    ))

    # Mouse Input Field
    create_mouse_tracker(
        fields_list=fields,
        x_start=65,
        count=197,
        y_start=CANVAS_BASE - 78,
        height=CANVAS_HEIGHT
    )

    # Renderer Field    
    add_renderer(fields, 65, CANVAS_BASE - 78, CANVAS_WIDTH, CANVAS_HEIGHT)

    # Load JS and assemble Template
    script_js = load_js('animation_generator.js')
    # Generate the page using the Engine
    page = create_page(fields, script_js, constants=game_constants)

    # Generator Configuration
    config = {
        "background": str(IMAGES_DIR / "ICSE_2026.jpg"),
        "width": PAGE_WIDTH,
        "height": PAGE_HEIGHT
    }

    return page, config