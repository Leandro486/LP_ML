import praw


reddit = praw.Reddit(
    client_id='XWLkBoloGyiakQmNzfGPSg',
    client_secret='nXCSJXIZhR23eJCdYJbEM2t6F2nTDA',
    user_agent='Leandro&Filhos'
)


subreddit = reddit.subreddit('TesteLP')

keyword = 'Exemplo'

for submission in subreddit.hot(limit=10):  # Limite de 10 postagens (você pode ajustar isso)
    if keyword in submission.title:
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


