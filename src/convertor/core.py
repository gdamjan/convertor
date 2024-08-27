from itertools import chain
from pathlib import Path
from typing import BinaryIO, Iterator, Union

from odf.element import Element, Text
from odf.opendocument import load
from odf.style import Style, TextProperties

from .util import the_stupid_fonts


# depth first iterator
def saxiter(node: Element) -> Iterator[Element]:
    """Return an interator over all elements reachable from node: later siblings and recursively all children."""
    while node:
        yield node
        if node.hasChildNodes():
            yield from saxiter(node.firstChild)  # type: ignore
        node = node.nextSibling  # type: ignore


def all_styles(doc):
    return chain(
        doc.styles.getElementsByType(Style),
        doc.automaticstyles.getElementsByType(Style),
    )


def get_font_styles(doc):
    """Retrieve all styles that define text properties with a font-name in the document.

    returns a dictionary of style-name -> font-name (lower-cased)
    """
    for style in all_styles(doc):
        if text_properties := style.getElementsByType(TextProperties):
            if font_name := text_properties[0].getAttribute("fontname"):
                yield style.getAttribute("name"), font_name


def filter_font_styles_to_convert(doc):
    for style, font_name in get_font_styles(doc):
        font_name = font_name.lower()
        if font_name in the_stupid_fonts:
            yield style, the_stupid_fonts[font_name]


def convert_styles(doc):
    for style in all_styles(doc):
        if text_properties := style.getElementsByType(TextProperties):
            text_properties = text_properties[
                0
            ]  # there's only one TextProperties in style
            if font_name := text_properties.getAttribute("fontname"):
                if conversion := the_stupid_fonts.get(font_name.lower()):
                    text_properties.setAttribute("fontname", conversion.target_font)


def convert_document(doc) -> None:
    """Find all text nodes using the specified font and replace them with unicode text.

    Mutates the document, so returns None.
    """

    styles = dict(filter_font_styles_to_convert(doc))

    for el in saxiter(doc.body):
        if el.__class__ is Text:
            style = el.parentNode.getAttribute("stylename")  # type: ignore
            if conversion := styles.get(style):
                el.data = conversion.convert(el.data)  # type: ignore

    convert_styles(doc)


def convert_file(
    file: Union[str, BinaryIO, Path], output_filename: Union[str, Path]
) -> None:
    doc = load(file)
    convert_document(doc)
    doc.save(output_filename)
