# -*- coding: utf-8 -*-
import unittest

from koala.ExcelCompiler import Spreadsheet
from koala.Cell import Cell
from koala.ExcelError import ExcelError


class Test_Excel(unittest.TestCase):

    def setUp(self):
        # This needs to be in setup so that further tests begin from scratch
        file_name = "./tests/ast/basic_evaluation.xlsx"

        self.sp = Spreadsheet(file_name, debug=True)

    @unittest.skip('This test fails.')
    def test_detect_alive(self):
        alive = self.sp.detect_alive()[0]
        self.assertEqual(len(alive), 8)

    @unittest.skip('This test fails.')
    def test_Volatile_Name_L6(self):
        self.sp.cell_set_value('Sheet1!A6', 10)
        self.assertEqual(self.sp.evaluate('Sheet1!L6'), 10)

    def test_add_ranges(self):
        self.sp.cell_set_value('Sheet1!A1', 10)
        self.assertEqual(self.sp.evaluate('Sheet1!D1'), 20)

        self.sp.cell_set_value('Sheet1!A2', 10)
        self.assertEqual(self.sp.evaluate('Sheet1!D2'), 30)

        self.sp.cell_set_value('Sheet1!A3', 10)
        self.assertEqual(self.sp.evaluate('Sheet1!D3'), 40)

    def test_add_ranges_and_integers(self):
        self.sp.cell_set_value('Sheet1!B1', 20)
        self.assertEqual(self.sp.evaluate('Sheet1!E1'), 22)

    def test_add__named_ranges_and_ranges(self):
        self.sp.cell_set_value('Sheet1!B1', 20)
        self.assertEqual(self.sp.evaluate('Sheet1!F1'), 120)

    def test_add__named_ranges(self):
        self.sp.cell_set_value('Sheet1!B1', 20)
        self.assertEqual(self.sp.evaluate('Sheet1!G1'), 41)

    def test_add_non_aligned_ranges(self):
        self.sp.cell_set_value('Sheet1!A8', 10)
        self.assertEqual(self.sp.evaluate('Sheet1!D8'), 17)

    def test_multiply_ranges(self):
        self.sp.cell_set_value('Sheet1!A6', 10)
        self.assertEqual(self.sp.evaluate('Sheet1!B6'), 20)

    def test_if_error(self):
        self.sp.cell_set_value('Sheet1!B1', 20)
        self.assertEqual(self.sp.evaluate('Sheet1!J1'), 4)

    def test_min_with_string(self):
        self.sp.cell_set_value('Sheet1!B2', 10)
        self.assertEqual(self.sp.evaluate('Sheet1!J2'), 0)

    def test_power(self):
        self.assertEqual(self.sp.evaluate('Sheet1!L8'), 4)
        self.sp.cell_set_value('Sheet1!K8', 3)
        self.assertEqual(self.sp.evaluate('Sheet1!L8'), 8)
        self.assertIsInstance(self.sp.evaluate('Sheet1!L9'), ExcelError)

    def test_J22(self):
        cell = self.sp.cellmap['Sheet1!J22']
        assert cell.value == 'George'

        assert self.sp.evaluate('Sheet1!J22') == 'George'

    def test_J23(self):
        cell = self.sp.cellmap['Sheet1!J23']
        assert cell.value == u'John☺'

        assert self.sp.evaluate('Sheet1!J23') == 'John☺'

    def test_J24(self):
        cell = self.sp.cellmap['Sheet1!J24']
        assert cell.value == 'Paul'

        assert self.sp.evaluate('Sheet1!J24') == 'Paul'

    def test_C17(self):
        self.sp.cell_set_value('Sheet1!A17', 40)
        self.assertEqual(self.sp.evaluate('Sheet1!C17'), 80)

    def test_I17(self):
        self.sp.cell_set_value('Sheet1!A2', 4)
        self.assertEqual(self.sp.evaluate('Sheet1!I17'), 4)

    def test_L1(self):
        self.sp.cell_set_value('Sheet1!B1', 13)
        self.assertEqual(self.sp.evaluate('Sheet1!L1'), 13)

    @unittest.skip('This test fails.')
    def test_F26(self): # Offset with range output, see Issue #70
        self.sp.cell_set_value('Sheet1!A23', 10)

        self.assertEqual(self.sp.evaluate('Sheet1!F26'), 21)

    def test_G26(self):
        self.sp.cell_set_value('Sheet1!B22', 3)
        self.assertEqual(self.sp.evaluate('Sheet1!G26'), 10)

    def test_N1(self):
        self.sp.cell_set_value('Sheet1!A1', 3)
        self.assertEqual(self.sp.evaluate('Sheet1!N1'), 3)

    def test_sheet_with_name(self):
        self.assertEqual(self.sp.evaluate('Sheet1!N8'), 1)
        self.sp.cell_set_value("'Sheet with space'!A1'", 2)
        self.assertEqual(self.sp.evaluate('Sheet1!N8'), 2)

    def test_E32(self):
        self.sp.cell_set_value('Sheet1!A31', 3)
        self.assertEqual(self.sp.evaluate('Sheet1!E32'), 19)

    def test_A37(self):
        self.sp.cell_set_value('Sheet1!A36', 0.5)
        self.assertEqual(self.sp.evaluate('Sheet1!A37'), 0.52)

    def test_C37(self):
        self.sp.cell_set_value('Sheet1!C36', 'David')
        self.assertEqual(self.sp.evaluate('Sheet1!C37'), 1)

    def test_G9(self):
        self.sp.cell_set_value('Sheet1!A1', 2)
        self.assertEqual(self.sp.evaluate('Sheet1!G9'), 67)

    def test_P1(self):
        self.sp.cell_set_value('Sheet1!A1', 2)
        self.assertEqual(self.sp.evaluate('Sheet1!P1'), 10)

    def test_Sheet2_B2(self):
        self.sp.cell_set_value('Sheet1!B2',1000)
        self.assertEqual(self.sp.evaluate('Sheet2!B2'), 1000)

    def test_Sheet1_A39(self):
        self.sp.cell_set_value('Sheet1!A2', 3)
        self.assertEqual(self.sp.evaluate('Sheet1!A39'), 2)

    def test_Sheet1_K17(self):
        self.sp.cell_set_value('Sheet1!A3', 5)
        self.assertEqual(self.sp.evaluate('Sheet1!K17'), 5)

    @unittest.skip('This test fails.')
    def test_Sumproduct_with_equality_H9(self):
        # DOESNT WORK BECAUSE OF RANGES OF DIFFERENT LENGTH, see Issue #50

        self.sp.cell_set_value('Sheet1!A1', 5)

        # print 'Test', RangeCore.apply_all('is_equal',self.sp.eval_ref("Sheet1!C1:C3"),self.sp.eval_ref("Sheet1!C1"),(9, 'H'))
        # print 'Test 2', RangeCore.apply_all('multiply',self.sp.eval_ref('Liste'),self.sp.eval_ref('Liste2'),(9, 'H'))
        # print 'Test 3', RangeCore.apply_all('multiply',RangeCore.apply_all('multiply',self.sp.eval_ref('Liste'),self.sp.eval_ref('Liste2'),(9, 'H')),RangeCore.apply_all('is_equal',self.sp.eval_ref("Sheet1!C1:C3"),self.sp.eval_ref("Sheet1!C1"),(9, 'H')),(9, 'H'))

        self.assertEqual(self.sp.evaluate('Sheet1!H9'), 50)

    def test_Vlookup_Range_Lookup_is_True(self):
        self.sp.cell_set_value('Sheet1!H22', 5)
        self.assertEqual(self.sp.evaluate('Sheet1!N22'), 120)

    def test_Vlookup_Range_Lookup_is_False(self):
        self.sp.cell_set_value('Sheet1!H22', 5)
        self.assertEqual(self.sp.evaluate('Sheet1!O22'), 130)

    def test_Vlookup_Range_Lookup_is_False_Value_not_Found(self):
        self.sp.cell_set_value('Sheet1!H22', 5)
        self.assertEqual(self.sp.evaluate('Sheet1!P22').value, '#N/A')

    @unittest.skip('This test fails.')
    def test_Vlookup_Text_Wildcard_Range_Lookup_is_False(self):
        self.sp.cell_set_value('Sheet1!H22', 5)
        self.assertEqual(self.sp.evaluate('Sheet1!N23'), 130)

    def test_Vlookup_Text_Range_Lookup_is_False(self):
        self.sp.cell_set_value('Sheet1!H22', 5)
        self.assertEqual(self.sp.evaluate('Sheet1!O23'), 140)

    def test_Vlookup_Text_Range_Lookup_is_False_Value_not_Found(self):
        self.sp.cell_set_value('Sheet1!H22', 5)
        self.assertEqual(self.sp.evaluate('Sheet1!P23').value, '#N/A')

    def test_Vlookup_Text_Smaller(self):
        self.sp.cell_set_value('Sheet1!H22', 5)
        self.assertEqual(self.sp.evaluate('Sheet1!N24'), 120)

    def test_Vlookup_Text_Exact(self):
        self.sp.cell_set_value('Sheet1!H22', 5)
        self.assertEqual(self.sp.evaluate('Sheet1!O24'), 140)

    def test_Vlookup_Text_Larger(self):
        self.sp.cell_set_value('Sheet1!H22', 5)
        self.assertEqual(self.sp.evaluate('Sheet1!P24'), 130)

    def test_Hlookup_Range_Lookup_is_True(self):
        self.assertEqual(self.sp.evaluate('Sheet1!N26'), "rhythm guitar")

    def test_Hlookup_Range_Lookup_is_False(self):
        self.sp.cell_set_value('Sheet1!H22', 5)
        self.assertEqual(self.sp.evaluate('Sheet1!O26'), 120)

    def test_Hlookup_Range_Lookup_is_False_Value_not_Found(self):
        self.sp.cell_set_value('Sheet1!H22', 5)
        self.assertEqual(self.sp.evaluate('Sheet1!P26').value, '#N/A')

    @unittest.skip('This test fails.')
    def test_Hlookup_Text_Wildcard_Range_Lookup_is_False(self):
        self.sp.cell_set_value('Sheet1!H22', 5)
        self.assertEqual(self.sp.evaluate('Sheet1!N27'), 120)

    def test_Hlookup_Text_Range_Lookup_is_False(self):
        self.assertEqual(self.sp.evaluate('Sheet1!O27'), "John☺")

    def test_Hlookup_Text_Range_Lookup_is_False_Value_not_Found(self):
        self.assertEqual(self.sp.evaluate('Sheet1!P27').value, '#N/A')

    def test_Hlookup_Text_Smaller(self):
        self.assertEqual(self.sp.evaluate('Sheet1!N28'), "rhythm guitar")

    def test_Hlookup_Text_Exact(self):
        self.assertEqual(self.sp.evaluate('Sheet1!O28'), "rhythm guitar")

    def test_Hlookup_Text_Larger(self):
        self.sp.cell_set_value('Sheet1!H22', 5)
        self.assertEqual(self.sp.evaluate('Sheet1!P28'), 120)

    def test_Choose(self):
        self.sp.cell_set_value('Sheet1!A1', 3)
        self.assertEqual(self.sp.evaluate('Sheet1!A41'), 'Paul')

    def test_Modify_graph(self):
        self.sp.cell_add(cell=Cell('Sheet1!P4', formula ='A1 + 10'))
        self.sp.cell_set_value('Sheet1!A1', 3)
        self.assertEqual(self.sp.evaluate('Sheet1!P4'), 13)
