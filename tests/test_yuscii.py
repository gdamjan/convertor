from convertor.yuscii import variant1, variant2, variant3

cyrillics_lower = "абвгдѓежзѕијклљмнњопрстќуфхцчџш"
cyrillics_upper = cyrillics_lower.upper()
cyrillics = cyrillics_lower + cyrillics_upper


def test_cyrillic_constant_length():
    assert len(cyrillics_lower) == 31


def test_cyrillic_constant_all_lowercase():
    assert all(map(lambda c: c.islower(), cyrillics_lower))


def test_cyrillic_constant_all_uppercase():
    assert all(map(lambda c: c.isupper(), cyrillics_upper))


def test_cyrillic_constant_uniqueness():
    assert len(set(cyrillics_lower)) == len(cyrillics_lower) == len(set(cyrillics_upper))


def test_variants_lengths():
    """Each variant must have all macedonian cyrillic letters, small and CAPITAL"""
    for v in (variant1, variant2, variant3):
        assert len(v) == 62


def test_variant_values():
    """Each variant must cover all cyrillic characters, small and CAPITAL"""
    for v in (variant1, variant2, variant3):
        chars = set(chr(c) for c in v.values())
        assert chars == set(cyrillics)


unicode_pangram = "Желката Љуба музицира на харфа читајќи го Његош, а песот Ѓоше се џари во ѕвезди."


def test_pangram_is_complete():
    """The pangram for testing needs to have all the characters of the macedonian cyrillic alphabet"""
    # remove non-alpha chars, spaces and punctuation
    test_chars = "".join(c for c in unicode_pangram if c.isalpha())
    assert set(test_chars.lower()) == set(cyrillics_lower)
    assert set(test_chars.upper()) == set(cyrillics_upper)


def test_variant1():
    yuscii_text = r"@elkata Quba muzicira na harfa ~itaj}i go Wego{, a pesot \o{e se xari vo yvezdi."
    assert yuscii_text.translate(variant1) == unicode_pangram


def test_variant2():
    yuscii_text = r"@elkata Quba muzicira na harfa ~itaj]i go Wego[, a pesot |o[e se xari vo yvezdi."
    assert yuscii_text.translate(variant2) == unicode_pangram


def test_variant3():
    yuscii_text = r"@elkata Quba muzicira na harfa ;itaj]i go Wego[, a pesot |o[e se xari vo yvezdi."
    assert yuscii_text.translate(variant3) == unicode_pangram
