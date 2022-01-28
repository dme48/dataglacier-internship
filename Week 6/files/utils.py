import yaml
import re
import pandas as pd


def validate_columns(dataframe: pd.DataFrame, config: dict) -> 0 | 1:
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
        print(f"Expected columns not present: {expected_not_provided}")
        print(f"Provided columns not expected: {provided_not_expected}")
        return 0

    return 1


def validate_row_count(dataframe: pd.DataFrame, config: dict) -> 0 | 1:
    """
    Compares the number of rows indicated in the config file with the rows in the dataframe.
    Returns 0 if any difference is found, 1 otherwise.
    """
    expected_rows = config["row_count"]
    provided_rows = len(dataframe.index)
    if provided_rows != expected_rows:
        print("Number of rows indicated in config file not the same as in dataframe.")
        print(f"Expected rows: {expected_rows}")
        print(f"Provided rows: {provided_rows}")
        return 0

    return 1


def validate_all(dataframe: pd.DataFrame, config: dict) -> 0 | 1:
    """
    Compares the number of rows and the name columns in the dataframe and config file.
    Returns 0 if any difference is found, 1 otherwise.
    """
    col_validation = validate_columns(dataframe, config)
    row_validation = validate_row_count(dataframe, config)
    return col_validation * row_validation


def format_column_names(df: pd.DataFrame) -> None:
    """
    Formats the names in the columns by
        - Turning whitespace into underscores
        - Removing non-ascii characters
        - Lowercasing everything
        - Removing repeated underscores
    """
    # Strip whitespaces at ends BEFORE replacing the rest with "_"
    df.columns = list(map(lambda x: x.strip(), list(df.columns)))
    df.columns = df.columns.str.replace('[^\w]', '_', regex=True)

    df.columns = list(map(remove_non_ascii_characters, list(df.columns)))

    df.columns = df.columns.str.lower()

    df.columns = list(
        map(lambda x: remove_duplicate_char(x, "_"), list(df.columns)))


def remove_duplicate_char(name: str, c: str):
    """Removes any consecutive duplicates of c from name, if any"""
    pattern = c + "{2,}"
    return re.sub(pattern, c, name)


def remove_non_ascii_characters(name: str):
    """Removes any non ascii characters"""
    ascii_projection = name.encode("ascii", errors="ignore")
    return ascii_projection.decode()
