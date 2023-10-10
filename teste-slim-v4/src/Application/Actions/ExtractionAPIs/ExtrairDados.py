import praw #reddit
import tweepy #twitter

#API REDDIT
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

#API FACEBOOK



#API TWITTER
class twitter_class:
    def __init__(self,client_key,client_secret,access_token,access_token_secret):
        self.client_key = client_key
        self.client_secret = client_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret

twitter = twitter_class(
    'gOR0lfXzYDgmi3HE92X1MFxZC', 
    'BQrR5ekfA8ji1O1IQB7GVpxCiX3UTJlymVaoHafPSNjAGfuTxX',
    '1706701378712633344-iyNfzFKAcpg3FeGXJ9swbkyziXNtxG',
    'c8aaSir9XjjS5QbmEAvbiGgPj67dg2J696ZHTq9GBGylr'
)


auth = tweepy.OAuthHandler(twitter.client_key,twitter.client_secret)
auth.set_access_token(twitter.access_token,twitter.access_token_secret)

api_twitter = tweepy.API(auth)

keyword_twitter = 'como'

tweet_limit = 10

tweets = api_twitter.search_tweets(q=keyword_twitter,count=tweet_limit)

for tweet in tweets:
    print(f'Tweet: {tweet.text}')
    print(f'Utilizador: {tweet.user.screen_name}')
    print(f'Data de criação: {tweet.create_at}')
    print('---')