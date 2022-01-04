import unittest
import re

from kotlin_keywords import exact_keyword


class TestExtractWord(unittest.TestCase):

    def test_numbers_on_sides(self):
        keyword = 'var'
        texts = ['1var1', 'var1', '1var', '1111var', '111var111', 'var111111']

        pattern = exact_keyword(keyword)

        for text in texts:
            match_list = re.findall(pattern, text)
            self.assertTrue(match_list.__len__() == 0)

    def test_numbers_inside(self):
        keyword = 'var'
        texts = ['1v1ar1', 'v1ar1', '1va1r', '1111v1a1r', '111v1a1r111', 'v1ar111111']

        pattern = exact_keyword(keyword)

        for text in texts:
            match_list = re.findall(pattern, text)
            self.assertTrue(match_list.__len__() == 0)


    def test_alphabet_characters_on_sides(self):
        keyword = 'var'
        texts = ['avar', 'varvar', 'vars', '1vara']
        pattern = exact_keyword(keyword)

        for text in texts:
            match_list = re.findall(pattern, text)
            self.assertTrue(match_list.__len__() == 0)


if __name__ == '__main__':
    unittest.main()
