from itertools import chain
from pathlib import Path
from typing import BinaryIO, Iterator, Union

from odf.element import Element, Text
from odf.opendocument import OpenDocument, load
from odf.style import Style, TextProperties

from .yuscii import the_stupid_fonts


# depth first iterator
def saxiter(node: Element) -> Iterator[Element]:
    """Return an interator over all elements reachable from node: later siblings and recursively all children."""
    while node:
        yield node
        if node.hasChildNodes():
            yield from saxiter(node.firstChild)  # type: ignore
        node = node.nextSibling  # type: ignore


def all_styles(doc: OpenDocument):
    return chain(
        doc.styles.getElementsByType(Style),
        doc.automaticstyles.getElementsByType(Style),
    )


def get_font_styles(doc: OpenDocument):
    """Retrieve all styles that define text properties with a font-name in the document.

    returns a dictionary of style-name -> font-name (lower-cased)
    """
    # TODO: cache the full style object
    styles_cache = {}
    for style in all_styles(doc):
        style_name = style.getAttribute("name")
        styles_cache |= {style_name: style}
        if (text_properties := style.getElementsByType(TextProperties)) and (
            font_name := text_properties[0].getAttribute("fontname")
        ):
            font_name = font_name.lower()
            yield style_name, font_name
        elif parent := style.getAttribute("parentstylename"):
            # FIXME: there can be multiple levels of parents
            # print(f"{style_name} -> {parent}")
            if parent in styles_cache:
                yield (
                    style.getAttribute("name"),
                    styles_cache[parent].getAttribute("fontname"),
                )
        else:
            # style with no parent-style, no text-properties or no fontname in the text-properties
            pass


def get_font_styles_to_convert(doc: OpenDocument):
    for style, font_name in get_font_styles(doc):
        if font_name in the_stupid_fonts:
            yield style, the_stupid_fonts[font_name]


def convert_styles(doc: OpenDocument) -> None:
    """
    Rewrite the styles that used to use the yuscii fonts, to use the replacement font.

    Mutates the document.
    """
    for style in all_styles(doc):
        if text_properties := style.getElementsByType(TextProperties):
            text_properties = text_properties[
                0
            ]  # there's only one TextProperties in style
            if font_name := text_properties.getAttribute("fontname"):
                font_name = font_name.lower()
                if conversion := the_stupid_fonts.get(font_name):
                    text_properties.setAttribute(
                        "fontname", conversion.replacement_font
                    )
                    # FIXME: maybe this part needs to be more carefull
                    # clean-up text-properties
                    for attr in "fontnamecomplex", "fontfamily", "fontfamilycomplex":
                        text_properties.setAttribute(attr, "")
                        text_properties.removeAttribute(attr)


def convert_document(doc: OpenDocument) -> None:
    """Find all text nodes using the specified font and replace them with unicode text.

    Mutates the document.
    """
    styles = dict(get_font_styles_to_convert(doc))

    for el in saxiter(doc.body):
        if el.__class__ is Text and el.parentNode.tagName.startswith("text:"):  # type: ignore[reportAttributeAccessIssue]
            # FIXME: we need to track the style of the parent text node too
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
