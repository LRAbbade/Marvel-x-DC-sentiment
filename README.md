# SO_Threads
Trabalho de threads do renzão

Resumo:
Cria uma thread para streamar cada um dos termos no array "keywords" em main.py, filtra as informações dos tweets, analisa o sentimento deles usando o TextBlob, os que não forem neutros são exibidos. 

Para executar, faça git clone, e então crie um arquivo "keys.py", onde deve se inserir as access keys do twitter de sua conta no seguinte formato:

```
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''
```

Insira as keys entre ' '

Execute com

```
python main.py
```

Requisitos:

- Python 3
- Tweepy
- TextBlob
