import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

APP_SECRET = os.environ.get('APP_SECRET')
USER_DB = os.path.abspath(os.environ.get('USER_DATABASE'))
CREDENTIALS_DB = os.path.abspath(os.environ.get('CREDENTIALS_DATABASE'))
