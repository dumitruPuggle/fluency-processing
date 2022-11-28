from src.auth.auth_provider_email import AuthProviderEmail

verify_email = AuthProviderEmail(email="Hello wOrl")
verify_email.send_code(to='dumitruiurie@gmail.com', code=verify_email.generate_code(), lang="ru")
# 
# from src.email_html.verification_code import VerificationCodeHTMLTemplate
# 
# e = VerificationCodeHTMLTemplate().to_html(1000)
# 
# print(str(e))