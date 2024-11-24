import os

from dotenv import load_dotenv
load_dotenv()


SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "secretkey",
)
if not SECRET_KEY:
    SECRET_KEY = os.urandom(32)

