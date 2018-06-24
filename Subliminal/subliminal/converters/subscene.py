# -*- coding: utf-8 -*-
from babelfish import Language, LanguageReverseConverter

from ..exceptions import ProviderConfigurationError as ConfigurationError


# alpha3 codes extracted from `https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes`
# Subscene language list extracted from it's upload form
from_subscene = {
        'Farsi/Persian': 'fas', 'Greek': 'ell', 'Greenlandic': 'kal',
        'Malay': 'msa', 'Pashto': 'pus', 'Punjabi': 'pan', 'Swahili': 'swa'
}

to_subscene = {v: k for k, v in from_subscene.items()}

exact_languages_alpha3 = [
        'ara', 'aze', 'bel', 'ben', 'bos', 'bul', 'cat', 'ces', 'dan', 'deu',
        'eng', 'epo', 'est', 'eus', 'fin', 'fra', 'heb', 'hin', 'hrv', 'hun',
        'hye', 'ind', 'isl', 'ita', 'jpn', 'kat', 'kor', 'kur', 'lav', 'lit',
        'mal', 'mkd', 'mni', 'mon', 'mya', 'nld', 'nor', 'pol', 'por', 'ron',
        'rus', 'sin', 'slk', 'slv', 'som', 'spa', 'sqi', 'srp', 'sun', 'swe',
        'tam', 'tel', 'tgl', 'tha', 'tur', 'ukr', 'urd', 'vie', 'yor'
]

# TODO: specify codes for unspecified_languages
unspecified_languages = [
        'Big 5 code', 'Brazillian Portuguese', 'Bulgarian/ English',
        'Chinese BG code', 'Dutch/ English', 'English/ German',
        'Hungarian/ English', 'Rohingya'
]

supported_languages = {Language(l) for l in exact_languages_alpha3}

alpha3_of_code = {l.name: l.alpha3 for l in supported_languages}

supported_languages.update({Language(l) for l in to_subscene})


class SubsceneConverter(LanguageReverseConverter):
    codes = {l.name for l in supported_languages}

    def convert(self, alpha3, country=None, script=None):
        if alpha3 in exact_languages_alpha3:
            return Language(alpha3).name

        if alpha3 in to_subscene:
            return to_subscene[alpha3]

        raise ConfigurationError('Unsupported language for subscene: %s, %s, %s' % (alpha3, country, script))

    def reverse(self, code):
        if code in from_subscene:
            return (from_subscene[code],)

        if code in alpha3_of_code:
            return (alpha3_of_code[code],)

        if code in unspecified_languages:
            raise NotImplementedError("currently this language is unspecified: %s" % code)

        raise ConfigurationError('Unsupported language code for subscene: %s' % code)
