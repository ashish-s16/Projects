#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression
lr= LogisticRegression()
from sklearn.tree import DecisionTreeClassifier
dt= DecisionTreeClassifier()
from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier(n_estimators=100, n_jobs=2, random_state=42)

from imblearn.over_sampling import RandomOverSampler, SMOTE


# In[6]:

print("importing data from source")

try:
    wine_data = pd.read_csv('https://raw.githubusercontent.com/edyoda/data-science-complete-tutorial/master/Data/winequality-white.csv', sep=';')
    print("data imported successfully")
except Exception as inst:
    print("error :", inst.args[1])

def reduced_category(r):
    if r <= 3:
        return 1
    elif r<= 6:
        return 2
    else:
        return 3

wine_data.quality = wine_data.quality.map(reduced_category)

sampler = RandomOverSampler()
feature_s, target_s = sampler.fit_sample(wine_data.drop(columns=['quality']), wine_data['quality'])

trainX, testX, trainY, testY = train_test_split(feature_s, target_s)

models = {"Logistic Regression":lr, "Decision tree": dt, "random forest": rf}

score_max=-1
for name, model in models.items():
    my_pipeline = Pipeline([('std_scaler', StandardScaler()),
                          (name, model)])
    my_pipeline.fit(trainX, trainY)
    score_=my_pipeline.score(testX, testY)
    print("accuracy of ", name,":- ", score_)
    if score_>score_max:
        score_max = score_
        score_name= name
        score_model = model
print("selecting ", score_name, "for prediction.")

print("selecting one of the entries at random from test data")

random_data_index = np.random.randint(0, len(testX))
random_data = testX[random_data_index:random_data_index+1]

print(random_data)

my_pipeline = Pipeline([('std_scaler', StandardScaler()),
                          (name, score_model)])
my_pipeline.fit(trainX, trainY)

print("Predicting with an accuracy of ", score_max)
print("The wine is of quality ", my_pipeline.predict(random_data)[0])
print("The actual quality of wine is", testY.iloc[random_data_index])

