# -*- coding: utf-8 -*-
"""
This module tests for GS1 barcode module.
"""

import unittest

from gs1 import GS1Check, GS1Create, GS1GetElement


class TestFunctions(unittest.TestCase):
    """Test functions.

    Arguments:
        unittest {unittest} -- Calling attribut
    """

    def setUp(self):
        self.gs1_check = GS1Check()
        self.gs1_create = GS1Create()
        self.gs1_get_element = GS1GetElement()
        self.gs1_get_element.barcode =\
            "01059965271763401020141719073121280122804"
        self.lot = "2014"
        self.catalog_number = "280122804"
        self.expiration_date = "190731"
        self.ean = "05996527176340"

    def test_check_gtin_id(self):
        """Test.
        """
        self.gs1_check.barcode = "01059965271763401020141719073121280122804"
        self.assertEqual(self.gs1_check.check_gtin_id(), True)

    def test_verify(self):
        """Test.
        """
        self.gs1_check.barcode = "01059965271763401020141719073121280122804"
        self.assertEqual(self.gs1_check.verify(), True)
        self.gs1_check.barcode = self.gs1_check.barcode + "5"
        self.assertEqual(self.gs1_check.verify(), False)

    def test_get_ean_number(self):
        """Test.
        """

        self.assertEqual(
            self.gs1_get_element.get_ean_number(), self.ean)

    def test_get_lot_number(self):
        """Test.
        """

        self.assertEqual(
            self.gs1_get_element.get_lot_number(), self.lot)

    def test_get_expiration_date(self):
        """Test.
        """

        self.assertEqual(
            self.gs1_get_element.get_expiration_date(), self.expiration_date)

    def test_get_catalog_number(self):
        """Test.
        """

        self.assertEqual(
            self.gs1_get_element.get_catalog_number(), self.catalog_number)


class TestFunctions2(unittest.TestCase):
    """Test functions.

    Arguments:
        unittest {unittest} -- Calling attribut
    """

    def setUp(self):
        self.gs1_get_element = GS1GetElement()
        self.gs1_get_element.barcode = \
            "01059965271763401020141719073121280122804"
        self.lot = "2014"
        self.catalog_number = "280122804"
        self.expiration_date = "190731"
        self.ean = "05996527176340"

    def test_parse_gs1(self):
        """Test.
        """

        self.assertEqual(self.gs1_get_element.parse_gs1(),
                         (self.ean,
                          self.lot,
                          self.expiration_date,
                          self.catalog_number))

    def test_format_barcode(self):
        """Test.
        """
        self.gs1_get_element.barcode = \
            "(01)05996527176340(10)2014(17)190731(21)280122804"
        self.assertEqual(self.gs1_get_element.format_barcode(),
                         "01059965271763401020141719073121280122804")


class TestFunctions3(unittest.TestCase):
    """Test functions.

    Arguments:
        unittest {unittest} -- Calling attribut
    """

    def setUp(self):
        self.gs1_create = GS1Create()
        self.gs1_create.barcode = "01059965271763401020141719073121280122804"
        self.lot = "2014"
        self.catalog_number = "280122804"
        self.expiration_date = "190731"
        self.ean = "05996527176340"
        self.code_brackets = \
            "(01)05996527176340(10)2014(17)190731(21)280122804"

    def test_create_gs1(self):
        """Test.
        """
        self.gs1_create.ean_number = self.ean
        self.gs1_create.lot_number = self.lot
        self.gs1_create.expiration_date = self.expiration_date
        self.gs1_create.catalog_number = self.catalog_number
        self.gs1_create.output_style = "Normal"
        self.assertEqual(self.gs1_create.create_gs1(),
                         "01059965271763401020141719073121280122804")

    def test_create_gs1_with_brackets(self):
        """Test.
        """
        self.gs1_create.ean_number = self.ean
        self.gs1_create.lot_number = self.lot
        self.gs1_create.expiration_date = self.expiration_date
        self.gs1_create.catalog_number = self.catalog_number
        self.gs1_create.output_style = "Brackets"
        self.assertEqual(self.gs1_create.create_gs1(), self.code_brackets)


class TestFunctions4(unittest.TestCase):
    """Test functions.

    Arguments:
        unittest {unittest} -- Calling attribut
    """

    def setUp(self):
        self.gs1_create = GS1Create()
        self.lot = "2014"
        self.catalog_number = "280122804"
        self.expiration_date = "190731"
        self.ean = "05996527176340"
        self.code_zpl = \
            "^BCN,,N,N^FD>;>80105996527176340102014>8171907312128012280>64^FS"
        self.code_zpl2 = \
            "^BCN,,N,N^FD>;>80105996527176340102014" + \
            ">6AA>5>8171907312128012280>64^FS"

    def test_create_gs1_zpl(self):
        """Test.
        """
        self.gs1_create.ean_number = self.ean
        self.gs1_create.lot_number = self.lot
        self.gs1_create.expiration_date = self.expiration_date
        self.gs1_create.catalog_number = self.catalog_number
        self.gs1_create.output_style = "ZPL"
        self.assertEqual(self.gs1_create.create_gs1(), self.code_zpl)

    def test_create_gs1_zpl2(self):
        """Test.
        """
        self.gs1_create.ean_number = self.ean
        self.gs1_create.lot_number = self.lot
        self.gs1_create.expiration_date = self.expiration_date
        self.gs1_create.catalog_number = self.catalog_number
        self.gs1_create.output_style = "ZPL"
        self.assertEqual(self.gs1_create.create_gs1(), self.code_zpl2)


class TestFunctions5(unittest.TestCase):
    """Test functions.

    Arguments:
        unittest {unittest} -- Calling attribut
    """

    def setUp(self):
        self.gs1_create = GS1Create()
        self.lot = "2014"
        self.catalog_number = "280122804"
        self.expiration_date = "190731"
        self.ean = "05996527176340"
        self.code_char = "ÍÊ!%Ça;1_H*4.Ê13'?5<!6pÈ4pÎ"

    def test_create_gs1_character(self):
        """Test.
        """
        self.gs1_create.ean_number = self.ean
        self.gs1_create.lot_number = self.lot
        self.gs1_create.expiration_date = self.expiration_date
        self.gs1_create.catalog_number = self.catalog_number
        self.gs1_create.output_style = "Character"
        self.assertEqual(self.gs1_create.create_gs1(), self.code_char)


if __name__ == '__main__':
    unittest.main()
