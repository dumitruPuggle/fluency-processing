import os
from random import randrange

with open('.env', 'w') as env_credentials:
   env_credentials.write(f'JWT_SECRET_KEY=dev-{randrange(1000, 9999)}')
   env_credentials.write('\n')
   env_credentials.write(f'SMS_JWT_KEY=dev-sms-key{randrange(1000, 9000)}')


print("Your .env file is Ready")
