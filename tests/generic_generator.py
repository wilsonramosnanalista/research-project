#### Read-me ####
# -------------------------------------------------------------------------------------------
# File responsible for:
#       Specifying component dimensions for the PDF
#       Adding widgets (bar, ball, stripe, screen) to the PDF with pre-defined dimensions
#       Creating a PDF page embedding the JavaScript
#       Saving/Generating the PDF and opening it in the Opera browser
# -------------------------------------------------------------------------------------------

#### Imports ####

import os
import webbrowser
from pdfrw import PdfWriter

from main_engine import create_field, create_page


#### Component Dimensions ####

# Page
PAGE_WIDTH = 612
PAGE_HEIGHT = 792

# Canvas
CANVAS_WIDTH = 612
CANVAS_HEIGHT = 400
CANVAS_BASE = PAGE_HEIGHT - CANVAS_HEIGHT

# Ball
BALL_WIDTH = 70
BALL_HEIGHT = 70
BAR_WIDTH = 70

#### Add interactive fields (widgets) for the project to work ####
fields = []

# Ball
ball = create_field(
    'ball',
    x=(CANVAS_WIDTH - BAR_WIDTH)/2, y=CANVAS_BASE + 30,
    width=BALL_WIDTH, height=BALL_HEIGHT,
    r=0.8, g=0, b=0.8
)
fields.append(ball)

# Auxiliary field used for rendering in Chrome
# Flow: Displays a large white screen, redraws screen components (ball, bar), then hides the white screen
# Purpose: To refresh components on screen
fields.append(create_field(
    'renderer',
    x=0, y=0,
    width=PAGE_WIDTH, height=PAGE_HEIGHT,
    r=1, g=1, b=1
))


#### Read the main JavaScript ####
with open('generic_javascript.js', 'r') as js_file:
    script_js = js_file.read()


#### Embed JavaScript and global variables into the PDF page ####
page = create_page(fields, """

var PAGE_WIDTH = %(PAGE_WIDTH)s;
var PAGE_HEIGHT = %(PAGE_HEIGHT)s;
                   
var CANVAS_WIDTH = %(CANVAS_WIDTH)s;
var CANVAS_HEIGHT = %(CANVAS_HEIGHT)s;
var CANVAS_BASE = %(CANVAS_BASE)s;

var BAR_WIDTH = %(BAR_WIDTH)s;

var BALL_WIDTH = %(BALL_WIDTH)s;
var BALL_HEIGHT = %(BALL_HEIGHT)s;

%(script_js)s

""" % locals())


#### PDF generation steps and automatic opening in Opera ####
output = PdfWriter()
output.addpage(page)
output.write('game_new.pdf')

# Absolute path of the generated PDF
pdf_path = os.path.abspath("game_new.pdf")

# Opera browser path
opera_path = r"C:\Users\Wilson\AppData\Local\Programs\Opera GX\opera.exe"

try:
    # Register Opera as the browser
    webbrowser.register(
        "opera",
        None,
        webbrowser.BackgroundBrowser(opera_path)
    )

    # Open PDF in Opera GX
    webbrowser.get("opera").open_new(pdf_path)
    print("Demo game opened in Opera!")

except Exception as e:
    # If it fails, open in the default browser
    print("Could not open in Opera. Opening in default browser instead...")
    webbrowser.open_new(pdf_path)
