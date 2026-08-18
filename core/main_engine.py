#### Imports ####

import os
import io
import webbrowser
from pdfrw import PdfDict, PdfName, PdfArray, PdfReader, PdfWriter, PageMerge
from pdfrw.objects.pdfname import PdfName
from pdfrw.objects.pdfstring import PdfString
from pdfrw.objects.pdfdict import PdfDict
from pdfrw.objects.pdfarray import PdfArray
from reportlab.pdfgen import canvas
from pdfrw.objects.pdfname import PdfName
from pdfrw.objects.pdfdict import PdfDict


#### Functions ####

# Creates an interactive PDF field
def create_widget(name, x, y, width, height, r=1, g=1, b=1, opaque=None, field_type="text", **kwargs):
    
    # Automatically sets default opacity based on field type (icons transparent, text fields opaque)
    if opaque is None:        
        opaque = False if field_type == "button" else True

    widget = PdfDict(
        Type=PdfName.Annot,
        Subtype=PdfName.Widget,
        T=PdfString.encode(name),
        Rect=PdfArray([x, y, x + width, y + height]),
        MK=PdfDict(BG=PdfArray([r, g, b]) if opaque else PdfArray([])) # Controls field background transparency via annotation settings (empty background removes fill)
    )

    # TEXT
    if field_type == "text":
        widget.FT = PdfName.Tx
        widget.V = PdfString.encode(kwargs.get("value", ""))
        widget.MaxLen = kwargs.get("maxlen", 160)
        
        multiline = kwargs.get("multiline", False)
        align = kwargs.get("align", 0)#
        readonly = kwargs.get("readonly", False)

        if multiline:
            widget.Ff = 4096
        elif readonly:
            widget.Ff = 1
        else:
            widget.Ff = kwargs.get("ff", 2)
            
        if align != 0:
            widget.Q = align
            
        if opaque:
            widget.AP = PdfDict(N=PdfDict(
                Type=PdfName.XObject, Subtype=PdfName.Form, FormType=1,
                BBox=PdfArray([0, 0, width, height]),
                stream="%f %f %f rg 0 0 %f %f re f" % (r, g, b, width, height)
            ))
        
        # Abstracts font styling by dynamically building the native PDF Default Appearance (/DA) string
        font_name = kwargs.get("font", "Cour")
        font_size = kwargs.get("size", 22)
        text_color = kwargs.get("text_color", "1 1 1")
        
        da_string = f"/{font_name} {font_size} Tf {text_color} rg"
        widget.DA = PdfString.encode(da_string)
        
        on_key_stroke = kwargs.get("on_key_stroke")
        if on_key_stroke:
            # Binds JS action to native /AA /K keystroke event
            widget.AA = PdfDict(K=create_js_action(on_key_stroke))

    # BUTTON
    elif field_type == "button":
        widget.FT = PdfName.Btn
        widget.Ff = 65536  # PushButton        
        icon_path = kwargs.get("icon_path")

        # ICON
        if icon_path:
            icon_xobject = _get_icon_xobject(icon_path, width, height)            
            widget.MK.BG = PdfArray([]) 
            widget.MK.I = icon_xobject
            widget.MK.TP = 1             
            widget.AP = PdfDict(N=PdfDict(
                Type=PdfName.XObject, Subtype=PdfName.Form,
                BBox=PdfArray([0, 0, width, height]),
                Resources=PdfDict(XObject=PdfDict(im0=icon_xobject)),
                stream="q /im0 Do Q"
            ))
        
        # TEXT BUTTON
        label = kwargs.get("label")
        if label:
            widget.TU = PdfString.encode(label)
            widget.MK.CA = PdfString.encode(label)
            
        # Sets the default font type, size, and text color for push buttons
        widget.DA = "/Cour 18 Tf 0 0 0 rg"            
       
        js_action = kwargs.get("js_action")
        if js_action:
            # Buttons use direct /A key without passing through /AA
            widget.A = create_js_action(js_action)
    
    return widget

# Loads an image and converts it into a PDF-compatible format so it can be embedded in the document
def _get_icon_xobject(path, w, h):
    if not os.path.exists(path): raise FileNotFoundError(path)

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=(w, h))
    c.drawImage(path, 0, 0, width=w, height=h, mask='auto')
    c.save()
    buffer.seek(0)
    img_page = PdfReader(buffer).pages[0]
    xobj_name = list(img_page.Resources.XObject.keys())[0]

    return img_page.Resources.XObject[xobj_name]

# Renderer Field: auxiliary full-page text field used to force screen refresh/redraw
def add_renderer(fields, x, y, width, height):    
    renderer = create_widget(
        name='renderer',
        x=x,
        y=y,
        width=width,
        height=height,
        r=1, g=1, b=1,
        field_type="text"
    )
    fields.append(renderer)
    return renderer

