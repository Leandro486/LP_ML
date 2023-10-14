import praw #reddit
import tweepy #twitter
import requests #facebook

#API REDDIT
def reddit_app():
    reddit = praw.Reddit(
        client_id='XWLkBoloGyiakQmNzfGPSg',
        client_secret='nXCSJXIZhR23eJCdYJbEM2t6F2nTDA',
        user_agent='Leandro&Filhos'
    )

    subreddit = reddit.subreddit('TesteLP')

    keyword = 'Teste'

    for submission in subreddit.hot(limit=10):  # Limite de 10 postagens (você pode ajustar isso)
        #if keyword in submission.title:
        print(f'Título: {submission.title}')
        print(f'Autor: {submission.author}')
        print(f'Pontuação: {submission.score}')
        print(f'URL: {submission.url}')
        
        # Itere pelos comentários de cada postagem
        submission.comments.replace_more(limit=None)  # Carregar todos os comentários
        for comment in submission.comments.list():
            print(f'Comentário: {comment.body}')
            print(f'Autor do Comentário: {comment.author}')
            print(f'Pontuação do Comentário: {comment.score}')
            print('---')

#API INSTAGRAM


#API FACEBOOK
def facebook_app():
    access_token = 'EAAOc0KF41aIBO41blFVqZB69PznvSoo5qEtTXiX9gONOywC1WxXyohE8HI0s8Upt6yFjwg7PZBE0NqvBsWr6jE7ikcEZCCpOekWiHchv2ZCMhS6nW135C3YZAqQZBZCshZA5yqxL6drmHnEGOcqKDfBHQ5BvIo5WlJzAxaojDdTaR1QjfQlKGWtgZC8MHZAboLDhdKksqVxuv3Dx0z4kjHcdZChzqEsZCL8elLuiXHtq'
    keyword = 'exemplo'

    url = f'https://graph.facebook.com/v18.0/search?q={keyword}&type=post&access_token={access_token}'
 
    response = requests.get(url)
    data = response.json()
    if 'data' in data:
        for post in data['data']:
            print(post)
    else:
        print(data) 


#API TWITTER
def twitter_app():
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

def func():
    twitter_data = []

    payload = {
        'api_key': 'af72815ef323c3513189062ad5b1eccf',
        'query': 'ronaldo',
        'num': '10'
    }

    response = requests.get(
        'https://api.scraperapi.com/structured/twitter/search',params=payload
    )

    data = response.json()
    print(data.keys())

    print(data['organic_results'][0]['snippet'])

    all_tweets = data['organic_results']
    for tweet in all_tweets:
        #print(tweet)
        twitter_data.append(tweet)

    df = pd.DataFrame(twitter_data)
    df.to_json('tweets.json',orient='index')
    print(df)
    



#func()
#twitter_app()
#facebook_app()