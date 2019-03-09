# import pyodbc
import re
import spacy
from commonregex import CommonRegex
from geotext import GeoText


class PICheck:
    def annotateValue(self, stringValue, stringLanguage):

        nlp = spacy.load(stringLanguage)
        returnString = ''
        suspectvars = ''
        parsed_text = CommonRegex(stringValue)
        if len(parsed_text.phones) > 0:
            suspectvars = suspectvars + \
                ' CR:PHONES:['+''.join(parsed_text.phones) + ']'

        if len(parsed_text.dates) > 0:
            suspectvars = suspectvars + \
                ' CR:DATES:['+''.join(parsed_text.dates) + ']'

        if len(parsed_text.links) > 0:
            suspectvars = suspectvars + \
                ' CR:LINKS:['+''.join(parsed_text.links) + ']'

        if len(parsed_text.emails) > 0:
            suspectvars = suspectvars + \
                ' CR:EMAILS:['+''.join(parsed_text.emails) + ']'

        if len(parsed_text.phones) > 0:
            suspectvars = suspectvars + \
                ' CR:PHONES:['+''.join(parsed_text.phones) + ']'

        if len(parsed_text.ips) > 0:
            suspectvars = suspectvars + \
                ' CR:IPS:['+''.join(parsed_text.ips) + ']'

        if len(parsed_text.ipv6s) > 0:
            suspectvars = suspectvars + \
                ' CR:IPV6S:['+''.join(parsed_text.ipv6s) + ']'

        if len(parsed_text.credit_cards) > 0:
            suspectvars = suspectvars + \
                ' CR:CC:['+''.join(parsed_text.credit_cards) + ']'

        spanishPostal = re.compile(r'([1-9]{2}|[0-9][1-9]|[1-9][0-9])[0-9]{3}')
        mo = spanishPostal.search(stringValue)
        if mo:
            suspectvars = suspectvars + ' SPOSTAL:[' + mo.group() + ']'

        spanishTax = re.compile(r'[1-9a-zA-Z][0-9]{7}[1-9a-zA-Z]')
        zo = spanishTax.search(stringValue)
        if zo:
            suspectvars = suspectvars + ' STAX:[' + zo.group() + ']'

        spanishSocialSecurity = re.compile(r'[0-9]{12}')
        sso = spanishSocialSecurity.search(stringValue)
        if sso:
            suspectvars = suspectvars + 'SSO:[' + sso.group() + ']'

        spanishDNI = re.compile(r'[0-9,X,M,L,K,Y][0-9]{7}[A-Z]')
        sDNI = spanishDNI.search(stringValue)
        if sDNI:
            suspectvars = suspectvars + 'SDNI:[' + sDNI.group() + ']'


        doc = nlp(stringValue)
        for entity in doc.ents:
            if entity.label_ in ["DATE", "PERSON", "NORP", "GPE"]:
                suspectvars = suspectvars + ' E:' + \
                    entity.label_ + '[' + entity.text + ']'

        places = GeoText(stringValue)
        if places.cities:
            suspectvars = suspectvars + ' GEOTEXT:[' +''.join(places.cities) + ']'



        if suspectvars is not None:
            returnString = suspectvars

        return returnString
