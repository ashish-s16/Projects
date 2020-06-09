#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Importing necessary modules and assigning objects

import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedShuffleSplit
import matplotlib.pyplot as plt
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LinearRegression
lr= LinearRegression()

from sklearn.tree import DecisionTreeRegressor
dt= DecisionTreeRegressor()

from sklearn.ensemble import RandomForestRegressor
rf = RandomForestRegressor(n_estimators=100, n_jobs=2, random_state=42)


# In[12]:


#importing file
print("Importing data.csv file")
try:
    housing = pd.read_csv("data.csv")
    print("file imported successfully")
except Exception as inst:
    print("error :", inst.args[1])

print("spliting data into testing and training")
split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
for train_index, test_index in split.split(housing, housing['CHAS']):
    strat_train_set = housing.loc[train_index]
    strat_test_set = housing.loc[test_index]

training_data = strat_train_set.copy()

#removing outlier from RM
print("Removing outlier from Training Data")
outlier_index = training_data[(training_data.RM<7) & (training_data.MEDV>49)].index.to_list()
outlier_index.extend(training_data[(training_data.RM<4) & (training_data.MEDV>20)].index.to_list())
training_data.drop(labels=outlier_index, inplace=True)


trainX = training_data.drop(columns=['MEDV'])
trainY = training_data['MEDV']

testX = strat_test_set.drop(columns=['MEDV'])
testY = strat_test_set.MEDV

models = {"Linear Regression":lr, "Decision tree": dt, "random forest": rf}
maxx=-1
for name, model in models.items():
    my_pipeline = Pipeline([('imputer', SimpleImputer(strategy="most_frequent")),
                          ('std_scaler', StandardScaler()),
                          (name, model)])
    my_pipeline.fit(trainX, trainY)
    score_ = my_pipeline.score(testX, testY)
    print("accuracy of ", name,"is :- ", score_)
    if score_ > maxx:
        maxx=score_
        final_model = model    #Selecting the best model
        model_name = name

print("Using ", name)
x=np.random.randint(0,len(testX))
random_testing_row = testX[x:x+1]
print("Predicting with below sample data ")
print("")
print(random_testing_row)

print("predicting with an accuracy of", np.round(my_pipeline.score(testX, testY),4)*100,"%")
print("Price of house would be ", np.round(my_pipeline.predict(random_testing_row)[0],2),"millions")

