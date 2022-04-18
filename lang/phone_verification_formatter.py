def phoneVerificationFormatter(code, language):
    if language == "en":
        return f'Your verification code is: {code}. Please don\'t share this code with anyone.'
    elif language == "ro":
        return f'Codul de verificare este: {code}. Nu-l partajati cu nimeni.'
    elif language == "ru":
        return f'Ваш код подтверждения: {code}. Не передавайте этот код никому.'