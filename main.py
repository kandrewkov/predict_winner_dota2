from preprocessing_data import Changer
from sklearn.linear_model import LogisticRegression
import pandas as pd

train = pd.read_csv('features.csv')
X_train, y = train.drop('radiant_win', axis=1),  train['radiant_win']
X_test = pd.read_csv('features_test.csv')

heroes_feats = ['d1_hero', 'd2_hero', 'd3_hero', 'd4_hero', 'd5_hero',
                'r1_hero', 'r2_hero', 'r3_hero', 'r4_hero', 'r5_hero']  # создадим признак попурлярности героя
categorical_features = ['lobby_type', 'first_blood_team',
                        'first_blood_player1', 'first_blood_player2']

changer = Changer(categorical_features)
X_train, y = changer.fit(X_train, y)

# changer.transform(X_test)

# clf = LogisticRegression()
# clf.fit(X_train, y)
# y_pred = clf.predict_proba(X_test)[:, 1]
# pd.DataFrame(y_pred).to_csv('y_pred.csv')
