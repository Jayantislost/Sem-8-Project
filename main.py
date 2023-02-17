import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Data Collection and Pre-Processing
# loading the data from csv file to a pandas DataFrame
raw_mail_data = pd.read_csv('/Users/jayantsharma/Developer/Sem 8 Project/mail_data.csv')

# replace the null values with a null stirng
mail_data = raw_mail_data.where((pd.notnull(raw_mail_data)),'')

# printing the first 5 rows of the dataframe
mail_data.head()

# checking the number of rows and columns in the dataframe
mail_data.shape

# labelling spam mail as 0; ham mail as 1;
mail_data.loc[mail_data['Category'] == 'spam', 'Category',] = 0
mail_data.loc[mail_data['Category'] == 'ham', 'Category',] = 1 

# separating the data as text and label
X = mail_data['Message']
Y = mail_data['Category']

# Splitting the data into training data and test data
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=3)

# Feature Extraction
# transform the text data to feature vectors that can be used as input to the Logistics regression
feature_extraction = TfidfVectorizer(min_df = 1, stop_words='english', lowercase=True)

X_train_features = feature_extraction.fit_transform(X_train)
X_test_features = feature_extraction.transform(X_test)

# convert Y_train and Y_test values as integers
Y_train = Y_train.astype('int')
Y_test = Y_test.astype('int')

# Training the Model
model = LogisticRegression()

# trainging the Logistic Regression model with the training data
model.fit(X_train_features, Y_train)

# Evaluating the trained model
# prediction on training data
prediction_on_training_data = model.predict(X_train_features)
accuracy_on_training_data = accuracy_score(Y_train, prediction_on_training_data)

# prediction on test data
prediction_on_test_data = model.predict(X_test_features)
accuracy_on_test_data = accuracy_score(Y_test, prediction_on_test_data)

# Building a predictive system 
input_mail = ["I'm gonna be home soon and i don't want to talk about this stuff anymore tonight, k? I've cried enough today."]

# convert text to feature vectors
input_data_features = feature_extraction.transform(input_mail)

# making predcitions
prediction = model.predict(input_data_features)


if (prediction[0]==1):
    print('Ham mail')
else:
    print('Spam mail')
