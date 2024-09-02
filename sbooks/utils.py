"""
Utility functions for the Sbooks module.

This module provides helper functions for file operations, UUID handling,
and data cleaning.
"""

import logging
import os
import uuid


def create_data_folder(filename):
    """
    Create a directory for the given filename if it doesn't exist.

    Args:
        filename (str): The path to the file for which to create a directory.
    """
    data_dir = os.path.dirname(filename)
    if data_dir and not os.path.exists(data_dir):
        os.makedirs(data_dir)
        logging.info(f"Created directory: {data_dir}")


def uuid_to_str(obj):
    """
    Convert UUID objects to strings.

    Args:
        obj: The object to convert.

    Returns:
        str or object: The string representation of the UUID if obj is a UUID,
                       otherwise returns the original object.
    """
    if isinstance(obj, uuid.UUID):
        return str(obj)
    return obj


def clean_numeric(value):
    """
    Clean and convert numeric strings to integers.

    Args:
        value: The value to clean and potentially convert.

    Returns:
        int or original value: The integer representation of the value if it's
                               a valid numeric string, otherwise the original value.
    """
    if isinstance(value, str):
        if value.isdigit():
            return int(value)
        elif value.replace(".", "", 1).isdigit() and value.count(".") <= 1:
            return int(float(value))
    return value
