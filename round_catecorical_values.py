class Rounder:
    def __init__(self):
        self.counts_features = None
        self.replaceable_values = None
        self.possible_numbers = None

    def fit(self, X, counts_features=None, border=1000):
        if counts_features is None:
            self.counts_features = ['dire_ward_sentry_count', 'radiant_ward_sentry_count', 'radiant_tpscroll_count']
        else:
            self.counts_features = counts_features

        self.replaceable_values = []
        self.possible_numbers = []

        for feat in self.counts_features:
            d = dict(X[feat].value_counts())
            keys = []
            for key in d:
                #         print(key, d[key], d[key]>1000)
                if d[key] > border:
                    self.keys.append(key)
                #             print('keys', keys)
                else:
                    self.possible_numbers.append(keys)
                    self.replaceable_values.append(key)

                    for i in range(len(X)):
                        if X[feat].iloc[i] not in keys:
                            X[feat].iloc[i] = key
                    break
        return X

    def transform(self, X):
        if self.keys is None:
            return print('Rounder dont fitted')

        for numbers, border, feat in zip(self.possible_numbers, self.replaceable_values, self.counts_features):
            for i in range(len(X)):
                if X[feat].iloc[i] not in numbers:
                    X[feat].iloc[i] = border
        return X
