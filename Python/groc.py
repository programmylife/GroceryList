import boto3
import json

def initialize_db():
    client = boto3.client('dynamodb')
    return client


def get_item():
    #Both of the below work.

    # response = client.query(
    #     #IndexName='list',
    #     Select='ALL_ATTRIBUTES',
    #     TableName='GroceryTest2',
    #     KeyConditionExpression='ListGUID = :v1',
    #     ExpressionAttributeValues={
    #     ':v1': {
    #         'S': '789345',
    #     },
    # },
    # )

    # response = client.get_item(
    #     Key={
    #     'ListGUID': {
    #         'S': '789345',
    #     },
    #     'CreateDate': {
    #         'S': '2016-12-30T14:20:00',
    #     },
    # },
    # TableName='GroceryTest2',
    # )

    print(response)



#put a list into the DB
#todo: auto generate GUID. Need to pass in list values. Autogen createDate OR make that 'shopDate'
def create_new_list(client):
    response = client.put_item(
        TableName='GroceryTest2',
        Item={
            'ListGUID': {
                'S': '654376'
            },
            'CreateDate': {
                'S': '2017-08-13T14:20:00'
            },
            'list': {
                'L': [
                    {'S': 'eggs'},
                    {'S':'bananas'}
                ]
            },
        }
    )

    print response

#todo: update the list variable to come from the API. Needs to pass in GUID, CreateDate, list for ExpressionAttributeValues
def update_list(client):
    #http://boto3.readthedocs.io/en/latest/reference/services/dynamodb.html#DynamoDB.Client.update_item

    response = client.update_item(
    ExpressionAttributeValues={
        ':l': {
            'L': [
                {'S': 'eggs'},
                {'S':'bananas'},
                {'S':'cherries'}
            ]
        }
    },
    Key={
        'ListGUID': {
            'S': '654376'
        },
        'CreateDate': {
            'S': '2017-08-13T14:20:00'
        },
    },
    TableName='GroceryTest2',
    ExpressionAttributeNames={
        '#L': 'list'
    },
    ReturnValues='ALL_NEW',
    UpdateExpression='SET #L = :l',
    )

    print response

#todo: implement
def get_latest_list():
    #This will be much easier if I just create a new field called 'latest'
    #Or I can scan the db and do the work to find the latest.
    #OR if I change the CreateDate field to ShopDate, I can just query for the item with the empty date field.
    return ''

def mark_list_as_shopped():
    #todo: update list to add generated 'shopeDate'
    print ''


client = initialize_db()
#create_new_list(client)
update_list(client)
