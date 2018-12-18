#reference : https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.01.html
# Python code to read data from table in Dynamodb

from __future__ import print_function # Python 2/3 compatibility
import boto3
import pandas as pd
import decimal
import json

#local db connection
#dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")

#aws db connection
dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

#connect to table in DB - tweet details
table = dynamodb.Table('wegmans_tweets_detail')

response = table.scan(
    #FilterExpression=fe,
    #ProjectionExpression=pe,
    #ExpressionAttributeNames=ean
    )

#iterate through data retrieved
for i in response['Items']:
    print(json.dumps(i))


print("Table status:", table.table_status)


# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

#connect to table, words - nouns and adjective and their counts
wordTable = dynamodb.Table('wegmans_tweets_words')

response = wordTable.scan(
    #FilterExpression=fe,
    #ProjectionExpression=pe,
    #ExpressionAttributeNames=ean
    )

#iterate through data
for i in response['Items']:
    print(json.dumps(i,indent=4, cls=DecimalEncoder))


print("Table status:", wordTable.table_status)
