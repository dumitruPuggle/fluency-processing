import os
from lang.translate import Translate

class HTMLTemplate:
	
	def get_str_from_file(self, path):
		with open(f"{os.getcwd()}/src/email_html/html/{path}", encoding = 'utf-8') as template_str:
		   as_text = template_str.read()
		   return as_text