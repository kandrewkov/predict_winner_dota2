from preprocessing_data import Changer
import pandas as pd

train = pd.read_csv('features.csv')
X_train, y = train.drop('radiant_win', axis=1),  train['radian_win']
X_test = pd.read_csv('features.csv')

changer = Changer()
X_train, y = changer.fit(X_train, y)

changer.transform(X_test)