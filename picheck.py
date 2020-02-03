import re
import spacy
from commonregex import CommonRegex

nlp = spacy.load('en_core_web_sm')


class PICheck:

    spanish_postal_regex = '([1-9]{2}|[0-9][1-9]|[1-9][0-9])[0-9]{3}'
    spanish_tax_regex = '[1-9a-zA-Z][0-9]{7}[1-9a-zA-Z]'
    spanish_ssn_regex = '[0-9]{12}'
    check_types = 'times,phones,dates,links,emails,ips,ipv6s,credit_cards'

    @staticmethod
    def common_regex_parse(text_to_parse):
        return CommonRegex(text_to_parse)

    @staticmethod
    def common_regex_check(check_type, parsed_text):
        result = ''
        if len(parsed_text.__getattribute__(check_type)) > 0:
            result = 'CR:' + check_type + ':[' + ''.join(parsed_text.__getattribute__(check_type)) + ']'
        return result

    @staticmethod
    def custom_regex_check(check_type, regex, text_string):
        result = ''
        mo = re.compile(regex).search(text_string)
        if mo:
            result = check_type + ':' + mo.group()
        return result

    @staticmethod
    def nlp_check(string_to_check):
        result = ''
        doc = nlp(string_to_check)
        for entity in doc.ents:
            if entity.label_ in ["DATE", "PERSON", "NORP", "GPE"]:
                result = result + ' E:' + entity.label_ + '[' + entity.text + ']'
        return result

    def annotate_value(self, string_to_check):
        return_string = ''
        suspect_vars = ''
        parsed_text = self.common_regex_parse(string_to_check)

        for check_type in self.check_types.split(','):
            suspect_vars += self.common_regex_check(str(check_type), parsed_text)

        suspect_vars += self.custom_regex_check('spanish postal',
                                                self.spanish_postal_regex, string_to_check)
        suspect_vars += self.custom_regex_check('spanish tax', self.spanish_tax_regex, string_to_check)
        suspect_vars += self.custom_regex_check('spanish ssn', self.spanish_ssn_regex, string_to_check)
        suspect_vars += self.nlp_check(string_to_check)

        if suspect_vars is not None:
            return_string = suspect_vars

        return return_string
