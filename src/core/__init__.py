"""
Bot TS - Core Module
"""
from .version import __version__, UPDATE_URL, APP_NAME
from . import config_manager
from . import license_validator
from . import license_updater
from . import app_updater

__all__ = [
    '__version__',
    'UPDATE_URL',
    'APP_NAME',
    'config_manager',
    'license_validator',
    'license_updater',
    'app_updater'
]
