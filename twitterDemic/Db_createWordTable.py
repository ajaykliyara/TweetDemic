#reference : https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.01.html
# Python code to create table

from __future__ import print_function # Python 2/3 compatibility
import boto3

#local dynamodb table
#dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")

#aws dynamodb table
dynamodb = boto3.resource('dynamodb', region_name='us-west-2')


#create table
table = dynamodb.create_table(
    TableName='wegmans_tweets_words',
    KeySchema=[
        {
            'AttributeName': 'sentiment_type',
            'KeyType': 'HASH'  #Partition key
        },
        {
            'AttributeName': 'word',
            'KeyType': 'RANGE'  #Sort key
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'sentiment_type',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'word',
            'AttributeType': 'S'
        },

    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }
)

print("Table status:", table.table_status)
