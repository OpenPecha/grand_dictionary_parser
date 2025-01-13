import pandas as pd
from utils import get_new_df, csv_to_df


def test_get_new_df():
    df = csv_to_df('./test/test_csv.csv')
    columns = ["wordindexid","word","pos"]
    new_df = get_new_df(df, columns)
    expected_df = pd.DataFrame({
        'wordindexid': [1,2,3,],
        'word': ['word1', 'word2', 'word3',],
        'pos': ['pos1', 'pos2', 'pos3',]
    })
    assert new_df.equals(expected_df)



if __name__ == '__main__':
    test_get_new_df()