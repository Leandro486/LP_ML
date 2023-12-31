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

import mysql.connector

def conBD():
    comments = [[],[],[]]
    con = mysql.connector.connect(host='localhost',database='bd',user='root',password='estgoh')
    if con.is_connected():
        #db_info = con.get_server_info()
        #print(db_info)
        cursor = con.cursor()
        cursor.execute("SELECT * FROM tabcomentarios WHERE Classification IS NULL")
        linha = cursor.fetchall()
        #print("Conectado ",linha)
        for row in linha:
            id, text, date, social, classification = row
            #print("ID: ",id)
            #print("Text: ",text)
            #print("Date: ",date)
            #print("Social: ",social)
            #print("Classification: ",classification)

            comments[0].append(id)
            comments[1].append(text)

    if con.is_connected():
        cursor.close()
        con.close()
        return comments
        #print("Conexão fechada")

def conBDUpdate(comments):
    con = mysql.connector.connect(host='localhost',database='bd',user='root',password='estgoh')
    if con.is_connected():
        cursor = con.cursor()
        for id, classificacao in zip(comments[0], comments[2]):
            cursor.execute("UPDATE tabcomentarios SET Classification = %s WHERE id = %s", (classificacao, id))
        con.commit()

def classification():
    #carregamento do dataset

    #Dataset "dataset_reviews.csv"
    data = pd.read_csv('C:\\Users\\Leandro\\OneDrive\\Documentos\\GitHub\\LP_ML\\Datasets\\dataset_reviews.csv', encoding='utf-8')

    #Eliminar metade do meu dataset aleatoriamente
    #Estava a dar problemas porque era 25 mil instancias e estava a demorar 30 min a ler o dataset

    data = data.sample(frac=1, random_state=42)#baralha as linhas aleatoriamente

    metade_do_tamanho = len(data) // 18

    data = data.iloc[:metade_do_tamanho]

    #text preprocessing

    #nltk.download('all')
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
        print(i)
    data['Text'] = corpus

    X = data['Text']
    y = data['Classification']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33,random_state=123)
    #print('Training data: ',X_train.shape)
    #print('Testing data: ', X_test.shape)

    #Extracao de features
    cv = CountVectorizer()
    X_train_cv = cv.fit_transform(X_train)

    #Model Training and Evaluation
    lr = LogisticRegression()
    lr.fit(X_train_cv, y_train)
    X_test_cv = cv.transform(X_test)
    predictions = lr.predict(X_test_cv)

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
    df = pd.DataFrame(metrics.confusion_matrix(y_test,predictions),index=['Verdadeiro Previsto','Falso Previsto'],columns=['Verdadeiro Real','Falso Real'])
    print(df)

    #Queremos os Verdadeiros Positivos, na Matriz de confusão como comentários positivos
    #Queremos os Verdadeiros Negativos, na Matriz de confusão como comentários negativos
    VP = df.at['Verdadeiro Previsto','Verdadeiro Real']
    FN = df.at['Falso Previsto','Falso Real']
    print("Comentários positivos: ",VP)
    print("Comentários negativos: ",FN)

    #Avaliação de novos comentários
    comentarios = [[],[],[]]
    #with open('C:\\Users\\Leandro\\OneDrive\\Documentos\\GitHub\\LP_ML\\comentarios.txt','r') as ficheiro:
        #for linha in ficheiro:
            #comentarios.append(linha)
    comentarios = conBD()

    comentarios_class = [[],[],[]]

    for id, comentario in zip(comentarios[0], comentarios[1]):
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
            comentarios_class[2].append(1)
            comentarios_class[1].append(comentario)
            comentarios_class[0].append(id)
        else:
            print(f"Comentário [{comentario}] negativo!")
            comentarios_class[2].append(0)
            comentarios_class[1].append(comentario)
            comentarios_class[0].append(id)

    conBDUpdate(comentarios_class)


classification()