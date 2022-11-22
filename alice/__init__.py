import os

from alice import public_api
from alice.public_api import *

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

__version__ = open(f"{ROOT_PATH}/VERSION").read()[:-1]

__all__ = public_api.__all__
