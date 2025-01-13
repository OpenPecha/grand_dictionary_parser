import csv
import pandas as pd


def csv_to_df(file_path):
    return pd.read_csv(file_path)

def get_new_df(df, columns):
    return df[columns]