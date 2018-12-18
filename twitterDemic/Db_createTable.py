#reference : https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.01.html
# Python code to create word count table

from __future__ import print_function # Python 2/3 compatibility
import boto3

#local dynamodb database
#dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")

#aws dynamodb database
dynamodb = boto3.resource('dynamodb', region_name='us-west-2')

#create table script
table = dynamodb.create_table(
    TableName='wegmans_tweets_detail',
    KeySchema=[
        {
            'AttributeName': 'tweet_id',
            'KeyType': 'HASH'  #Partition key
        },
        {
            'AttributeName': 'created_at_utc',
            'KeyType': 'RANGE'  #Sort key
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'tweet_id',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'created_at_utc',
            'AttributeType': 'S'
        },

    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }
)

print("Table status:", table.table_status)
