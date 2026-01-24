"""
Facade for backward compatibility.
Delegates to the new modular package src.core.importers.
"""

from src.core.importers import ExcelImporter

__all__ = ["ExcelImporter"]
