from one_hot_encoder import OneHotEncoder
from round_catecorical_values import Rounder
from scaler import Scaler
from pandas import DataFrame


class Changer:

    def __init__(self, uniq_values, categorical_features):
        self.cat_feats = categorical_features
        self.uniq_values = uniq_values
        self.corr_feats = None
        self.features_corr_matrix = None

        self.X_test = None
        self.X_train = None
        self.y_train = None

        self.encoder = None
        self.scaler = None
        self.rounder = None

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

    def delete_corr(self, X,  border=0.6, show=False):
        '''border - float value'''
        popular_corr_feats = {}
        self.features_corr_matrix = DataFrame(X.corr)
        self.corr_feats = set([])

        for i, feat_x in enumerate(self.features_corr_matrix.columns):
            for feat_y in self.features_corr_matrix.columns[i:]:
                if feat_y != feat_x:
                    if self.features_corr_matrix[feat_x][feat_y] > border:
                        # popular_corr_feats[feat_y] = popular_corr_feats.get(feat_y, 0) + 1
                        # popular_corr_feats[feat_x] = popular_corr_feats.get(feat_x, 0) + 1
                        self.corr_feats.add(feat_x)
                        self.corr_feats.add(feat_y)

        if show:
            print(self.features_corr_matrix[list(self.corr_feats)])

        #delete features with lh, xp, for all players

        #                 print(Corr[feat_x][feat_y], feat_x, feat_y)


        popular_corr_feats = sorted(popular_corr_feats.items(), key=lambda element: element[1])

        return X

    def find_abnormal_values(self, drop=True):
        for feat in self.X_train.columns:
            median = self.X_train[feat].median()
            quantile_1 = self.X_train[feat].quantile(q=0.25)
            quantile_3 = self.X_train[feat].quantile(q=0.75)
            iqr = quantile_3 - quantile_1


    def fit(self, X, y):
        print("start fitting")
        self.X_train = X
        self.y_train = y

        self.rounder = Rounder()
        self.X_train = self.rounder.fit(self.X_train)
        print('Rounded')

        self.encoder = OneHotEncoder(self.cat_feats)
        self.X_train = self.encoder.fit(self.X_train)
        print('One hot encoding finished')

        self.X_train = self.fill_nan(self.X_train)
        print('Gaps filled')

        # self.X_train = self.delete_corr(self.X_train)
        self.corr_feats = []
        for feat in X.columns:
            if 'xp' in feat or 'lh' in feat:
                self.corr_feats.append(feat)
        self.X_train = self.X_train.drop(self.corr_feats, axis=1)
        print('correlated features removed')

        # self.find_abnormal_values()
        self.scaler = Scaler()
        self.X_train = self.scaler.fit(self.X_train)
        print('The values of the features scaled')
        print('end of fitting')

    def transform(self, X):
        if self.encoder is None:
            return print("Model has not got OneHotEncoder. Try to fit Changer")
        if self.scaler is None:
            return print("Model has not got Scaler. Try to fit Changer")
        if self.rounder is None:
            return print("Model has not got Rounder. Try to fit Changer")
        self.X_test = X

        self.X_test = self.rounder.transform(self.X_test)
        print('Rounded')

        self.X_test = self.encoder.transform(self.X_test)
        print('One hot encoding finished')

        self.X_test = self.fill_nan(self.X_test)
        print('Gaps filled')

        # self.X_test = self.delete_corr(self.X_test)
        self.X_test = self.X_test.drop(self.corr_feats, axis=1)
        print('correlated features removed')

        self.X_test = self.scaler.transform(self.X_test)
