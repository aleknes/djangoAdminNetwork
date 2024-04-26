""""
This module contains utility functions for syncing the database
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

#Temp hardcoded path for testing
filepath = BASE_DIR / 'networkProvisioning' / 'files' / 'test.xls'


def sync_db():
    """
    Sync the database with the contents of the file
    """
    print(f"Syncing the database with the contents of {filepath}")