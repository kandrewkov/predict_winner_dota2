from one_hot_encoder import OneHotEncoder
from round_catecorical_values import Rounder
from scaler import Scaler
from pandas import DataFrame
from  numpy import zeros

class Changer:

    def __init__(self, categorical_features, border=1000):
        self.cat_feats = categorical_features
        self.corr_feats = None
        self.features_corr_matrix = None
        self.encoder = None
        self.scaler = None
        self.rounder = None
        self.border = border
        self.new_hero_features = None

    def show_nan(self, X):
        have_null_feats = []
        for feat in X.columns:
            n = X[feat].isnull().sum()
            if n > 0:
                have_null_feats.append(feat)
        print(have_null_feats)
        return have_null_feats

    def fill_nan(self, X, time_non_happening_event=450):
        have_null_feats = self.show_nan(X)

        for feat in have_null_feats:
            X[feat] = X[feat].fillna(X[feat].max())

        # X[null_times_plus] = X[null_times_plus].fillna(time_non_happening_event)
        # X[null_times_minus] = X[null_times_minus].fillna(-50)
        # print(have_null_feats)

        return X

    def delete_corr(self, X,  border=0.6, show=False):
        '''border - float value'''

        if self.corr_feats is None:
            self.corr_feats = []
            for feat in X.columns:
                if 'level' in feat:
                    self.corr_feats.append(feat)

        return X.drop(self.corr_feats, axis=1)

        # popular_corr_feats = {}
        # self.features_corr_matrix = DataFrame(X.corr)
        # self.corr_feats = set([])
        #
        # for i, feat_x in enumerate(self.features_corr_matrix.columns):
        #     for feat_y in self.features_corr_matrix.columns[i:]:
        #         if feat_y != feat_x:
        #             if self.features_corr_matrix[feat_x][feat_y] > border:
        #                 # popular_corr_feats[feat_y] = popular_corr_feats.get(feat_y, 0) + 1
        #                 # popular_corr_feats[feat_x] = popular_corr_feats.get(feat_x, 0) + 1
        #                 self.corr_feats.add(feat_x)
        #                 self.corr_feats.add(feat_y)
        #
        # if show:
        #     print(self.features_corr_matrix[list(self.corr_feats)])

        #  delete features with lh, xp, for all player
        # popular_corr_feats = sorted(popular_corr_feats.items(), key=lambda element: element[1])


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
            X['hero='+str(hero)] = DataFrame(zeros(size))

        for r_hero, d_hero in zip(team_r, team_d):
            for hero in range(1, 114):
                X.loc[X[r_hero] == hero, 'hero='+str(hero)] = 1
                X.loc[X[d_hero] == hero, 'hero='+str(hero)] = -1
                # print(hero, X.loc[X[d_hero] == hero, 'dh=' + str(hero)])
            X = X.drop([r_hero, d_hero], axis=1)

        return X

    def add_new_features(self, X, second_features=None):
        if second_features is None:
            second_features = ['_gold', '_lh', '_deaths', '_xp','_kills',  '_items' ]
        for feat in self.new_hero_features:
            player = feat[:2]
            print('player', player)
            for second_feat in second_features:
                X[feat + '_' + player + second_feat] = X[feat] + X[player+second_feat]
        return X

    def get_non_binary_features(self, X):
        return [feat for feat in X.columns if len(X[feat].unique()) > 2]

    def fit(self, X, y):
        print("start fitting:")

        self.rounder = Rounder()
        X = self.rounder.fit(X, border=self.border)
        print('-Rounded')

        self.encoder = OneHotEncoder(self.cat_feats)
        X, self.new_hero_features = self.encoder.fit(X)

        print('-One hot encoding finished')
        # X = self.selected_heroes(X)

        X = self.fill_nan(X)
        print('-Gaps filled')

        # X = self.delete_corr(X)

        print('-Correlated features removed')

        # self.find_abnormal_values()
        self.scaler = Scaler()
        X = self.scaler.fit(X, features=self.get_non_binary_features(X))
        # 0.6878638280366142
        # 0.6878432582536255
        # 0.689787102746066
        # 0.6902910624292914

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

        X = self.encoder.transform(X)[0]
        # X = self.selected_heroes(X)
        print('-One hot encoding finished')

        # X = self.add_new_features(X)

        X = self.fill_nan(X)
        print('-Gaps filled')

        # X = self.delete_corr(X)
        # print(self.corr_feats)
        print('-Correlated features removed')

        X = self.scaler.transform(X)

        print('-The values of the features scaled')
        print('end of transforming')
        print('_'*50)
        return X
