import socket
import tweepy
from config import secrets, HOST, PORT


s = socket.socket()
s.bind((HOST, PORT))
print(f"Aguardando conexão na porta: {PORT}")

s.listen(5)
connection, address = s.accept()

bearer_token = secrets["bearer_token"]
print(bearer_token)
keyword = "lula"

class GetTweets(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        print(tweet.text)
        print("="*50)
        connection.send(tweet.text.encode('latin1', 'ignore'))
        # return super().on_tweet(tweet)

printer = GetTweets(bearer_token)
printer.add_rules(tweepy.StreamRule(keyword))
printer.filter()

connection.close()