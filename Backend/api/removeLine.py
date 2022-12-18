import pandas as pd
def treureColumna():
    df = pd.read_csv('test.csv')
    # If you know the name of the column skip this
    first_column = df.columns[0]
    # Delete first
    df = df.drop([first_column], axis=1)
    df.to_csv('test.csv', index=False)