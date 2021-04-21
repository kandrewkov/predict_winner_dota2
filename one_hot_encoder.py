from pandas import DataFrame
from numpy import zeros


class OneHotEncoder:

    def __init__(self, categorical_features, unique_values):
        self.features = categorical_features
        self.unique_values = unique_values

    def transform(self, X):
        size = len(X)
        for i, feat in enumerate(self.features):
            # print(feat)
            for val in self.unique_values[i]:
                X[feat + '=' + str(val)] = DataFrame(zeros(size))
                X.loc[X[feat] == val, feat + '=' + str(val)] = 1
        return X

