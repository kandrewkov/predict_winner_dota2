class Scaler:
    def __init__(self):
        self.biases = None
        self.intervals = None

    def fit(self, X, bias_type='median', interval_type='range'):
        '''
        X_norm = (X - bias)/ interval

        :param X:
        :param bias_type:
        median - is good for not Gaussian distribution,
        mean - is good for Gaussian distribution,
        min - is good for x to [0,1]

        :param interval_type:
        'range' = Xmax-Xmin - is good for not Gaussian distribution,
        'std' - is good for Gaussian distribution,
        'centr' = [0.75, 0.25] q
        :return: scaled X
        '''
        self.biases = []
        self.intervals = []

        bias = 0
        interval = 1
        for feat in X.columns:
            if bias_type == 'median':
                bias = X[feat].median()
            elif bias_type == 'mean':
                bias = X[feat].mean()
            elif bias_type == 'min':
                bias = X[feat].min()

            if interval_type == 'range':
                interval = X[feat].max() - X[feat].min()
            elif interval_type == 'std':
                interval = X[feat].std()
            elif interval_type == 'center':
                interval = X[feat].quantile(q=0.75) - X[feat].quantile(q=0.25)

            self.biases.append(bias)
            self.intervals.append(interval)
            X[feat] = (X[feat] - bias)/interval
        return X

    def transform(self, X):
        for feat, bias, interval in zip(X.columns, self.biases, self.intervals):
            X[feat] = (X[feat] - bias) / interval
        return X
