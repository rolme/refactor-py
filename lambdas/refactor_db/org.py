from typing import TypedDict, NotRequired
from datetime import datetime
from .id import generate_id, is_valid_id

OBJECT_TYPE='ORG'

class Org(TypedDict):
    orgId: str
    orgName: str
    createdAt: NotRequired[int]
    updatedAt: NotRequired[int]
    deletedAt: NotRequired[int]

def add(table: any, item: Org, verbose: bool = False):
    if verbose:
        print(f"function: org add()")
        print(f"table name: {table.table_name}")
        print(f"item: {item}")

    # validate orgId format and if it already exists
    if 'orgId' in item and is_valid_id(OBJECT_TYPE, item['orgId']):
        org = find(table, item['orgId'], item['orgId'], verbose)
        if 'orgId' in org:
            print(f"Error: orgId already exists: {item['orgId']}")
            # TODO: Return an error object instead
            return {}
    else:
        item['orgId'] = generate_id(OBJECT_TYPE)

    now = int(datetime.now().timestamp())
    item['createdAt'] = item['updatedAt'] = now

    try:
        response = table.put_item(
            Item={
                'hashKey': item["orgId"],
                'rangeKey': item["orgId"],
                'itemType': OBJECT_TYPE,
                'id': item["orgId"],
                'orgId': item["orgId"],
                'orgName': item["name"],
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
        print(f"org: {item}")

    return item

def delete(table: any, item: Org, verbose: bool = False):
    if verbose:
        print(f"function: org delete()")
        print(f"table name: {table.table_name}")
        print(f"org: {item}")

    now = int(datetime.now().timestamp())
    update_expression = "SET deletedAt = :d"
    expression_values = {
        ":d": now,
    }

    try:
        # TODO: delete all users in the org
        response = table.update_item(
            Key={
                'hashKey': item["orgId"],
                'rangeKey': item["orgId"],
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
        print(f"org: {item}")

    return item 

def restore(table: any, orgId: str, verbose: bool = False):
    if verbose:
        print(f"function: org restore()")
        print(f"table name: {table.table_name}")
        print(f"orgId: {orgId}")

    update_expression = "REMOVE deletedAt"

    try:
        # TODO: restore all users in the org
        response = table.update_item(
            Key={
                'hashKey': orgId,
                'rangeKey': orgId,
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

def destroy(table: any, orgId: str, verbose: bool = False, force: bool = False):
    if verbose:
        print(f"function: org destroy()")
        print(f"table name: {table.table_name}")
        print(f"orgId: {orgId}")

    try:
        if force:
            response = table.delete_item(
                Key={
                    'hashKey': orgId,
                    'rangeKey': orgId,
                },
            )
            return response

        response = table.delete_item(
            Key={
                'hashKey': orgId,
                'rangeKey': orgId,
            },
            ConditionExpression="attribute_exists(deletedAt)"
        )
        return response
    except Exception as e:
        if e['errorType'] == 'TypeError':
            print(f"Error: org is not marked for deletion: {orgId}")

def update(table: any, item: Org, verbose: bool = False):
    if verbose:
        print(f"function: org update()")
        print(f"table name: {table.table_name}")
        print(f"org: {item}")

    update_expression = "SET orgName = :n, updatedAt = :u"
    expression_values = {
        ":n": item["orgName"],
        ":u": int(datetime.now().timestamp()),
    }
    response = table.update_item(
        Key={
            'hashKey': item["orgId"],
            'rangeKey': item["orgId"],
        },
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_values
        )
    return item

def find_all(table: any, orgId: str, verbose: bool = False):
    if verbose:
        print(f"function: org find_all()")
        print(f"table name: {table.table_name}")
        print(f"org id: {orgId}")

    query_conditions = {
        'KeyConditionExpression': 'itemType = :t and begins_with(id, :i)',
        'ExpressionAttributeValues': {
            ':t': OBJECT_TYPE,
            ':i': f'{OBJECT_TYPE}-',
        },
        'IndexName': 'itemTypeIdIndex',
    }

    orgs = []
    try:
        response = table.query(**query_conditions)
        if 'Items' in response:
            orgs = response['Items']
    except Exception as e:
        print(f"Error: {e}")
        response = e
        # TODO: return an error object instead

    return orgs

def find(table: any, orgId: str, verbose: bool = False):
    if verbose:
        print(f"function: org find()")
        print(f"table name: {table.table_name}")
        print(f"org id: {orgId}")

    # TODO: Verify its a valid orgId

    org = {}
    try:
        response = table.get_item(
            Key={
                'hashKey': orgId,
                'rangeKey': orgId,
            }
        )
        if 'Item' in response:
            org = response['Item']

    except Exception as e:
        print(f"Error: {e}")
        response = e
        # TODO: return an error object instead

    if verbose:
        print(f"response: {response}")
        print(f"org: {org}")

    return org
