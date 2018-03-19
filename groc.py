import boto3
import json
import uuid
import datetime
from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

TABLE_NAME = 'GroceryList'

def initialize_db():
    client = boto3.client('dynamodb', region_name='us-east-1')
    return client

@app.route('/doneShopping', methods=['POST'])
def done_shopping():
    response = '';
    if request.method == 'POST':
        #Can't get flask to recognize JSON data from fetch, so I'm getting it as a string, then parsing.
        #json_data = request.get_json() doesn't seem to work even when sending sample JSON of {'foo':'bar'}

        json_items = json.loads(request.data)
        response = create_new_list(initialize_db(), str(uuid.uuid4()), create_list_from_front_end(json_items), datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

    return jsonify(response['ResponseMetadata'])

@app.route('/postList', methods=['POST'])
def post_list():
    response = '';
    if request.method == 'POST':
        json_items = json.loads(request.data)

        #if no GUID, make one, and create a new list in the DB with it.
        #This shouldn't really happen since all should be 'latest' or have a real GUID...
        if json_items[0]["ListGUID"] == '':
            print "NO GUID"
            newGUID = 'latest'
            response = create_new_list(initialize_db(), newGUID, create_list_from_front_end(json_items),'null')

        elif json_items[0]["ListGUID"] == 'latest':
            print "latest GUID"
            response = update_list(initialize_db(), create_list_from_front_end(json_items) )

        else:
            #not sure what to do in this case
            print 'real guid?'

    print response['ResponseMetadata']
    #Is there something better I should return?
    return jsonify(response['ResponseMetadata'])

@app.route('/getLatest')
def get_latest_list():
    latest_list_dict = get_list('latest')
    latest_list = latest_list_dict['Items'][0]['list']['L']

    print latest_list
    return jsonify(latest_list)

def get_list(id):
    client = initialize_db()
    response = client.query(
        #IndexName='list',
        Select='ALL_ATTRIBUTES',
        TableName=TABLE_NAME,
        KeyConditionExpression='GUID = :v1',
        ExpressionAttributeValues={
            ':v1': {
                'S': id,
            },
        },
    )
    return response

#put a new list into the DB
def create_new_list(client, id, items, shop_date):
    response = client.put_item(
        TableName=TABLE_NAME,
        Item={
            'GUID': {
                'S': id
            },
            'ShopDate': {
                'S': shop_date
            },
            'list': {
                'L': items
            },
        }
    )
    return response

def create_list_from_front_end(items):
    item_list = [];
    for item in items:
        item_list.append({'S': item["text"]})
    return item_list

def update_list(client, items):
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
        TableName=TABLE_NAME,
        ExpressionAttributeNames={
            '#L': 'list'
        },
        ReturnValues='ALL_NEW',
        UpdateExpression='SET #L = :l',
    )

    return response

#if __name__ == '__main__':
 #   app.run(host='0.0.0.0', port=5000, debug=True)
