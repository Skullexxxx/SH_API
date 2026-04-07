from authx import AuthX, AuthXConfig

import os
from dotenv import load_dotenv


load_dotenv()

config = AuthXConfig()
config.JWT_SECRET = os.getenv("SECRET_KEY")
config.JWT_ACCESS_COOKIE_NAME = os.getenv("ACCESS_COOKIE_NAME")
config.JWT_TOKEN_COOKIE_NAME = [os.getenv("TOKEN_LOCATION")]

security = AuthX(config=config)
