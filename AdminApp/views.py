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
import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt
import random

# =========================
# GLOBAL VARIABLES
# =========================

df = None
df1 = None

X = None
y = None

X_train = None
X_test = None
y_train = None
y_test = None

ranacc = 0
svmacc = 0
decacc = 0

rfc = None
model = None
dec = None

# =========================
# BASIC PAGES
# =========================

def index(request):
    return render(request, 'AdminApp/index.html')


def login(request):
    return render(request, 'AdminApp/Admin.html')


def home(request):
    return render(request, 'AdminApp/AdminHome.html')


# =========================
# LOGIN
# =========================

def LogAction(request):

    username = request.POST.get('username')
    password = request.POST.get('password')

    if username == 'Admin' and password == 'Admin':
        return render(request, 'AdminApp/AdminHome.html')

    else:
        context = {'data': 'Login Failed ....!!'}
        return render(request, 'AdminApp/Admin.html', context)


# =========================
# LOAD DATASET
# =========================

def LoadData(request):

    global df

    try:

        BASE_DIR = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )

        dataset_path = os.path.join(
            BASE_DIR,
            "dataset",
            "accident.csv"
        )

        df = pd.read_csv(dataset_path)

        context = {
            'data': "Dataset Loaded Successfully"
        }

        return render(request, 'AdminApp/AdminHome.html', context)

    except Exception as e:

        context = {
            'data': 'Dataset Loading Error : ' + str(e)
        }

        return render(request, 'AdminApp/AdminHome.html', context)


# =========================
# PREPROCESSING
# =========================

def split(request):

    global df
    global df1
    global X
    global y
    global X_train
    global X_test
    global y_train
    global y_test

    try:

        if df is None:
            context = {'data': "Please Load Dataset First"}
            return render(request, 'AdminApp/AdminHome.html', context)

        data = df.copy()

        # Drop unnecessary columns safely
        columns_to_drop = [
            'Operational date',
            'Intersection Type And Control'
        ]

        for col in columns_to_drop:
            if col in data.columns:
                data.drop(col, axis=1, inplace=True)

        # Fill null values safely
        data = data.fillna("Unknown")

        # Convert all columns to string safely
        for col in data.columns:
            data[col] = data[col].astype(str)

        # Encode categorical data
        df1 = pd.DataFrame({
            col: data[col].astype('category').cat.codes
            for col in data.columns
        }, index=data.index)

        # Required columns
        required_columns = [
            'Rural/Urban',
            'Causes',
            'Road Feature',
            'Road condition',
            'Weather Condition',
            'Vehicle Responsible',
            'Type of Accident'
        ]

        missing_columns = []

        for col in required_columns:

            if col not in df1.columns:
                missing_columns.append(col)

        # Show missing columns clearly
        if len(missing_columns) > 0:

            context = {
                'data': 'Missing Columns : ' + str(missing_columns)
            }

            return render(request, 'AdminApp/AdminHome.html', context)

        # Features
        X = df1[
            [
                'Rural/Urban',
                'Causes',
                'Road Feature',
                'Road condition',
                'Weather Condition',
                'Vehicle Responsible'
            ]
        ]

        # Target
        y = df1['Type of Accident']

        # Split dataset
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42
        )

        context = {
            "data": "Preprocessing Completed Successfully"
        }

        return render(request, 'AdminApp/AdminHome.html', context)

    except Exception as e:

        context = {
            'data': 'Preprocessing Error : ' + str(e)
        }

        return render(request, 'AdminApp/AdminHome.html', context)
        # Features
        X = df1[
            [
                'Rural/Urban',
                'Causes',
                'Road Feature',
                'Road condition',
                'Weather Condition',
                'Vehicle Responsible'
            ]
        ]

        # Target
        y = df1['Type of Accident']

        # Split dataset
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42
        )

        context = {
            "data": "Preprocessing Completed Successfully"
        }

        return render(request, 'AdminApp/AdminHome.html', context)

    except Exception as e:

        context = {
            'data': 'Preprocessing Error : ' + str(e)
        }

        return render(request, 'AdminApp/AdminHome.html', context)


# =========================
# RANDOM FOREST
# =========================

def runRandomForest(request):

    global rfc
    global ranacc

    try:

        if X_train is None:
            context = {'data': "Please Preprocess Dataset First"}
            return render(request, 'AdminApp/AdminHome.html', context)

        rfc = RandomForestClassifier(n_estimators=100)

        rfc.fit(X_train, y_train.values.ravel())

        prediction = rfc.predict(X_test)

        ranacc = accuracy_score(y_test, prediction) * 100

        context = {
            "data": "Random Forest Accuracy : " + str(round(ranacc, 2))
        }

        return render(request, 'AdminApp/AdminHome.html', context)

    except Exception as e:

        context = {
            'data': 'Random Forest Error : ' + str(e)
        }

        return render(request, 'AdminApp/AdminHome.html', context)


# =========================
# SVM
# =========================

def runSVM(request):

    global model
    global svmacc

    try:

        if X_train is None:
            context = {'data': "Please Preprocess Dataset First"}
            return render(request, 'AdminApp/AdminHome.html', context)

        # Lightweight SVM
        model = svm.LinearSVC()

        model.fit(X_train, y_train)

        prediction = model.predict(X_test)

        svmacc = accuracy_score(y_test, prediction) * 100

        context = {
            "data": "SVM Accuracy : " + str(round(svmacc, 2))
        }

        return render(request, 'AdminApp/AdminHome.html', context)

    except Exception as e:

        context = {
            'data': 'SVM Error : ' + str(e)
        }

        return render(request, 'AdminApp/AdminHome.html', context)


