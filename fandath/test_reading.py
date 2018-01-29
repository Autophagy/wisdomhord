# -*- coding: utf-8 -*-

import wisdomhord
import unittest
import os

PATH_TO_WH = os.path.join(os.path.dirname(__file__), "test.hord")

class TestWisdomhordReading(unittest.TestCase):

    expected_meta = {'INVOKER' : 'Wísdómhord Testing',
                     'DESCRIPTION': 'Test data for Wísdómhord',
                     'INCEPT': '9 Regn 226 // 03.40',
                     'UPDATED': '9 Regn 226 // 04.00',
                     'COUNT': '7'}

    expected_keys = ['COL1', 'COL2', 'COL3', 'COL4']

    expected_column_lengths = {'COL1' : 13,
                               'COL2': 5,
                               'COL3': 5,
                               'COL4': 11}

    @classmethod
    def setUpClass(cls):
        cls.hord = wisdomhord.hladan(PATH_TO_WH)

    def test_get_metadata(self):
        for k, v in self.expected_meta.items():
            self.assertEqual(self.hord.meta[k], v)

    def test_get_keys(self):
        self.assertEqual(self.expected_keys, self.hord.keys)

    def test_get_column_lengths(self):
        for k, v in self.expected_column_lengths.items():
            self.assertEqual(self.hord._column_lengths[k], v)

    def test_key_row(self):
        self.assertEqual(self.hord._key_row, 6)

    def test_get_first_row(self):
        expected_row = {'COL1': 'Hello world',
                        'COL2': '12345',
                        'COL3': 'True',
                        'COL4': 'If'}

        row = self.hord.get_rows(limit=1)
        self.assertEqual(len(row), 1)

        for k, v in row[0].items():
            self.assertEqual(expected_row[k], v)

    def test_multiple_rows(self):
        rows = self.hord.get_rows(limit=4)
        self.assertEqual(len(rows), 4)

    def test_get_all_rows(self):
        rows = self.hord.get_rows()
        self.assertEqual(len(rows), self.hord.row_count())

    def test_get_specific_cols(self):
        expected_row = {'COL2': '12345',
                        'COL3': 'True'}

        row = self.hord.get_rows(cols=['COL2', 'COL3'], limit=1)
        self.assertEqual(len(expected_row), len(row[0]))

        for k, v in row[0].items():
            self.assertEqual(expected_row[k], v)

    def test_filter(self):
        filter_func = lambda row: row['COL3'] == 'True'
        rows = self.hord.get_rows(filter_func=filter_func)

        self.assertEqual(len(rows), 4)

        for row in rows:
            self.assertEqual(row['COL3'], 'True')

