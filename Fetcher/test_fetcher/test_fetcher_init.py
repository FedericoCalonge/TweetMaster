'''
Created on Nov 20, 2018

@author: Gabriel Torrandella
'''
import simplejson as json
import Tweet.Tweet as tweet

hastag = {
        "statuses": [
                {
                        "created_at": "Sun Feb 25 18:11:01 +0000 2018",
                        "id_str": "967824267948773377",
                        "entities": {
                                "hashtags": ["marth"],
                                "symbols": [],
                                "user_mentions": [],
                                },
                        "user": {
                                "id_str": "11348282",
                                "name": "NASA"
                                }
                },
                {
                        "created_at": "Sun Feb 25 18:11:01 +0000 2018",
                        "id_str": "967824267948773378",
                        "entities": {
                                "hashtags": ["marth"],
                                "symbols": [],
                                "user_mentions": [],
                                },
                        "user": {
                                "id_str": "11348282",
                                "name": "NASA"
                                }
                }
            ]
}

mention = {
        "statuses": [
                {
                        "created_at": "Sun Feb 25 18:11:01 +0000 2018",
                        "id_str": "967824267948773377",
                        "entities": {
                                "hashtags": [],
                                "symbols": [],
                                "user_mentions": ["marth"],
                                },
                        "user": {
                                "id_str": "11348282",
                                "name": "NASA"
                                }
                },
                {
                        "created_at": "Sun Feb 25 18:11:01 +0000 2018",
                        "id_str": "967824267948773378",
                        "entities": {
                                "hashtags": [],
                                "symbols": [],
                                "user_mentions": ["marth"],
                                },
                        "user": {
                                "id_str": "11348282",
                                "name": "NASA"
                                }
                }
            ]
}

responseMention = [tweet.Tweet(mention["statuses"][0]), tweet.Tweet(mention["statuses"][1])]

print(responseMention)
