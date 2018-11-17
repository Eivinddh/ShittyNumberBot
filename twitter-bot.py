from TwitterAPI import TwitterAPI
import requests
import re

f = open("keys.txt", "r")
if f.mode == 'r':
    contents = list(map(lambda x: x.replace('\n', ''), f.readlines()))
    consumer_key = contents[0]
    consumer_secret = contents[1]
    access_token_key = contents[2]
    access_token_secret = contents[3]


def authenticate() -> TwitterAPI:
    return TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)


def get_trivia_about_number(number_to_check: int) -> requests:
    return requests.get("http://numbersapi.com/" + str(number_to_check) + "/trivia?json")


def get_random_trivia() -> requests:
    return requests.get("http://numbersapi.com/random/trivia")


def reply(tweet: dict, api: TwitterAPI) -> None:
    tweet_id = tweet['id']
    sender = tweet['user']

    tweet_text = str(tweet["text"]).split(" ")[1]
    print(tweet_text)
    if re.match("^[+-]?(\d+)[^.,]$", tweet_text) is not None:
        json_response = get_trivia_about_number(int(tweet_text)).json()

        if json_response["found"]:
            print(json_response["text"])
            trivia_text = json_response["text"]
        else:
            trivia_text = "Gosh, get a better number... Here's a random fact: " + get_random_trivia().text
    else:
        trivia_text = "You need to write an integer, fool!"

    tweet_to_send = "@" + sender["screen_name"] + " " + trivia_text
    r = api.request('statuses/update', {'status': tweet_to_send, 'in_reply_to_status_id': tweet_id})
    print(r.text)


if __name__ == "__main__":

    API = authenticate()
    print("Bot starting...")
    while True:
        stream = API.request('statuses/filter', {'track': '@EivindsShitBot'})
        for t in stream.get_iterator():
            reply(t, API)
