from odf.opendocument import load
from odf.text import P, Span
from odf.style import Style, TextProperties

def get_font_styles(doc):
    """Retrieve all styles that define text properties in the document."""
    styles = {}
    for style in doc.styles.childNodes:
        if isinstance(style, Style):
            text_properties = style.getElementsByType(TextProperties)
            if text_properties:
                font_name = text_properties[0].getAttribute("fontname")
                if font_name:
                    styles[style.getAttribute("name")] = font_name
    return styles

def find_text_nodes_with_font(doc, target_font):
    """Find all text nodes using the specified font."""
    styles = get_font_styles(doc)
    matching_texts = []

    for paragraph in doc.getElementsByType(P):
        for span in paragraph.getElementsByType(Span):
            style_name = span.getAttribute("stylename")
            if style_name and styles.get(style_name) == target_font:
                matching_texts.append(span.text)

    return matching_texts

# Load the ODT document
doc = load("your_document.odt")

# Find all text nodes using the Arial font
arial_texts = find_text_nodes_with_font(doc, "Arial")

# Print the results
for text in arial_texts:
    print(text)

