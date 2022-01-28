import logging
import yaml
import pandas as pd
from dask import dataframe as dd


def validate_columns(dataframe, config: dict) -> 0 | 1:
    """
    Compares the columns in the config file with the columns in the dataframe.
    Returns 0 if any difference is found, 1 otherwise.
    """
    expected_columns = set(config["columns"])
    provided_columns = set(dataframe.columns)

    if len(expected_columns) != len(provided_columns):
        print("Count of provided and expected columns differed.")
        return 0

    if expected_columns != provided_columns:
        print("Names of the provided and expected columns differed.")
        expected_not_provided = expected_columns.difference(provided_columns)
        provided_not_expected = provided_columns.difference(expected_columns)
        logging.info(f"Expected columns not present: {expected_not_provided}")
        logging.info(f"Provided columns not expected: {provided_columns}")
        return 0

    return 1


def validate_row_count(dataframe, config: dict) -> 0 | 1:
    """
    Compares the number of rows indicated in the config file with the rows in the dataframe.
    Returns 0 if any difference is found, 1 otherwise.
    """
    expected_rows = config["row_count"]
    provided_rows = len(dataframe.index)
    if provided_rows != expected_rows:
        print("Number of rows indicated in config file not the same as in dataframe.")
        logging.info(f"Expected rows: {expected_rows}")
        logging.info(f"Provided rows: {provided_rows}")
        return 0

    return 1

def validate_all(dataframe, config: dict) -> 0 | 1:
    """
    Compares the number of rows and the name columns in the dataframe and config file.
    Returns 0 if any difference is found, 1 otherwise.
    """
    col_validation = validate_columns(dataframe, config)
    row_validation = validate_row_count(dataframe, config)
    return col_validation * row_validation


if __name__ == "__main__":
    df = pd.DataFrame({"city": ["Rome", "Chicago"], "population": [6, 10]})
    with open("config.yaml") as config_file:
        config = yaml.safe_load(config_file)

    validate_row_count(df, config)
