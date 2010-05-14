from util import the_stupid_fonts

# from http://code.google.com/p/py-dom-xpath/
import xpath

from xml.dom import minidom
from zipfile import ZipFile
from cStringIO import StringIO

# Global sentinels
INHERIT_CONVERT = object()
DONT_CONVERT = object()
NO_PARENT_STYLE = object()


def convert_doc(document_file):
    '''Given a filename or a file object of a ODT file (a zip file really)
    returns a converted file object'''

    file_in = ZipFile(document_file)
    styles = minidom.parse(file_in.open('styles.xml'))
    content = minidom.parse(file_in.open('content.xml'))

    style_mapping = {}
    convert_styles(styles, style_mapping)
    convert_styles(content, style_mapping)
    convert_content(content, style_mapping)

    # build a new odt file in memory
    fp = StringIO()
    file_out = ZipFile(fp, mode='w', compression=file_in.compression)
    for zinfo in file_in.infolist():
        name = zinfo.filename
        if name not in ('styles.xml', 'content.xml'):
            file_out.writestr(zinfo, file_in.read(zinfo))
    file_out.writestr('styles.xml', styles.toxml(encoding='utf8'))
    file_out.writestr('content.xml', content.toxml(encoding='utf8'))
    file_out.close()
    return fp

def convert_styles(tree, style_mapping):
    '''Iterates through all styles defined in the tree and extracts the
    convertor function to use for that style.

    The tree and style_mapping are changed inplace.
    '''
    context = xpath.XPathContext()
    context.namespaces['style'] = 'urn:oasis:names:tc:opendocument:xmlns:style:1.0'

    for style in context.find('//style:default-style|//style:style', tree):
        if style.tagName == 'style:default-style':
            style_name = style.getAttribute('style:family')
        else:
            style_name = style.getAttribute('style:name')
        parent_style_name = style.getAttribute('style:parent-style-name') or NO_PARENT_STYLE

        font = None
        font_xpath = './/style:text-properties[@style:font-name|@style:font-name-complex]'
        for text_properties in context.find(font_xpath, style):
            font = text_properties.getAttribute('style:font-name') \
                    or text_properties.getAttribute('style:font-name-complex')

        if font is None:
            if parent_style_name in style_mapping:
                # if the style has no font by itself but has a parent-style that
                # had the stupid font then just remember the style and use the
                # conversion from the parent style
                style_mapping[style_name] = style_mapping[parent_style_name]
            else:
                # no font-name, no parent-style in this style
                # the element will inherit the conversion from
                # it's parent in the content *tree*
                style_mapping[style_name] = INHERIT_CONVERT

        elif font in the_stupid_fonts:
            # if a stupid font is used in this style:
            #  - change the font in the style
            #  - and remember the style so that we can convert the text later
            text_properties.setAttribute('style:font-name', the_stupid_fonts[font].replacement_font)
            style_mapping[style_name] = the_stupid_fonts[font].convert_func
        else:
            # there's a font but not a stupid one, use null conversion
            style_mapping[style_name] = DONT_CONVERT
    return


def convert_content(tree, style_mapping):
    context = xpath.XPathContext()
    context.namespaces['office'] = 'urn:oasis:names:tc:opendocument:xmlns:office:1.0'

    text_path = '/office:document-content/office:body/office:text'
    body = context.findnode(text_path, tree)

    convert_body(body, style_mapping)

def convert_body(tree, style_mapping, inherited_convert=DONT_CONVERT):
    for child in tree.childNodes:
        if child.nodeType == tree.TEXT_NODE:
            if inherited_convert is not DONT_CONVERT:
                child.nodeValue = inherited_convert(child.nodeValue)
        else:
            style = child.getAttribute('text:style-name')
            if style in style_mapping:
                convert_func = style_mapping[style]
            else:
                convert_func = DONT_CONVERT

            if convert_func is INHERIT_CONVERT:
                convert_func = inherited_convert
            # recurse (depth-first) inside the tree
            convert_body(child, style_mapping, convert_func)
