#### Imports ####

from pdfrw.objects.pdfname import PdfName
from pdfrw.objects.pdfstring import PdfString
from pdfrw.objects.pdfdict import PdfDict
from pdfrw.objects.pdfarray import PdfArray
from core.main_engine import create_js_action, create_page, create_widget, add_renderer
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
    fields = []

    # Character: Game Bar
    bar = create_widget(
        name='bar',
        x=(CANVAS_WIDTH - BAR_WIDTH) / 2,
        y=BAR_BASE_DISTANCE,
        width=BAR_WIDTH,
        height=BAR_HEIGHT,
        r=0.7, g=0.1, b=0,
        field_type="text"
    )
    fields.append(bar)

    # Character: Enemy
    ball = create_widget(
        name='ball',
        x=(CANVAS_WIDTH - BAR_WIDTH) / 2,
        y=CANVAS_BASE + 30,
        width=BALL_WIDTH,
        height=BALL_HEIGHT,
        r=0.8, g=0, b=0.8,
        field_type="text"
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
        opaque=False,
        field_type="text",
        value=""
    )
    scoreArea.DA = PdfString.encode("/Cour 22 Tf 1 1 1 rg")
    fields.append(scoreArea)

    # Mouse Input Field
    for x in range(0, CANVAS_WIDTH):
        stripe = create_widget(
            name='stripe' + str(x),
            x=x,
            y=0,
            width=1,
            height=CANVAS_BASE,
            r=0, g=1, b=0,
            field_type="text"
        )
        stripe.Ff = 1
        # Event: Update global mouse coordinate on enter
        stripe.AA = PdfDict()
        stripe.AA.E = create_js_action(f"global.mouseX = {x};")
        fields.append(stripe)

    # Mouse Instruction
    mouseWarning = create_widget(
        name='mouseWarning',
        x=0,
        y=0,
        width=CANVAS_WIDTH,
        height=CANVAS_HEIGHT - 10,
        r=0.9, g=0.9, b=0.9,
        opaque=False,
        field_type="text",
        value=""
    )
    mouseWarning.DA = PdfString.encode("/Cour 22 Tf 1 1 1 rg")
    mouseWarning.Q = 1          # Center alignment
    mouseWarning.Ff = 4096      # Multiline
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
        field_type="text",
        value=""
    )
    start_screen.Ff = 1  # ReadOnly
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
        field_type="button"
    )
    newGameButton.TU = PdfString.encode("New Game")
    newGameButton.MK.CA = PdfString.encode("New Game")
    newGameButton.DA = "/Cour 18 Tf 0 0 0 rg"
    newGameButton.A = PdfDict(
        S=PdfName.JavaScript,
        JS=PdfString.encode("onNewGameClick()")
    )
    fields.append(newGameButton)

    # Static Instruction Label
    instruction = create_widget(
        name="instruction",
        x=10,
        y=CANVAS_HEIGHT / 1.25,
        width=440,
        height=20,
        r=1, g=1, b=1,
        field_type="text",
        opaque=True,
        value=""
    )
    instruction.Ff = 1  # ReadOnly
    instruction.AP = PdfDict()
    appearance = instruction.AP.N = PdfDict()
    appearance.Type = PdfName.XObject
    appearance.Subtype = PdfName.Form
    appearance.FormType = 1
    appearance.BBox = PdfArray([0, 0, 440, 20])
    appearance.stream = """
    q
    1 1 1 rg
    0 0 440 20 re f
    BT
    /Helv-BoldOblique 12 Tf
    0 0 0 rg
    10 5 Td
    (*Version 1.0 - Tested and functional in Chrome or Opera!) Tj
    ET
    Q
    """
    fields.append(instruction)

    # JavaScript loading and setup
    script_js = load_js('game_demo.js')
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

    # Creates the page linking widgets to the JavaScript logic
    page = create_page(fields, js_template)

    # Rendering Configuration: background and dimensions
    config = {
        "background": str(IMAGES_DIR / "background_space.png"),
        "width": PAGE_WIDTH,
        "height": PAGE_HEIGHT
    }

    return page, config