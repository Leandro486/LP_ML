import praw


reddit = praw.Reddit(
    client_id='XWLkBoloGyiakQmNzfGPSg',
    client_secret='nXCSJXIZhR23eJCdYJbEM2t6F2nTDA',
    user_agent='Leandro&Filhos'
)


subreddit = reddit.subreddit('footballmanagergames')

keyword = 'portugal'

for submission in subreddit.hot(limit=10):  
    submission.comments.replace_more(limit=None)  
    for comment in submission.comments.list():
        if keyword in comment.body.lower():  
            print(f'Comentário encontrado: {comment.body}')



