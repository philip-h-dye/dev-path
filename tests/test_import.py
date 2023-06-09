import unittest

from importlib import import_module

class Test_Import ( unittest.TestCase ) :

    def setUp(self):
        self.package = 'dev_path'

    def test_import(self) :

        self.assertTrue ( import_module(self.package), f"'import {self.package}' failed" )
        
    def test_main_exists(self) :

        m = import_module(self.package)
        sym = 'main'
        self.assertTrue ( hasattr(m, sym), f"{self.package} missing '{sym}'")
