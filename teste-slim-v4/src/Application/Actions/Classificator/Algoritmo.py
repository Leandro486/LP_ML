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

print(predictions)




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


#Pré-processamento de um novo comentário 

novo_comentario = "i hate this product"
novo_comentario = re.sub('[^a-zA-Z]', ' ', novo_comentario)
novo_comentario = novo_comentario.lower()
novo_comentario = novo_comentario.split()
novo_comentario = [word for word in novo_comentario if word not in stopwords.words('english')]
novo_comentario = [lemmatizer.lemmatize(word) for word in novo_comentario]
novo_comentario = ' '.join(novo_comentario)

#Vetorizacao
novo_comentario_cv = cv.transform([novo_comentario])


#Classificacao
previsao = lr.predict(novo_comentario_cv)
print(novo_comentario)
if previsao[0] == 1:
    print("O comentário é positivo!")
else:
    print("O comentário é negativo.")


#data['generation'].value_counts(normalize = True).plot.bar()
#plt.show()


