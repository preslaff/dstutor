"""
DS-Tutor: AI-Powered Data Science Learning in Jupyter
"""

__version__ = "0.1.0"
__author__ = "DS-Tutor Team"

from .core.extension import load_ipython_extension, unload_ipython_extension

__all__ = ["load_ipython_extension", "unload_ipython_extension"]
