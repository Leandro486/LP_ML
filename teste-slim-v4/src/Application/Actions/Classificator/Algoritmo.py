import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import nltk

import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
#from sklearn.naive_bayes import MultinomialNB
#from sklearn.metrics import accuracy_score, classification_report
from sklearn.linear_model import LogisticRegression
from sklearn import metrics

#from sklearn.ensemble import RandomForestRegressor
#from sklearn.svm import SVC
#from sklearn.tree import DecisionTreeClassifier
#from sklearn.naive_bayes import MultinomialNB


#carregamento do dataset

#Dataset "pokemons.csv"
#data = pd.read_csv('pokemons.csv', encoding='utf-8')
#data.drop(['rank','evolves_from','type2','hp','atk','def','spatk','spdef','speed','total','height','weight','abilities'],axis=1,inplace=True)

#Dataset "dataset_reviews.csv"
data = pd.read_csv('C:\\Users\\Leandro\\OneDrive\\Documentos\\GitHub\\LP_ML\\dataset_reviews.csv', encoding='utf-8')

#Dataset "dataset.csv"

#Eliminar metade do meu dataset aleatoriamente
#Estava a dar problemas porque era 25 mil instancias e estava a demorar 30 min a ler o dataset

data = data.sample(frac=1, random_state=42)#baralha as linhas aleatoriamente

metade_do_tamanho = len(data) // 18

data = data.iloc[:metade_do_tamanho]

#print(data.head())

#text preprocessing

#nltk.download('all')
#text = list(data['desc'])
text = list(data['Text'])
#print(text)
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

    print(i)


#data['desc'] = corpus
data['Text'] = corpus
#print(data['Text'].head())

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


#Model Training and Evaluation

lr = LogisticRegression()

lr.fit(X_train_cv, y_train)

X_test_cv = cv.transform(X_test)

predictions = lr.predict(X_test_cv)

#print(predictions)

#Testar outros algoritmos
#algorithms = [
#    ('Logistic Regression', LogisticRegression()),
#    ('SVM', SVC()),
#    ('Decision Tree', DecisionTreeClassifier()),
#    ('Naive Bayes', MultinomialNB())
#]

#for name, algorithm in algorithms:
#    clf = algorithm
#    clf.fit(X_train_cv,y_train)
#    y_pred = clf.predict(X_test_cv)

#    accuracy = accuracy_score(y_test,y_pred)
#    classification_rep = classification_report(y_test,y_pred)

#    print(f"Algoritmo: {name}")
#    print(f"Precisão: {accuracy}")
#    print(f"Classificação: \n{classification_rep}")
#    print("="*50)


#confusion matrix
#df = pd.DataFrame(metrics.confusion_matrix(y_test,predictions),index=['normal','water','fire','water','bug','grass','rock','psychic','fairy','ice','poison','ground','electric','ghost','flying','dark','fighting','steel'],columns=['normal','water','fire','water','bug','grass','rock','psychic','fairy','ice','poison','ground','electric','ghost','flying','dark','fighting','steel'])
df = pd.DataFrame(metrics.confusion_matrix(y_test,predictions),index=['Verdadeiro Previsto','Falso Previsto'],columns=['Verdadeiro Real','Falso Real'])

print(df)

#Queremos os Verdadeiros Positivos, na Matriz de confusão como comentários positivos
#Queremos os Verdadeiros Negativos, na Matriz de confusão como comentários negativos
VP = df.at['Verdadeiro Previsto','Verdadeiro Real']
FN = df.at['Falso Previsto','Falso Real']
print("Comentários positivos: ",VP)
print("Comentários negativos: ",FN)

#Avaliação de novos comentários

comentarios = []

with open('C:\\Users\\Leandro\\OneDrive\\Documentos\\GitHub\\LP_ML\\comentarios.txt','r') as ficheiro:
    for linha in ficheiro:
        comentarios.append(linha)


for comentario in comentarios:
    comentario = re.sub('[^a-zA-Z]',' ',comentario)
    comentario = comentario.lower()
    comentario = comentario.split()
    comentario = [word for word in comentario if word not in stopwords.words('english')]
    comentario = [lemmatizer.lemmatize(word) for word in comentario]
    comentario = ' '.join(comentario)

    comentario_cv = cv.transform([comentario])

    previsao = lr.predict(comentario_cv)
    if previsao[0] == 1:
        print(f"Comentário [{comentario}] positivo!")
    else:
        print(f"Comentário [{comentario}] negativo!")



