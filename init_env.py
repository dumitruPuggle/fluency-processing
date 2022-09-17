from random import randrange


class EnvWriter:
   def __init__(self, writer):
      self.writer = writer
      self.writer.write('# ENVIRONMENT - DEV')

   def add_env_credential(self, key, string):
      self.writer.write('\n')
      self.writer.write(f'{key}={string}')


with open('.env', 'w') as env_credentials:
   writer = EnvWriter(env_credentials)
   writer.add_env_credential("HOST", "0.0.0.0")
   writer.add_env_credential("PORT", "5000")
   writer.add_env_credential("JWT_SECRET_KEY", f'dev-{randrange(1000, 9999)}')
   writer.add_env_credential("SMS_JWT_KEY", f"dev-sms-key{randrange(1000, 9000)}")
   writer.add_env_credential("TWILIO_PHONE_NUMBER", input('Enter Twillio phone number: '))
   writer.add_env_credential("TWILIO_ACCOUNT_SID", input('Enter Twillio Account SID: '))
   writer.add_env_credential("TWILIO_AUTH_TOKEN", input('Enter Twillio Auth Token: '))
   writer.add_env_credential("SMS_CODE_ENCRYPTION_KEY", f'dev-encryptionkey-{randrange(1000, 9999)}')
   writer.add_env_credential("NEXMO_FROM", input('Enter Nexmo From Message Title: '))
   writer.add_env_credential("NEXMO_KEY", input('Enter Nexmo Key: '))
   writer.add_env_credential("NEXMO_SECRET", input('Enter Nexmo Secret: '))

print("Your .env file is Ready")
