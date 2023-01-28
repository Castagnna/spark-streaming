import socket
import tweepy
from config import secrets, HOST, PORT


s = socket.socket()
s.bind((HOST, PORT))
print(f"Aguardando conexão na porta: {PORT}")

s.listen(5)
connection, address = s.accept()
print(f"Recebendo solicitação de {address}")

bearer_token = secrets["bearer_token"]

keyword = "lula"

class GetTweets(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        print(tweet.text)
        print("="*50)
        connection.send(tweet.text.encode('utf-8', 'ignore'))

printer = GetTweets(bearer_token)
printer.add_rules(tweepy.StreamRule(keyword))
printer.filter()


connection.close()