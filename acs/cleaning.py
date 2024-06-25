import pandas as pd
import numpy as np

def dicts_to_df(dicts):
    columns = set().union(*(d.keys() for d in dicts))

    filled_dicts = [{key: d.get(key) for key in columns} for d in dicts]

    return pd.DataFrame(filled_dicts)

def combine_percent_columns(df):
    # open variables/variables_acs5_2022.csv
    variables = pd.read_csv('variables/variables_acs5_2022.csv')

    percent_columns = variables[variables['Label'].str.lower().str.contains(r'\brate\b|\bpercentage\b')]
    percent_columns['Name'].apply(lambda x: x[:-2])

    # for each row in acs_data
    for index, row in df.iterrows():
        # for each column in percent_columns
        for col in percent_columns['Name']:
            # if col + E and col + PE are in acs columns
            if col + 'E' in df.columns and col + 'PE' in df.columns:
                # get col + E and col + PE
                est = row[col + 'E']
                percent_est = row[col + 'PE']

                # if percent_est is nan, set PE to est and set E to nan
                if np.isnan(percent_est) or percent_est == 0:
                    df.at[index, col + 'PE'] = est
                    df.at[index, col + 'E'] = np.nan

def remove_invalid_columns(df):
    # checking for columns with invalid data
    invalid = []
    # for each column except the first 2
    for col in df.columns[2:]:
        valid = False
        # for each value in the column
        for val in df[col]:
            # if the value is not nan and is greater than 0
            if not np.isnan(val) and val > 0:
                valid = True
                break
        if not valid:
            invalid.append(col)
    # remove invalid columns
    df.drop(columns=invalid, inplace=True)

def remove_nonaggregatables(df):
    # open statistics.xlsx
    statistics = pd.read_excel('statistics.xlsx')
    # for each column in acs_data
    for col in df.columns:
        # if it ends in E and not PE
        if col in statistics['agg_var'].values:
            # if pop_var is NaN, delete col from acs_data
            if statistics[statistics['agg_var'] == col]['pop_var'].isnull().values[0]:
                df.drop(columns=[col], inplace=True)
            elif col.endswith('PE') and (col[:-2] + 'E') in df.columns:
                # drop the corresponding E column
                df.drop(columns=[col[:-2] + 'E'], inplace=True)
        # if it ends in E and PE in columns
        if col.endswith('E') and (col[:-1] + 'PE') not in statistics['agg_var'].values and (col[:-1] + 'PE') in df.columns:
            # drop the corresponding PE column
            df.drop(columns=[col[:-1] + 'PE'], inplace=True)

def replace_error_values(df):
    # replace all (X), -, or N with nan
    df.replace('(X)', np.nan, inplace=True)
    df.replace('-', np.nan, inplace=True)
    df.replace('N', np.nan, inplace=True)
    # convert all columns except the first 2 to floats
    for col in df.columns[2:]:
        df[col] = df[col].astype(float)
        # replace all negative values with NaN except the first 4 columns
        df[col] = df[col].apply(lambda x: np.nan if x < 0 else x)