# Generates a PDF-compatible page script by dynamically injecting game constants into the JavaScript engine
def create_page(fields, js_script, page_width, page_height, constants=None):
    js_variables = ""
    
    if constants:
        for key, value in constants.items():
            # Formats values with proper JavaScript syntax depending on their data type
            if isinstance(value, str):
                js_variables += f'var {key} = "{value}";\n'
            else:
                js_variables += f"var {key} = {value};\n"

    full_js_code = js_variables + js_script

    # Injects telemetry widgets
    create_fps_counter(fields)
    create_latency_counter(fields)

    # Initializes a standard native PDF Page object with structural resources and dimensions
    page = PdfDict()
    page.Type = PdfName.Page
    page.Resources = PdfDict()
    page.Resources.Font = PdfDict()
    page.Resources.Font.F1 = PdfDict()
    page.Resources.Font.F1.Type = PdfName.Font
    page.Resources.Font.F1.Subtype = PdfName.Type1
    page.Resources.Font.F1.BaseFont = PdfName.Helvetica

    # Defines the page dimensions according to the parameters provided
    page.MediaBox = PdfArray([0, 0, page_width, page_height])

    page.Contents = PdfDict()
    page.Contents.stream = """
        BT
        /F1 24 Tf
        ET
        """

    # Pass True to inject runtime error handling natively
    page.AA = PdfDict(O=create_js_action(full_js_code, with_try_catch=True))
    page.Annots = PdfArray(fields)

    return page

#Factory function that encapsulates raw JavaScript strings into native PDF JavaScript Action dictionaries, with optional try-catch routing.
def create_js_action(js_code, with_try_catch=False):   
    if with_try_catch:
        js_code = f"try {{\n{js_code}\n}} catch (e) {{ app.alert(e.message); }}"
        
    return PdfDict(
        S=PdfName.JavaScript,
        JS=PdfString.encode(js_code)
    )

# Insert an image into a PDF at a specific position
def insert_image(input_pdf, image_path, width, height, x=0, y=0):
    pdf_temp = "_temp_imagem.pdf"
    c = canvas.Canvas(pdf_temp, pagesize=(612, 792))
    c.drawImage(image_path, x, y, width=width, height=height, mask='auto')
    c.showPage()
    c.save()

    base = PdfReader(input_pdf)
    imagem = PdfReader(pdf_temp)

    PageMerge(base.pages[0]).add(imagem.pages[0]).render()   
    PdfWriter().write(input_pdf, base)
    if os.path.exists(pdf_temp):
        os.remove(pdf_temp)

# Open a PDF in a specified or default browser
def open_PDF_in_browser(pdf_path, browser_path=None):
    pdf_url = f"file:///{os.path.abspath(pdf_path)}".replace("\\", "/")
    
    try:
        if browser_path and os.path.exists(browser_path):
            webbrowser.register(
                "custom_browser", 
                None, 
                webbrowser.BackgroundBrowser(browser_path)
            )
            webbrowser.get("custom_browser").open_new(pdf_url)
        else:
            webbrowser.open_new(pdf_url)
            
    except Exception as e:
        print(f"❌ ERROR: Opening Browser: {e}. Trying default system browser!")
        webbrowser.open(pdf_url)

#
#   Abstracts the creation of invisible vertical target fields across the canvas 
#   to track the mouse X-coordinate and stream it into the PDF's global JavaScript scope.
#
def create_mouse_tracker(fields_list, x_start, count, y_start, height, width_per_stripe=1):

    for idx in range(count):
        current_x = x_start + (idx * width_per_stripe)
        
        stripe = create_widget(
            name=f"stripe_{current_x}",
            x=current_x,
            y=y_start,
            width=width_per_stripe,
            height=height,
            r=0, g=1, b=0,
            field_type="text",
            opaque=False
        )        
        stripe.Ff = 1 
        
        # Injects the coordinate tracking script into the native PDF Additional Actions (/AA) on Mouse Enter (/E)
        js_code = f"global.mouseX = {current_x};"
        
        stripe.AA = PdfDict(
            E=PdfDict(
                S=PdfName.JavaScript,
                JS=js_code
            )
        )        
        fields_list.append(stripe)

# Creates a FPS widget
def create_fps_counter(fields_list, page_width=612):    
    fps_field = create_widget(
        name="fps_counter",
        x=page_width - 45,
        y=355,
        width=42,
        height=15,
        r=1, g=1, b=1,
        opaque=True,
        field_type="text",
        value="FPS: --",
        readonly=True,
        font="Helv",
        size=10,
        text_color="0 0 0"
    )
    fields_list.append(fps_field)

# Creates a Latency widget
def create_latency_counter(fields_list, page_width=612):    
    latency_field = create_widget(
        name="latency_counter",
        x=page_width - 45,
        y=338,
        width=42,
        height=15,
        r=1, g=1, b=1,
        opaque=True,
        field_type="text",
        value="LAT: --",
        readonly=True,
        font="Helv",
        size=10,
        text_color="0 0 0"
    )    
    fields_list.append(latency_field)