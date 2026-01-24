"""
Facade for backward compatibility.
Delegates to the new modular package src.core.importers.
"""

import pandas as pd
from src.core.importers import ExcelImporter
from src.core.schemas import validate_contabilita, validate_giornaliere

__all__ = ["ExcelImporter", "pd", "validate_contabilita", "validate_giornaliere"]