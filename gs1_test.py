# -*- coding: utf-8 -*-
"""
This module tests for GS1 barcode module.
"""

import unittest

import gs1


class TestFunctions(unittest.TestCase):
    """Test functions.

    Arguments:
        unittest {unittest} -- Calling attribut
    """

    def setUp(self):
        self.code = "01059965271763401020141719073121280122804"
        self.wrong_code = "0105996527163401020141719073121280122804"
        self.lot = "2014"
        self.catalog_number = "280122804"
        self.expiration_date = "190731"
        self.ean = "05996527176340"

    def test_check_gtin_id(self):
        """Test.
        """

        self.assertEqual(gs1.check_gtin_id(self.code), True)

    def test_verify(self):
        """Test.
        """

        self.assertEqual(gs1.verify(self.code), True)
        self.assertEqual(gs1.verify(self.wrong_code), False)

    def test_get_ean_number(self):
        """Test.
        """

        self.assertEqual(gs1.get_ean_number(self.code), self.ean)

    def test_get_lot_number(self):
        """Test.
        """

        self.assertEqual(gs1.get_lot_number(self.code), self.lot)

    def test_get_expiration_date(self):
        """Test.
        """

        self.assertEqual(gs1.get_expiration_date(
            self.code), self.expiration_date)

    def test_get_catalog_number(self):
        """Test.
        """

        self.assertEqual(gs1.get_catalog_number(
            self.code), self.catalog_number)


class TestFunctions2(unittest.TestCase):
    """Test functions.

    Arguments:
        unittest {unittest} -- Calling attribut
    """

    def setUp(self):
        self.code = "01059965271763401020141719073121280122804"
        self.lot = "2014"
        self.catalog_number = "280122804"
        self.expiration_date = "190731"
        self.ean = "05996527176340"
        self.code_brackets = \
            "(01)05996527176340(10)2014(17)190731(21)280122804"

    def test_parse_gs1(self):
        """Test.
        """

        self.assertEqual(gs1.parse_gs1(self.code), (self.ean,
                                                    self.lot,
                                                    self.expiration_date,
                                                    self.catalog_number))

    def test_format_barcode(self):
        """Test.
        """

        self.assertEqual(gs1.format_barcode(self.code_brackets), self.code)


class TestFunctions3(unittest.TestCase):
    """Test functions.

    Arguments:
        unittest {unittest} -- Calling attribut
    """

    def setUp(self):
        self.code = "01059965271763401020141719073121280122804"
        self.lot = "2014"
        self.catalog_number = "280122804"
        self.expiration_date = "190731"
        self.ean = "05996527176340"
        self.code_brackets = \
            "(01)05996527176340(10)2014(17)190731(21)280122804"

    def test_create_gs1(self):
        """Test.
        """

        self.assertEqual(gs1.create_gs1(
            self.ean, self.lot, self.expiration_date,
            self.catalog_number, "Normal"), self.code)

    def test_create_gs1_with_brackets(self):
        """Test.
        """

        self.assertEqual(gs1.create_gs1(
            self.ean, self.lot, self.expiration_date,
            self.catalog_number, "Brackets"), self.code_brackets)


class TestFunctions4(unittest.TestCase):
    """Test functions.

    Arguments:
        unittest {unittest} -- Calling attribut
    """

    def setUp(self):
        self.lot = "2014"
        self.catalog_number = "280122804"
        self.expiration_date = "190731"
        self.ean = "05996527176340"
        self.code_zpl = \
            "^BCN,,N,N^FD>;>80105996527176340102014>8171907312128012280>64^FS"
        self.code_zpl2 = \
            "^BCN,,N,N^FD>;>80105996527176340102014" + \
            ">6AA>5>8171907312128012280>64^FS"
        self.lot2 = "2014AA"

    def test_create_gs1_zpl(self):
        """Test.
        """

        self.assertEqual(gs1.create_gs1(
            self.ean, self.lot, self.expiration_date,
            self.catalog_number, "ZPL"), self.code_zpl)

    def test_create_gs1_zpl2(self):
        """Test.
        """

        self.assertEqual(gs1.create_gs1(
            self.ean, self.lot2, self.expiration_date,
            self.catalog_number, "ZPL"), self.code_zpl2)


class TestFunctions5(unittest.TestCase):
    """Test functions.

    Arguments:
        unittest {unittest} -- Calling attribut
    """

    def setUp(self):
        self.lot = "2014"
        self.catalog_number = "280122804"
        self.expiration_date = "190731"
        self.ean = "05996527176340"
        self.code_char = "ÍÊ!%Ça;1_H*4.Ê13'?5<!6pÈ4pÎ"

    def test_create_gs1_character(self):
        """Test.
        """

        self.assertEqual(gs1.create_gs1(
            self.ean, self.lot, self.expiration_date,
            self.catalog_number, "Character"), self.code_char)


if __name__ == '__main__':
    unittest.main()
