from pandas import DataFrame
from numpy import zeros


class OneHotEncoder:

    def __init__(self, categorical_features):
        self.features = categorical_features
        self.unique_values = None

    def fit(self, X):
        self.unique_values = []
        self.unique_values = [X[feat].unique() for feat in self.features]
        return self.transform(X)

    def transform(self, X):
        size = len(X)
        for values, feat in zip(self.unique_values, self.features):
            print(feat)
            for val in values:
                if val is not None and str(val) != 'nan':
                    X[feat + '=' + str(val)] = DataFrame(zeros(size))
                    X.loc[X[feat] == val, feat + '=' + str(val)] = 1
            X = X.drop(feat, axis=1)
        return X


