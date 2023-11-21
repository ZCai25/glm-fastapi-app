import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

# list of selected features of the final model in the notebook
selected_features = ['x5_saturday', 'x81_July', 'x81_December', 'x31_japan',
                     'x81_October', 'x5_sunday', 'x31_asia', 'x81_February',
                     'x91', 'x81_May', 'x5_monday', 'x81_September', 'x81_March',
                     'x53', 'x81_November', 'x44', 'x81_June', 'x12', 'x5_tuesday',
                     'x81_August', 'x81_January', 'x62', 'x31_germany', 'x58', 'x56']


def transform_and_select_features(data):
    # 1. Fixing the money and percents#
    data['x12'] = data['x12'].str.replace('$', '', regex=True)
    data['x12'] = data['x12'].str.replace(',', '', regex=True)
    data['x12'] = data['x12'].str.replace(')', '', regex=True)
    data['x12'] = data['x12'].str.replace('(', '-', regex=True)
    data['x12'] = data['x12'].astype(float)
    data['x63'] = data['x63'].str.replace('%', '', regex=True)
    data['x63'] = data['x63'].astype(float)

    # 2. With mean imputation from data set

    # handle case when there is only one null value in the column in one row
    # fill the missing value with 0
    if (data.isnull().sum() == 1).any():
        columns_to_impute = data.columns[data.isnull().sum() == 1].tolist()
        data[columns_to_impute] = data[columns_to_impute].fillna(0)

    imputer = SimpleImputer(missing_values=np.nan, strategy='mean')

    data_to_drop = ['x5', 'x31', 'x81', 'x82']
    data_imputed_array = imputer.fit_transform(data.drop(columns=data_to_drop))

    # Construct DataFrame
    data_imputed = pd.DataFrame(
        data_imputed_array, columns=data.drop(columns=data_to_drop).columns)
    std_scaler = StandardScaler()
    data_imputed_std = pd.DataFrame(std_scaler.fit_transform(
        data_imputed), columns=data_imputed.columns)

    # 3. create dummies
    dumb5 = pd.get_dummies(data['x5'], drop_first=True,
                           prefix='x5', prefix_sep='_', dummy_na=True)
    data_imputed_std = pd.concat([data_imputed_std, dumb5], axis=1, sort=False)

    dumb31 = pd.get_dummies(
        data['x31'], drop_first=True, prefix='x31', prefix_sep='_', dummy_na=True)
    data_imputed_std = pd.concat(
        [data_imputed_std, dumb31], axis=1, sort=False)

    dumb81 = pd.get_dummies(
        data['x81'], drop_first=True, prefix='x81', prefix_sep='_', dummy_na=True)
    data_imputed_std = pd.concat(
        [data_imputed_std, dumb81], axis=1, sort=False)

    dumb82 = pd.get_dummies(
        data['x82'], drop_first=True, prefix='x82', prefix_sep='_', dummy_na=True)
    data_imputed_std = pd.concat(
        [data_imputed_std, dumb82], axis=1, sort=False)

    del dumb5, dumb31, dumb81, dumb82

    return data_imputed_std
