from typing import TypedDict, NotRequired, cast
from datetime import datetime
from .id import generate_id, is_valid_id
from .org import OBJECT_TYPE as ORG_OBJECT_TYPE

OBJECT_TYPE='USER'

class User(TypedDict):
    orgId: str
    userId: NotRequired[str]
    username: str
    email: str
    createdAt: NotRequired[int]
    updatedAt: NotRequired[int]
    deletedAt: NotRequired[int]

def add(table: any, item: User, verbose: bool = False):
    if verbose:
        print(f"function: user add()")
        print(f"table name: {table.table_name}")
        print(f"item: {item}")

    # validate org id
    if not is_valid_id(ORG_OBJECT_TYPE, item['orgId']):
        raise Exception(f"Error: orgId is not valid: {item['orgId']}")

    # validate email does not already exist
    user = find_by_email(table, item['email'], verbose)
    if 'userId' in user:
        print(f"Error: user email already exists: {user['email']}")
        # TODO: Return an error object instead
        return {}

    # validate userId format and if it already exists
    if 'userId' in item and is_valid_id(OBJECT_TYPE, item['userId']):
        user = find(table, item['orgId'], item['userId'], verbose)
        if 'userId' in user:
            print(f"Error: userId already exists: {item['userId']}")
            # TODO: Return an error object instead
            return {}
    else:
        item['userId'] = generate_id(OBJECT_TYPE)

    now = int(datetime.now().timestamp())
    item['createdAt'] = item['updatedAt'] = now

    try:
        response = table.put_item(
            Item={
                'hashKey': item["orgId"],
                'rangeKey': item["userId"],
                'itemType': OBJECT_TYPE,
                'id': item["email"],
                'orgId': item["orgId"],
                'userId': item["userId"],
                'email': item["email"],
                'username': item["username"],
                'createdAt': item['createdAt'],
                'updatedAt': item['updatedAt'],
            }
        )
    except Exception as e:
        print(f"Error: {e}")
        response = e
        # TODO: return an error object instead
        item = {}

    if verbose:
        print(f"response: {response}")
        print(f"user: {item}")

    return item

def delete(table: any, item: User, verbose: bool = False):
    if verbose:
        print(f"function: user delete()")
        print(f"table name: {table.table_name}")
        print(f"user: {item}")

    now = int(datetime.now().timestamp())
    update_expression = "SET deletedAt = :d"
    expression_values = {
        ":d": now,
    }

    try:
        response = table.update_item(
            Key={
                'hashKey': item["orgId"],
                'rangeKey': item["userId"],
            },
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_values
            )
    except Exception as e:
        print(f"Error: {e}")
        response = e
        item = {}

    item['deletedAt'] = now
    if verbose:
        print(f"response: {response}")
        print(f"user: {item}")

    return item 

def restore(table: any, orgId: str, userId: str, verbose: bool = False):
    if verbose:
        print(f"function: user delete()")
        print(f"table name: {table.table_name}")
        print(f"orgId: {orgId}")
        print(f"userId: {userId}")

    update_expression = "REMOVE deletedAt"

    try:
        response = table.update_item(
            Key={
                'hashKey': orgId,
                'rangeKey': userId,
            },
            UpdateExpression=update_expression,
            ReturnValues="ALL_NEW"
        )
    except Exception as e:
        print(f"Error: {e}")
        response = e
        item = {}

    if verbose:
        print(f"response: {response}")

    return response['Attributes']

def destroy(table: any, orgId: str, userId: str, verbose: bool = False, force: bool = False):
    if verbose:
        print(f"function: user destroy()")
        print(f"table name: {table.table_name}")
        print(f"orgId: {orgId}")
        print(f"userId: {userId}")

    try:
        if force:
            response = table.delete_item(
                Key={
                    'hashKey': orgId,
                    'rangeKey': userId,
                },
            )
            return response

        response = table.delete_item(
            Key={
                'hashKey': orgId,
                'rangeKey': userId,
            },
            ConditionExpression="attribute_exists(deletedAt)"
        )
        return response
    except Exception as e:
        if e['errorType'] == 'TypeError':
            print(f"Error: user is not marked for deletion: {userId}")

def update(table: any, item: User, verbose: bool = False):
    if verbose:
        print(f"function: user update()")
        print(f"table name: {table.table_name}")
        print(f"user: {item}")

    # validate email does not already exist
    user = find_by_email(table, item['email'], verbose)
    if 'userId' in user and user['userId'] != item['userId']:
        print(f"Error: user email already exists: {user['email']}")
        # TODO: Return an error object instead
        return {}


    update_expression = "SET id = :i, email = :e, username = :n, updatedAt = :u"
    expression_values = {
        ":i": item["email"],
        ":e": item["email"],
        ":n": item["username"],
        ":u": int(datetime.now().timestamp()),
    }
    response = table.update_item(
        Key={
            'hashKey': item["orgId"],
            'rangeKey': item["userId"],
        },
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_values,
            ReturnValues="ALL_NEW"
        )
    return response['Attributes']

def find_all(table: any, orgId: str, verbose: bool = False):
    if verbose:
        print(f"function: user find_all()")
        print(f"table name: {table.table_name}")
        print(f"org id: {orgId}")

    query_conditions = {
        'KeyConditionExpression': 'hashKey = :h and begins_with(rangeKey, :r)',
        'ExpressionAttributeValues': {
            ':h': orgId,
            ':r': f'{OBJECT_TYPE}-',
        },
    }

    users = []
    try:
        print(f'query_conditions: {query_conditions}')
        response = table.query(**query_conditions)
        if 'Items' in response:
            users = response['Items']
    except Exception as e:
        print(f"Error: {e}")
        response = e
        # TODO: return an error object instead

    return users

def find(table: any, orgId: str, userId: str, verbose: bool = False):
    if verbose:
        print(f"function: user find()")
        print(f"table name: {table.table_name}")
        print(f"org id: {orgId}")
        print(f"user id: {userId}")

    # TODO: Verify its a valid orgId
    # TODO: Verify its a valid userId

    user = {}
    try:
        response = table.get_item(
            Key={
                'hashKey': orgId,
                'rangeKey': userId,
            }
        )
        if 'Item' in response:
            user = response['Item']

    except Exception as e:
        print(f"Error: {e}")
        response = e
        # TODO: return an error object instead

    if verbose:
        print(f"response: {response}")
        print(f"user: {user}")

    return user

def find_by_email(table: any, email: str, verbose: bool = False):
    if verbose:
        print(f"function: user find_by_email()")
        print(f"table name: {table.table_name}")
        print(f"email: {email}")

    query_conditions = {
        'KeyConditionExpression': 'itemType = :t and id = :i',
        'ExpressionAttributeValues': {
            ':t': OBJECT_TYPE,
            ':i': email,
        },
        'IndexName': 'itemTypeIdIndex'
    }

    user = {}
    try:
        response = table.query(**query_conditions)
        if 'Items' in response:
            user = response['Items'][0]
        else:
            user = {}
    except Exception as e:
        print(f"Error: {e}")
        response = e
        # TODO: return an error object instead

    return user
