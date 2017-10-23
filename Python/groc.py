import boto3
import json
import uuid
import datetime
from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

@app.route('/doneShopping', methods=['POST'])
def done_shopping():
    if request.method == 'POST':
        #Can't get flask to recognize JSON data from fetch, so I'm getting it as a string, then parsing.
        #json_data = request.get_json() doesn't seem to work even when sending sample JSON of {'foo':'bar'}

        json_items = json.loads(request.data)
        mark_list_as_shopped(initialize_db(), create_list_from_front_end(json_items))

    print 'sdjkfhajklsdf'
    return 'Hello, World!'

@app.route('/postList', methods=['POST'])
def post_list():
    if request.method == 'POST':
        #Can't get flask to recognize JSON data from fetch, so I'm getting it as a string, then parsing.
        #json_data = request.get_json() doesn't seem to work even when sending sample JSON of {'foo':'bar'}

        json_items = json.loads(request.data)
        print (json_items)

        #if no GUID, make one, and create a new list in the DB with it.
        if json_items[0]["ListGUID"] == '':
            print "NO GUID"
            newGUID = 'latest'
            create_new_list(initialize_db(), newGUID, create_list_from_front_end(json_items))

        elif json_items[0]["ListGUID"] == 'latest':
            print "Got dat latest GUID: " + json_items[0]["ListGUID"]
            update_list(initialize_db(), create_list_from_front_end(json_items) )

        else:
            #not sure what to do in this case
            print 'real guid?'

    #Is there something better I should return?
    return ""



def initialize_db():
    client = boto3.client('dynamodb')
    return client

#todo: do I need this? I think I really just want to use it for get latest list.
def get_list(id):
    #Both of the below work.

    client = initialize_db()

    response = client.query(
        #IndexName='list',
        Select='ALL_ATTRIBUTES',
        TableName='GroceryList',
        KeyConditionExpression='GUID = :v1',
        ExpressionAttributeValues={
        ':v1': {
            'S': id,
        },
    },
    )

    # response = client.query(
    #     #IndexName='list',
    #     Select='ALL_ATTRIBUTES',
    #     TableName='GroceryList',
    #     KeyConditionExpression='GUID = :v1',
    #     ExpressionAttributeValues={
    #     ':v1': {
    #         'S': 'f2100b8e-5a91-40d7-b664-1cf80a6f95a2',
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

    return response

#put a new list into the DB
def create_new_list(client, id, items):

    print items
    print id

    response = client.put_item(
        TableName='GroceryList',
        Item={
            'GUID': {
                'S': id
            },
            'ShopDate': {
                'S': 'null'
            },
            'list': {
                'L': items
            },
        }
    )

    print response


def create_list_from_front_end(items):
    item_list = [];
    for item in items:
        item_list.append({'S': item["text"]})
    return item_list


#todo: update the list variable to come from the API. Needs to pass in GUID, CreateDate, list for ExpressionAttributeValues
def update_list(client, items):
    #http://boto3.readthedocs.io/en/latest/reference/services/dynamodb.html#DynamoDB.Client.update_item

    print items

    response = client.update_item(
    ExpressionAttributeValues={
        ':l': {
            'L': items
        }
    },
    Key={
        'GUID': {
            'S': 'latest'
        },
        'ShopDate': {
            'S': 'null'
        },
    },
    TableName='GroceryList',
    ExpressionAttributeNames={
        '#L': 'list'
    },
    ReturnValues='ALL_NEW',
    UpdateExpression='SET #L = :l',
    )

    print response

#todo: implement
@app.route('/getLatest')
def get_latest_list():
    latest_list_dict = get_list('latest')
    latest_list = latest_list_dict['Items'][0]['list']['L']

    print latest_list
    return jsonify(latest_list)
    #{'foo':'bar'}

def mark_list_as_shopped(client, items):

    response = client.put_item(
        TableName='GroceryList',
        Item={
            'GUID': {
                'S': str(uuid.uuid4())
            },
            'ShopDate': {
                'S': datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            },
            'list': {
                'L': items
            },
        }
    )

    print(response)
    return ''