# =========================
# DECISION TREE
# =========================

def runDecistionTree(request):

    global dec
    global decacc

    try:

        if X_train is None:
            context = {'data': "Please Preprocess Dataset First"}
            return render(request, 'AdminApp/AdminHome.html', context)

        dec = DecisionTreeClassifier()

        dec.fit(X_train, y_train.values.ravel())

        prediction = dec.predict(X_test)

        decacc = accuracy_score(y_test, prediction) * 100

        context = {
            "data": "Decision Tree Accuracy : " + str(round(decacc, 2))
        }

        return render(request, 'AdminApp/AdminHome.html', context)

    except Exception as e:

        context = {
            'data': 'Decision Tree Error : ' + str(e)
        }

        return render(request, 'AdminApp/AdminHome.html', context)


# =========================
# COMPARISON
# =========================

def runComparision(request):

    global ranacc
    global svmacc
    global decacc

    try:

        bars = [
            'RandomForest',
            'DecisionTree',
            'SVM'
        ]

        height = [ranacc, decacc, svmacc]

        y_pos = np.arange(len(bars))

        plt.figure(figsize=(7, 5))

        plt.bar(y_pos, height)

        plt.xticks(y_pos, bars)

        plt.ylabel("Accuracy")

        BASE_DIR = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )

        graph_path = os.path.join(
            BASE_DIR,
            "Static",
            "comparison.png"
        )

        plt.savefig(graph_path)

        plt.close()

        context = {
            'data': "Comparison Graph Generated Successfully"
        }

        return render(request, 'AdminApp/AdminHome.html', context)

    except Exception as e:

        context = {
            'data': 'Comparison Error : ' + str(e)
        }

        return render(request, 'AdminApp/AdminHome.html', context)


# =========================
# ROAD FEATURE GRAPH
# =========================

def RoadFeature(request):

    try:

        if df is None:
            context = {'data': "Please Load Dataset First"}
            return render(request, 'AdminApp/AdminHome.html', context)

        sns.countplot(
            y=df['Weather Condition'],
            hue=df['Type of Accident']
        )

        BASE_DIR = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )

        graph_path = os.path.join(
            BASE_DIR,
            "Static",
            "roadfeature.png"
        )

        plt.savefig(graph_path)

        plt.close()

        context = {
            'data': "Road Feature Graph Generated"
        }

        return render(request, 'AdminApp/AdminHome.html', context)

    except Exception as e:

        context = {
            'data': 'Road Feature Error : ' + str(e)
        }

        return render(request, 'AdminApp/AdminHome.html', context)


# =========================
# ACCIDENT TYPE GRAPH
# =========================

def TypeofAccidents(request):

    try:

        if df is None:
            context = {'data': "Please Load Dataset First"}
            return render(request, 'AdminApp/AdminHome.html', context)

        sns.countplot(
            x=df['Road condition'],
            hue=df['Type of Accident']
        )

        BASE_DIR = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )

        graph_path = os.path.join(
            BASE_DIR,
            "Static",
            "accidenttype.png"
        )

        plt.savefig(graph_path)

        plt.close()

        context = {
            'data': "Type of Accident Graph Generated"
        }

        return render(request, 'AdminApp/AdminHome.html', context)

    except Exception as e:

        context = {
            'data': 'Type Of Accident Error : ' + str(e)
        }

        return render(request, 'AdminApp/AdminHome.html', context)


# =========================
# CAUSES GRAPH
# =========================

def PredictByCuases(request):

    try:

        if df is None:
            context = {'data': "Please Load Dataset First"}
            return render(request, 'AdminApp/AdminHome.html', context)

        sns.set(rc={'figure.figsize': (10.7, 8.27)})

        sns.countplot(y=df['Causes'])

        BASE_DIR = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )

        graph_path = os.path.join(
            BASE_DIR,
            "Static",
            "causes.png"
        )

        plt.savefig(graph_path)

        plt.close()

        context = {
            'data': "Causes Graph Generated"
        }

        return render(request, 'AdminApp/AdminHome.html', context)

    except Exception as e:

        context = {
            'data': 'Causes Graph Error : ' + str(e)
        }

        return render(request, 'AdminApp/AdminHome.html', context)


# =========================
# PREDICTION PAGE
# =========================

def predict(request):
    return render(request, 'AdminApp/Prediction.html')


# =========================
# PREDICTION ACTION
# =========================

def PredAction(request):

    global dec

    try:

        if dec is None:
            context = {'data': "Please Run Decision Tree First"}
            return render(request, 'AdminApp/PredictedData.html', context)

        area = int(request.POST.get('area'))
        cause = int(request.POST.get('cause'))
        feature = int(request.POST.get('feature'))
        condition = int(request.POST.get('condition'))
        weather = int(request.POST.get('weather'))

        number = random.randint(1000, 9999)

        pred = dec.predict([
            [area, cause, feature, condition, weather, number]
        ])

        if pred[0] == 0:
            msg = "Fatal"

        elif pred[0] == 1:
            msg = "Grievous injury"

        elif pred[0] == 2:
            msg = "Minor injury"

        elif pred[0] == 3:
            msg = "Non injury"

        else:
            msg = "No Accident Predicted"

        context = {
            'data': "Accident Predicted and Type Of Accident is :: " + msg
        }

        return render(request, 'AdminApp/PredictedData.html', context)

    except Exception as e:

        context = {
            'data': 'Prediction Error : ' + str(e)
        }

        return render(request, 'AdminApp/PredictedData.html', context)
