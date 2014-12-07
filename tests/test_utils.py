import unittest
import eunomia.utils
import os

class TestUtils(unittest.TestCase):
    
    def test_base_setup(self):
        self.assertEqual(1,1)

    def test_clear_tmp_parse_files(self):
        # first create files
        with open('parser.out', 'a'):
            os.utime('parser.out', None)
        with open('parsetab.py', 'a'):
            os.utime('parsetab.py', None)
        with open('parsetab.pyc', 'a'):
            os.utime('parsetab.pyc', None)
        self.assertTrue(os.path.isfile('parser.out'))
        self.assertTrue(os.path.isfile('parsetab.py'))
        self.assertTrue(os.path.isfile('parsetab.pyc'))
        eunomia.utils.clear_tmp_parse_files()
        self.assertFalse(os.path.isfile('parser.out'))
        self.assertFalse(os.path.isfile('parsetab.py'))
        self.assertFalse(os.path.isfile('parsetab.pyc'))


