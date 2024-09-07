from pathlib import Path

import pytest
from odf.opendocument import load

from convertor.convert_odf import convert_document, get_font_styles

unicode_pangram = (
    "Желката Љуба музицира на харфа читајќи го Његош, а песот Ѓоше се џари во ѕвезди."
)


@pytest.fixture
def simple_example():
    example_file = Path(__file__).parent / "fixtures" / "simple-example.odt"
    doc = load(example_file)
    return doc


def test_simple_num_styles(simple_example):
    styles = dict(get_font_styles(simple_example))
    assert len(styles) == 2


def test_simple_baseline(simple_example):
    """
    simple-example.odt has the macedonian pangram twice, once in proper unicode, another time in "mac c swiss"
    """
    xml = simple_example.contentxml()
    assert xml.count(unicode_pangram.encode("utf-8")) == 1


def test_simple_conversion(simple_example):
    """
    after the conversion, it should match twice
    """
    convert_document(simple_example)
    xml = simple_example.contentxml()
    assert xml.count(unicode_pangram.encode("utf-8")) == 2
