#reference : https://docs.aws.amazon.com/comprehend/latest/dg/get-started-api-sentiment.html#get-started-api-sentiment-python
# Testing AWS Comprehend API
import boto3
import json

comprehend = boto3.client(service_name='comprehend', region_name='us-east-2')

text = "Can you taste it with your eyes? Well, let me tell you that it was amazing! Thank you Wegmans food bar! #wegmans #roastedbrusselsprouts https://t.co/8Kus0xUaF3"

def getSentiment(text):
    sentimentBody = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    sentiment = sentimentBody['Sentiment']
    return sentiment, sentimentBody['SentimentScore'][sentiment[0]+sentiment[1:].lower()]



sentimentType, sentimentScore = getSentiment(text)

print(sentimentType, sentimentScore)

syntaxBody = comprehend.detect_syntax(Text=text, LanguageCode='en')
tokens = syntaxBody["SyntaxTokens"]
print(json.dumps(syntaxBody["SyntaxTokens"], sort_keys=True, indent=4))

adjDict = {}
for token in tokens:
    if token['PartOfSpeech']['Tag'] == 'ADJ' or token['PartOfSpeech']['Tag'] == 'NOUN':
        if adjDict.get(token['Text'],'none') == 'none':
            adjDict[token['Text']]=1
        else:
            adjDict[token['Text']]=adjDict[token['Text']]+1

print(adjDict)
