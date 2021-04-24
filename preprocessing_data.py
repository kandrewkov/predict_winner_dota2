from one_hot_encoder import OneHotEncoder
from round_catecorical_values import Rounder
from scaler import Scaler
from pandas import DataFrame
from  numpy import zeros

class Changer:

    def __init__(self, categorical_features):
        self.cat_feats = categorical_features
        self.corr_feats = None
        self.features_corr_matrix = None
        self.encoder = None
        self.scaler = None
        self.rounder = None

    def show_nan(self, X):
        have_null_feats = []
        for feat in X.columns:
            n = X[feat].isnull().sum()
            if n > 0:
                have_null_feats.append(feat)
        print(have_null_feats)
        return have_null_feats

    def fill_nan(self, X, time_non_happening_event=450):
        # have_null_feats = []
        # for feat in X.columns:
        #     n = X[feat].isnull().sum()
        #     if n > 0:
        #         have_null_feats.append(feat)
        #
        # null_times_plus = []
        # null_times_minus = []
        # for feat in have_null_feats:
        #     if 'time' in feat:
        #         if X[feat].min() >= 0:
        #             null_times_plus.append(feat)
        #         else:
        #             null_times_minus.append(feat)
        #
        # X[null_times_plus] = X[null_times_plus].fillna(time_non_happening_event)
        # X[null_times_minus] = X[null_times_minus].fillna(-50)
        # print(have_null_feats)

        return X.fillna(0)

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

        #  delete features with lh, xp, for all players

        #                 print(Corr[feat_x][feat_y], feat_x, feat_y)


        popular_corr_feats = sorted(popular_corr_feats.items(), key=lambda element: element[1])

        return X

    # def find_abnormal_values(self, drop=True):
    #     for feat in X.columns:
    #         median = X[feat].median()
    #         quantile_1 = X[feat].quantile(q=0.25)
    #         quantile_3 = X[feat].quantile(q=0.75)
    #         iqr = quantile_3 - quantile_1
    #     return X, y

    def selected_heroes(self, X):

        team_r = ('r'+str(i)+'_hero' for i in range(1, 6))
        team_d = ('r'+str(i)+'_hero' for i in range(1, 6))

        size = len(X)

        for hero in range(1, 114):
            X['rh=' + str(hero)] = DataFrame(zeros(size))
            X['dh=' + str(hero)] = DataFrame(zeros(size))

        for r_hero, d_hero in zip(team_r, team_d):
            for hero in range(1, 114):
                X.loc[X[r_hero] == hero, 'rh=' + str(hero)] = 1
                X.loc[X[d_hero] == hero, 'dh=' + str(hero)] = 1
                # print(hero, X.loc[X[d_hero] == hero, 'dh=' + str(hero)])
            X = X.drop([r_hero, d_hero], axis=1)

        return X.drop(['rh=24', 'dh=24', 'rh=107', 'dh=107', 'rh=108',
                       'dh=108', 'rh=111', 'dh=111', 'rh=113', 'dh=113'], axis=1)

    def fit(self, X, y):
        print("start fitting:")

        self.rounder = Rounder()
        X = self.rounder.fit(X, border=2000)
        print('-Rounded')

        self.encoder = OneHotEncoder(self.cat_feats)
        X = self.encoder.fit(X)

        print('-One hot encoding finished')
        X = self.selected_heroes(X)

        X = self.fill_nan(X)
        print('-Gaps filled')

        # self.X = self.delete_corr(X)
        self.corr_feats = []
        for feat in X.columns:
            if 'xp' in feat or 'lh' in feat:
                self.corr_feats.append(feat)
        X = X.drop(self.corr_feats, axis=1)
        print('-Correlated features removed')

        # self.find_abnormal_values()
        self.scaler = Scaler()
        X = self.scaler.fit(X)
        print('-The values of the features scaled')
        print('end of fitting.')
        return X, y

    def transform(self, X):
        if self.encoder is None:
            return print("Model has not got OneHotEncoder. Try to fit Changer")
        if self.scaler is None:
            return print("Model has not got Scaler. Try to fit Changer")
        if self.rounder is None:
            return print("Model has not got Rounder. Try to fit Changer")

        print('start transform:')

        X = self.rounder.transform(X)
        print('-Rounded')

        X = self.encoder.transform(X)
        X = self.selected_heroes(X)
        print('-One hot encoding finished')

        X = self.fill_nan(X)
        print('-Gaps filled')

        # X = self.delete_corr(X)
        print(self.corr_feats)
        X = X.drop(self.corr_feats, axis=1)
        print('-Correlated features removed')

        X = self.scaler.transform(X)
        print('-The values of the features scaled')
        print('end of transforming')
        return X
