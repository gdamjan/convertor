from convertor.yuscii import the_stupid_fonts

unicode_pangram = "Желката Љуба музицира на харфа читајќи го Његош, а песот Ѓоше се џари во ѕвезди."


def test_mac_c_swiss():
    yuscii_text = r"@elkata Quba muzicira na harfa ~itaj}i go Wego{, a pesot \o{e se xari vo yvezdi."
    yuscii_font = "mac c swiss"

    conversion = the_stupid_fonts[yuscii_font]
    assert conversion.convert(yuscii_text) == unicode_pangram
    assert conversion.replacement_font == "Arial"


def test_makedonski_tajms():
    yuscii_text = r"@elkata Quba muzicira na harfa ~itaj}i go Wego{, a pesot \o{e se xari vo yvezdi."
    yuscii_font = "makedonski tajms"

    conversion = the_stupid_fonts[yuscii_font]
    assert conversion.convert(yuscii_text) == unicode_pangram
    assert conversion.replacement_font == "Times"


def test_sans_k():
    yuscii_text = r"@elkata Quba muzicira na harfa ~itaj]i go Wego[, a pesot |o[e se xari vo yvezdi."
    yuscii_font = "sans_k"

    conversion = the_stupid_fonts[yuscii_font]
    assert conversion.convert(yuscii_text) == unicode_pangram
    assert conversion.replacement_font == "Arial"


def test_maksans_beta():
    yuscii_text = r"@elkata Quba muzicira na harfa ;itaj]i go Wego[, a pesot |o[e se xari vo yvezdi."
    yuscii_font = "makarial_beta"

    conversion = the_stupid_fonts[yuscii_font]
    assert conversion.convert(yuscii_text) == unicode_pangram
    assert conversion.replacement_font == "Arial"
