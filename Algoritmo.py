import numpy as np
import pandas as pd


from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report


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
#print("Relatorio:"
#print(report)
