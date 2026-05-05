#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  4 10:05:44 2026

@author: jeppelund
"""

# hent data fra adresse og valgkreds

import requests as rq
import pandas as pd

url = "https://api.dataforsyningen.dk/adresser?vejnavn=J.M.Thieles%20Vej&husnr=8&postnr=1961"

res = rq.get(url)
data = res.json()

resdf = pd.json_normalize(data)







### 2) data retrieval
import pandas as pd

csv_fil = "dataVideoMLIII.csv"

bolig = pd.read_csv(csv_fil)

print(bolig.head())

dfbolig = pd.read_excel("/Users/jeppelund/Documents/Dataanalyse - 2.semester/Valgfag - NLP og Deep Learning/Uge 19/boligstart.xlsx")


import numpy as np

pd.options.display.float_format = '{:,.0f}'.format

dfbolig.info



### 3.1) data cleaning

# pris – numerisk
dfbolig['prisnum'] = pd.to_numeric(dfbolig['pris'].str.replace("[. a-z]", "", regex=True))

# subset data
dfboligsub = dfbolig.query('~type.str.startswith("Hel")')
dfboligsub = dfboligsub.query('~type.str.startswith("Fritid")')
dfboligsub = dfboligsub.query('~kvm.str.startswith("-")')

# ejerudg – numerisk
dfboligsub['ejerudgnum'] = pd.to_numeric(dfboligsub['ejerudg'].str.replace("[. a-zA-Z/]", "", regex=True))

# kvm – numerisk
dfboligsub['kvmnum'] = pd.to_numeric(dfboligsub['kvm'].str.replace(" m²", "", regex=True))

# grund – numerisk
dfboligsub['grundnum'] = dfboligsub['grund'].str.replace(" m²", "", regex=True)
dfboligsub['grundnum'] = pd.to_numeric(dfboligsub['grundnum'].str.replace("[^0-9]", "", regex=True))

# værelser – numerisk(?)
dfboligsub['vaercat'] = pd.to_numeric(dfboligsub['vaer'].str.replace("[^0-9]", "", regex=True))

### Energi – kategori
testrækker = dfboligsub.loc[1:5, 'energi']
testrækker2 = dfboligsub['energi'].value_counts()
dfboligsub['energicat'] = dfboligsub['energi'].str.replace("Energimærke ", "")
testrækker2 = dfboligsub['energicat'].value_counts()
dfboligsub['energicat'] = dfboligsub['energicat'].str.replace("Intet energimærke", "I")
dfboligsub['energicat'] = dfboligsub['energicat'].str.replace("A[0-9]+", "A", regex=True)

# fjern boliger uden energimærke
dfboligsub = dfboligsub.query('~energicat.str.contains("I")')

### 3.2) Feature engineering

# alder ud fra årstal
#dfboligsub['alder'] = dfboligsub['opført']
dfboligsub['aldernum'] = 2024 - pd.to_numeric(dfboligsub['alder'].str.replace("Opført ", "", regex=True))

### 4) data exploration

#### 4.1) simple exploration – numeric
dfboligsub['prisnum'].plot.hist(bins=50)
dfboligsub['ejerudgnum'].plot.hist(bins=90)
dfboligsub['kvmnum'].plot.hist(bins=50)
dfboligsub['grundnum'].plot.box()
dfboligsub['aldernum'].plot.hist(bins=50)
dfboligsub['aldernum'].plot.box()

#### 4.1) simple exploration – categorical
testrækker2.plot.bar()


#### 4.2) combined – numeric + numeric
dfboligsub.plot.scatter(x='kvmnum', y='prisnum')
dfboligsub.plot.scatter(x='ejerudgnum', y='prisnum')
dfboligsub.plot.scatter(x='aldernum', y='prisnum')

#### 4.2) combined – categorical + numeric
statenergi = (dfboligsub.groupby('energicat')['prisnum'].mean().astype(int).reset_index())

statenergi.plot.bar(x='energicat', y='prisnum')

#### 5 Model
#### 5.1) Import libraries

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import r2_score

# importing full data
dfbolignew=pd.read_pickle("bolig.pickle")

#### 5.1) model selection and variables
# create instances
lr=LinearRegression()
sc=StandardScaler()
oh=OneHotEncoder()

# filter out numeric variables
mv=list(dfbolignew.columns)
newn=[print(e) for e in mv if e.find("num") > 0]
dfbolignew['husnr'].info
dfboligNum=dfbolignew[newn]

# scale
dfboligNumSc=pd.DataFrame(sc.fit_transform(dfboligNum))
dfboligNumSc.columns=newn

# remove target variable
y=dfboligNumSc['prisnum']
X=dfboligNumSc.iloc[:,[1,2,3,4,5,6]]
XZip=dfbolignew['postnr']

# split in test - train
X_train, X_test, y_train, y_test =train_test_split(X, y, test_size=0.2)

# fit the model to the training data
model=lr.fit(X_train,y_train)

# now predict
predprice=lr.predict(X_test)
r2pric=r2_score(y_test,predprice)
print(r2pric)