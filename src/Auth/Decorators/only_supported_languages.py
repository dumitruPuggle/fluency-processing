from functools import wraps
from flask_restful import request
from lang.supported_languages import languages

def only_supported_languages(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        _ = function(*args, **kwargs)
        language = request.headers.get('lang')
        isLanguageProvided = language is not None
        if isLanguageProvided:
            if language not in languages:
                return {
                    "message": "Language not supported",
                    "field": "lang"
                }, 403
        return _
    return wrapper