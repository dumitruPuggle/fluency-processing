import json

languages = [
    {
        "code": "en",
        "path": './lang/en.json'
    },
    {
        "code": "ro",
        "path": './lang/ro.json'
    },
    {
        "code": "ru",
        "path": './lang/ru.json'
    },
    {
        "code": "en-US",
        "path": './lang/en.json'
    },
    {
        "code": "en-GB",
        "path": './lang/en.json'
    },
    {
        "code": "en-AU",
        "path": './lang/en.json'
    },
    {
        "code": "en-CA",
        "path": './lang/en.json'
    },
    {
        "code": "en-NZ",
        "path": './lang/en.json'
    },
    {
        "code": "en-IE",
        "path": './lang/en.json'
    },
    {
        "code": "en-ZA",
        "path": './lang/en.json'
    },
    {
        "code": "en-JM",
        "path": './lang/en.json'
    },
    {
        "code": "ro-MD",
        "path": './lang/ro.json'
    },
    {
        "code": "ro-RO",
        "path": './lang/ro.json'
    },
    {
        "code": "ro-CH",
        "path": './lang/ro.json'
    },
    {
        "code": "ru-RU",
        "path": './lang/ru.json'
    },
    {
        "code": "ru-UA",
        "path": './lang/ru.json'
    },
    {
        "code": "ru-KG",
        "path": './lang/ru.json'
    },
    {
        "code": "ru-BY",
        "path": './lang/ru.json'
    },
    {
        "code": "ru-KZ",
        "path": './lang/ru.json'
    },
    {
        "code": "ru-MD",
        "path": './lang/ru.json'
    }
]

fallback_lang = "en"

class Translate:
    def __init__(self, lang=fallback_lang):
        self.lang = lang
    def t(self, key: str):
        # Load the language file by the lang code
        for lang in languages:
            if lang['code'] == self.lang:
                with open(lang['path']) as f:
                    lang_data = json.load(f)
                    return lang_data[key]
            elif self.lang == fallback_lang:
                with open(lang['path']) as f:
                    lang_data = json.load(f)
                    return lang_data[key]
