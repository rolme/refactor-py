from typing import cast
import boto3, os
from refactor_db import user, id, org

VERBOSE = True
FORCE = True

def handler(event, context):
    # Initialize the DynamoDB client
    dynamodb = boto3.resource('dynamodb', region_name=os.environ["AWS_REGION"])  # Replace with your region if different

    # Select your table
    table = dynamodb.Table(os.environ["TABLE_NAME"])

    # TODO: check there is an action

    match event['action']:
        case 'add':
            # TODO: Validate email format
            if 'userId' in event and not id.is_valid_id(user.OBJECT_TYPE, event['userId']):
                raise Exception(f"Error: userId is not valid: {event['userId']}")

            if not id.is_valid_id(org.OBJECT_TYPE, event['orgId']):
                raise Exception(f"Error: orgId is not valid: {event['orgId']}")

            response = user.add(table, cast(user.User, event), VERBOSE)
        case 'find':
            if not id.is_valid_id(org.OBJECT_TYPE, event['orgId']):
                raise Exception(f"Error: orgId is not valid: {event['orgId']}")

            if not id.is_valid_id(user.OBJECT_TYPE, event['userId']):
                raise Exception(f"Error: userId is not valid: {event['userId']}")

            response = user.find(table, event['orgId'], event['userId'], VERBOSE)
        case 'find_by_email':
            # TODO: Validate email format
            response = user.find_by_email(table, event['email'], VERBOSE)
        case 'find_all':
            if not id.is_valid_id(org.OBJECT_TYPE, event['orgId']):
                raise Exception(f"Error: orgId is not valid: {event['orgId']}")

            response = user.find_all(table, event['orgId'], VERBOSE)
        case 'update':
            # TODO: Validate email format
            if not id.is_valid_id(org.OBJECT_TYPE, event['orgId']):
                raise Exception(f"Error: orgId is not valid: {event['orgId']}")

            response = user.update(table, cast(user.User, event), VERBOSE)
        case 'delete':
            if not id.is_valid_id(user.OBJECT_TYPE, event['userId']):
                raise Exception(f"Error: userId is not valid: {event['userId']}")

            if not id.is_valid_id(org.OBJECT_TYPE, event['orgId']):
                raise Exception(f"Error: orgId is not valid: {event['orgId']}")

            response = user.delete(table, cast(user.User, event), VERBOSE)
        case 'restore':
            if not id.is_valid_id(user.OBJECT_TYPE, event['userId']):
                raise Exception(f"Error: userId is not valid: {event['userId']}")

            if not id.is_valid_id(org.OBJECT_TYPE, event['orgId']):
                raise Exception(f"Error: orgId is not valid: {event['orgId']}")

            response = user.restore(table, event['orgId'], event['userId'], VERBOSE)
        case 'destroy':
            if not id.is_valid_id(user.OBJECT_TYPE, event['userId']):
                raise Exception(f"Error: userId is not valid: {event['userId']}")

            if not id.is_valid_id(org.OBJECT_TYPE, event['orgId']):
                raise Exception(f"Error: orgId is not valid: {event['orgId']}")

            response = user.destroy(table, event['orgId'], event['userId'], VERBOSE)
        case 'force_destroy':
            if not id.is_valid_id(user.OBJECT_TYPE, event['userId']):
                raise Exception(f"Error: userId is not valid: {event['userId']}")

            if not id.is_valid_id(org.OBJECT_TYPE, event['orgId']):
                raise Exception(f"Error: orgId is not valid: {event['orgId']}")

            response = user.destroy(table, event['orgId'], event['userId'], VERBOSE, FORCE)

    return {
        'statusCode': 200,
        'body': f'{response}'
    }