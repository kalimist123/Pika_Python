from unittest import TestCase
from picheck import PICheck


class TestPICheck(TestCase):
    def setUp(self):
        self.PICheck = PICheck()

    def test_common_regex_should_find_date(self):
        parsed_text=self.PICheck.common_regex_parse('01/10/1977')
        self.assertEqual(self.PICheck.common_regex_check('dates', parsed_text), 'CR:dates:[01/10/1977]')

    def test_custom_regex_check_should_find_spanish_postal(self):
        self.assertEqual(self.PICheck.custom_regex_check('spanish postal',
                                                         self.PICheck.spanish_postal_regex, 'bong 76038'),
                         'spanish postal:76038')

    def test_nlp_check_should_find_names_and_places(self):
        self.assertEqual(self.PICheck.nlp_check('Michael Malone  Mary Maguire  New York'),
                         ' E:PERSON[Michael Malone] E:PERSON[Mary Maguire] E:GPE[New York]')

    def test_annotate_value_should_annotate_date_and_name(self):
        self.assertEqual(self.PICheck.annotate_value('Michael Malone  01/10/1971'),
                         'CR:dates:[01/10/1971] E:PERSON[Michael Malone]')
