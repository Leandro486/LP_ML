import praw #reddit
import tweepy #twitter
import requests #facebook
import mysql.connector
from datetime import datetime
import pandas as pd
import snscrape.modules.twitter as sntwitter

def insertBD(text, date, social):
    con = mysql.connector.connect(
        host='localhost',
        user='rafaela',
        password='rafaela17',
        database='lp'
    )

    if con.is_connected():
        cursor = con.cursor()
        query = "INSERT INTO tabcomentarios (Text, Date, Social_Media) VALUES (%s, %s, %s)"
        values = (text, date, social)
        
        try:
            cursor.execute(query, values)
            con.commit()  # Commit the changes
        except mysql.connector.Error as err:
            print(f"Erro ao inserir na base de dados: {err}")
        finally:
            cursor.close()
            con.close()

#API REDDIT
def reddit_app():
    reddit = praw.Reddit(
        client_id='XWLkBoloGyiakQmNzfGPSg',
        client_secret='nXCSJXIZhR23eJCdYJbEM2t6F2nTDA',
        user_agent='Leandro&Filhos'
    )

    subreddit = reddit.subreddit('all')
    keywords = 'teste'

    for submission in subreddit.search(keywords, limit=1000):
        text = submission.selftext
        timestamp = submission.created_utc
        date = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d')
        social = 'Reddit'
        classification = submission.score
        if text:  # Verifica se o texto não está vazio
            insertBD(text, date, social)

#API INSTAGRAM
def instagram_app():
    access_token = 'IGQWRNVkcwSGhSb3l0YnAzYktFZA3U4NUZAWTkF2ZAGVNb3dXR3FXc0VFb25zajJLWWRBaUtPWDI0bTJidnk2ZAWtrZAllIb2lqalpzbmE5QUNtckU3ajZA0WGRFdDFpUFNqeVJ0NG9Gc1FDTzJ4V2VkRk5fSmtteDZA2M2cZD'
    user_id = 'greenenergyfusion'

    # Endpoint para obter postagens do seu próprio perfil
    endpoint = f'https://graph.instagram.com/v13.0/{user_id}/media?fields=id,caption,media_type,media_url,thumbnail_url,permalink,timestamp&access_token={access_token}'

    response = requests.get(endpoint)

    if response.status_code == 200:
        data = response.json()
        for post in data['data']:
            caption = post.get("caption", "Nenhuma legenda")
            media_url = post.get("media_url", "URL da mídia não disponível")
            timestamp = post.get("timestamp", "Data da postagem não disponível")
            
            print(f'Post: {caption}')
            print(f'Media URL: {media_url}')
            print(f'Timestamp: {timestamp}')
            print('---')
    else:
        print(f'Erro na solicitação: {response.status_code}')

#API FACEBOOK
def facebook_app():
    access_token = 'EAAOc0KF41aIBO6ZBbnpSVyOMEXQTfUZBjCVKK6a3cFsHw9l8zdVt3xklZA7FdI2ZBZCkHiZCXyO4SBNdQN5fRx3SANDhc6eBQDFd2j32JAUZAPIYSdtOvtlQbLw9697Bo56RZBeD8lpbL0ui1ddtLSzJHfvCgNXfcoWDJZC1nRat40InaylovrSeIhXt4Wc80hEf7'  
    page_id = '61553130849319'

    url = f'https://graph.facebook.com/v18.0/{page_id}/posts?access_token={access_token}'

    response = requests.get(url)
    data = response.json()

    if 'data' in data:
        for post in data['data']:
            print(post)
    else:
        print(data)


#API TWITTER
def twitter_appi():
        class twitter_class:
            def __init__(self,client_key,client_secret,access_token,access_token_secret):
                self.client_key = client_key
                self.client_secret = client_secret
                self.access_token = access_token
                self.access_token_secret = access_token_secret

        twitter = twitter_class(
            'dg5T1OqhR62oadQAnTcWEsmOV', 
            'spfw2ygf2buFc1XpjXca9PVzvDydrCx0p94TYxIPtJphpM09qs',
            '1706701378712633344-zJYlIQBf4aUERyhhxjwRFoPSWCG612',
            '27fNjIUIu9S2VZ9EKDcxlTXtX2uJ758Wdg2BXWTQxcL2s'
        )


        auth = tweepy.OAuth1UserHandler(
            twitter.client_key,twitter.client_secret,
            twitter.access_token,twitter.access_token_secret
        )


        api = tweepy.API(auth, wait_on_rate_limit=True)

        search_query = "'Messi' 'World Cup' -filter:retweets AND -filter:replies AND -filter:links"

        tweet_limit = 10

        tweets = api.search_tweets(q=search_query,lang="en",count=tweet_limit,tweet_mode='extended')

        for tweet in tweets:
            print(f'Tweet: {tweet.text}')
            print(f'Utilizador: {tweet.user.screen_name}')
            print(f'Data de criação: {tweet.create_at}')
            print('---')


import requests
import pandas as pd

def twitter_app():
    date = datetime.now()
    date_formatted = date.strftime('%Y-%m-%d')
    twitter_data = []

    payload = {
        'api_key': 'af72815ef323c3513189062ad5b1eccf',
        'query': 'teste',
        'num': '1000'
    }

    response = requests.get(
        'https://api.scraperapi.com/structured/twitter/search', params=payload
    )

    data = response.json()
    print(data.keys())

    all_tweets = data['organic_results']
    for tweet in all_tweets:
        content = tweet.get('snippet', 'Nenhum conteúdo disponível')  # Obtém o conteúdo ou retorna 'Nenhum conteúdo disponível'
        date = tweet.get('time', 'Data não disponível')  # Obtém a data ou retorna 'Data não disponível'
        social_media = 'Twitter'
        score = 'Classificação não disponível'
        #print(f'Texto: {content}')
        #print(f'Data: {date_formatted}')
        #print(f'Rede Social: {social_media}')
        #print(f'Classificação: {score}')
        #print('---')

        if content:  # Verifica se o texto não está vazio
            insertBD(content, date_formatted, social_media)
    #print(df)
    

#func()
#insertBD()
reddit_app()
twitter_app()
#facebook_app()
#instagram_app()