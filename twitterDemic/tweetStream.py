#reference : https://www.dataquest.io/blog/streaming-data-python/
#Python code to use twitter streaming api , extract live tweats and write to Kinesis
import tweepy
from tweepy.streaming import StreamListener
import csv
import pandas as pd
import csv
from datetime import datetime
import json
import boto3
import googlemaps
import creds #import from credentials file
import time

#google maps get co-ordindates
gmaps = googlemaps.Client(key=creds.google_map_key)
def getGeoCord(location):
    try:
        #print(location)
        geocode_result = gmaps.geocode(location)
        if(len(geocode_result)>0):
            return geocode_result[0].get('geometry',{}).get('location',None)
        return
    except:
        return None

#assgin tweet geo if avail, if not use author location
def getMappingLocation(tweetCoOrd, authorCoOrd):
    if tweetCoOrd:
        return str(tweetCoOrd['coordinates'][0]) + ',' + str(tweetCoOrd['coordinates'][1])
    if authorCoOrd:
        return str(authorCoOrd['lng']) + ',' + str(authorCoOrd['lat'])

    return '-69.942848,37.176654' #atlantic ocean location

#invoke kinesis
kinesis = boto3.client('kinesis', region_name='us-east-1')

#twitter streaming api
class StreamListener(StreamListener):
    def on_status(self, status):
        status_dict={}
        #attributes to be pulled
        status_dict = {
                    'id' : status.id,
                    'created_at_utc' : time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(status.timestamp_ms)/1000)) ,
                    'tweet_text' : status.text,
                    'tweet_url' : "www.twitter.com/" + str(status.author.screen_name) + "/status/" + str(status.id),
                    'geo_coordinates' : status.coordinates,
                    'fav_count_or_likes' : status.favorite_count,
                    'retweet_count' : status.retweet_count,
                    'author_location' :  status.author.location,
                    'author_geo_coordinates' : getGeoCord(status.author.location),
                    'author_followers_count' : status.author.followers_count,
                    'author_screen_name' : status.author.screen_name,
                    'author_fav_count' : status.author.favourites_count,
                    'geo' : status.geo,
                    'retweeted' : status.retweeted,
                    'source url' : status.source_url,
                    'source' : status.source
        }

        status_dict['mapping_location'] = getMappingLocation(status_dict['geo_coordinates'], status_dict['author_geo_coordinates'])
        #add record to kinesis / data producer
        kinesis.put_record(StreamName="wegmans_tweets", Data=json.dumps(status_dict), PartitionKey="filler")



    def on_error(self, status_code):
        print(status_code)
        if status_code == 420:
            return False


if __name__ == '__main__':
    #Get Twitter credentials from cred.py
    consumer_key = creds.consumer_key
    consumer_secret = creds.consumer_secret
    access_token = creds.access_token
    access_token_secret = creds.access_token_secret

    #init Twitter API
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    stream_listener = StreamListener()
    stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
    stat = stream.filter(track=["#Wegmans"])
