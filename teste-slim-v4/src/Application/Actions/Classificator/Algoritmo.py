import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import nltk

import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
from sklearn.linear_model import LogisticRegression
from sklearn import metrics


#carregamento do dataset

#Dataset "pokemons.csv"
#data = pd.read_csv('pokemons.csv', encoding='utf-8')
#data.drop(['rank','evolves_from','type2','hp','atk','def','spatk','spdef','speed','total','height','weight','abilities'],axis=1,inplace=True)

#Dataset "dataset_reviews.csv"
data = pd.read_csv('dataset_reviews.csv', encoding='utf-8')

#print(data.head())

#text preprocessing

#nltk.download('all')
#text = list(data['desc'])
text = list(data['Text'])

lemmatizer = WordNetLemmatizer()

corpus = []

for i in range(len(text)):

    r = re.sub('[^a-zA-Z]', ' ', text[i])

    r = r.lower()

    r = r.split()

    r = [word for word in r if word not in stopwords.words('english')]

    r = [lemmatizer.lemmatize(word) for word in r]

    r = ' '.join(r)

    corpus.append(r)


#data['desc'] = corpus
data['Text'] = corpus

#X = data['desc']
#y = data['type1']
X = data['Text']
y = data['Classification']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33,random_state=123)

print('Training data: ',X_train.shape)
print('Testing data: ', X_test.shape)


#Extracao de features

cv = CountVectorizer()

X_train_cv = cv.fit_transform(X_train)

#print(X_train_cv.shape)


#Model Training and Evaluation

lr = LogisticRegression()

lr.fit(X_train_cv, y_train)

X_test_cv = cv.transform(X_test)

predictions = lr.predict(X_test_cv)

print(predictions)


#confusion matrix
#df = pd.DataFrame(metrics.confusion_matrix(y_test,predictions),index=['normal','water','fire','water','bug','grass','rock','psychic','fairy','ice','poison','ground','electric','ghost','flying','dark','fighting','steel'],columns=['normal','water','fire','water','bug','grass','rock','psychic','fairy','ice','poison','ground','electric','ghost','flying','dark','fighting','steel'])

#print(df)
#print("Acertou no tipo normal: ")
#print(df.loc['ice','ice'])
#print(data.isna().sum())
#print(data.shape)

#data['generation'].value_counts(normalize = True).plot.bar()
#plt.show()


