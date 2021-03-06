import os

from alice.public_api import *
from alice import public_api

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

__version__ = open(f"{ROOT_PATH}/VERSION", "r").read()[:-1]

__all__ = public_api.__all__
