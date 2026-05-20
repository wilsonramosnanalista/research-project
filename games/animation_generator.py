#### Imports ####

from pdfrw.objects.pdfname import PdfName
from pdfrw.objects.pdfdict import PdfDict
from core.main_engine import create_widget, create_page, add_renderer
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
    for x in range(0, 197):
        stripe = create_widget(
            'stripe' + str(x),        
            x = 65 + x,
            y = CANVAS_BASE - 78,
            width = 1,
            height = CANVAS_HEIGHT,
            r = 0, g = 1, b = 0, 
            field_type="text", opaque=False
        )
        # Event: Update global mouse coordinate on enter
        stripe.AA = PdfDict(E=PdfDict(S=PdfName.JavaScript, JS=f"global.mouseX = {65 + x};"))
        fields.append(stripe)

    # Renderer Field    
    add_renderer(fields, 65, CANVAS_BASE - 78, CANVAS_WIDTH, CANVAS_HEIGHT)

    # Load JS and assemble Template
    script_js = load_js('animation_generator.js')
    
    js_template = """
    var PAGE_HEIGHT = %(PAGE_HEIGHT)s;
    var CANVAS_WIDTH = %(CANVAS_WIDTH)s;
    var CANVAS_HEIGHT = %(CANVAS_HEIGHT)s;
    var CANVAS_BASE = %(CANVAS_BASE)s;
    var BAR_WIDTH = %(BAR_WIDTH)s;
    var BAR_HEIGHT = %(BAR_HEIGHT)s;
    var BAR_BASE_DISTANCE = %(BAR_BASE_DISTANCE)s;
    var BALL_WIDTH = %(BALL_WIDTH)s;
    var BALL_HEIGHT = %(BALL_HEIGHT)s;
    %(script_js)s
    """ % {
        "PAGE_HEIGHT": PAGE_HEIGHT,
        "CANVAS_WIDTH": CANVAS_WIDTH,
        "CANVAS_HEIGHT": CANVAS_HEIGHT,
        "CANVAS_BASE": CANVAS_BASE,
        "BAR_WIDTH": BAR_WIDTH,
        "BAR_HEIGHT": BAR_HEIGHT,
        "BAR_BASE_DISTANCE": BAR_BASE_DISTANCE,
        "BALL_WIDTH": BALL_WIDTH,
        "BALL_HEIGHT": BALL_HEIGHT,
        "script_js": script_js
    }

    # Generate the page using the Engine
    page = create_page(fields, js_template)

    # Generator Configuration
    config = {
        "background": str(IMAGES_DIR / "ICSE_2026.jpg"),
        "width": PAGE_WIDTH,
        "height": PAGE_HEIGHT
    }

    return page, config