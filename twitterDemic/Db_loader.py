#reference : https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.01.html
# Python code to load data into DynamoDb tables from local files (csv)

from __future__ import print_function # Python 2/3 compatibility
import boto3
import pandas as pd
import decimal
import sys

#local dynamodb database
#dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")

#aws dynamodb database
dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

#connect to tables
table = dynamodb.Table('wegmans_tweets_detail') #tweet detail / master table
wordTable = dynamodb.Table('wegmans_tweets_words') # noun, adjective word count table

# connect to aws comprehend api
comprehend = boto3.client(service_name='comprehend', region_name='us-east-2')

#function to derive sentiment using aws comprehend
def getSentiment(text):
    sentimentBody = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    sentiment = sentimentBody['Sentiment']
    return sentiment, sentimentBody['SentimentScore'][sentiment[0]+sentiment[1:].lower()]


#function to get words - noun and adjective
def getKeyWords(text):
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

#function to update word table with counts
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

#connect to local csv file
raw_data = pd.read_csv("wegmans/" + sys.argv[1])

#iterate through records and write to table
for index, row in raw_data.iterrows():
   print(row['id'], row['created_at_utc'])
   #extract sentiment
   sentimentType, sentimentScore = getSentiment(row['tweet_text'])
   #update tweets detail master table
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


   #get key words : noun and adjective
   #reference : https://stackoverflow.com/questions/43986643/python3-dynamodb-update-item-do-not-work
   wordDict = getKeyWords(row['tweet_text'])

   #update word count table
   for key in wordDict.keys():
       updateWordsTable(key,wordDict[key],sentimentType)



print("Table status:", table.table_status)
