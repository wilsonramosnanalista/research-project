#### Imports ####

from pdfrw.objects.pdfname import PdfName
from pdfrw.objects.pdfstring import PdfString
from pdfrw.objects.pdfdict import PdfDict
from pdfrw.objects.pdfarray import PdfArray
from core.main_engine import create_page, create_widget, add_renderer, create_mouse_tracker
from core.config import IMAGES_DIR, load_js


#### Variables ####

PAGE_WIDTH = 612
PAGE_HEIGHT = 792
CANVAS_WIDTH = 612
CANVAS_HEIGHT = 400
CANVAS_BASE = PAGE_HEIGHT - CANVAS_HEIGHT
BAR_WIDTH = 70
BAR_HEIGHT = 10
BAR_BASE_DISTANCE = CANVAS_BASE + 10
BALL_WIDTH = 70
BALL_HEIGHT = 70


#### Functions ####

def build():

    # Dynamically builds a data dictionary from global constants, filtering primitive types for safe JavaScript injection.
    game_constants = {
        k: v for k, v in globals().items() 
        if k.isupper() and isinstance(v, (int, float, str))
    }

    fields = []

    # Character: Game Bar
    bar = create_widget(
        name='bar',
        x=(CANVAS_WIDTH - BAR_WIDTH) / 2,
        y=BAR_BASE_DISTANCE,
        width=BAR_WIDTH,
        height=BAR_HEIGHT,
        r=0.7, g=0.1, b=0
    )
    fields.append(bar)

    # Character: Enemy
    ball = create_widget(
        name='ball',
        x=(CANVAS_WIDTH - BAR_WIDTH) / 2,
        y=CANVAS_BASE + 30,
        width=BALL_WIDTH,
        height=BALL_HEIGHT,
        r=0.8, g=0, b=0.8
    )
    fields.append(ball)

    # Score Field
    scoreArea = create_widget(
        name='scoreArea',
        x=231,
        y=746,
        width=130,
        height=36,
        r=0.9, g=0.9, b=0.9,
        opaque=False
    )
    fields.append(scoreArea)

    # Mouse Input Field
    create_mouse_tracker(
        fields_list=fields,
        x_start=0,
        count=CANVAS_WIDTH,
        y_start=0,
        height=CANVAS_BASE
    )

    # Mouse Instruction
    mouseWarning = create_widget(
        name='mouseWarning',
        x=0,
        y=0,
        width=CANVAS_WIDTH,
        height=CANVAS_HEIGHT - 10,
        r=0.9, g=0.9, b=0.9,
        opaque=False,
        multiline=True,
        align=1
    )    
    fields.append(mouseWarning)   

    # Renderer Field
    add_renderer(fields, 0, CANVAS_BASE, CANVAS_WIDTH, CANVAS_HEIGHT)
    
    # Start Screen Overlay
    start_screen = create_widget(
        name='start_screen',
        x=0,
        y=0,
        width=CANVAS_WIDTH,
        height=CANVAS_HEIGHT,
        r=1, g=1, b=1,
        opaque=True,
        readonly=True
    )
    fields.append(start_screen)

    # Button: New Game
    newGameButton = create_widget(
        name="newGameButton",
        x=CANVAS_WIDTH / 2 - 60,
        y=PAGE_HEIGHT / 1.5 - 20,
        width=120,
        height=45,
        r=0.8, g=0.8, b=0.8,
        opaque=True,
        field_type="button",
        label="New Game",
        js_action="onNewGameClick()"
    )
    fields.append(newGameButton)
    
    # JavaScript loading and setup
    script_js = load_js('game_demo.js')
    
    # Creates the page linking widgets to the JavaScript logic
    page = create_page(fields, script_js, constants=game_constants)

    # Rendering Configuration: background and dimensions
    config = {
        "background": str(IMAGES_DIR / "background_space.png"),
        "width": PAGE_WIDTH,
        "height": PAGE_HEIGHT
    }

    return page, config