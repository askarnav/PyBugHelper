# __init__.py

"""PyBugHelper: A package to help you debug Python code."""

__version__ = "2026.0.0"
__author__ = "askarnav"

# Print greeting when the package is imported
print("PyBugHelper is here to help you!")
print("PyBugHelper 2026 Super PYTHON - askarnav")

# Expose core functionality here
# from .debugger import BugHelper
# __all__ = ["BugHelper"]


from .pybughelper import dataman, file_manager, crypt, games, logger, maths, validate
