import praw #reddit
import tweepy #twitter
import requests #facebook
#import mysql.connector
from datetime import datetime
import pandas as pd
import snscrape.modules.twitter as sntwitter


#API REDDIT
def reddit_app():
    reddit = praw.Reddit(
        client_id='XWLkBoloGyiakQmNzfGPSg',
        client_secret='nXCSJXIZhR23eJCdYJbEM2t6F2nTDA',
        user_agent='Leandro&Filhos'
    )

    subreddit = reddit.subreddit('TesteLP')

    keyword = 'Teste'

    for submission in subreddit.hot(limit=10): 
        print(f'Texto: {submission.selftext}')
        timestamp = submission.created_utc
        date = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d')
        print(f'Data: {date}')
        print(f'Rede Social: Reddit')
        print(f'Classificação: {submission.score}')
        print('---')

#API INSTAGRAM
def instagram_app():
    access_token = 'IGQWRNdElhV0ZAFS1ZANeXdUcS1QemVPUy0xMjJ1enJJMmp5Wm5tUHBWX1pQaU5LQlg0c09Da0lHeVd0M2Q3ZAi1pSUtTak45YWl2dktTb0w0V25uMFJ0OVF5TDBqQ2x1Y0tXMVAxMXJzN3BrQktVYU0zZAmlIS1RidWMZD'
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

if __name__ == "__main__":
    instagram_app()

#API FACEBOOK
def facebook_app():
    access_token = 'EAAKMj6M8bpMBOwjTr9wZCU9zb9eMRMSydMN0RWy6HckYGHpjl0gFq4GZC5OfZCIkitmOht5YLc4RcF1PDypIktP3UiiwopmXZCNPr3hThnFhskNi7kb6kA3ZBtZBpizen86MvySPOguMtzi7X44S5mAAgZCTjiONQLz27KDK2SbZAdurMNSvCq8ZCQSNu2Ds0Q4u1biUjAqHL7huuIXyxEgjzJlrkb4ggzuZAZCaFZAdeMEqfKqVrFXNIBPG0ytyo5Fy7AZDZD'  
    user_id = '190901262497519'

    url = f'https://graph.facebook.com/v18.0/{user_id}/posts?access_token={access_token}'

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
    twitter_data = []

    payload = {
        'api_key': 'af72815ef323c3513189062ad5b1eccf',
        'query': 'teste',
        'num': '10'
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
        print(f'Texto: {content}')
        print(f'Data: {date}')
        print(f'Rede Social: {social_media}')
        print(f'Classificação: {score}')
        print('---')

        twitter_data.append({'Conteúdo': content, 'Data': date, 'Rede Social': social_media, 'Classificação': score})

    df = pd.DataFrame(twitter_data)
    df.to_json('tweets.json', orient='index')
    #print(df)
    

#func()
#reddit_app()
#twitter_app()
#facebook_app()
instagram_app()