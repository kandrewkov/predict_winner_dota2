from preprocessing_data import Changer
from sklearn.linear_model import LogisticRegression
import pandas as pd

train = pd.read_csv('features.csv')
train = train.drop(['tower_status_radiant', 'tower_status_dire',
                  'barracks_status_radiant', 'barracks_status_dire',
                  'duration', 'match_id' #'start_time'
                    ], axis=1)

X_train, y = train.drop('radiant_win', axis=1),  train['radiant_win']
test = pd.read_csv('features_test.csv')
# test['match_id']
X_test = test.drop('match_id', axis=1)

heroes_feats = ['d1_hero', 'd2_hero', 'd3_hero', 'd4_hero', 'd5_hero',
                'r1_hero', 'r2_hero', 'r3_hero', 'r4_hero', 'r5_hero']  # создадим признак попурлярности героя

categorical_features = ['lobby_type', 'first_blood_team',
                        'first_blood_player1', 'first_blood_player2']

changer = Changer(categorical_features+heroes_feats)
# X_train = changer.selected_heroes(X_train)
X_train, y = changer.fit(X_train, y)
X_test = changer.transform(X_test)

clf = LogisticRegression(max_iter=1000, penalty='l1', solver='saga')
# print(changer.show_nan(X_train))
clf.fit(X_train, y)
coefs = list(zip(clf.coef_[0], X_train.columns))
coefs.sort(key=lambda x:abs(x[0]) )
coefs_names = [coef[1] for coef in coefs if abs(coef[0]) < 0.2]
print(coefs)
print(coefs_names)
print(clf.score(X_train, y), 'score')


# y_pred = pd.DataFrame(clf.predict_proba(X_test)[:, 1], index=test['match_id'], columns=['radiant_win'])
# pd.DataFrame(y_pred).to_csv('y_pred.csv')
# print('saved')

# 0.654221947958449 score
# 0.6875552812917823 score
# 0.6903013473207857 score
# 0.6904144811272241 score


# 0.6902910624292914 without level
# 0.6897768178545717 score without xp
# 0.6879975316260414 score without lh