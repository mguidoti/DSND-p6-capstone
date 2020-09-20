import pandas as pd


def to_pickle(df, path):
    """This is the most unnecessary function that I wrote for this project.
    However, for the sake of consistency, since I'm modularizing all ETL
    process, I decided to write this function.

    Args:
        df (pandas.DataFrame): Dataframe to be loaded into a pickle file
        path (str): Filepath of the pickle file to be generated
    """

    df.to_pickle(path)
