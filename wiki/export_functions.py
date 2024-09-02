"""
Export functions for the Wiki module.

This module provides functions to export data to CSV and JSON formats.
"""

import json
import logging

import pandas as pd

from .utils import create_data_folder, uuid_to_str


def exportToCsv(df, filename="./data/output.csv"):
    """
    Export a DataFrame to a CSV file.

    Args:
        df (pandas.DataFrame): The DataFrame to export.
        filename (str, optional): The path to the output CSV file.
                                  Defaults to './data/output.csv'.
    """
    create_data_folder(filename)
    df.to_csv(filename, index=False)
    logging.info(f"Data exported to {filename}")


def exportToJson(df, filename="./data/output.json"):
    """
    Export a DataFrame to a JSON file, handling UUID conversion.

    Args:
        df (pandas.DataFrame): The DataFrame to export.
        filename (str, optional): The path to the output JSON file.
                                  Defaults to './data/output.json'.
    """
    create_data_folder(filename)
    # Convert DataFrame to dict, handling UUID conversion
    json_data = df.to_dict(orient="records")
    json_data = [{k: uuid_to_str(v) for k, v in record.items()} for record in json_data]

    with open(filename, "w") as f:
        json.dump(json_data, f, indent=2)
    logging.info(f"Data exported to {filename}")
