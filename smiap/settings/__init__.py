import os

from dotenv import load_dotenv
from split_settings.tools import include

load_dotenv(verbose=True)
ENV = os.getenv('ENV', 'development')
DEBUG = ENV == 'development'

base_settings = [
    'components/general.py',
    'components/app.py',
    'components/database.py',
    'components/logging.py',
    'components/martor.py',

    # Select the environment
    f'environments/{ENV}.py',
]

include(*base_settings)
