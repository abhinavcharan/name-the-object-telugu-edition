"""
Telugu Lens App - Core Modules Package
--------------------------------------
This package contains all core functionality for the Telugu Lens application.
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

# Import key modules to make them easily accessible
from . import i18n
from . import styles
from . import auth
from . import storage
from . import images
from . import ai
from . import ui

# Define what gets imported with `from app import *`
__all__ = [
    'i18n',
    'styles', 
    'auth',
    'storage',
    'images',
    'ai',
    'ui'
]

# Package initialization code
print(f"Initializing Telugu Lens App Core Modules v{__version__}")
