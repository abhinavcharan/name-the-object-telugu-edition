"""
Telugu Lens App - Views Package
-------------------------------
This package contains all the view modules for the Telugu Lens application.
"""

__version__ = "1.0.0"

# Import view modules to make them easily accessible
from . import home
from . import identify
from . import upload
from . import explore
from . import browse

# Define what gets imported with `from views import *`
__all__ = [
    'home',
    'identify',
    'upload',
    'explore',
    'browse'
]

# View registry - maps page names to view functions
VIEW_REGISTRY = {
    "home": home.render_home,
    "identify": identify.render_identify,
    "upload": upload.render_upload,
    "explore": explore.render_explore,
    "browse": browse.render_browse
}

def get_view(page_name):
    """
    Get the view function for a given page name.
    
    Args:
        page_name (str): Name of the page/view
        
    Returns:
        function: The view rendering function
    """
    return VIEW_REGISTRY.get(page_name, lambda: None)

# Package initialization code
print(f"Initializing Telugu Lens App Views v{__version__}")
