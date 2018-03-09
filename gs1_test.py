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
        self.wrong_code = "0105996527163401020141719073121280122804"
        self.wrong_code2 = "01059965271763401020141719073121280122804"
        self.lot = "2014"
        self.wrong_lot = "2014"
        self.lic = "0599"
        self.catalog_number = "280122804"
        self.expiration_date = "190731"
        self.ean = "05996527176340"
        self.gtin_id = "01"
        self.lot_id = "10"
        self.expiration_date_id = "17"
        self.catalog_number_id = "21"

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


if __name__ == '__main__':
    unittest.main()
