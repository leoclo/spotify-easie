import os
import sys
import unittest
import pandas as pd


sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
)
from src.easie import Easie
from src.utils import utils


class TestEasie(unittest.TestCase):
    """ Test Easie Class """

    @classmethod
    def setUpClass(cls):
        cls.easie = Easie.from_settings(utils.get_settings())

    def test_a_insert_in_easie(self):
        """Tests easie insert_in_easie method"""

        dfs_params = [
            {
                'table_name':'tb_test_1',
                'params':{
                    'not_exists_create': True,
                    'replace':True
                },
                'df': pd.DataFrame({'a': [0, 1, 2], 'b': ['a', 'b', 'c']})
            },
            {
                'table_name':'tb_test_2',
                'params':{
                    'not_exists_create': True,
                    'replace':True
                },
                'df': pd.DataFrame({
                    'a': [0, 1, 2],
                    'b': ['a', 'b', 'c'],
                    'c': [0, 'a', 'b']
                })
            }
        ]
        self.easie.insert_in_easie(dfs_params)
        self.assertTrue(
            self.easie.insertion_res[f'tb_test_1 @{self.easie.user}']['success']
        )
        self.assertTrue(
            self.easie.insertion_res[f'tb_test_2 @{self.easie.user}']['success']
        )

    def test_b_get_easie_tables(self):
        """Tests easie get_easie_tables method"""

        table_names = ['tb_test_1', 'tb_test_2']
        dfs = self.easie.get_easie_tables(table_names)
        self.assertTrue(f'tb_test_1' in dfs)
        self.assertTrue(f'tb_test_2' in dfs)


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'])
