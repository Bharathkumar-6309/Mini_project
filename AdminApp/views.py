from django.shortcuts import render
import pymysql
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import random

# Create your views here.
def index(request):
    return render(request,'AdminApp/index.html')
def login(request):
    return render(request,'AdminApp/Admin.html')
def LogAction(request):
    username=request.POST.get('username')
    password=request.POST.get('password')
    if username=='Admin' and password=='Admin':      
        return render(request,'AdminApp/AdminHome.html')
    else:
        context={'data':'Login Failed ....!!'}
        return render(request,'AdminApp/Admin.html',context)
def home(request):
    return render(request,'AdminApp/AdminHome.html')
global df
def LoadData(request):
    global df
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    df=pd.read_csv(BASE_DIR+"\\dataset\\accident.csv")
    #data.fillna(0, inplace=True)
    context={'data':"Dataset Loaded\n"}
    
    return render(request,'AdminApp/AdminHome.html',context)
global X
global y
global X_train,X_test,y_train,y_test
global df1
def split(request):
    global df1
    global X_train,X_test,y_train,y_test
    df.drop('Operational date',axis=1,inplace=True)
    df.drop('Intersection Type And Control',axis=1,inplace=True)
    df.fillna(0,inplace=True)
    df1=pd.DataFrame({col: df[col].astype('category').cat.codes for col in df}, index=df.index)
    X=df1[['Rural/Urban','Causes','Road Feature','Road condition','Weather Condition','Vehicle Responsible']]
    y=df1[['Type of Accident']]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    context={"data":"Preprocess Has Done"}
    return render(request,'AdminApp/AdminHome.html',context)
global ranacc
global rfc
def runRandomForest(request):
    global ranacc
    global rfc
    rfc = RandomForestClassifier(n_estimators=100)  
    rfc.fit(X_train, y_train)
    prediction=rfc.predict(X_test)
    ranacc=accuracy_score(y_test, prediction)*100
    context={"data":"RandomForest Accurary: "+str(ranacc)}
    return render(request,'AdminApp/AdminHome.html',context)

    
global svmacc
global model
def runSVM(request):
    global svmacc
    global model
    model = svm.SVC(random_state=0)  
    model.fit(X_train, y_train)
    prediction=model.predict(X_test)
    svmacc=accuracy_score(y_test, prediction)*100
    context={"data":"SVM Accurary: "+str(svmacc)}
    return render(request,'AdminApp/AdminHome.html',context)
global decacc
global dec
def runDecistionTree(request):
    global decacc
    global dec
    dec = DecisionTreeClassifier()
    dec.fit(X_train, y_train)
    prediction=dec.predict(X_test)
    decacc=accuracy_score(y_test, prediction)*100
    context={"data":"Decision Tree Accurary: "+str(decacc)}
    return render(request,'AdminApp/AdminHome.html',context)

global ranacc,decacc,svmacc    
def runComparision(request):   
    global ranacc,decacc,svmacc
    bars = ['RandomForest Accuracy','Decision Accurary','Support Vector Accurary']
    height = [ranacc,decacc, svmacc]
    y_pos = np.arange(len(bars))
    plt.bar(y_pos, height)
    plt.xticks(y_pos, bars)
    plt.show()
    return render(request,'AdminApp/AdminHome.html')
def RoadFeature(request):
    sns.countplot(y=df['Weather Condition'],hue=df['Type of Accident'],data=df1)
    plt.show()
    return render(request,'AdminApp/AdminHome.html')
def TypeofAccidents(request):
    sns.countplot(x=df['Road condition'],hue=df['Type of Accident'],data=df1)
    plt.show()
    return render(request,'AdminApp/AdminHome.html')
def PredictByCuases(request):
    sns.set(rc={'figure.figsize':(10.7,8.27)})
    sns.countplot(y=df.Causes, data=df1)
    plt.show()
    return render(request,'AdminApp/AdminHome.html')


def predict(request):
    return render(request,'AdminApp/Prediction.html')

def PredAction(request):
    global dec
    area=request.POST.get('area')
    cause=request.POST.get('cause')
    feature=request.POST.get('feature')
    condition=request.POST.get('condition')
    weather=request.POST.get('weather')
    number = random.randint(1000,9999)
    pred=dec.predict([[area,cause,feature,condition,weather,number]])
    if pred[0]==0:
        context={'data':"Accident Predicted and The Type Of Accident is:: Fatal"}
        return render(request,'AdminApp/PredictedData.html',context)
    elif pred[0]==1:
        context={'data':"Accident Predicted and The Type Of Accident is:: Grievious injury"}
        return render(request,'AdminApp/PredictedData.html',context)
    elif pred[0]==2:
        context={'data':"Accident Predicted and The Type Of Accident is:: Minor injury"}
        return render(request,'AdminApp/PredictedData.html',context)
    elif pred[0]==3:
        context={'data':"Accident Predicted and The Type Of Accident is:: Non injury"}
        return render(request,'AdminApp/PredictedData.html',context)
    else:
        context={'data':"No Accident Predicted"}
        return render(request,'AdminApp/PredictedData.html',context)
        
    
        
        
    
    



    




    

