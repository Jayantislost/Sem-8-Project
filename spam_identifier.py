import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import sys

class SpamIdentifier:
    def __init__(self, **kwargs):
        self.dataset_path = kwargs.get("dataset_path")
        self.input_mail = kwargs.get("input_mail")

        self.feature_extraction = None
        self.si_model = None
        self.X_train = self.X_test = self.Y_train = self.Y_test = None
        self.X_train_features = self.X_test_features = None

        self.create_model()
        self.train_model()

    def create_model(self):

        # Data Collection and Pre-Processing
        # loading the data from csv file to a pandas DataFrame
        raw_mail_data = pd.read_csv(self.dataset_path)

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
        self.X_train, self.X_test, self.Y_train, self.Y_test = train_test_split(X, Y, test_size=0.2, random_state=3)

        # Feature Extraction
        # transform the text data to feature vectors that can be used as input to the Logistics regression
        self.feature_extraction = TfidfVectorizer(min_df = 1, stop_words='english', lowercase=True)

        self.X_train_features = self.feature_extraction.fit_transform(self.X_train)
        self.X_test_features = self.feature_extraction.transform(self.X_test)

        # convert Y_train and Y_test values as integers
        self.Y_train = self.Y_train.astype('int')
        self.Y_test = self.Y_test.astype('int')

    def train_model(self):

        # Training the Model
        self.si_model = LogisticRegression()

        # trainging the Logistic Regression model with the training data
        self.si_model.fit(self.X_train_features, self.Y_train)

        # Evaluating the trained model
        # prediction on training data
        prediction_on_training_data = self.si_model.predict(self.X_train_features)
        accuracy_on_training_data = accuracy_score(self.Y_train, prediction_on_training_data)

        # prediction on test data
        prediction_on_test_data = self.si_model.predict(self.X_test_features)
        accuracy_on_test_data = accuracy_score(self.Y_test, prediction_on_test_data)

    def classify_spam(self):
        # Building a predictive system

        # convert text to feature vectors
        input_data_features = self.feature_extraction.transform([self.input_mail])

        # making predcitions
        prediction = self.si_model.predict(input_data_features)

        if (prediction[0] == 1):
            return False
        else:
            return True
