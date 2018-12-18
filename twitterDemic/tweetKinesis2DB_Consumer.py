#reference : https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.01.html
#code used as draft for the final 'lambda' print_function

from __future__ import print_function # Python 2/3 compatibility
import boto3
import pandas as pd
import decimal
import sys
import time
import json

#local
#dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")

#function to derive sentiment using aws comprehend
def getSentiment(text):
    comprehend = boto3.client(service_name='comprehend', region_name='us-east-2')
    sentimentBody = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    sentiment = sentimentBody['Sentiment']
    return sentiment, sentimentBody['SentimentScore'][sentiment[0]+sentiment[1:].lower()]


#function to get words - noun and adjective
def getKeyWords(text):
    comprehend = boto3.client(service_name='comprehend', region_name='us-east-2')
    syntaxBody = comprehend.detect_syntax(Text=text, LanguageCode='en')
    tokens = syntaxBody["SyntaxTokens"]
    adjDict = {}
    for token in tokens:
        if token['PartOfSpeech']['Tag'] == 'ADJ' or token['PartOfSpeech']['Tag'] == 'NOUN':
            if adjDict.get(token['Text'],'none') == 'none':
                adjDict[token['Text']]=1
            else:
                adjDict[token['Text']]=adjDict[token['Text']]+1

    return adjDict

def updateWordsTable(key,value,sentimentType):
        try:
            wordTable.update_item(
                     Key={
                         'sentiment_type': str(sentimentType),
                         'word': key
                     },
                     UpdateExpression="set #attrName.word_count = #attrName.word_count + :val",
                     ExpressionAttributeNames = {
                         "#attrName" : "info"
                     },
                     ExpressionAttributeValues={
                         ':val': decimal.Decimal(wordDict[key])
                     },
                     ReturnValues="UPDATED_NEW"
                 )
        except:
            wordTable.update_item(
                     Key={
                         'sentiment_type': str(sentimentType),
                         'word': key
                     },
                     UpdateExpression="set #attrName = :attrValue",
                     ExpressionAttributeNames = {
                         "#attrName" : "info"
                     },
                     ExpressionAttributeValues={
                         ':attrValue': {
                             'word_count': decimal.Decimal(wordDict[key])
                             }
                     },
                     ReturnValues="UPDATED_NEW"
                 )


def lambda_handler(row, context):
    #aws services
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
    table = dynamodb.Table('wegmans_tweets_detail')
    wordTable = dynamodb.Table('wegmans_tweets_words')
    print(row['id'], row['created_at_utc'])
    #extract sentiment
    return
    sentimentType, sentimentScore = getSentiment(row['tweet_text'])
    table.put_item(
      Item={
           'tweet_id': str(row['id']),
           'created_at_utc': row['created_at_utc'],
           'info': {
               'tweet_text':row['tweet_text'],
               'tweet_url':row['tweet_url'],
               'geo_coordinates':str(row['geo_coordinates']),
               'fav_count_or_likes': str(row['fav_count_or_likes']),
               'retweet_count': str(row['retweet_count']),
               'fav_count_or_likes': str(row['fav_count_or_likes']),
               'author_location':str(row['author_location']),
               'author_geo_coordinates':str(row['author_geo_coordinates']),
               'author_screen_name':row['author_screen_name'],
               'author_followers_count': str(row['author_followers_count']),
               'author_fav_count': str(row['author_fav_count']),
               'source url':str(row['source url']),
               'geo':str(row['geo']),
               'source':str(row['source']),
               'mapping_location':str(row['mapping_location']),
               'sentiment_type' : str(sentimentType),
               'sentiment_score' : str(sentimentScore)
           }
       }
       )
    wordDict = getKeyWords(row['tweet_text'])
    for key in wordDict.keys():
        updateWordsTable(key,wordDict[key],sentimentType)

    return {
        'statusCode': 200,
        'body': json.dumps(row['id'])
    }


#init Kinesis Consumer
kinesis = boto3.client("kinesis",region_name='us-east-1')
shard_id = "shardId-000000000000" #only one shard!
#iterate through data / kinesis consumer
pre_shard_it = kinesis.get_shard_iterator(StreamName="wegmans_tweets", ShardId=shard_id, ShardIteratorType="LATEST")
shard_it = pre_shard_it["ShardIterator"]
while 1==1:

     out = kinesis.get_records(ShardIterator=shard_it, Limit=1)
     shard_it = out["NextShardIterator"]
     print(out)
     time.sleep(5.0)
     if(len(out['Records'])==0):
         continue
     data = out['Records'][0].get('Data','None')
     if data == 'None':
         continue
     data = data.decode('utf-8')
     lambda_handler(json.loads(data), 'a')
