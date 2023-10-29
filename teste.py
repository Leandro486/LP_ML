import praw #reddit
import requests #facebook
#import facebook

#API REDDIT
def reddit_app(keywords_file):
    reddit = praw.Reddit(
        client_id='XWLkBoloGyiakQmNzfGPSg',
        client_secret='nXCSJXIZhR23eJCdYJbEM2t6F2nTDA',
        user_agent='Leandro&Filhos'
    )

    with open(keywords_file, 'r') as file:
        keywords = [line.strip() for line in file]

    for keyword in keywords:
        print(f'Pesquisando por: {keyword}')
        for submission in reddit.subreddit("all").search(keyword, limit=10):
            print(f'Título: {submission.title}')
            print(f'Autor: {submission.author}')
            print(f'Pontuação: {submission.score}')
            print(f'URL: {submission.url}')

            submission.comments.replace_more(limit=None)  # Carrega todos os comentários
            for comment in submission.comments.list():
                print(f'Comentário: {comment.body}')
                print(f'Autor do Comentário: {comment.author}')
                print(f'Pontuação do Comentário: {comment.score}')
                print('---')

keywords_file = 'keywords.txt'

#API INSTAGRAM


#API FACEBOOK
def facebook_app():
    access_token = 'EAAOc0KF41aIBO80fdt0knUoHeWIDDkIAwdAyoGQu4oGCtNZCj7sypsX6YL6PC3zgyAXSPYHoLYCSXnB9ZA2Ew6HwZB9IHd9PyEr5Gj83idk5XydmckeENzOo5nfWlS5AYqAaWGsX2o7gQI93BPlvJPPfsP4flb93uAENNZC9HQhJjz5pSvmhN76Ia9QnEcFJWAZBC2nB6SmZASlj6Ygq4p6G5kqgZDZD'

    # Leia o arquivo "keywords.txt" e obtenha as palavras-chave
    with open('keywords.txt', 'r') as file:
        keywords = [line.strip() for line in file]

    for keyword in keywords:
        url = f'https://graph.facebook.com/v18.0/search?q={keyword}&type=post&access_token={access_token}'
        response = requests.get(url)
        data = response.json()
        if 'data' in data:
            for post in data['data']:
                print(post)
        else:
            print(data)

#import pandas as pd

#facebook_app()
reddit_app(keywords_file)