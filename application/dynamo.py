import os
import boto3

def get_aws_connection():
    region = os.environ.get('REGION')
    database_table = os.environ.get('DATABASE_TABLE')
    # To run locally
    #aws_session = boto3.session.Session(region_name=region, profile_name='default')
    aws_session = boto3.session.Session(region_name=region)
    aws_dynamodb = aws_session.resource('dynamodb')
    dynamo_table_prices = aws_dynamodb.Table(database_table)
    
    return dynamo_table_prices


def put_item(item):
    prices_table = get_aws_connection()
    print(item)
    prices_table.put_item(Item=item)


def get_day_data(day):
    prices_table = get_aws_connection()
    prices_dynamo = prices_table.query(
        ExpressionAttributeValues={
            ":date": day,
        },
        KeyConditionExpression='pk = :date',
    )

    data_prices = prices_dynamo['Items']

    while 'LastEvaluatedKey' in prices_dynamo:
        prices_dynamo = prices_table.query(
            ExpressionAttributeValues={
                ":date": day,
            },
            KeyConditionExpression='pk = :date',
            ExclusiveStartKey=prices_dynamo['LastEvaluatedKey'])
        data_prices.extend(prices_dynamo['Items'])
    
    return data_prices

def get_month_data(month):
    prices_table = get_aws_connection()
    prices_dynamo = prices_table.query(
        ExpressionAttributeNames={
            "#month": "month"
        },
        ExpressionAttributeValues={
            ":date": month,
        },
        IndexName='month-index',
        KeyConditionExpression='#month = :date',
    )

    data_prices = prices_dynamo['Items']

    while 'LastEvaluatedKey' in prices_dynamo:
        prices_dynamo = prices_table.query(
            ExpressionAttributeNames={
              "#month": "month"
            },
            ExpressionAttributeValues={
                ":date": month,
            },
            IndexName='month-index',
            KeyConditionExpression='#month = :date',
            ExclusiveStartKey=prices_dynamo['LastEvaluatedKey'])
        data_prices.extend(prices_dynamo['Items'])
    
    return data_prices