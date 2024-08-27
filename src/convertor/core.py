from odf.opendocument import load
from odf.text import P, Span
from odf.style import Style, TextProperties

from .util import the_stupid_fonts


def get_font_styles(doc):
    """Retrieve all styles that define text properties in the document."""
    styles = {}
    for style in doc.styles.childNodes:
        if isinstance(style, Style):  # type: ignore
            text_properties = style.getElementsByType(TextProperties)
            if text_properties:
                font_name = text_properties[0].getAttribute("fontname")
                if font_name:
                    styles[style.getAttribute("name")] = font_name
    return styles


def convert_text_nodes(doc):
    """Find all text nodes using the specified font and replace them with uppercase text."""
    styles = get_font_styles(doc)

    for paragraph in doc.getElementsByType(P):
        for span in paragraph.getElementsByType(Span):
            style_name = span.getAttribute("stylename")

            if not style_name:
                return
            if not (orig_font := styles.get(style_name)):
                return
            if orig_font.lower() in the_stupid_fonts:
                orig_text = span.text
                conversion = the_stupid_fonts[orig_font]
                span.text = conversion.convert(orig_text)
                style_element = doc.styles.getElementsByType(Style, name=style_name)[0]
                text_properties = style_element.getElementsByType(TextProperties)[0]
                text_properties.setAttribute("fontname", conversion.target_font)


def convert_document(file, output_filename):
    # Load the ODT document
    doc = load(file)

    # Replace all text using the Arial font with its uppercase version
    convert_text_nodes(doc)

    # Save the modified document
    doc.save(output_filename)
