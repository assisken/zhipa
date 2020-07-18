import os

from dotenv import load_dotenv
from split_settings.tools import include

# Stubs for IDE
BASE_DIR: str
BRAND: str
TIME_ZONE: str

ENV = os.getenv("ENV", "development")
DEBUG = ENV == "development"
if ENV != "testing":
    load_dotenv(verbose=True)

base_settings = [
    "components/general.py",
    "components/app.py",
    "components/logging.py",
    "components/flatpages.py",
    "components/constance.py",
    # Select the environment
    f"environments/{ENV}.py",
]

include(*base_settings)
