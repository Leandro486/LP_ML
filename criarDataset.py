import os
import pandas as pd


def read_reviews(folder_path, label):
    reviews = []
    
    os.chdir(folder_path)

    for file in os.listdir():
        if file.endswith(".txt"):
            file_path = f"{folder_path}/{file}"
            with open(file_path, 'r',encoding='utf-8') as f:
                reviews.append((f.read(),label))
    return reviews


reviews_negativas = read_reviews('C://Users//Leandro//Desktop//LP//aclImdb//train//neg',0)

reviews_positivas = read_reviews('C://Users//Leandro//Desktop//LP//aclImdb//train//pos',1)

reviews = reviews_negativas + reviews_positivas

#print(reviews)

df = pd.DataFrame(reviews, columns=['Text','Classification'])

print(df.head())


df.to_csv('C://Users//Leandro//Desktop//LP//dataset_reviews.csv',index=False)


