import utils
import yaml
from dask import dataframe as dd

# Load the config
with open("config.yaml") as config_file:
    df_config = yaml.safe_load(config_file)

# Use the config to load the dataframe
df = dd.read_csv(df_config["current_file_name"],
                 sep=df_config["current_delimiter"],
                 compression=df_config["current_compression"])

# The validation will fail if we call it before formatting the df
print("BEFORE FORMATTING:")
print("------------------")
utils.validate_all(df, df_config)

utils.format_column_names(df)
# But now it passes
print("\nAFTER FORMATTING")
print("------------------")
utils.validate_all(df, df_config)
print("Finished validating")


# Finally we save it using the parameters in the config file
print("Compressing file...")
df.to_csv(df_config["desired_file_name"],
          sep=df_config["desired_delimiter"],
          compression=df_config["desired_compression"],
          index=False,
          single_file=True)

print("Finished compressing file.")

