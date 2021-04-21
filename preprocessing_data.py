from one_hot_encoder import OneHotEncoder
from sklearn.preprocessing import StandardScaler

class Changer:

    def __init__(self, uniq_values, categorical_features):
        self.X_test = None
        self.X_train = None
        self.y_train = None
        self.y_test = None
        self.encoder = None
        self.scaler = None
        self.cat_feats = None
        self.uniq_values = None

    def fill_nan(self, X):
        return X

    def delete_corr(self, X,  delta=0.6):
        '''delta - float value'''
        return X

    def find_abnormal_values(self, drop=True):
        if drop:

        else:


    def scale(self, X, bias='median', interval='range'):
        '''
        X_norm = (X - bias)/ interval

        :param X:
        :param bias:
        median - is good for not Gaussian distribution,
        mean - is good for Gaussian distribution,
        min - is good for x to [0,1]

        :param interval:
        'range' = Xmax-Xmin - is good for not Gaussian distribution,
        'std' - is good for Gaussian distribution,
        'centr' = [0.75, 0.25] q
        :return: scaled X
        '''


        return X

    def fit(self, X, y):

        self.X_train = X
        self.y_train = y
        self.encoder = OneHotEncoder()
        self.X_train = self.fill_nan(self.X_train)
        self.X_train = self.delete_corr(self.X_train)
        self.X_train = self.encoder.transform(self.X_train)
        self.find_abnormal_values()
        self.X_train = self.scale(self.X_train)

    def transform(self, X):
        if self.encoder is None:
            print("Model have not got OneHotEncoder. Try to fit Changer")
        self.X_test = X

        self.X_test = self.fill_nan(self.X_test)
        self.X_test = self.delete_corr(self.X_test)
        self.X_test = self.encoder.transform(X)
        self.X_test = self.scale(self.X_test)


    def fit_transform(self, X, y):
        self.X_train = X
        self.y_train = y