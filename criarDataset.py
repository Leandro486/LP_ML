import os
import pandas as pd
import glob

def read_reviews(path,tipo):
    reviews = []
    for path in glob.glob(os.path.join(path, '*.txt')):
        with open(path, 'r', encoding='utf-8') as file:
            text = file.read()
            reviews.append((text,tipo))
    return reviews

reviews_negativas = read_reviews('acllmdb/train/neg',0)

reviews_positivas = read_reviews('acllmdb/train/pos',1)

reviews = reviews_negativas + reviews_positivas

df = pd.DataFrame(reviews, columns=['Texto','Pos/Neg'])

df.to_csv('dataset_reviews.csv',index=False)


