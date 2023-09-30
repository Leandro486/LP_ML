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


#textos = [
#    "Este é um texto de exemplo.",
#    "Python é uma linguagem de programação.",
#    "A classificação de texto é interessante.",
#    "Aprendizado de máquina é empolgante.",
#    "Classificação de texto usando Python.",
#    "Algoritmo de classificação de texto.",
#]

#classes = [0,1,0,1,0,1]

#vectorizer = CountVectorizer()
#X = vectorizer.fit_transform(textos)

#X_train, X_test, y_train, y_test = train_test_split(X, classes, test_size=0.2, random_state=42)

#clf = MultinomialNB()
#clf.fit(X_train, y_train)

#y_pred = clf.predict(X_test)

#accuracy = accuracy_score(y_test, y_pred)
#report = classification_report(y_test, y_pred, target_names=["Negativo","Positivo"])

#print(f"Acuracia : {accuracy:.2f}")
#print("Relatorio:")
#print(report)


#carregamento do dataset
data = pd.read_csv('pokemons.csv', encoding='utf-8')

data.drop(['rank','evolves_from','type2','hp','atk','def','spatk','spdef','speed','total','height','weight','abilities'],axis=1,inplace=True)


#text preprocessing

#nltk.download('all')

text = list(data['desc'])

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


data['desc'] = corpus


X = data['desc']

y = data['type1']


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33,random_state=123)



print('Training data: ',X_train.shape)
print('Testing data: ', X_test.shape)

#print(data.head())


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
df = pd.DataFrame(metrics.confusion_matrix(y_test,predictions),index=['normal','water','fire','water','bug','grass','rock','psychic','fairy','ice','poison','ground','electric','ghost','flying','dark','fighting','steel'],columns=['normal','water','fire','water','bug','grass','rock','psychic','fairy','ice','poison','ground','electric','ghost','flying','dark','fighting','steel'])

#print(df)
print(df.loc['normal','normal'])
#print(data.isna().sum())
#print(data.shape)

#data['generation'].value_counts(normalize = True).plot.bar()
#plt.show()


