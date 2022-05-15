def phoneVerificationFormatter(code, language):
    if "en" in language:
        return f'Your verification code is: {code}. Please don\'t share this code with anyone.'
    elif "ro" in language:
        return f'Codul de verificare este: {code}. Nu-l partajati cu nimeni.'
    elif "ru" in language:
        return f'Ваш код подтверждения: {code}. Не передавайте этот код никому.'