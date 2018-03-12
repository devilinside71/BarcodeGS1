# -*- coding: utf-8 -*-
"""
This module tests for GS1 barcode module.
"""
import sys
import gs1
import unittest


class testFunctions(unittest.TestCase):
    def setUp(self):
        self.code = "01059965271763401020141719073121280122804"
        self.code_brackets = \
            "(01)05996527176340(10)2014(17)190731(21)280122804"
        self.wrong_code = "0105996527163401020141719073121280122804"
        self.wrong_code2 = "01059965271763401020141719073121280122804"
        self.lot = "2014"
        self.lot2 = "2014AA"
        self.wrong_lot = "2014"
        self.lic = "0599"
        self.catalog_number = "280122804"
        self.expiration_date = "190731"
        self.ean = "05996527176340"
        self.gtin_id = "01"
        self.lot_id = "10"
        self.expiration_date_id = "17"
        self.catalog_number_id = "21"
        self.code_zpl = \
            "^BCN,,N,N^FD>;>80105996527176340102014>8171907312128012280>64^FS"
        self.code_zpl2 = \
            "^BCN,,N,N^FD>;>80105996527176340102014>6AA>5>8171907312128012280>64^FS"

    def test_check_gtin_id(self):
        self.assertEqual(gs1.check_gtin_id(self.code), True)

    def test_verify(self):
        self.assertEqual(gs1.verify(self.code), True)
        self.assertEqual(gs1.verify(self.wrong_code), False)

    def test_get_ean_number(self):
        self.assertEqual(gs1.get_ean_number(self.code), self.ean)

    def test_get_lot_number(self):
        self.assertEqual(gs1.get_lot_number(self.code), self.lot)

    def test_get_expiration_date(self):
        self.assertEqual(gs1.get_expiration_date(
            self.code), self.expiration_date)

    def test_get_catalog_number(self):
        self.assertEqual(gs1.get_catalog_number(
            self.code), self.catalog_number)

    def test_parse_gs1(self):
        self.assertEqual(gs1.parse_gs1(self.code), (
                         self.ean, self.lot, self.expiration_date,
                         self.catalog_number))

    def test_create_gs1(self):
        self.assertEqual(gs1.create_gs1(
            self.ean, self.lot, self.expiration_date,
            self.catalog_number, "Normal"), self.code)

    def test_create_gs1_with_brackets(self):
        self.assertEqual(gs1.create_gs1(
            self.ean, self.lot, self.expiration_date,
            self.catalog_number, "Brackets"), self.code_brackets)

    def test_create_gs1_ZPL(self):
        self.assertEqual(gs1.create_gs1(
            self.ean, self.lot, self.expiration_date,
            self.catalog_number, "ZPL"), self.code_zpl)

    def test_create_gs1_ZPL2(self):
        self.assertEqual(gs1.create_gs1(
            self.ean, self.lot2, self.expiration_date,
            self.catalog_number, "ZPL"), self.code_zpl2)

    def test_format_barcode(self):
        self.assertEqual(gs1.format_barcode(self.code_brackets), self.code)


if __name__ == '__main__':
    unittest.main()
