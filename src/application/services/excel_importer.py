"""Facade for backward compatibility.

Delegates to the new modular package src.application.services.importers.
"""

import pandas as pd

from src.application.services.importers import ExcelImporter
from src.application.services.schemas import validate_contabilita, validate_giornaliere

__all__ = ["ExcelImporter", "pd", "validate_contabilita", "validate_giornaliere"]
