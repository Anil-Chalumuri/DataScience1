import pandas as pd
import os
from sklearn import tree, model_selection, ensemble

path = 'C:\\Users\\Algorithmica\\Downloads'
titanic_train = pd.read_csv(os.path.join(path, 'titanic_train.csv'))
print(titanic_train.shape)
print(titanic_train.info())

features = ['Sex', 'Pclass', 'Embarked','Parch','SibSp']
titanic_train1 = pd.get_dummies(titanic_train, columns=['Sex','Pclass','Embarked'])
X_train = titanic_train1.drop(['PassengerId','Survived','Name','Age','Cabin','Ticket'], axis=1)
y_train = titanic_train['Survived']

classifier = ensemble.RandomForestClassifier(random_state=100, n_jobs=1, verbose=1, oob_score=True)
rf_grid = {'max_depth':[3,4,5,6], 'n_estimators':[5,10,20,30,40], 'max_features':[3,4,5,11]}
grid_classifier = model_selection.GridSearchCV(classifier, rf_grid, cv=10, refit=True, return_train_score=True)
grid_classifier.fit(X_train, y_train)
results = grid_classifier.cv_results_
print(results.get('params'))
print(results.get('mean_test_score'))
print(results.get('mean_train_score'))
print(grid_classifier.best_params_)
print(grid_classifier.best_score_)
final_model = grid_classifier.best_estimator_
final_model.estimators_
print(final_model.oob_score_)

titanic_test = pd.read_csv(os.path.join(path, 'titanic_test.csv'))
print(titanic_test.shape)
print(titanic_test.info())
titanic_test.loc[titanic_test['Fare'].isnull() == True, 'Fare'] = titanic_test['Fare'].mean()

titanic_test1 = pd.get_dummies(titanic_test, columns=['Sex','Pclass','Embarked'])
X_test = titanic_test1.drop(['PassengerId','Name','Age','Cabin','Ticket'], axis=1)
titanic_test['Survived'] = final_model.predict(X_test)
titanic_test.to_csv(os.path.join(path,'submission.csv'), columns=['PassengerId','Survived'], index=False)
