import logging
import yaml
import pandas as pd
from dask import dataframe as dd


def validate_columns(dataframe, config: dict) -> 0 | 1:
    expected_columns = set(config["columns"])
    provided_columns = set(dataframe.columns)

    if len(expected_columns) != len(provided_columns):
        print("Count of provided and expected columns differed.")
        return

    if expected_columns != provided_columns:
        print("Names of the provided and expected columns differed.")
        expected_not_provided = expected_columns.difference(provided_columns)
        provided_not_expected = provided_columns.difference(expected_columns)
        logging.info(f"Expected columns not present: {expected_not_provided}")
        logging.info(f"Provided columns not expected: {provided_columns}")

def validate_row_count(dataframe, config: dict) -> 0 | 1:
    expected_rows = config["row_count"]
    provided_rows = len(dataframe.index)
    if provided_rows != expected_rows:
        print("Number of rows indicated in config file not the same as in dataframe.")
        logging.info(f"Expected rows: {expected_rows}")
        logging.info(f"Provided rows: {provided_rows}")

if __name__ == "__main__":
    df = pd.DataFrame({"city": ["Rome", "Chicago"], "population": [6, 10]})
    with open("config.yaml") as config_file:
        config = yaml.safe_load(config_file)

    validate_row_count(df, config)