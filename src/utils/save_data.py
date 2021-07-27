import json

import pandas as pd


def save_to_csv(_data, _filepath, _new_dir=None):
    """
    Function exports data to csv file.

    :param _data: list or array - whatever Pandas DataFrame can handle.
    :type _data: list
    :param _filepath: name of the exported file
    :type _filepath: Path
    :param _new_dir: user can create a new directory for the data by passing string
    :type _new_dir: str
    :return: None
    """

    try:
        # make Pandas DF and export to csv
        data_to_export = pd.DataFrame(_data)
        data_to_export.to_csv(_filepath)

        print(f"Data exported to: {_filepath}")

    except NotADirectoryError as err:
        print(err)


def dump_data(data, path):
    """
    Method dumps simulation data to json file

    :param data: data in dictionary
    :param path: path of the file to save
    :return: None
    """

    with open(path, "w") as file:
        json.dump(data, file)

    print("Data to viz save complete")
