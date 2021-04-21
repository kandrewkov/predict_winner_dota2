from one_hot_encoder import OneHotEncoder
from sklearn.preprocessing import StandardScaler
from round_catecorical_values import Rounder
from pandas import DataFrame

class Changer:

    def __init__(self, uniq_values, categorical_features):
        self.cat_feats = categorical_features
        self.uniq_values = uniq_values
        self.corr_feats = None

        self.X_test = None
        self.X_train = None
        self.y_train = None

        self.encoder = None
        self.scaler = None
        self.rounder = None

    def round_catecorical_features(self, X):

        return X

    def fill_nan(self, X, time_non_happening_event=450):

        have_null_feats = []
        for feat in X.columns:
            n = X[feat].isnull().sum()
            if n > 0:
                have_null_feats.append(feat)

        null_times_plus = []
        null_times_minus = []
        for feat in have_null_feats:
            if 'time' in feat:
                if X[feat].min() >= 0:
                    null_times_plus.append(feat)
                else:
                    null_times_minus.append(feat)

        X[null_times_plus] = X[null_times_plus].fillna(time_non_happening_event)
        X[null_times_minus] = X[null_times_minus].fillna(-50)
        return X

    def delete_corr(self, X,  border=0.6):
        '''border - float value'''
        features_corr_matrix = DataFrame(X.corr)
        self.corr_feats = []
        for i, feat_x in enumerate(features_corr_matrix.columns):
            for feat_y in features_corr_matrix.columns[i:]:
                if feat_y != feat_x:
                    if features_corr_matrix[feat_x][feat_y] > border:
                        self.corr_feats.append((features_corr_matrix[feat_x][feat_y], feat_x, feat_y))
        #                 print(Corr[feat_x][feat_y], feat_x, feat_y)
        self.corr_feats.sort(key=lambda x: x[0])

        return X

    def find_abnormal_values(self, drop=True):
        for feat in self.X_train.columns:
            median = self.X_train[feat].median()
            quantile_1 = self.X_train[feat].quantile(q=0.25)
            quantile_3 = self.X_train[feat].quantile(q=0.75)
            iqr = quantile_3 - quantile_1



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
        print("start fitting")
        self.X_train = X
        self.y_train = y

        self.rounder = Rounder()
        self.X_train = self.rounder.fit(self.X_train)
        print('Rounded')

        self.encoder = OneHotEncoder(self.cat_feats, self.uniq_values)
        self.X_train = self.encoder.transform(self.X_train)
        print('One hot encoding finished')

        self.X_train = self.fill_nan(self.X_train)
        print('Gaps filled')

        self.X_train = self.delete_corr(self.X_train)
        print('correlated features removed')

        # self.find_abnormal_values()
        self.X_train = self.scaler.fit(self.X_train)
        print('The values of the features scaled')
        print('end of fitting')

    def transform(self, X):
        if self.encoder is None:
            print("Model have not got OneHotEncoder. Try to fit Changer")
        self.X_test = X

        self.X_test = self.fill_nan(self.X_test)
        self.X_test = self.delete_corr(self.X_test)
        self.X_test = self.encoder.transform(self.X_test)
        self.X_test = self.scale(self.X_test)
