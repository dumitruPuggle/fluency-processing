from src.email_html.html_template import HTMLTemplate
from lang.translate import Translate, fallback_lang

class VerificationCodeHTMLTemplate(HTMLTemplate):
	def __init__(self, lang=fallback_lang):
		self.template = self.get_str_from_file('confirmation_code.html')
		self.translate = Translate(lang)
	
	def to_html(self, code):
		return self.template.format(
			confirmation_code_description_1=self.translate.t('confirmation_code_description_1'),
			code=code
		)
		