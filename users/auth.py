from authx import AuthX, AuthXConfig

import os
from dotenv import load_dotenv

load_dotenv()

"""Auth Settings"""

config = AuthXConfig()

config.JWT_SECRET_KEY = os.getenv('SECRET_KEY')
config.JWT_ACCESS_COOKIE_NAME = os.getenv('COOKIE_NAME')
config.JWT_TOKEN_LOCATION = [os.getenv('TOKEN_LOCATION')]

security = AuthX(config=config)